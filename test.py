import os
import sys

def menu():
    print(" Welcome in initiation script ")

    print("""

[1] Install python modules (flask,pip,etc)
[2] Install 
[3] Install gcc modules
[4] Install gcc modules
[5] Install gcc modules
[6] Install gcc modules
[7] Install gcc modules
[8] Install gcc modules
[9] Install gcc modules
[10] Install gcc modules
[11] Install gcc modules
          """)
    choice = input("choose an option ")
    if choice == "1":
        os.system("apt install gcc-8")
    elif choice == "2":
        os.system("apt install mc")
    else:
         menu()

menu()
