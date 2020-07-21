#!/usr/bin/env python3

# usersetup.py
#
# Copyright (C) 2016 Intel Corporation
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

import argparse
import subprocess
import os
import sys
import grp
import pwd

def sanity_check_workdir(workdir):
    st = os.stat(workdir)
    if st.st_uid == 0 or st.st_gid == 0:
        print('The uid:gid for "{}" is "{}:{}". The uid and gid must be '
               'non-zero. Please check to make sure the "volume" or "bind" '
               'specified using either "-v" or "--mount" to docker, exists '
               'and has a non-zero uid:gid.'.format(workdir, st.st_uid,
                                                    st.st_gid))
        return False

    return True


parser = argparse.ArgumentParser()

parser.add_argument("--uid", type=int,
                    help="uid to use for the user. If not specified, "
                         "the uid of the owner of WORKDIR is used")

parser.add_argument("--gid", type=int,
                    help="gid to use for the initial login group for the "
                         "user. If not specified, the gid of WORKDIR is used")

parser.add_argument("--skel", default="",
                    help="directory to use as the skeleton for user's home")

parser.add_argument("--username", default="genericuser",
                    help="username of the user to be modified")

parser.add_argument("--workdir", default="/workdir",
                    help="Directory to base the uid on")

parser.add_argument("cmd", help="command to exec after setting up the user")

# All positional arguments are passed to args.cmd when it is ran
parser.add_argument("args", default="", nargs=argparse.REMAINDER)

args = parser.parse_args()

if not args.uid:
    # Use the owner of the workdir for the uid if the uid isn't specified
    st = os.stat(args.workdir)
    args.uid = st.st_uid
    if not sanity_check_workdir(args.workdir):
        sys.exit(1)

if not args.gid:
    # Use the group of the workdir for the gid if the gid isn't specified
    st = os.stat(args.workdir)
    args.gid = st.st_gid
    if not sanity_check_workdir(args.workdir):
        sys.exit(1)

# don't create group if exist in container
try:
    grp.getgrgid(args.gid)
except KeyError:
    cmd = "sudo restrict_groupadd.sh {} {}".format(args.gid, args.username)
    subprocess.check_call(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

try:
    pwd.getpwuid(args.uid)
except KeyError:    
    cmd = "sudo restrict_useradd.sh {} {} {} {}".format(args.uid, args.gid,
                                                        args.username, args.skel)
    subprocess.check_call(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

usercmd = [ args.cmd ] + args.args

cmd = "sudo -E -H -u {} ".format(args.username)
cmd = cmd.split() + usercmd
os.execvp(cmd[0], cmd)
