###
# シンボリックリンクを消して、リンク先のものをそこにハードコピー
###
set -eu
target_dir=$1
for link in $(find $target_dir -type l); do
    dir=`dirname $link`
    origin=$dir/`readlink $link`
    rm $link
    cp $origin $link
done

