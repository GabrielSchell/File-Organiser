import contextlib
import os
import shutil
import json
import logging
import time
import getpass
import os
import sys

global struct
global ext




def move_file_to_directory(name, extensions, source, destination):
    rm=0
    dest_path = destination + name + extensions
    copy = 2
    # print("FINAL PATH STEP #2:", destination)
    # print("FINAL PATH STEP #3:", dest_path)

    while os.path.exists(destination) != True:
        #print("DESTINATION DOESN'T EXIST (NOT GOOD)")
        os.makedirs(str(destination))

    if (name + extensions) == "Organize Folder":
        print("I DON'T KNOW WHY BUT IT DOESN'T FEEL RIGHT TO MOVE THIS FOLDER...\nI WILL NOT MOVE IT")
        return
    elif os.path.exists(destination) != True:
        #print("DESTINATION DOESN'T EXIST (NOT GOOD)")
        #print("destination:", destination)
        os.makedirs(str(destination))
        rm+=1
        #print("SITUATION IS UNDER CONTROL")
    elif os.path.exists(dest_path) == True:
        #print("DESTPATH ALREADY EXIST (NOT GOOD)")
        try:
            while os.path.exists(dest_path) == True:
                new_name = f"{destination}/{name}_{str(copy)}{extensions}"
                os.rename(source, new_name)
                copy = +1
        except:
            print("I GUESS I KINDA BROKE ?...")
        else:
            print("SITUATION IS UNDER CONTROL")
    else:
        #print("DESTPATH DOESN'T EXIST (GOOD) ")
        # print("-")
        #print("BEGINNING:", source)
        #print("END:", destination+name+extensions)
        shutil.move(source, destination)
        #print("{} has been moved in {} ".format(os.path.basename(source), destination))
        return 0


def jle(d, sp, e, *spo):  # json level explorer  # sourcery skip: assign-if-exp, none-compare
    if sp == None:  # subpath (chemins d'accés, en morceaux)
        sp = ""
    if not spo:  # spo = subpath original (morceau du chemin d'accès du niveau précédent)
        spo = ""
    else:
        spo = spo[0]
    for i in d:
        if i != "sp":
            sp = d.get("sp")
            if type(d[i][0]) != dict:
                e.setdefault(i, "")
            """
            print()
            print("0 SPO| ", spo)
            print("0 SP| "+sp)
            print("d[i]: ", d[i])
            """

            if type(d[i]) == list and type(d[i][0]) == dict:
                spo = sp
                d1 = d[i][0]
                jle(d1, sp, e, spo)
                #print("1 SPO| ", spo)
                #print("1| "+sp)

            elif type(d[i]) == str:
                if not spo:
                    sp = sp+d[i]
                else:
                    if spo == sp:
                        spo=""
                    sp = spo+sp+d[i]
                e[i] += sp
                #print("2| "+sp)
                #print(i+" : "+sp)
                # print(e)
                #print("---")

    return e


def of2(folder,*v):
    def pprint(*data):
        if v != 0:
            logging.info(' '.join(map(str, data)))
        data=""

    cc = {}  # Compiled Correspondance


    with open('struct.json', encoding="utf-8", mode='r') as struct:
        ext = open('ext.json', encoding="utf-8", mode='r')

        
        d_e = json.loads(ext.read())  # extension -> categories
        d_s = json.loads(struct.read())  # categories -> path
        sp = ""

        #print(d_e)
        #print(d_s)
        counter = 0

        for j in d_s:  # If you get a 'KeyError: 0' error, that means your forgot the [] around the {}

            # value isn't a string, it's a dict, meaning there's more down there
            if type(d_s[j]) != str and type(d_s[j][0]) == dict:
                sp += d_s[j][0].get("sp")
                cc = jle(d_s[j][0], sp, cc)

            elif type(d_s[j]) == str:  # value is a string meaning end of path at lvl 1
                cc[j] = d_s[j]
            else:
                pprint(type(d_s[j][0]))
                pprint(
                    "INVALIDE DATA TYPE: REQUIRE EITHER STRING OR DICT.")
                pprint("---")
        """
    for i in cc:
        print("{} : {}\n".format(i,cc[i]))
    """
        # Make the difference between files and folders
        for filename in os.listdir(folder):
            name, extension = os.path.splitext(filename)
            sub_path = d_e.get(extension.lower())
            if os.path.isfile(f"{folder}/{filename}") == False:
                #print("Folder name: ",name+extension)
                #print("Folders aren't managed by the program")
                #print("------")
                pass
            elif sub_path is not None:
                pprint("File name: ", name+extension)
                pprint("category: ", cc.get(sub_path))
                if cc.get(sub_path) != None:
                    destination = f"{folder}/↪ Organize Folder ↩/{cc.get(sub_path)}/"
                    source = f"{folder}/{filename}"
                    pprint(f"{source} ->")
                    pprint(f"{destination} + {filename}")

                    res = move_file_to_directory(
                        name, extension, source, destination)
                    if res == 0:
                        counter += 1
                pprint("------")
            else:
                pprint("File name: \"{}\"".format(name+extension))
                pprint("The extention file \"{}\" hasn't been yet implemented".format(extension))
                pprint("------")

        pprint()
        if counter == 0:
            pprint("It's already organized :)")
        else:
            pprint("{} files have been moved".format(counter))
        pprint()
        """
        if len(d_s[j][0]) > 1 and type(d_s[j][0]) == dict: #if data is longer than 1 and is a dict
            print(j,":",d_s[j][0])
            sp=d_s[j][0].get("sp") # get the subpath in the dict
            for j1 in d_s[j][0]:
                if len(d_s[j][0][j1]) > 1:
                    pass
                else:
                    pass
        
        else:
            print(j,": ",d_s[j][0],"(null)")
            print(type(d_s[j][0]))
        print("--")
        print()
    """

    ext.close()

def update(path,*v):

    def pprint(*data):
        if v != 0:
            logging.info(' '.join(map(str, data)))

    abs_path=path #Absolut path
    fof_path= f"{path}/↪ Organize Folder ↩" #files organiser folder path
    def fm(A,B): #file mover
        try:
            k = 0
            for i in os.listdir(B):
                tff_path=f"{A}/{i}" # Temporary file folder path
                ni=f"{B}/{i}" # Current path
                if os.path.isfile(ni) == True:
                    shutil.move(ni, tff_path)
                    k+=1
                    print("---")
                    print("File: {}".format(i))
                    print("{} ->".format(ni))
                    print("{}".format(tff_path))   
                else:
                    fm(A,ni)
            return int(k)
        except Exception:
            print("the \'↪ Organize Folder ↩\' folder doesn't exist")

    def frm(B): #folder remover
        with contextlib.suppress(Exception):
            l = 0
            while len(os.listdir(B)) > 0:
                for i in os.listdir(B):
                    cp=f"{B}/{i}" # Current path
                    if len(os.listdir(cp)) >= 1: 
                        #print("FOLDER NOT EMPTY") 
                        frm(cp)               
                    else:
                        pprint("---")
                        pprint("Parent folder: {}".format(B)) 
                        pprint("Current folder: {}".format(cp))
                        pprint("Current folder deleted") 
                        os.rmdir(cp)

    fm(abs_path, fof_path)
    print("---\n 33 % ")
    frm(fof_path)
    print("---\n 66 % \n------")
    of2(path,0)
    print("100%, Update finished !\n------")



# Don't touch, I'm using this line in debugging to skip the question at the beginning and immediatly work in the download directory
#of2(os.path.join("C:/Users", getpass.getuser(), "Downloads").replace("\\", "/"))
