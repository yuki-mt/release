alias ssh='ssh -o ServerAliveInterval=60'

syn () {
  public_ip=`gcloud compute instances describe instance-1 \
    --zone "us-central1-a" \
    --project "..." \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'`
  rsync --exclude='.mypy_cache' --exclude='.git' --exclude='.venv' \
    --exclude='node_modules' --exclude='__pycache__' \
    -e "ssh -i ~/.ssh/google_compute_engine" \
    -zzav `git rev-parse --show-toplevel`/ \
    ymatoba@$public_ip:/home/ymatoba/workspace/$(basename `git rev-parse --show-toplevel`)/
}
syn-del () {
  public_ip=`gcloud compute instances describe instance-1 \
    --zone "us-central1-a" \
    --project "..." \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'`
  rsync --exclude='.mypy_cache' --exclude='.git' --exclude='.venv' \
    --exclude='node_modules' --exclude='__pycache__' \
    --delete
    -e "ssh -i ~/.ssh/google_compute_engine" \
    -zzav `git rev-parse --show-toplevel`/ \
    ymatoba@$public_ip:/home/ymatoba/workspace/$(basename `git rev-parse --show-toplevel`)/
}
pf () {
  ssh -fNL $1:10.128.0.5:$1 matoba.us-central1-a.newagent-4664b
  if [ "$2" != '-s' ]; then
    termux-open-url http://localhost:$1
  fi
}
