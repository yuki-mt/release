"""
Toggleの履歴から
「何日に何時から何時まで働いて何分休憩したか」を出力する

# 使い方
1. https://toggl.com/app/reports/summary/2476989 にアクセス
2. 期間を指定
3. 右上のダウンロードボタンを押す(PCのみ) (CSVをダウンロード)
4. toggle.csvとして保存
5. python format.pyを実行

# 補足
- MINUNIT (15分) 区切り
- fpormat_report関数で出力結果のフォーマットを変更できる
"""
import csv
import datetime as dt
from collections import OrderedDict
from typing import List, NamedTuple, Tuple, Iterator
import math


SEC_UNIT = 60
MIN_UNIT = 15


class DailyReport(NamedTuple):
    date: dt.date
    start: dt.time
    end: dt.time
    rest: dt.time


def format_time(t: dt.time) -> dt.time:
    new_sec = round(t.second / SEC_UNIT) * SEC_UNIT
    new_min = t.minute
    if new_sec == 60:
        new_sec = 0
        new_min += 1
    new_min = round(new_min / MIN_UNIT) * MIN_UNIT
    new_hour = t.hour
    if new_min == 60:
        new_min = 0
        new_hour += 1
    if new_hour == 24:
        new_hour = 0
    return dt.time(hour=new_hour, minute=new_min, second=new_sec)


def format_min(duration: float) -> dt.time:
    hour = math.floor(duration / 60)
    minute = round((duration - hour * 60) / MIN_UNIT) * MIN_UNIT
    if minute == 60:
        minute = 0
        hour += 1
    return dt.time(hour=hour, minute=minute)


def get_dayily_report(target_time_str: str,
                      times: List[Tuple[dt.datetime, dt.datetime]]) -> DailyReport:
    rest_min = 0.0
    for i, t in enumerate(times):
        if i == 0:
            continue
        rest_min += (t[0] - times[i - 1][1]).total_seconds() / 60
    return DailyReport(
        date=dt.datetime.strptime(target_time_str, '%Y-%m-%d').date(),
        start=format_time(times[0][0].time()),
        end=format_time(times[-1][-1].time()),
        rest=format_min(rest_min)
    )


def get_report_from_csv(filepath: str) -> List[DailyReport]:
    with open(filepath) as f:
        reader = csv.DictReader(f)
        return get_monthly_report(reader)


def get_monthly_report(reader: Iterator[OrderedDict]) -> List[DailyReport]:
    times = []  # type: List[Tuple[dt.datetime, dt.datetime]]
    result = []  # type: List[DailyReport]
    last_row_date = None
    for row in reader:
        start_date = row['Start date']
        if last_row_date != start_date:
            if last_row_date is not None:
                result.append(get_dayily_report(last_row_date, times))
            last_row_date = start_date
            times = []
        times.append((
            dt.datetime.strptime(row['Start time'], '%H:%M:%S'),
            dt.datetime.strptime(row['End time'], '%H:%M:%S')
        ))
    if last_row_date is not None:
        result.append(get_dayily_report(last_row_date, times))
    return result


def format_report(year: int, month: int, reports: List[DailyReport]) -> str:
    start_date = dt.date(year=year, month=month, day=1)
    end_date = dt.date(year=year, month=month + 1, day=1)
    result = []
    for i in range((end_date - start_date).days):
        date = start_date + dt.timedelta(i)
        if len(reports) > 0 and reports[0].date == date:
            r = reports.pop(0)
            result.append(','.join([r.start.strftime('%H:%M:%S'),
                                    r.end.strftime('%H:%M:%S'),
                                    r.rest.strftime('%H:%M:%S')]))
        else:
            result.append(',,')
    return '\n'.join(result)


def main():
    reports = get_report_from_csv('toggle.csv')
    with open('output.csv', 'w') as f:
        f.write(format_report(2019, 10, reports))


if __name__ == '__main__':
    main()
