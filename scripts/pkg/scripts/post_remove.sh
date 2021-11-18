#!/bin/sh

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Description:
# Post-remove script to clean up the environment.

set -e

REMOVE_USER_AND_GROUP=false
REMOVE_DIRS=false

case $1 in
  # Includes cases for all valid arguments, exit 1 otherwise
  # Setup for Debian environment
  purge)
    REMOVE_USER_AND_GROUP=true
    REMOVE_DIRS=true
  ;;
  remove)
    REMOVE_DIRS=true
  ;;

  failed-upgrade|abort-install|abort-upgrade|disappear|upgrade|disappear)
  ;;

  # Setup for RPMs environment
  0)
    REMOVE_USER_AND_GROUP=true
    REMOVE_DIRS=true
  ;;

  1)
  ;;

  *)
      echo "post remove script called with unknown argument \`$1'" >&2
      exit 1
  ;;
esac

if [ "$REMOVE_USER_AND_GROUP" = "true" ]; then
  if getent passwd "<%= user %>" >/dev/null; then
    userdel "<%= user %>"
  fi

  if getent group "<%= group %>" >/dev/null; then
    groupdel "<%= group %>"
  fi
fi

if [ "$REMOVE_DIRS" = "true" ]; then

  if [ -d "<%= homeDir %>" ]; then
    rm -rf "<%= homeDir %>"
  fi

  if [ -d "<%= configDir %>" ]; then
    rmdir --ignore-fail-on-non-empty "<%= configDir %>"
  fi

  if [ -d "<%= dataDir %>" ]; then
    rmdir --ignore-fail-on-non-empty "<%= dataDir %>"
  fi
fi
