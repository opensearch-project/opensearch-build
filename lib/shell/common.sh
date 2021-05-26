#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# This is a library of all OpenSearch/Dashboards cluster related functions
# Source this file in your scripts

set -m

TRAP_SIG_LIST="TERM INT EXIT CHLD"
TRAP_SIG_LIST_NO_SIGCHLD="TERM INT EXIT"
PARENT_PID_LIST=()
TEMP_FOLDER=""


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

function Temp_Folder_Create() {
    TEMP_SUFFIX="_TEMP"
    TEMP_FOLDER=$(mktemp --suffix=$TEMP_SUFFIX -d)
    echo $TEMP_FOLDER
    
}

function Trap_File_Delete() {
    echo "Trap deletion of $TEMP_FOLDER for these signals: $TRAP_SIG_LIST"
    trap '{ echo Attempt to rm "$TEMP_FOLDER"; if [ ! -z "$TEMP_FOLDER" ]; then echo Removing "$TEMP_FOLDER"; rm -rf -- "$TEMP_FOLDER"; else echo No File/Folder Exist; fi;}' $TRAP_SIG_LIST
    
}

function Trap_File_Delete_No_Sigchld() {
    echo "Trap deletion of $TEMP_FOLDER for these signals: $TRAP_SIG_LIST_NO_SIGCHLD"
    trap '{ echo Attempt to rm "$TEMP_FOLDER"; if [ ! -z "$TEMP_FOLDER" ]; then echo Removing "$TEMP_FOLDER"; rm -rf -- "$TEMP_FOLDER"; else echo No File/Folder Exist; fi;}' $TRAP_SIG_LIST_NO_SIGCHLD
    
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
    echo "PID List: ${PARENT_PID_LIST[@]}"
    echo "Working Directory: $@"
    echo "Trap and Wait for these signals: ${TRAP_SIG_LIST}"

    trap '{ Kill_Process_PID ${PARENT_PID_LIST[@]}; echo Removing $TEMP_FOLDER; rm -rf -- "$TEMP_FOLDER"; }' $TRAP_SIG_LIST

    Wait_Process_PID ${PARENT_PID_LIST[@]}
}



