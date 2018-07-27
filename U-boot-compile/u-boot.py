#!/usr/bin/python3

import os
import sys


def menu():

    if len(sys.argv) == 2 and sys.argv[1] == "-install":
        os.system("apt-get update")
        os.system("apt-get install -y make ncurses-dev gedit flex bc bison u-boot-tools gcc gcc-arm-linux-gnueabihf "
                  "gcc-arm-linux-gnueabi g++-arm-linux-gnueabihf libc6-armel-cross libncurses5-dev git-core git-gui "
                  "gitk device-tree-compiler gcc-aarch64-linux-gnu mtools")
        os.system("apt-get install -y u-boot-tools autoconf texinfo g++ gettext build-essential "
                  "crossbuild-essential-armhf gcc-arm-linux-gnueabihf gcc-aarch64-linux-gnu mtools parted libssl-dev")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-install-rpi":
        os.system("apt-get update")
        os.system("apt-get install -y gcc-aarch64-linux-gnu")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-install-gcc":
        os.system("apt-get update")
        os.system("apt-get install -y gcc-8 gcc-6")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-asus":
        os.system("mkdir ~/asus")
        os.system("mkdir ~/asus/u_boot")
        os.system("mkdir ~/asus/kernel")
        os.system("git clone https://github.com/TinkerBoard/debian_u-boot.git ~/asus/u_boot")
        os.system("git clone https://github.com/TinkerBoard/debian_kernel.git ~/asus/kernel")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-rpi":
        os.system("mkdir ~/rpi")
        os.system("mkdir ~/rpi/u_boot")
        os.system("mkdir ~/rpi/kernel")
        os.system("git clone https://github.com/u-boot/u-boot ~/rpi/u_boot")
        os.system("git clone https://github.com/raspberrypi/linux.git ~/rpi/kernel")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-delete-asus":
        os.system("rm -rf asus")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-delete-rpi":
        os.system("rm -rf ~/rpi/")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-clone-buildroot":
        os.system("mkdir ~/buildroot")
        os.system("git clone git://git.buildroot.net/buildroot ~/buildroot")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-destroy_buildroot":
        os.system("rm -rf buildroot")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-rpi-tool":
        os.system("mkdir ~/rpi-tools")
        os.system("git clone git://github.com/raspberrypi/tools rpi-tools")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-make-rpi":
        os.system("PATH=~/rpi/u_boot/:$PATH")
        os.system("make -C ~/rpi/u_boot ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- O=Rpi rpi_2_defconfig all -j4")
        print("""
        \n
        Compilation done Output folder is rpi/u_boot/RPI   
        
        """)
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-help":
        os.system("clear")
        print('''

   ++==============================================================================++
   ||                            Use with switches:                                ||
   ++==============================================================================++
   ||                                                                              ||
   || -install: Install all package to cross compiler                              ||
   ||                                                                              ||
   ||                                                                              ||
   || -install-rpi: install cross compiler for Raspberry pi (ARCH=64bit)           ||
   ||                                                                              ||
   || -clone-asus: Make directory asus and clone kernel and u boot for asus        ||
   ||                                                                              ||
   || -clone-rpi: Make directory asus and clone kernel and u boot for rpi          ||
   ||                                                                              ||
   || -clone-buildroot: Cloning builroot repo from github                          ||
   ||                                                                              ||
   || -delete-asus: Delete directory asus                                          ||
   ||                                                                              ||
   || -delete-rpi: Delete directory rpi                                            ||
   ||                                                                              ||
   || -rpi-tool  Clone rpi cross-compile tool from repo                            ||
   ||                                                                              ||
   || -make-rpi make and compile u-boot for RPI                                    ||
   ||                                                                              ||
   ||                                                                              ||
   ||                                                                              ||
   ||                                                                              ||
   ++------------------------------------------------------------------------------++
      ''')
        return
    else:
        print('Use command ./u-boot -help')
    return


menu()
