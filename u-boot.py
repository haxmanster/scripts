#!/usr/bin/python3

import os
import sys



def console():

    if len(sys.argv) == 2 and sys.argv[1] == "-install":
        os.system("apt-get update")
        os.system("apt-get install -y ncurses-dev gedit flex bc bison u-boot-tools gcc gcc-arm-linux-gnueabihf gcc-arm-linux-gnueabi g++-arm-linux-gnueabihf libc6-armel-cross libncurses5-dev git-core git-gui gitk device-tree-compiler gcc-aarch64-linux-gnu mtools")
        os.system("apt-get install -y u-boot-tools autoconf texinfo g++ gettext build-essential crossbuild-essential-armhf gcc-arm-linux-gnueabihf gcc-arm-linux-gnueabi device-tree-compiler gcc-aarch64-linux-gnu mtools parted libssl-dev")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-install-rpi":
        os.system("apt-get update")
        os.system("apt-get install -y gcc-arch64-linux-gnu")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-install-gcc":
        os.system("apt-get update")
        os.system("apt-get install -y gcc-8 gcc-6")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-asus":
        os.system("mkdir asus")
        os.system("mkdir asus/u_boot")
        os.system("mkdir asus/kernel")
        os.system("git clone https://github.com/TinkerBoard/debian_u-boot.git asus/u_boot")
        os.system("git clone https://github.com/TinkerBoard/debian_kernel.git asus/kernel")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-rpi":
        os.system("mkdir rpi")
        os.system("mkdir rpi/u_boot")
        os.system("mkdir rpi/kernel")
        os.system("git clone git://git.denx.de/u-boot.git rpi/u_boot")
        os.system("git clone https://github.com/raspberrypi/linux.git rpi/kernel")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-delete-asus":
        os.system("rm -rf asus")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-delete-rpi":
        os.system("rm -rf rpi")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-buildroot":
        os.system("mkdir ~/buildroot")
        os.system("git clone git://git.buildroot.net/buildroot ~/buildroot")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-destroy_buildroot":
        os.system("rm -rf buildroot")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "menu":
        menu()
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-help":
        os.system("clear")
        print ('''

   +==============================================================================+
   |                            Use with switches:                                |
   +==============================================================================+
   |                                                                              |
   | -install: Install all package to cross compiler                              |
   |                                                                              |
   | -install-gcc: install gcc package                                            |
   |                                                                              |
   | -install-rpi: install cross compiler for Raspberry pi (ARCH=64bit)           |
   |                                                                              |
   | -clone-asus: Make directory asus and clone kernel and u boot for asus        |
   |                                                                              |
   | -clone-rpi: Make directory asus and clone kernel and u boot for rpi          |
   |                                                                              |
   | -clone-buildroot: Cloning builroot repo from github                          |
   |                                                                              |
   | -delete-asus: Delete directory asus                                          |
   |                                                                              |
   | -delete-rpi: Delete directory rpi                                            |
   |                                                                              |
   |                                                                              |
   +------------------------------------------------------------------------------+
      ''')
        return
    else:
         print('Use command ./u-boot -help')
    return


def menu():
    print(" Welcome in initiation script ")

    print("""
**************************************************************
*============================================================*
*|               Master control unit xD                     |*
*============================================================*
**************************************************************
* [1] Install python modules (flask,pip,etc)                 *
* [2] Install gitlab-ce                                      *
* [3] Install gcc modules                                    *
* [4] Install gcc modules                                    *
* [5] Install gcc modules                                    *
* [6] Install gcc modules                                    *
* [7] Install gcc modules                                    *
* [8] Install gcc modules                                    *
* [9] Install gcc modules                                    *
* [10] Install gcc modules                                   *
* [11] Exit this menu                                        *
**************************************************************
          """)
    choice = input("choose an option ")

    if choice == "1":
        os.system("apt install gcc-8")

    elif choice == "2":
        os.system("apt install mc")

    elif choice == "11":
        print("bye")

    else:
        os.system("clear")
        menu()

console()
