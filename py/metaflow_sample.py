import pandas as pd
from metaflow import FlowSpec, step
import numpy as np

items_path = 'data/items.csv'
test_path = 'data/test.csv'
sales_path = 'data/sales_train.csv'
grid_cols = ['shop_id', 'item_id', 'date_block_num']
enc_col_fmt = '{}_target_enc'

class SalesFlow(FlowSpec):
    @step
    def start(self):
        self.df = pd.read_csv(sales_path)
        self.df.drop_duplicates(inplace=True)
        self.df['sales_price'] = self.df['item_cnt_day'] * self.df['item_price']
        self.next(self.remove_outliner)

    @step
    def remove_outliner(self):
        def remove(df: pd.DataFrame, col: str):
            q = df[col].quantile(0.99)
            return df[df[col] < q]

        self.df = remove(self.df, 'item_price')
        self.df = remove(self.df, 'item_cnt_day')
        self.df.loc[self.df.item_price < 0, 'item_price'] = self.df.item_price.median()
        self.next(self.grid)

    @step
    def grid(self):
        from itertools import product

        grid = []
        for block_num in self.df['date_block_num'].unique():
            cur_shops = self.df[self.df['date_block_num']==block_num]['shop_id'].unique()
            cur_items = self.df[self.df['date_block_num']==block_num]['item_id'].unique()
            grid.append(np.array(list(product(*[cur_shops, cur_items, [block_num]])), dtype='int32'))
        self.grid_df = pd.DataFrame(np.vstack(grid), columns=grid_cols, dtype=np.int32)

        self.group_cols = [
            ('both', grid_cols),
            ('shop', ['date_block_num', 'shop_id']),
            ('item', ['date_block_num', 'item_id']),
        ]
        self.next(self.group, foreach='group_cols')

    @step
    def group(self):
        name, cols = self.input
        gb = self.df.groupby(cols, as_index=False)
        target_name = 'target' if name == 'both' else f'target_{name}'
        self.df = gb.item_cnt_day.agg({target_name: 'sum'})
        if name != 'shop':
            self.df[f'{name}_price'] = gb.item_price.agg({'item_price': 'mean'}).item_price
        self.df[f'{name}_sales_price'] = gb.sales_price.agg({'sales_price': 'sum'}).sales_price
        self.cols = cols
        self.next(self.join_grouped)

    @step
    def join_grouped(self, inputs):
        df = inputs[0].grid_df
        self.price_map = {}
        for i in inputs:
            df = pd.merge(df, i.df, how='left', on=i.cols)
        self.df = self.downcast_dtypes(df)
        self.next(self.fill_grouped)

    @step
    def fill_grouped(self):
        self.df.loc[self.df.both_price.isnull(), 'both_price'] = self.df.item_price
        self.df.fillna(0, inplace=True)
        self.next(self.calc_global_mean)

    @step
    def calc_global_mean(self):
        self.global_mean = self.df.target.mean()
        self.next(self.item_category)

    @step
    def item_category(self):
        self.df = pd.merge(self.df, pd.read_csv(items_path), on='item_id')
        self.df.drop('item_name', axis=1, inplace=True)
        self.category_cols = ['shop_id', 'item_id', 'item_category_id']

        self.next(self.mean_encoding, foreach='category_cols')

    @step
    def mean_encoding(self):
        from sklearn.model_selection import KFold
        target_col = self.input

        kf = KFold(n_splits=5, shuffle=True, random_state=132)
        X = self.df.drop(['target'], axis=1)
        y = self.df['target']
        feats = []
        for train_index, test_index in kf.split(X, y):
            train_df = self.df.iloc[train_index, :]
            test_df = self.df.iloc[test_index, :]
            feats.append(test_df[target_col].map(train_df.groupby(target_col).target.mean()))
        self.feature = pd.concat(feats).sort_index()
        self.feature.fillna(self.global_mean, inplace=True)
        self.feature.rename(enc_col_fmt.format(target_col), inplace=True)

        self.next(self.join_mean_encoding)

    @step
    def join_mean_encoding(self, inputs):
        self.merge_artifacts(inputs, exclude='feature')
        self.df = pd.concat([self.df] + [i.feature for i in inputs], axis=1)
        self.next(self.nothing)

    @step
    def nothing(self):
        self.next(self.lag, self.build_test_data)

    @step
    def build_test_data(self):
        self.test_df = pd.merge(pd.read_csv(test_path),
                                pd.read_csv(items_path),
                                on='item_id')
        self.test_df.drop('item_name', axis=1, inplace=True)
        self.next(self.encode_test, self.pricing_map)

    @step
    def encode_test(self):
        self.next(self.run_encoding_test, foreach='category_cols')

    @step
    def run_encoding_test(self):
        enc_col = enc_col_fmt.format(self.input)
        enc_map = self.df.groupby(self.input)[enc_col].mean().to_dict()

        self.feature = self.test_df[self.input].map(enc_map)
        self.feature.rename(enc_col, inplace=True)
        self.next(self.join_test_encoded)

    @step
    def join_test_encoded(self, inputs):
        self.merge_artifacts(inputs, exclude='feature')
        self.encoded_df = pd.concat([i.feature for i in inputs], axis=1)
        self.next(self.join_test_data)

    @step
    def pricing_map(self):
        category_map = self.df.groupby('item_category_id').item_price.mean().to_dict()
        item_map = self.df.groupby('item_id').item_price.mean().to_dict()
        shop_item_s = self.df.groupby(['shop_id', 'item_id']).item_price.mean()
        shop_item_s.index = shop_item_s.index.map(lambda x: f'{x[0]}-{x[1]}')
        shop_item_map = shop_item_s.to_dict()

        df = pd.DataFrame(index=self.test_df.index)

        test_shop_item_s = self.test_df.shop_id.astype(str) + '-' + self.test_df.item_id.astype(str)
        df['both_price'] = test_shop_item_s.map(shop_item_map)
        df.loc[df.both_price.isnull(), 'both_price'] = self.test_df.item_id.map(item_map)
        df.loc[df.both_price.isnull(), 'both_price'] = self.test_df.item_category_id.map(category_map)

        df['item_price'] = self.test_df.item_id.map(item_map)
        df.loc[df.item_price.isnull(), 'item_price'] = self.test_df.item_category_id.map(category_map)

        self.price_df = df
        self.next(self.join_test_data)

    @step
    def join_test_data(self, inputs):
        self.merge_artifacts(inputs, exclude='test_df')
        self.test_df = pd.concat([
            inputs[0].test_df,
            self.encoded_df,
            self.price_df,
        ], axis=1)
        self.next(self.join_all_data)

    @step
    def lag(self):
        self.lag_drop_cols = ['item_category_id'] \
            + [enc_col_fmt.format(c) for c in self.category_cols]\
            + ['both_price', 'item_price']

        self.cols_to_rename = list(self.df.columns.difference(grid_cols + self.lag_drop_cols))
        self.shift_range = [1, 2, 3, 4, 5, 12]
        self.next(self.calc_lag, foreach='shift_range')

    @step
    def calc_lag(self):
        train_shift = self.df.copy()
        train_shift['date_block_num'] = train_shift['date_block_num'] + self.input
        train_shift.drop(self.lag_drop_cols, axis=1, inplace=True)

        def rename_lag(x: str) -> str:
            return '{}_lag_{}'.format(x, self.input) if x in self.cols_to_rename else x

        self.train_shift = train_shift.rename(columns=rename_lag)
        self.next(self.join_lag)

    @step
    def join_lag(self, inputs):
        self.merge_artifacts(inputs, exclude='train_shift')
        self.train_df = self.df[self.df['date_block_num'] >= max(self.shift_range)]

        self.shifts = [i.train_shift for i in inputs]
        self.next(self.join_all_data)

    @step
    def join_all_data(self, inputs):
        import dask.dataframe as dd
        from dask.diagnostics import ProgressBar

        npartitions = 8
        self.merge_artifacts(inputs)

        self.test_df['date_block_num'] = self.train_df['date_block_num'].max() + 1
        df = pd.concat([self.train_df, self.test_df], ignore_index=True)
        ddf = dd.from_pandas(df, npartitions=npartitions)
        for s in self.shifts:
            _ddf = dd.from_pandas(s, npartitions=npartitions)
            ddf = dd.merge(ddf, _ddf, how='left', on=grid_cols).fillna(0)
        with ProgressBar():
            self.df = ddf.compute(scheduler='processes')

        self.next(self.remove_cols)

    @step
    def remove_cols(self):
        lag_cols = [col for col in self.df.columns if col[-1] in [str(item) for item in self.shift_range]]

        keep_cols = ['ID'] + list(set(grid_cols) - set(['date_block_num'])) + self.lag_drop_cols + lag_cols
        # VERSION: remove original ID (item_id, shop_id, item_category_id) data
        # keep_cols = (set(lag_cols) | set(self.lag_drop_cols) | set(['ID'])) - set(['item_category_id'])
        # VERSION: remove mean-encoded ID
        # keep_cols = (set(lag_cols) | set(grid_cols) | set(['ID', 'item_category_id'])) - set(['date_block_num'])

        self.date_blocks = self.df.date_block_num
        self.X = self.df[keep_cols]
        self.y = self.df.target
        self.next(self.split_data)

    @step
    def split_data(self):
        test_block = self.date_blocks.max()
        val_block = test_block - 1
        self.X_train = self.X.loc[self.date_blocks < val_block].drop(['ID'], axis=1)
        self.y_train = self.y.loc[self.date_blocks < val_block]
        self.X_val = self.X.loc[self.date_blocks == val_block].drop(['ID'], axis=1)
        self.y_val = self.y.loc[self.date_blocks == val_block]
        self.X_test = self.X.loc[self.date_blocks == test_block]
        self.next(self.end)

    @step
    def end(self):
        pass

    def downcast_dtypes(self, df):
        float_cols = [c for c in df if df[c].dtype == "float64"]
        int_cols = [c for c in df if df[c].dtype == "int64"]

        df[float_cols] = df[float_cols].astype(np.float32)
        df[int_cols] = df[int_cols].astype(np.int32)

        return df


if __name__ == '__main__':
    SalesFlow()
