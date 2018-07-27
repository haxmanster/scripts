import os
import sys

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

menu()
