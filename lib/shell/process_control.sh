#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a library of all Processes related functions
# Source this file in your scripts

set -m

TRAP_SIG_LIST="TERM INT EXIT CHLD"
TRAP_SIG_LIST_NO_SIGCHLD="TERM INT EXIT"
PARENT_PID_LIST=()

function Wait_Process_PID() {
    for pid_wait in $@
    do
        wait $pid_wait
        echo -e "\tProcess $pid_wait confirmed exited with code $?"
    done
}

function Kill_Process_PID() {
    # Reset all the signals in case all the trap check again due to Kill_Process_PID() and child processes exit from subshells
    trap - $TRAP_SIG_LIST

    echo "Attempt to Terminate Process with PID: $@"
    for pid_kill in $@
    do
      echo "Check PID $pid_kill Status"

      CHILD_PID_LIST=`pgrep -P $pid_kill`

      if [ ! -z "$CHILD_PID_LIST" ]
      then
          echo -e "\tProcess have childs $CHILD_PID_LIST exist, gracefully terminated with code $?"
          kill -TERM $CHILD_PID_LIST
      fi

      if kill -0 $pid_kill > /dev/null 2>&1
      then
          echo -e "\tProcess $pid_kill exist, gracefully terminated with code $?"
          kill -TERM $pid_kill
          Wait_Process_PID $pid_kill
      else
          echo -e "\tProcess $pid_kill not exist"
      fi

    done
}

function Spawn_Process_And_Save_PID() {
    echo "Spawn '$@' in `pwd`"
    eval $@
    CURR_PID=$!
    echo "PID: $CURR_PID"
    PARENT_PID_LIST+=( $CURR_PID )
}


function Trap_Wait_Term_Cleanup() {
    # Reset -e so that the process does not quit in the middle of cleanup
    set +e
    TEMP_WORKING_DIR=$@
    echo "PID List: ${PARENT_PID_LIST[@]}"
    echo "Working Directory: $@"
    echo "Trap and Wait for these signals: ${TRAP_SIG_LIST}"

    trap '{ Kill_Process_PID ${PARENT_PID_LIST[@]}; echo Removing $TEMP_WORKING_DIR; rm -rf -- "$TEMP_WORKING_DIR"; }' $TRAP_SIG_LIST

    Wait_Process_PID ${PARENT_PID_LIST[@]}
}



