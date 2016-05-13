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
# This dockerfile is meant to create a container that contains an extensible
# sdk that has already been "prepared."
#
# In order to use it, create a directory that contains both the extensible
# sdk(created by "bitbake someimage -c populate_sdk_ext") and the Dockerfile.
#
# Since the extensible sdk can have various names, rename it to ./extsdk.sh
# so that the Dockerfile can remain simple.
FROM crops/yocto:debian-8-base

USER root

# We remove the user because we add a new one of our own.
# Set sdkuser to 1000 so that we can use a known uid in sudoers for
# after usermod has been ran.
RUN userdel -r yoctouser && \
    useradd -U -m -o -u 1000 sdkuser && \
    apt-get -y install sudo && \
    echo "#include /etc/sudoers.usersetup" >> /etc/sudoers

COPY usersetup.py esdk-launch.py esdk-entry.py restrict_usermod.sh /usr/bin/
COPY sudoers.usersetup /etc

ENTRYPOINT ["esdk-entry.py"]
