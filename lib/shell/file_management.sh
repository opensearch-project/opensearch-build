#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# This is a library of all File/Folder management related functions
# Source this file in your scripts

set -m

TRAP_SIG_LIST="TERM INT EXIT CHLD"
TRAP_SIG_LIST_NO_SIGCHLD="TERM INT EXIT"

function Temp_Folder_Create() {
    TEMP_SUFFIX="_TEMP"
    TEMP_FOLDER=$(mktemp --suffix=$TEMP_SUFFIX -d)
    echo $TEMP_FOLDER
    
}

function Trap_File_Delete() {
    TEMP_FOLDER=$@
    echo "Trap deletion of $TEMP_FOLDER for these signals: $TRAP_SIG_LIST"
    trap '{ echo Attempt to rm "$TEMP_FOLDER"; if [ ! -z "$TEMP_FOLDER" ]; then echo Removing "$TEMP_FOLDER"; rm -rf -- "$TEMP_FOLDER"; else echo No File/Folder Exist; fi;}' $TRAP_SIG_LIST
    
}

function Trap_File_Delete_No_Sigchld() {
    TEMP_FOLDER=$@
    echo "Trap deletion of $TEMP_FOLDER for these signals: $TRAP_SIG_LIST_NO_SIGCHLD"
    trap '{ echo Attempt to rm "$TEMP_FOLDER"; if [ ! -z "$TEMP_FOLDER" ]; then echo Removing "$TEMP_FOLDER"; rm -rf -- "$TEMP_FOLDER"; else echo No File/Folder Exist; fi;}' $TRAP_SIG_LIST_NO_SIGCHLD
    
}

