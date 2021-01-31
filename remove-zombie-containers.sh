#!/bin/sh

SILENCE=0
for arg in "$@"
do
    case $arg in
    -h|--help)
        echo "Usage: show-scans-status [options]"
        echo "options:"
        echo "-h, --help               show this help message"
        echo "-s, --silence            don't wait for approval to remove containers"
        echo "examples:"
        echo "Linux and MinGw distribution (gitbash, cygwin etc.)"
        echo "  $ sh show-scans-status.sh"
        echo "WSL2 ubuntu:"
        echo "  $ /bin/bash show-scans-status.sh"
        exit 0
        ;;
    -s|--silence)
        SILENCE=1
        shift 
        ;;
    esac
done

echo "Removing following containers:"
docker ps --no-trunc -f name=sca-agent* --format "table {{.ID}}\t{{.Names}}" || exit
echo "-------------------------------------------"
if [ $SILENCE -eq 0 ]; then
   echo "Press any key to continue..."
   read -n 1
fi

echo "Starting"
ids=$(docker ps --no-trunc -f name=sca-agent* --format "{{.ID}}")

# check if Linux or wsl/mingw by try find cmd.exe
cmd=$(command -v cmd.exe || echo shell)
if [ "$cmd" != 'shell' ]; then
   echo "Creating zombie container with cmd to access MobyLinuxVM"
   cmd.exe /C "docker run --name zombie --net=host --ipc=host --uts=host --pid=host --security-opt=seccomp=unconfined --privileged -it -d -v /:/host alpine sh" || exit
   removeCmd='cmd.exe /C "docker exec -i zombie rm -r /host/var/lib/docker/containers"'
else
   removeCmd='rm -r /var/lib/docker/containers'
fi
echo "-------------------------------------------"
for id in $(echo "$ids")
do
   if [ "$cmd" = 'shell' ]; then
      umount /var/lib/docker/containers/$id/mounts/shm&> /dev/null && echo "$id container unmounted" || echo "$id nothing to unmount"
   fi
   eval "$removeCmd/$id" && echo "$id container deleted" || continue
done 

echo "-------------------------------------------"
if [ "$cmd" != 'shell' ]; then
   zombie=$(docker container rm -f zombie)
   if [ "$zombie" = 'zombie' ]; then
      echo "Zombie container deleted"
   else
      echo "Error deleting zombie container"
      exit
   fi
   echo -e "\e[1mPlease restart docker to complete the operation"
else
   echo "Restarting docker"
   service docker restart
fi
