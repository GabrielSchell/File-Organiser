import os
import shutil
import json
import contextlib
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def struct_compiler(s_path="", path="struct.json") -> dict:
    """Compile the struct.json file into a simple key:values dictionary.
    s_path: the path of the root organised folder.
    path: An optional variable that contains the path of struct.json (or equivalent) file."""

    def ljle(data={}, up="", cs={}, cc={}, lvl=-1) -> dict:
        """
        local json level explorer: Construct each path of categories based on the JSON levels
        data: the data to explore
        up: path of the folder above the current folder (up: upper path)
        cs: the variable holing the results
        lvl: Level of recursion inside the folder tree.
        """

        # Managing parameters cases
        if type(data) != dict:
            print(Fore.RED+"DATA INVALID: The data is not a dictionary.")
            raise TypeError
        elif (data == {}) & (lvl != 0):
            print("DATA INVALID: data is empty.")
            raise ValueError

        if type(s_path) != str:
            print(Fore.RED+"UPPER PATH INVALID: The upper path is not a string.")
            raise TypeError
        elif (up == "") & (lvl != 0):
            print(Fore.RED+"UPPER PATH INVALID: The upper path is empty.")
            raise ValueError

        if type(data) != dict:
            print(Fore.RED+"DATA INVALID: The data is not a dictionary.")
            raise TypeError
        elif (cs == {}) & (lvl != 0):
            print(Fore.RED+"DATA INVALID: cs is empty.")
            raise ValueError

        if type(data) != dict:
            print(Fore.RED+"DATA INVALID: The data is not a dictionary.")
            raise TypeError
        elif (cc == {}) & (lvl != 0):
            print(Fore.RED+"DATA INVALID: cc is empty.")
            raise ValueError

        # Setting the variables
        cufn = data.get("sp")  # cufn: current upper folder name
        cufp = "{}{}".format(up, cufn)  # cfp: current upper folder path
        lvl = 0  # Level of recursion inside the folder tree.

        for key in data:
            if key != "sp":
                if type(data[key]) != str and type(data[key]) == list and type(data[key][0]) == dict:
                    lvl += 1
                    ljle(data[key][0], cufp, cs, cc, lvl)
                elif type(data[key]) == str:
                    # cfn: current folder name
                    cfn = os.path.join(cufn, data[key])
                    cfp = "{}{}".format(up, cfn)  # cfp: current folder path
                    cs[key] = cfp
                    cc[key] = data[key]
                    #print(Fore.GREEN+"CS: {}".format(json.dumps(cs, indent=4)))
                    #print(Fore.GREEN+"CC: {}".format(json.dumps(cc, indent=4)))
                    # print("------")
                else:
                    print(
                        Fore.RED+"DATA[KEY] INVALID: The data[key] type is incorrect.")
                    raise TypeError
            else:
                #print("KEY INVALID: The key is 'sp'.\nKEY SKIPPED\n------")
                pass

        return cs, cc

    # Managing variable cases

    if os.path.exists(s_path) == False:
        print(Fore.RED+"PATH INVALID: The path doesn't exist.")
        raise FileNotFoundError
    elif type(s_path) != str:
        print(Fore.RED+"PATH INVALID: The path is not a string.")
        raise TypeError
    elif s_path == "":
        print(Fore.RED+"PATH INVALID: The path is empty.")
        raise ValueError

    elif os.path.exists(path) == False:
        print(Fore.RED+"PATH INVALID: The path doesn't exist.")
        raise FileNotFoundError
    elif type(path) != str:
        print(Fore.RED+"PATH INVALID: The path is not a string.")
        raise TypeError
    elif path == "":
        print(Fore.RED+"PATH INVALID: The path is empty.")
        raise ValueError

    # Setting the variables
    with open(path, encoding="utf-8", mode='r') as f:
        # struct: variable that contains the struct.json file
        struct = json.loads(f.read())
        compiled_struct = {}  # compiled_struct: the compiled paths in the struct.json file
        compiled_cat = {}  # compiled_cat: the compiled names in the struct.json file

        for cat in struct:
            if type(struct[cat]) != str and type(struct[cat][0]) == dict:
                pass
                compiled_struct, compiled_cat = ljle(
                    struct[cat][0], s_path, compiled_struct, compiled_cat, 0)
            elif type(struct[cat]) == str:
                cfp = os.path.join(s_path, struct[cat]).replace(
                    "\\", "/")  # current folder path
                compiled_struct[cat] = cfp
                compiled_cat[cat] = struct[cat]
    f.close()
    #print(Fore.GREEN+"COMPILED_STRUCT: {}\n".format(json.dumps(compiled_struct, indent=4)))
    return compiled_struct, compiled_cat

def file_mover(name: str, extensions: str, source: str, destination: str):
    """
    Move the file from the source to the destination.
    name: the name of the file.
    extensions: the extension of the file.
    source: the initial path of the file.
    destination: the final path of the file.
    """
    dest_path = os.path.join(destination, name + extensions).replace("\\", "/")
    copy = 1

    if len(source) < len(destination):
        # Check if the destination is in a subfolder of the source:
        # if not checked, it will created folder with name of the file and will confuse everything.
        while not os.path.exists(destination):
            os.makedirs(destination)

    if os.path.exists(dest_path):
        try:
            while os.path.exists(dest_path):
                new_name = os.path.join(
                    destination, f"{name}_{str(copy)}{extensions}")
                shutil.move(source, new_name)
                copy += 1
        except:
            print("An error occurred while renaming {}.".format(name + extensions))
        else:
            print("{} has been renamed to avoid conflicts.".format(name + extensions))
    else:

        shutil.move(source, destination)
        print(Fore.LIGHTRED_EX+"{} ->".format(os.path.dirname(source)))
        print(Fore.LIGHTGREEN_EX+"{}".format(destination))
    print("---")

def estimation(path:str):
    global of_path
    def count_files(A, counter = 0):
        if os.path.exists(A):
            for fi in os.listdir(A):
                fsp = os.path.join(A, fi).replace("\\", "/")  # fsp: file source path
                if os.path.isfile(fsp):
                    counter += 1
                else:
                    counter=int(count_files(fsp, counter=counter))
        else:
            print(Fore.RED+"The {} folder doesn't exist.".format(A))
            raise ValueError
        return counter
    
    with open("./struct.json", encoding="utf-8", mode='r') as f:
        data = json.loads(f.read())
        for key in data:
            of_path = os.path.join(path, data[key][0].get("sp")).replace("\\", "/")  # of_path: organised folder path
    f.close()
        
    count=0
    for filename in os.listdir(path):
        if (os.path.isfile(f"{path}/{filename}")) == True:
            count += 1

    return count+count_files(of_path)

def intialiser(path: str, progress_bar=None, max=0):
    """Resets all files location in the organised folder into the folder above it.
    path: the path of the folder to organise.
    progress_bar: the progress bar
    fec: track the number of function executed consequently in the GUI to adapt the percentage
    """

    def move_files(A: str, B: str, maxbar=0, counter = 0):
        if os.path.exists(A):
            for file in os.listdir(A):
                #print("A: ", A)
                #print("B: ", B)
                fsp = os.path.join(A, file).replace(
                    "\\", "/")  # fsp: file source path
                #print("FSP: ", fsp)
                if os.path.isfile(fsp):
                    print("{}".format(file))
                    name, extension = os.path.splitext(file)
                    file_mover(name, extension, fsp, B)
                    counter += 1
                    if maxbar != 0:
                        progress_bar.setValue(int((counter/maxbar)*100))
                        print("{}%".format(int((counter/maxbar)*100)))
                else:
                    #print("\nFOLDER: GOING IN ⤵️ \n")
                    counter=int(move_files(fsp, B, maxbar=maxbar, counter=counter))
        else:
            print(Fore.RED+"The {} folder doesn't exist.".format(A))
            raise ValueError
        return counter

    def remove_empty_folders(B: str):
        removed_folders = 0

        with contextlib.suppress(Exception):
            while len(os.listdir(B)) > 0:
                for item in os.listdir(B):
                    current_path = os.path.join(B, item)
                    if len(os.listdir(current_path)) >= 1:
                        remove_empty_folders(current_path)
                    else:
                        print("Parent folder:", B)
                        print("Current folder:", current_path)
                        os.rmdir(current_path)
                        print("Current folder deleted.")
                        print("---")
                        removed_folders += 1

        if removed_folders == 0:
            print("No empty folders were removed.")

    if progress_bar != None:
        maxbar = max

    print("\n------\n0%: Starting initialisation\n------")
    c=move_files(of_path, path, maxbar=maxbar)
    print("50%: Files moved\n------")
    remove_empty_folders(of_path)
    print("100%: Root cleaned\nIntialisation finished!\n------")
    
    return c

def organiser(folder, progress_bar=None, count=0, max=0):
    """Organize the files in the folder depending on their extension.
    folder: the path of the folder to organise.
    progress_bar: the progress bar
    fec: track the number of function executed consequently in the GUI to adapt the percentage
    """
    with open('ext.json', encoding="utf-8", mode='r') as ext_file:
        ext_data = json.loads(ext_file.read())
        struct_data, cat_data = struct_compiler(folder.replace("\\", "/")+"/")
        # fut_ext: future extensions files to implement (the ones not yet implemented)
        fut_ext = []

        #print(Fore.GREEN+"EXT_DATA: {}".format(json.dumps(ext_data, indent=4)))
        #print(Fore.GREEN+"STRUCT_DATA: {}".format(json.dumps(struct_data, indent=4)))
        #print(Fore.GREEN+"CAT_DATA: {}".format(json.dumps(cat_data, indent=4)))

        ign = [".driveupload", ".drivedownload"]
        
        counter = 0

        if progress_bar != None:
            maxbar = max

        for filename in os.listdir(folder):
            #os.rename( os.path.join(folder,filename).replace("\\","/") , os.path.join(folder,filename.replace("FILE-", "")).replace("\\","/"))
            if os.path.isfile(f"{folder}/{filename}") == True:
                if filename not in ign:
                    name, extension = os.path.splitext(filename)
                    source = os.path.join(folder, filename).replace("\\", "/")
                    category = ext_data.get(extension.lower())
                    pretty_category = cat_data.get(category)
                    dest = struct_data.get(category)
                    print("{}{} -".format(name, extension) +
                          Fore.LIGHTBLUE_EX + " {} ".format(pretty_category))
                    if category != None or dest != None:
                        file_mover(name, extension, source, dest)
                        counter += 1
                        if maxbar != 0:
                            progress_bar.setValue(int(((count+counter)/maxbar)*100))
                            print("{}%".format(int(((count+counter)/maxbar)*100)))
                    elif category == None:
                        print(
                            Fore.LIGHTBLUE_EX+"The extention file \"{}\" hasn't been yet implemented".format(extension))
                        print("---")
                        if extension not in fut_ext:
                            fut_ext.append(extension)

        print("\n")

        if counter == 0:
            print("The folder is already organized.")
        else:
            print("{} files have been moved.".format(counter))

        print("------")

        if len(fut_ext) > 0:
            print("The following extensions should be implemented:\n")
            for ext in fut_ext:
                print(Fore.LIGHTYELLOW_EX+ext)
        else:
            print("All extensions encontered have been implemented.")
        print()
