# EzEat Android App

## Building Kivy App from Source

1. Ensure you have Python3 and Pip3 installed beforehand.

2. Follow the installation instructions for Kivy here: [Windows](https://kivy.org/doc/stable/installation/installation-windows.html), [macOS](https://kivy.org/doc/stable/installation/installation-osx.html), [Linux](https://kivy.org/doc/stable/installation/installation-linux.html).

3. Clone this repository.

## Using Buildozer to Build Android App (Ubuntu 18.04, Elementary OS 5.0 Juno)

- Install `buildozer`:

      # via pip (latest stable, recommended)
      sudo pip3 install --upgrade buildozer

- Targetting Android on Ubuntu 18.04

      sudo pip3 install --upgrade cython==0.28.6
      sudo dpkg --add-architecture i386
      sudo apt update
      sudo apt install build-essential ccache git libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 python2.7 python2.7-dev openjdk-8-jdk unzip zlib1g-dev zlib1g:i386

- Use Java EE Module:

      export JAVA_OPTS='-XX:+IgnoreUnrecognizedVMOptions --add-modules java.se.ee'

- Go into your application directory and run:

      buildozer init
      # edit the buildozer.spec, then
      buildozer android debug deploy run 