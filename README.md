Extensible SDK Container
========================
This repo is to create an image that is able to setup and use an extensible
sdk generated using openembedded-core.

Running the container
---------------------
* **Determine the workdir**

  The workdir you create will be used for all output from the extensible sdk,
  as well as where your workspace will be saved. You can either create a new
  directory or use an existing one.

  *It is important that you are the owner of the directory.* The owner of the
  directory is what determines the user id used inside the container. If you
  are not the owner of the directory, you may not have access to the files the
  container creates.

  For the rest of the instructions we'll assume the workdir chosen was
  `/home/myuser/workdir`.

* **The docker command**

  Assuming you used the *workdir*` from above, the command
  to run a container for the first time would be:
\
  ```
  docker run --rm -it -v /home/myuser/workdir:/workdir crops/extsdk-container \
  --url http://someserver/extensible_sdk_installer.sh
  ```
  Let's discuss some of the options:
  * **_-v /home/myuser/workdir:/workdir_**: The default location of the workdir
    inside of the container is /workdir. So this part of the command says to
    use */home/myuser/workdir* as */workdir* inside the container.
  * **_--url http://someserver/extensible_sdk_installer.sh_**: This is the
      url of the extensible sdk installer. It will automatically be downloaded
      and prepared to use inside of the workdir. Substitute in the url for
      whatever extensible sdk installer you want to use.

  You should see output similar to the following:
  ```
  Attempting to download http://someserver/extensible_sdk_installer.sh 
  ######################################################################## 100.0%
  Poky (Yocto Project Reference Distro) Extensible SDK installer version 2.1
  ==========================================================================
  You are about to install the SDK to "/workdir". Proceed[Y/n]? Y
  Extracting SDK.....done
  Setting it up...
  Extracting buildtools...
  ePreparing build system...
  done
  SDK has been successfully set up and is ready to be used.
  Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.
   $ . /workdir/environment-setup-i586-poky-linux
  SDK environment now set up; additionally you may now run devtool to perform development tasks.
  Run devtool --help for further details.
  [genericuser@b9579bd468e4 workdir]$
  ```
  At this point you should be able to use the shell to use the extensible sdk.

* **Using a previous workdir**

  In the case where you have previously setup an extensible sdk you will
  no longer need to specify the *--url* argument when starting the container.

  So the following command:
  ```
  docker run --rm -it -v /home/myuser/workdir:/workdir crops/extsdk-container
  ```
  on a previously setup workdir, should generate output similar to:
  ```
  SDK environment now set up; additionally you may now run devtool to perform development tasks.
  Run devtool --help for further details.
  [genericuser@2e42fa87f96c workdir]$
  ```

Building the container image
----------------------------
If for some reason you want to build your own image rather than using the one
on dockerhub, then run the command below in the directory containing the
Dockerfile:

```
docker build -t crops/extsdk-container .
```

The argument to `-t` can be whatever you choose.
