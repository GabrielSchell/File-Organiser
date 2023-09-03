import getpass
import os
import sys
from lib import intialiser, organiser

FOLDER_NAME = "↪ Organize Folder ↩"

def build_name_of_directory(id_):
    return os.path.join("C:/Users",id_, "Downloads")


def choice_1():
    return build_name_of_directory(
        str(
            input(
                r"Please write down your exact username (you can found it in C:\Users): "
            )
        )
    ).replace("\\", "/")


def choice_2():
    return str(input(r"Please write the exact path of the folder: "))


def main():
    USER_ID = f"{getpass.getuser()}"
    def_path = build_name_of_directory(USER_ID).replace("\\", "/")

    while True:
        print("\nBy default, I clean your download directory but you can use me to clean any folder you want !")
        print("I do this by moving files in an organized folder structure which is described in 2 files:")
        print(" - struct.json: the structure of the folder depending on the category of the file extension.")
        print(" - ext.json: the list of the file extensions and their category.")
        input("press 'enter' to continue\n")

        path_choice = input(
            "Choose by typing the number\n1 - (default) Download Folder\n2 - Another folder\nYour choice: "
        )
        print()

        if path_choice in ["1", ""]:
            yes_or_no_dlf = input(
                f"Do you confirm that your download directory is {def_path} ? \n1 - (default) yes\n2 - no\nYour choice: "
            )
            if yes_or_no_dlf in ["2","no"]:
                path = choice_1()
                while os.path.exists(path) != True:
                    print(
                        '\nIt appears that the path "'
                        + path
                        + "\" doesn't exist, thus your 'downloads' location was not found. Please retry\n"
                    )
                    print(" --- \n")
                    path = choice_1()
                def_path = path
            break

        elif path_choice == "2":
            path = choice_2()
            while os.path.exists(path) != True:
                print(
                    '\nIt appears that the path "'
                    + path
                    + "\" doesn't exist, thus your 'downloads' location was not found. Please retry\n"
                )
                print(" --- \n")
                path = choice_2()
            def_path = path
            break

        elif path_choice == "stop":
            sys.exit()
        else:
            print("That answer was not expected. Please write yes or no")
            print("------------")

    print()
    intialiser(def_path, FOLDER_NAME)
    organiser(def_path, FOLDER_NAME)
    input("press 'enter' to finish")


if __name__ == "__main__":
    main()
