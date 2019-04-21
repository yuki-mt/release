#!/bin/bash
set -eu

CONFIG_PATH=`dirname $0`/config.json
SPEC_PATH=`dirname $0`/spec.json
SNAP_NAME='my_work'
NUM_KEEP_SNAPSHOTS=2
TOKEN=`cat \`dirname $0\`/.token`

request () {
  method=$1
  path=$2
  body=${3:-""}
  curl -sS -X $method -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$body" \
    "https://api.digitalocean.com/v2/$path"
}

snapshot_ids () {
  request GET "snapshots?page=1&per_page=100" | \
    jq -r ".snapshots[] | select(.name == \"$SNAP_NAME\") | .id"
}

snap_size () {
  snap_ids=`snapshot_ids`
  if [ -z "$snap_ids" ]; then
    echo 0
  else
    echo $snap_ids | awk '{print NF}'
  fi
}

droplet_status () {
  id=$1
  request GET "droplets/$id" | jq -r '.droplet.status'
}

shutdown () {
  id=$1
  status=`droplet_status $id`
  if [ -z $status ]; then
    echo "the droplet does not exist"
    return 1
  elif [ $status == 'off' ]; then
    echo 'the droplet is already shut down'
  else
    request POST "droplets/$id/actions" '{"type": "shutdown"}' > /dev/null
    echo "waiting for shutdown..."
    sleep 10
    while [ $status != 'off' ]; do
      sleep 5
      status=`droplet_status $id`
    done
    echo "complete shutting down"
  fi
  return 0
}

rotate_snapshots () {
  snap_ids=`snapshot_ids`
  size=`echo $snap_ids | awk '{print NF}'`

  delete_num=`expr $size - $NUM_KEEP_SNAPSHOTS`
  if [ $delete_num -gt 0 ]; then
    IFS_BACKUP=$IFS
    IFS=' '
    for old_image_id in `echo $snap_ids | head -$delete_num` ; do
      request DELETE "snapshots/$old_image_id"
      echo "deleted an old snapshot. ID: $old_image_id"
    done
    IFS=$IFS_BACKUP
  fi
}

snapshot () {
  id=$1
  shutdown $id
  if [ $? -eq 1 ]; then
    return 1
  fi

  current_size=`snap_size`
  request POST "droplets/$id/actions" "{\"type\": \"snapshot\", \"name\": \"$SNAP_NAME\"}" > /dev/null
  echo "waiting for creating snapshot..."
  sleep 40
  new_size=`snap_size`
  while [ $current_size -eq $new_size ]; do
    sleep 5
    new_size=`snap_size`
  done
  echo "complete creatging snapshot"

  rotate_snapshots
}

subcommand="$1"
shift

case $subcommand in
  get)
    request GET "droplets?page=1&per_page=10" | jq
    ;;
  create)
    # replace base image with snapshot ID if exists
    image_id=`snapshot_ids | tail -1`
    if [ -z "$image_id" ]; then
      echo 'use the prepared base image'
      spec_json=`cat $SPEC_PATH`
    else
      echo 'use the latest snapshot'
      spec_json=`sed -e "s/\"image\": \".*\"/\"image\": \"$image_id\"/" $SPEC_PATH`
    fi

    # create Droplet and save info to config.json
    id=`request POST "droplets" "$spec_json" | jq '.droplet.id'`
    ip_address=`request GET "droplets/$id" | jq '.droplet.networks.v4[0].ip_address'`
    echo "{\"instance_id\": $id, \"ip\": $ip_address}" > $CONFIG_PATH
    ;;
  snap)
    id=`cat $CONFIG_PATH | jq -r '.instance_id'`
    snapshot $id
    ;;
  delete)
    option=${1:-""}
    if [ "$option" == '-t' ] ; then
      # remove by tag
      request DELETE "droplets?tag_name=work" | jq
    else
      id=`cat $CONFIG_PATH | jq -r '.instance_id'`
      if [ "$option" != '-n' ] ; then
        snapshot $id
      fi
      request DELETE "droplets/$id" | jq
    fi
    ;;
  list_ssh)
    request GET "account/keys" | jq
    ;;
  ssh)
    ssh root@`cat $CONFIG_PATH | jq -r '.ip'`
    ;;
  status)
    id=`cat $CONFIG_PATH | jq -r '.instance_id'`
    droplet_status $id
    ;;
  other)
    echo 'you can try some experimental commands here'
    ;;
  *)
    echo "subcommand is wrong"
    echo "[get, create, snap, delete, list_ssh, ssh, status, other]"
    ;;
esac
