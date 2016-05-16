#!/usr/bin/env python

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

parser = argparse.ArgumentParser()

parser.add_argument("--uid", type=int,
                    help="uid to use for the user. If not specified, "
                         "the uid of the owner of WORKDIR is used")

parser.add_argument("--username", default="genericuser",
                    help="username of the user to be modified")

parser.add_argument("--workdir", default="/workdir",
                    help="Directory to base the uid on")

parser.add_argument("cmd", help="command to exec after setting up the user")

# All positional arguments are passed to args.cmd when it is ran
parser.add_argument("args", default="", nargs=argparse.REMAINDER)

args = parser.parse_args()
st = os.stat(args.workdir)

if not args.uid:
    # Use the owner of the workdir for the uid if the uid isn't specified
    args.uid = st.st_uid

cmd = "sudo restrict_useradd.sh {} {}".format(args.uid, args.username)

subprocess.check_call(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

usercmd = "{} {}".format(args.cmd, " ".join(args.args))

cmd = ("sudo -u {} ".format(args.username) + usercmd).split()
os.execvp(cmd[0], cmd)
