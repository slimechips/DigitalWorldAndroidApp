# EzEat Android App

## Building Kivy App from Source

1. Ensure you have Python and Pip installed beforehand.

2. Follow the installation instructions for Kivy here: [Windows](https://kivy.org/doc/stable/installation/installation-windows.html), [macOS](https://kivy.org/doc/stable/installation/installation-osx.html), [Linux](https://kivy.org/doc/stable/installation/installation-linux.html).

3. Clone this repository.

## Using Buildozer to Build Android App (Ubuntu, Elementary OS)

- Install `buildozer`:

      # via pip (latest stable, recommended)
      sudo pip install buildozer

      # latest dev version
      sudo pip install   https://github.com/kivy/buildozer/archive/master.zip

      # git clone, for working on buildozer
      git clone https://github.com/kivy/buildozer
      cd buildozer
      python setup.py build
      sudo pip install -e .

- Install `virtualenv`:

      sudo apt-get install virtualenv

- Install dependencies for Python-for-Android (P4A):

      sudo dpkg --add-architecture i386
      sudo apt-get update
      sudo apt-get install -y build-essential ccache git zlib1g-dev python2.7 python2.7-dev libncurses5:i386 libstdc++6:i386 zlib1g:i386 openjdk-8-jdk unzip ant ccache autoconf libtool

- Ensure that you are using the latest version of Cython:

      sudo apt-get update
      sudo apt-get install cython

- Go into your application directory and run:

      buildozer init
      # edit the buildozer.spec, then
      buildozer android debug deploy run 
