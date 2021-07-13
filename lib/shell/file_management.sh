#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# This is a library of all File/Folder management related functions
# Source this file in your scripts

set -m

TRAP_SIG_LIST="TERM INT EXIT CHLD"
TRAP_SIG_LIST_NO_SIGCHLD="TERM INT EXIT"

function Temp_Folder_Create() {
    mktemp -d
    
}

function File_Delete() {
    FILE_NAME=$@
    echo Attempt to rm "$FILE_NAME"

    if [ -z "$FILE_NAME" ]
    then
        echo "No File/Folder Exist"
    else
        echo "Removing $FILE_NAME"
        rm -rf -- "$FILE_NAME"
    fi
}

function Trap_File_Delete() {
    FILE_NAME=$@
    echo "Trap deletion of $FILE_NAME for these signals: $TRAP_SIG_LIST"
    trap '{File_Delete $FILE_NAME;}' TRAP_SIG_LIST
}

function Trap_File_Delete_No_Sigchld() {
    FILE_NAME=$@
    echo "Trap deletion of $FILE_NAME for these signals: $TRAP_SIG_LIST_NO_SIGCHLD"
    trap '{File_Delete $FILE_NAME;}' TRAP_SIG_LIST_NO_SIGCHLD
    
}

