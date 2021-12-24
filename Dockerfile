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
ARG BASE_DISTRO=ubuntu-20.04

FROM crops/yocto:$BASE_DISTRO-base

USER root

COPY usersetup.py \
         esdk-launch.py \
         esdk-entry.py \
         restrict_groupadd.sh \
         restrict_useradd.sh \
     /usr/bin/
COPY sudoers.usersetup /etc/

# We remove the user because we add a new one of our own.
# The usersetup user is solely for adding a new user that has the same uid,
# as the workspace. 70 is an arbitrary *low* unused uid on debian.
RUN userdel -r yoctouser && \
    groupadd -g 70 usersetup && \
    useradd -N -m -u 70 -g 70 usersetup && \
    apt-get -y install curl sudo && \
    echo "#include /etc/sudoers.usersetup" >> /etc/sudoers && \
    chmod 755 /usr/bin/usersetup.py \
        /usr/bin/esdk-launch.py \
        /usr/bin/esdk-entry.py \
        /usr/bin/restrict_groupadd.sh \
        /usr/bin/restrict_useradd.sh

USER usersetup
ENV LANG=en_US.UTF-8

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/usr/bin/esdk-entry.py"]
