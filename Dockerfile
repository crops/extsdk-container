# Copyright (C) 2015-2016 Intel Corporation
# Copyright (C) 2022 Konsulko Group
#
# SPDX-License-Identifier: GPL-2.0-only
#

# ext sdk container
#
FROM crops/yocto:ubuntu-18.04-base

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
