from os import scandir, path, DirEntry, makedirs
from shutil import move
from json import load as load_json


class FolderOrganizer:
    def __init__(self) -> None:
        self._categories = self._load_categories()
        self._dont_touch = ["folder_organizer.py", "categories.json", "test.py", "folder_organizer_CLI.py"]

    #========== Helpers methods ==========#
    def _get_file_extension(self, file:DirEntry) -> str:
        """return the extension of the given file or 'unknown' if the file has no extension"""
        extension = path.splitext(file.name)[1]
        return extension if extension else "Unknown"

    
    def _default_dont_touch(self, output_folder_name) -> list[str]:
        dont_touch = self._dont_touch
        dont_touch.append(output_folder_name)
        return dont_touch
        

    def _safe_move(self, item:DirEntry, destination_path:str) -> tuple:
        """move the item to the destination path if the destination path already exists, 
        else create the destination path and then move the item to it.
        
        return a tuple of two items:
            - 1: the count of total moved items (int)
            - 2: list of errors tuples (if errors occur else empty list), each tuple contains the item name and the error message
        """
        if not path.exists(destination_path):
            makedirs(destination_path)

        try:
            move(item.path, path.join(destination_path, item.name))
            return (True, )
        #expected errors
        except PermissionError as e:
            return (False, "Permission Error! File may be open or incomplete.")
        except FileNotFoundError as e:
            return (False, "File not Found ¯\_(ツ)_/¯")
        #unexpected error
        except Exception as e:
            return (False, str(e))
        

    #---- Helpers to read categories file ----#
    def _get_sub_categories(self, categories:dict) -> list:
        """return a list of all sub-extensions for the given categories dict"""
        sub_categories = []
        for k, v in categories.items():
            if type(v) is list:
                sub_categories.extend(v)
            else:
                sub_categories.extend(self._get_sub_categories(v))

        return sub_categories


    def _set_all_sub_categories(self, categories:dict) -> dict:
        """
        get normal categories dict and return a copy with 'all' key for each category has sub-categories, 
        so it become easy to search for a category to a given file.
        
        e.g: 
        -----
        input:
        ------        
        {
            "cat1": ["ext1", "ext2", "ext3"],
            "cat2": {
                "sub-cat1": ["ext1", "ext2", "ext3"],
                "sub-cat2": ["ext1", "ext2"]
            }
        }

        output:
        -------
            "cat1": ["ext1", "ext2", "ext3"],
            "cat2": {
                "all": ["ext1", "ext2", "ext3", "ext4", "ext5"]
                "sub-cat1": ["ext1", "ext2", "ext3"],
                "sub-cat2": ["ext4", "ext5"]
            }
        }
        
        """
        for k, v in categories.items():
            if type(v) is list:
                continue
            #dict
            categories[k]["all"] = self._get_sub_categories(v)
            categories[k] = self._set_all_sub_categories(v)
        
        return categories

    
    def _load_categories(self) -> dict:
        """Load categories from json file then return a dict with 'all' key for each category has sub-categories"""
        with open("categories.json", "r") as f:
            categories = load_json(f)
        #add 'all' key for each category has sub-categories
        return self._set_all_sub_categories(categories)

    
    def _get_category(self, item:DirEntry, categories:dict=None) -> 'str|list[str]|None':
        """get an os.DirEntry object and search for crresponding category.

        return:
            - str: if a category is found and there is no sub-categories
            - list[str]: if a category is found but it have sub-categories
            - None: in case that no category is found
        
        """
        if not categories: categories = self._categories

        if extension := self._get_file_extension(item)[1: ]: #extension without '.'
            for category, extensions in categories.items():
                #category with no sub-categories
                if type(extensions) is list:
                    if extension in extensions:
                        return category
                    continue
                
                #category with sub-categories
                if type(extensions) is dict:
                    if extension in extensions["all"]:
                        categories_lst = []
                        categories_lst.append(category)
                        #find the sub category
                        sub_cat = self._get_category(item, categories=extensions)
                        #one sub-category
                        if type(sub_cat) is str:
                            categories_lst.append(sub_cat)
                        #multiple sub-categories
                        if type(sub_cat) is list:
                            categories_lst.extend(sub_cat)

                        return categories_lst            
        return None

    #========== methods to scan folder content ==========#
    def get_stats(self) -> dict:
        """return the counts of each different extension in the folder, as well as the count of fodlers and the unknown files"""
        content = scandir()
        stats = {"Total": 0}
        #check each item in folder
        for item in content:
            stats["Total"] += 1

            #-- if Folder --#
            if item.is_dir():
                #add 'folders' to stats if not exist
                if "folders" not in stats.keys():
                    stats["folders"] = 0

                #increment the count of folders
                stats["folders"] += 1
                continue
            
            #-- if File --#
            #get the extension
            extension = path.splitext(item.name)[1]
            
            #if file has an extension
            if extension:
                #add the extension to stats if not exist
                if extension not in stats.keys():
                    stats[extension] = 0

                #increment the count of the extension
                stats[extension] += 1
                continue

            #if file has no extension (unknown file type)
            #add 'unknown' to stats if not exist
            if "unknown" not in stats.keys():
                stats["unknown"] = 0
            
            #increment the count of unknown
            stats["unknown"] += 1

        return stats


    def get_content(self, type:str) -> list[DirEntry]:
        """return a list of all items in the folder of selected type\n
            type can be:
                - 'files' to select all files 
                - 'folders' to select all folders
                - 'all' to select both files and folders
        """
        #return both files and folders
        if type == "all":
            return list(scandir())
        #return files
        elif type == "files":
            return [item for item in scandir() if item.is_file()]
        #return folders
        elif type == "folders":
            return [item for item in scandir() if item.is_dir()]
        #invalid type
        else:
            raise ValueError(f"Type should be 'all', 'files', or 'folders'. But '{type}' is given!")


    #========== Methods to organize folder ==========#
    def organize_by_extensions(self, output_folder_name:str, include_folders:bool=True, dont_touch:list[str]=None) -> tuple:
        """organize the folder by extensions.
        all files with the same extension are placed in the same folder

        params:
            - output_folder_name: string for the name of folder that will contains all organized content
            - include_folders: True to organize folders and place in 'Folders' folder, False to not
            - dont_touch: list of names of files or folders to do not move, by default it will contains the constant self._dont_touch plus the given output_folder_name
        
        return a tuple of two items:
            - 1: the count of total moved items (int)
            - 2: list of errors tuples (if errors occur else empty list), each tuple contains the item name and the error message
        """
        if not dont_touch: dont_touch = self._default_dont_touch(output_folder_name)
        content = self.get_content("all" if include_folders else "files")

        moved = 0
        errors = []

        for item in content:
            if item.name in dont_touch:
                continue

            #-- Folder --#
            if item.is_dir():
                response = self._safe_move(item, path.join(output_folder_name, "Folders"))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.path, response[1]))
                continue

            #-- File --#
            extension = self._get_file_extension(item)
            response = self._safe_move(item, path.join(output_folder_name, extension))
            if response[0]:
                moved += 1
            else:
                errors.append((item.name, response[1]))

        #finish
        return (moved, errors)

    
    def organize_by_categories(self, output_folder_name, include_folders:bool=True, dont_touch:list[str]=None) -> tuple:
        """organize the folder by pre-defined categories (categories.json).
        all files with the same category are placed in the same folder, files with no category will be placed in 'Other' folder.

        params:
            - output_folder_name: string for the name of folder that will contains all organized content
            - include_folders: True to organize folders and place in 'Folders' folder, False to not
            - dont_touch: list of names of files or folders to do not move, by default it will contains the constant self._dont_touch plus the given output_folder_name
        
        return a tuple of two items:
            - 1: the count of total moved items (int)
            - 2: list of errors tuples (if errors occur else empty list), each tuple contains the item name and the error message
        """
        if not dont_touch: dont_touch = self._default_dont_touch(output_folder_name)
        content = self.get_content("all" if include_folders else "files")

        moved = 0
        errors = []

        for item in content:
            if item.name in dont_touch:
                continue

            #-- Folder --#
            if item.is_dir():
                response = self._safe_move(item, path.join(output_folder_name, "Folders"))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.path, response[1]))
                continue

            #-- File --#
            category = self._get_category(item)

            #one category
            if type(category) is str:
                response = self._safe_move(item, path.join(output_folder_name, category.title()))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.name, response[1]))
                continue
            
            #many sub-categories
            if type(category) is list:
                response = self._safe_move(item, path.join(output_folder_name, *list(map(lambda c: c.title(), category))))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.name, response[1]))
                continue

            #unknown category
            if category is None:
                response = self._safe_move(item, path.join(output_folder_name, "Other"))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.name, response[1]))
            
        #finish
        return (moved, errors)
