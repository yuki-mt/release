alias vim='nvim'

vf() {
  file=`find . | grep -v -e \.venv -e mypy_cache -e pycache -e \.git -e node_module | fzf`
  if [ -n "$file" ]; then
  vim $file
  fi
}
vm() {
  file=`git grep "$1" | fzf | cut -f1 -d:`
  if [ -n "$file" ]; then
    vim $file
  fi
}
eruda() {
    sed -i -e '/<\/head>/i<script src="https://cdnjs.cloudflare.com/ajax/libs/eruda/1.4.3/eruda.min.js"></script>\n<script>eruda.init();</script>' $1
}
rm-eruda() {
  sed -i -e '/eruda/d' $1
}
