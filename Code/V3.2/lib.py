import os
import shutil
import json
import contextlib
import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)


def struct_compiler(s_path="", path="struct.json") -> dict:
    """Compile the struct.json file into a simple key:values dictionary.
    s_path: the path of the root organised folder.
    path: An optional variable that contains the path of struct.json (or equivalent) file."""

    def ljle(data={}, up="", cs={}, cc={}) -> dict:
        """
        local json level explorer: Construct each path of categories based on the JSON levels
        data: the data to explore
        up: path of the folder above the current folder (up: upper path)
        cs: the variable holing the results
        """

        # Managing parameters cases
        if data != {}:
            if type(data) != dict:
                print("DATA INVALID: The data is not a dictionary.")
                raise TypeError
        else:
            print("DATA INVALID: The data is empty.")
            raise ValueError
        
        if up != "":
            if type(s_path) != str:
                print("UPPER PATH INVALID: The upper path is not a string.")
                raise TypeError
        else:
            print("UPPER PATH INVALID: The upper path is empty.")
            raise ValueError

        if cs != {}:
            if type(data) != dict:
                print("DATA INVALID: The data is not a dictionary.")
                raise TypeError
        else:
            print("DATA INVALID: The data is empty.")
            raise ValueError

        if cc != {}:
            if type(data) != dict:
                print("DATA INVALID: The data is not a dictionary.")
                raise TypeError
        else:
            print("DATA INVALID: The data is empty.")
            raise ValueError

        # Setting the variables
        cufn = data.get("sp")  # cufn: current upper folder name
        cufp = "{}{}".format(up, cufn)  # cfp: current upper folder path

        for key in data:
            if key != "sp":
                if type(data[key]) != str and type(data[key]) == list and type(data[key][0]) == dict:
                    ljle(data[key][0], cufp, cs, cc)
                elif type(data[key]) == str:
                    cfn = os.path.join(cufn, data[key])# cfn: current folder name
                    cfp = "{}{}".format(up, cfn)  # cfp: current folder path
                    #print("KEY: ", key)
                    #print("DATA[KEY]: ", data[key])
                    cs[key] = cfp
                    cc[key] = data[key]
                    #print(Fore.GREEN+"CS: {}".format(json.dumps(cs, indent=4)))
                    #print(Fore.GREEN+"CC: {}".format(json.dumps(cc, indent=4)))
                    #print("------")
                else:
                    print("DATA[KEY] INVALID: The data[key] type is incorrect.")
                    raise TypeError
            else:
                #print("KEY INVALID: The key is 'sp'.\nKEY SKIPPED\n------")
                pass

        return cs, cc

    # Managing variable cases
    if s_path != "":
        if os.path.exists(s_path):
            pass
        elif os.path.exists(s_path) == False:
            print("PATH INVALID: The path doesn't exist.")
            raise FileNotFoundError
        elif type(s_path) != str:
            print("PATH INVALID: The path is not a string.")
            raise TypeError
    else:
        print("PATH INVALID: The path is empty.")
        raise ValueError

    if path != "":
        if os.path.exists(path):
            pass
        elif os.path.exists(path) == False:
            print("PATH INVALID: The path doesn't exist.")
            raise FileNotFoundError
        elif type(path) != str:
            print("PATH INVALID: The path is not a string.")
            raise TypeError

    # Setting the variables
    with open(path, encoding="utf-8", mode='r') as f:
        # struct: variable that contains the struct.json file
        struct = json.loads(f.read())
        compiled_struct = {}  # compiled_struct: the compiled paths in the struct.json file
        compiled_cat = {}  # compiled_cat: the compiled names in the struct.json file

        for cat in struct:
            if type(struct[cat]) != str and type(struct[cat][0]) == dict:
                compiled_struct, compiled_cat = ljle(
                    struct[cat][0], s_path, compiled_struct, compiled_cat)
            elif type(struct[cat]) == str:
                cfp = os.path.join(s_path, struct[cat]).replace("\\", "/")  # current folder path
                compiled_struct[cat] = cfp
                compiled_cat[cat] = struct[cat]
    f.close()
    #print(Fore.GREEN+"COMPILED_STRUCT: {}\n".format(json.dumps(compiled_struct, indent=4)))
    return compiled_struct, compiled_cat


def file_mover(name:str, extensions:str, source:str, destination:str):
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
                new_name = os.path.join(destination, f"{name}_{str(copy)}{extensions}")
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


def intialiser(path:str, fn:str):
    """Resets all files location in the organised folder into the folder above it.
    path: the path of the folder to organise.
    fn: the name of the organised folder.
    """

    def move_files(A, B):
        if os.path.exists(A):
            counter = 0
            for file in os.listdir(A):
                #print("A: ", A)
                #print("B: ", B)
                fsp = os.path.join(A, file).replace("\\", "/") # fsp: file source path
                #print("FSP: ", fsp)
                if os.path.isfile(fsp):
                    print("{}".format(file))
                    name, extension = os.path.splitext(file)
                    file_mover(name,extension, fsp, B)
                    counter+=1
                else:
                    #print("\nFOLDER: GOING IN ⤵️ \n")
                    move_files(fsp, B)
        else:
            print("The {} folder doesn't exist.".format(A))
            raise ValueError

    def remove_empty_folders(B):
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

    of_path = os.path.join(path, fn).replace("\\", "/") # of_path: organised folder path

    print("\n------\n0%: Starting initialisation\n------")
    move_files(of_path, path)
    print("50%: Files moved\n------")
    remove_empty_folders(of_path)
    print("100%: Root cleaned\nIntialisation finished!\n------")


def organiser(folder, fn):
    """Organize the files in the folder depending on their extension.
    folder: the path of the folder to organise.
    fn: the name of the organised folder.
    """

    with open('ext.json', encoding="utf-8", mode='r') as ext_file:
        ext_data = json.loads(ext_file.read())
        struct_data, cat_data = struct_compiler(os.path.join(folder, fn).replace("\\", "/")+"/")
        fut_ext=[] # fut_ext: future extensions files to implement (the ones not yet implemented)

        counter = 0

        #print(Fore.GREEN+"EXT_DATA: {}".format(json.dumps(ext_data, indent=4)))
        #print(Fore.GREEN+"STRUCT_DATA: {}".format(json.dumps(struct_data, indent=4)))
        #print(Fore.GREEN+"CAT_DATA: {}".format(json.dumps(cat_data, indent=4)))

        ign=[".driveupload",".drivedownload"]

        for filename in os.listdir(folder):
            #os.rename( os.path.join(folder,filename).replace("\\","/") , os.path.join(folder,filename.replace("FILE-", "")).replace("\\","/"))       
            if os.path.isfile(f"{folder}/{filename}") == True:
                if filename not in ign:
                    name, extension = os.path.splitext(filename)
                    source = os.path.join(folder, filename).replace("\\", "/")
                    category = ext_data.get(extension.lower())
                    pretty_category = cat_data.get(category)
                    dest = struct_data.get(category)
                    print("{}{} -".format(name, extension) + Fore.LIGHTBLUE_EX +" {} ".format(pretty_category))
                    if category != None or dest != None:
                        file_mover(name, extension, source, dest)
                        counter += 1
                    elif category == None:
                        print(Fore.LIGHTBLUE_EX+"The extention file \"{}\" hasn't been yet implemented".format(extension))
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
