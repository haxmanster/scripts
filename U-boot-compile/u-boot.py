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

    if len(sys.argv) == 2 and sys.argv[1] == "-make-asus-uboot":
        os.system("PATH=~/asus/u_boot/:$PATH")
        os.system("make -C ~/asus/u_boot CROSS_COMPILE=arm-linux-gnueabi- O=miniarm-rk3288 tinker-rk3288_defconfig all -j4 -s ")
        print("""
        \n
        Compilation done Output folder ~/asus/u_boot/miniarm-rk3288
        """)
        print("Creating image boot.img")
        os.system("mkdir ~/uboot-out")
        os.system("mkimage -n rk3288 -T rksd -d ~/asus/u_boot/miniarm-rk3288/spl/u-boot-spl-dtb.bin u-boot.img")
        os.system("cat ~/asus/u_boot/miniarm-rk3288/u-boot.bin >> ~/uboot-out/u-boot.img")
        print("""
        \n
        Creating image done. Output directory $home/uboot-out"
        """)
        return


    if len(sys.argv) == 2 and sys.argv[1] == "-make-rpi":
        os.system("PATH=~/rpi/u_boot/:$PATH")
        os.system("make -C ~/rpi/u_boot ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- O=Rpi rpi_2_defconfig all -j4")
        print("""
        \n
        Compilation done Output folder is rpi/u_boot/RPI
        """)
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-make-asus-kernel":
        os.system("PATH=~/asus/kernel/:$PATH")
        os.system("mkdir ~/tinkerboard-zImage/")
        os.system("make -C ~/asus/kernel ARCH=arm O=miniarm-3288 miniarm-rk3288_defconfig -j4")
        os.system("make -C ~/asus/kernel zImage ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- O=miniarm-3288 -j4")
        os.system("cp ~/asus/kernel/miniarm-3288/arch/arm/boot/zImage ~/tinkerboard-zImage")
        print("""
        \n
        Compilation done Output folder is ~/tinkerboard-zImage
        """)
        return

    if len(sys.argv) == 2 and sys.argv[1] == "-help":
        os.system("clear")
        print('''

   ++=================================================================================================================================================================++
   ||                                                                  Use command ./u-boot.py - <switch>                                                             ||
   ++=================================================================================================================================================================++
   ||                                                                              ||                                                                                 ||
   || -install: Install all package to cross compiler                              ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -install-rpi: install cross compiler for Raspberry pi (ARCH=64bit)           ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -clone-asus: Make directory asus and clone kernel and u boot for asus        ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -clone-rpi: Make directory asus and clone kernel and u boot for rpi          ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -clone-buildroot: Cloning builroot repo from github                          ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -delete-asus: Delete directory asus                                          ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -delete-rpi: Delete directory rpi                                            ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -rpi-tool  Clone rpi cross-compile tool from repo                            ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -make-rpi make and compile u-boot for RPI                                    ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -make-asus-uboot make and compile u-boot for tinkerboard                     ||                                                                                 ||
   ||                                                                              ||                                                                                 ||
   || -make-asus-kernel make and compile kernel source for tinkerboard             ||                                                                                 ||
   ++------------------------------------------------------------------------------++---------------------------------------------------------------------------------++
   ++------------------------------------------------------------------------------++---------------------------------------------------------------------------------++
      ''')
        return
    else:
        print('Use command ./u-boot -help')
    return


menu()
