alias ssh='ssh -o ServerAliveInterval=60'

syn () {
  rsync --exclude='.mypy_cache' --exclude='.git' --exclude='*_venv' --exclude='node_modules' --exclude='__pycache__' \
    -zzav `git rev-parse --show-toplevel`/ matoba.us-central1-a.newagent-4664b:/home/u0_a84/workspace/$(basename `git rev-parse --show-toplevel`)/
}
syn-del () {
  rsync --exclude='.mypy_cache' --exclude='.git' --exclude='*_venv' --exclude='node_modules' --exclude='__pycache__' \
    --delete -zzav `git rev-parse --show-toplevel`/ matoba.us-central1-a.newagent-4664b:/home/u0_a84/workspace/$(basename `git rev-parse --show-toplevel`)/
}
pf () {
  ssh -fNL $1:10.128.0.5:$1 matoba.us-central1-a.newagent-4664b
  if [ "$2" != '-s' ]; then
    termux-open-url http://localhost:$1
  fi
}
