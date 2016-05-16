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

#
# ext sdk container
#
FROM crops/yocto:debian-8-base

USER root

# We remove the user because we add a new one of our own.
# The usersetup user is solely for adding a new user that has the same uid,
# as the workspace. 70 is an arbitrary *low* unused uid on debian.
RUN userdel -r yoctouser && \
    useradd -U -m -u 70 usersetup && \
    apt-get -y install sudo && \
    echo "#include /etc/sudoers.usersetup" >> /etc/sudoers

COPY usersetup.py esdk-launch.py esdk-entry.py restrict_useradd.sh /usr/bin/
COPY sudoers.usersetup /etc

USER usersetup

ENTRYPOINT ["esdk-entry.py"]
