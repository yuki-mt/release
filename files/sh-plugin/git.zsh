alias rm-merged='git branch --merged | grep -v master | grep -v develop | grep -v "*" | while read BRANCH; do git branch -d ${BRANCH}; done; unset BRANCH;'
alias ga='git add -A && git diff --cached'
alias gr='cd `git rev-parse --show-toplevel`'
alias grh='git reset --hard HEAD'
alias gp='git pull'
alias gs='git status'
alias gu='git submodule update'
alias gg="git log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all --date-order"
gc () {
  git checkout $1
}
gcbf () {
  git checkout -b feature/$1
}
gcb () {
  git checkout -b $1
}
gcm () {
  git commit -m "$*"
}
gcl() {
  branch=`git branch | fzf | sed 's/^[ |\*]*//'`
  if [ -n "$branch" ]; then
    git checkout $branch
  fi
}
gcr() {
  branch=`git branch -r | fzf | sed 's/^[ |\*]*origin\///'`
  if [ -n "$branch" ]; then
    git checkout $branch
  fi
}
or () {
  remote=`git remote -v | grep origin | tr '\n' ' ' | awk '{print $2}' | head -1`
  if [ "$remote" = "http*" ]; then
    open $remote
  else
    echo "$remote" | sed -e "s/git@\(.*\):\(.*\)\.git.*/https:\/\/\1\/\2/" | xargs open
  fi
}
