#!/bin/bash
# Copyright (C) 2015-2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# This is just a lightweight wrapper around useradd that prevents using a uid
# less than 101 as the uid.

# "Force" the argument to be an integer, it should error if it isn't an int
gid=$(($1))
groupname=$2

if [ $gid -eq 0 ]; then
    echo "Refusing to use a gid of 0"
    exit 1
else
    groupadd -o -g $gid "$groupname"
fi
