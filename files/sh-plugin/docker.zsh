alias k='kubectl'
alias dri='docker rmi $(docker images -f "dangling=true" -qa)'
alias drc='docker rm $(docker ps -aq)'
alias ka="kubectl apply -f"
alias kd="kubectl delete -f"
alias hi="helm install"

cache_file="$HOME/.sh-plugin/docker_ns.txt"
alias k_ns_clear="rm $cache_file"

_k_search () {
  local resource ns
  resource=$1
  ns=${2:="-n default"}

  kubectl get $resource $ns --no-headers \
    | fzf --select-1 \
    | awk '{ print $1 }'
}

_k_search_for_forward () {
  local ns svcs pods
  ns=${1:="-n default"}

  svcs=`kubectl get svc $ns --no-headers \
    | grep ClusterIP | awk '{print "svc/"$1,$5}' \
    | sed -e 's;/TCP;;'`
  pods=`kubectl get po $ns --no-headers \
    | awk '{print $1}' | sed -e "s/$/${TAB}80/"`
  echo "$pods\n$svcs" | fzf --select-1
}

_k_search_ns () {
  local rtn
  if [ ! -f "$cache_file" ]; then
    kubectl get ns --no-headers > "$cache_file"
    echo "all-namespaces" >> "$cache_file"
  fi
  rtn=`cat "$cache_file" | fzf --select-1 | awk '{ print $1 }'`
  if [[ "$rtn" =~ "all-namespaces" ]]; then
    echo '--all-namespaces'
  else
    echo "-n $rtn"
  fi
}

_k_search_resource_type () {
  cat ~/.sh-plugin/k_rs.txt | fzf --select-1
}

_k_cmd_search () {
  echo "get\ndescribe\nexec\nlogs\nport-forward" | fzf
}

_k_echo() {
  local reset_color="\033[0m"
  local bold_green="\033[1;32m"
  local message=$1
  echo -e "\n$bold_green $message $reset_color\n"
}

kk() {
  local rn rt _rn cmd ns ary ext fnl_cmd port _port host_port
  cmd=`_k_cmd_search`
  ns=`_k_search_ns`

  # Select Resource Type
  ary=(get describe)
  if [[ " ${ary[@]} " =~ " ${cmd} " ]]; then
    rt=`_k_search_resource_type`
  else
    rt=''
  fi

  # Select Resource
  ary=('exec' logs)
  if [[ " ${ary[@]} " =~ " ${cmd} " ]]; then
    rn=`_k_search pod $ns`
  elif [[ "port-forward" == $cmd ]]; then
    _rn=`_k_search_for_forward $ns`
    rn=`echo $_rn | awk '{print $1}'`
    _port=`echo $_rn | awk '{print $2}'`
  elif [[ "describe" == $cmd ]]; then
    rn=`_k_search $rt $ns`
  else
    rn=''
  fi

  # modify sub-command and add extra options
  if [[ $cmd == 'exec' ]] ; then
    cmd='exec -it'
    echo -n 'command [sh]: '
    read ext
    ext=${ext:-sh}
  elif [[ $cmd == 'port-forward' ]] ; then
    echo -n "port [$_port]: "
    read port
    port=${port:-$_port}
    echo -n "host port [8888]: "
    read host_port
    host_port=${host_port:-8888}
    ext=$host_port:$port
  elif [[ $cmd == 'logs' ]] ; then
    cmd='logs -f'
  fi

  fnl_cmd="kubectl $cmd $rt $ns $rn $ext"
  _k_echo $fnl_cmd
  # echo ": `date +%s`:0;$fnl_cmd" >> ~/.zsh_history
  eval $fnl_cmd
}

k-login() {
  image=${1:-"cosmintitei/bash-curl"}
  com=${@:2:($#-1)}
  com=${com:-"sh"}
  kubectl run --generator=run-pod/v1 test-pod -it --rm --image $image -- $com
}

hd() {
  local chart
  chart=`helm list | fzf | awk '{print $1}'`
  helm delete --purge $chart
}

hu() {
  local filepath chart
  filepath=$1
  chart=`helm list | fzf | awk '{print $1}'`
  helm upgrade -f $filepath $chart stable/$chart
}

kc() {
  local cluster_name
  cluster_name=`kubectl config get-contexts | awk '{print $2}' | tail -n +2 | fzf`
  kubectl config use-context $cluster_name
}
