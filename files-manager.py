"""
Functions to automate basic working with files tasks
You can directely run and use the script as a CLI app 

by Abdelrahman Tlayjeh @ https://github.com/Abdelrahman-tlayjeh
"""

from os import scandir, makedirs, path, DirEntry, rename
from shutil import move

#########################
#---Folder Organizer--###
#########################
MAIN_FOLDER = "Organized Folder"
CATEGORIES = {
    "programs": ["exe", "EXE", "msi"],
    "documents": ["pdf", "PDF", "txt"],
    "office": ["doc", "docx", "xls", "xlsx", "pptx", "ACCDA", "ACCDB", "one", "ecf", "pub"],
    "media": ["m4a", "mp4", "mp3", "jpg", "jpeg", "png", "Jif"],
    "zip": ["zip"]
}

SUB_CATEGORIES = {
    "documents": {
    "pdf": ["pdf", "PDF"],
    "text": ["txt"]
    },
    "office": {
        "word": ["doc", "docx"],
        "excel": ["xls", "xlsx"],
        "power point": ["pptx"],
        "access": ["ACCDA", "ACCDB"]
    },
    "media": {
        "images": ["jpg", "jpeg", "png", "Jif"],
        "videos": ["m4a", "mp4"],
        "audios": ["mp3"]
    }
}

DONT_TOUCH = [MAIN_FOLDER, "files-manager.py"]

#helper: check if file can be categorized
def check_category(file:DirEntry, categories:dict) -> 'str|False':
    """return category if found, else False"""
    #if the file has extension
    if ext := path.splitext(file.name)[1]:
        ext = ext[1:]  #e.g: '.txt'  --> 'txt'
        for category, extensions in categories.items():
            if ext in extensions:
                return category
    return False


def run_organizer():
    #Generate Main Categories Folders
    for category in CATEGORIES.keys():
        makedirs(path.join(MAIN_FOLDER, category.title()), exist_ok=True)

    #default fodlers
    makedirs(path.join(MAIN_FOLDER, "Folders"), exist_ok=True)
    makedirs(path.join(MAIN_FOLDER, "Other"), exist_ok=True)

    #Generate Sub-Categories Folders
    for main_category, sub_categories in SUB_CATEGORIES.items():
        for sub_category in sub_categories.keys():
            makedirs(path.join(MAIN_FOLDER, main_category, sub_category), exist_ok=True)

    #Get Folder content
    print("Exploring Folder...")
    content = scandir()

    #save errors
    expected_errors = []
    unexpected_errors = []

    #counts of items
    all_items_count = len(tuple(scandir()))
    success_move_count = 0

    #Organize all content
    print("Organizing content...")
    for item in content:
        if item.name in DONT_TOUCH:
            continue
        try:
            #check if is a fodler
            if item.is_dir():
                move(item.path, path.join(MAIN_FOLDER, "Folders", item.name))
                success_move_count += 1
                continue
            #check file extension
            if category := check_category(item, CATEGORIES):
                #check for sub-category
                if category in SUB_CATEGORIES.keys():
                    if sub_category := check_category(item, SUB_CATEGORIES[category]):
                        #move to a sub-category folder
                        move(item.path, path.join(MAIN_FOLDER, category.title(), sub_category.title(), item.name))
                        success_move_count += 1
                        continue
                #move to a main category folder
                move(item.path, path.join(MAIN_FOLDER, category.title(), item.name))
                success_move_count += 1
                continue
            #move to other
            move(item.path, path.join(MAIN_FOLDER, "Other", item.name))
            success_move_count += 1
            continue
            
        except (PermissionError, FileNotFoundError) as e:
            error = "File is not allowed to move(may be open or incompleted)" if type(e) is PermissionError else "File not Found"
            expected_errors.append((item.path, error))
        except Exception as e:
            unexpected_errors.append((item.path, e))

    #show summary
    print(f"{all_items_count} found, {success_move_count} successfully moved.")

    #show errors
    if expected_errors:
        print("There is some issues:")
        for file_path, error in expected_errors:
            print(f"\t- {file_path}: {error}")

    if unexpected_errors:
        print("There is Some Unexpected Errors:")
        for file_path, error in unexpected_errors:
            print(f"\t- {file_path}: {error}")

    if not any((expected_errors, unexpected_errors)):
        print("There is No Errors :)")


#########################
#---Anti-Organizer--#####
#########################
def run_anti_organizer():
    success_move_counts = 0
    for folder in CATEGORIES.keys():
        #check for sub-categories
        if folder in SUB_CATEGORIES.keys():
            #exrtact files that are not categorized in a sub-category
            for item in scandir(path.join(MAIN_FOLDER, folder.title())):
                if item.name not in SUB_CATEGORIES[folder].keys():
                    try:
                        move(item.path, item.name)
                        success_move_counts += 1
                    except Exception as e:
                        print(f"ERROR: {item.path}: {e}")
            #extract files from each sub-folder
            for sub_folder in SUB_CATEGORIES[folder].keys():
                for item in scandir(path.join(MAIN_FOLDER, folder.title(), sub_folder.title())):
                    try:
                        move(item.path, item.name)
                        success_move_counts += 1
                    except Exception as e:
                        print(f"ERROR: {item.path}: {e}")

        #extract files from each main folder
        else:
            for item in scandir(path.join(MAIN_FOLDER, folder.title())):
                try:
                    move(item.path, item.name)
                    success_move_counts += 1
                except Exception as e:
                    print(f"ERROR: {item.path}: {e}")

    #extract files from "Folders" and "Other"
    for folder in ["Folders", "Other"]:
        for item in scandir(path.join(MAIN_FOLDER, folder)):
            try:
                move(item.path, item.name)
                success_move_counts += 1
            except Exception as e:
                print(f"ERROR: {item.path}: {e}")

    #show summary
    print(f"Successfully {success_move_counts} items moved..")


#########################
#---Folder Scanner--#####
#########################
def run_scanner():
    print("Exploring Folder...")
    content = scandir()
    counts = {"folders": 0, "unknown-files": 0}

    print(f"---{len(tuple(scandir()))} items found:")

    #start counting different items
    for item in content:
        if item.is_dir():
            counts["folders"] += 1
            continue
        #get the extension
        if ext := path.splitext(item.name)[1]:
            ext = ext[1:]  #the extension without '.'
            if ext in counts.keys():
                counts[ext] += 1
                continue
            else:
                counts[ext] = 1
                continue
        #file with no extension
        counts["unknown-files"] += 1

    #show result
    for key, counts in counts.items():
        if counts:
            print(f"\t-->'{key}': {counts} found")


##########################
#---Extesnion Changer--###
##########################
def run_extension_changer():
    try:
        base, to = input("Enter the base extesnion and the replacement extension seperated by space (e.g: 'mp3 mp4'): ").split()
        #get all files with base extension
        all_counts = 0
        success_counts = 0
        for item in scandir():
            #check if item is file and have extension
            if item.is_file() and path.splitext(item.name)[1]:
                #check if extension have to be changed
                if path.splitext(item.name)[1][1:] == base:
                    all_counts += 1
                    try:
                        rename(item.path, path.splitext(item.name)[0]+"."+to)
                        success_counts += 1
                    except Exception as e:
                        print(f"ERROR: {item}: {e}")
        
        #show summary
        print(f"{all_counts} '.{base}' files found...")
        print(f"\t-->{success_counts} successfully changed to '.{to}'")
        
    except Exception as e:
        print(f"Unexpected error occur... {e}")
        print("Restarting...")
        run_extension_changer()


#---------------------Decoration--------------------------------->
def show_starting(title:str):
    print("-"*10 + title + "-"*10)

def show_ending():
    print("-"*40)

def show_instructions(instructions:str):
    print(instructions)
#------------------------------------------------------------------


if __name__ == "__main__":
    #run program
    while True:
        #get program nb
        choice = input(
        """
        Please Enter:
            -1- for folder organizer
            -2- for anti-folder organizer
            -3- for folder scanner
            -4- for extension changer

            -?- for help
        """)
        if choice not in ["1", "2", "3", "4", "?"]:
            print("Invalid Input!")
            continue

        if choice == "1":
            show_starting("Folder Organizer")
            show_instructions(
                """
                1) Place this script inside the folder that you need to organize.
                2) Make sure that all files and folders are close.
                3) In order to use the 'anti-organizer' don't change any name of any folder generated.
                4) If you face any unexpected error, start debugging... 
                """
            )
            input("Press ENTER to start...")
            run_organizer()
            show_ending()

        elif choice == "2":
            show_starting("anti-organizer")
            show_instructions(
                """
                1) Place this script inside the folder that you need to unorganize.
                2) Make sure that all files and folders are close.
                3) Make sure that names of all folders generated by 'folder organizer' are not changed.
                4) If you face any unexpected error, start debugging... 
                """
            )
            input("Press ENTER to start...")
            run_anti_organizer()
            show_ending()

        elif choice == "3":
            show_starting("Folder Scanner")
            run_scanner()
            show_ending()

        elif choice == "4":
            show_starting("Extensions Changer")
            run_extension_changer()
            show_ending()

        elif choice == "?":
            print("--> Go read the code <--")
        
        #ask to exit or restart
        print("-"*50)
        if input("Press ENTER if you want to restart or enter anything to Exit:   ") != "":
            break