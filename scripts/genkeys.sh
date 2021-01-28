#!/bin/sh

genkeys(){
    placeHolder="{GenKey()}"
    for str in $(grep ${placeHolder} $1)
    do
      sed -i "s/${placeHolder}/$(openssl rand -hex 12)/" $1
    done
}
export genkeys