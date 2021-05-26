#!/bin/bash

. ../lib/shell/common.sh

TESTARR=()

sleep 5 &
TESTARR+=( $! )

sleep 10 &
TESTARR+=( $! )

#echo ${TESTARR[@]}
Trap_And_Wait ${TESTARR[@]}

#ps -ef | grep sleep
