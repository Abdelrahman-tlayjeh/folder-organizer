from os import scandir, path, DirEntry, makedirs, rename
from shutil import move
from json import load as load_json

"""
TO-DO:
------
    - review select_files, rename, and change_extensions
    - add comments and documentations to these 3
"""
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

    #========== methods to scan/select folder content ==========#
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
            raise ValueError(f"Type should be 'all', 'files', or 'folders', but '{type}' is given!")


    def select_files(self, by:str, value:'str|list') -> list[DirEntry]:
        """
        return a list of all items with given properties

        Args:
            - by: either 'ext' to select files with specific extension(s) or 'names' to select files with given name(s)
            - value: can be one string or list of strings
        """
        if type(value) is str:
            value = [value]

        if by == "ext":
            return [file for file in self.get_content("files") if self._get_file_extension(file) in value]
        
        if by == "names":
            return [file for file in self.get_content("files") if file.name in value]
        
        #invalid [by] argument
        raise ValueError(f"By argument should be 'ext' or 'names', but '{by}' is given!")

    #========== Methods to organize folder ==========#
    def organize_by_extensions(self, output_folder_name:str, include_folders:bool=True, dont_touch:list[str]=None) -> tuple:
        """organize the folder by extensions.
        all files with the same extension are placed in the same folder

        Args:
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

        Args:
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


    #========== Modifying folder content ==========#
    def rename_content(self, new_name_pattern:str, include_folder=True, dont_touch:list=None) -> tuple:
        """Rename folder content to similar names (as the given name pattern)

        Args:
            - new_name_pattern: the pattern string. [special characters: []: an index | {}: the old name]
            - include_folders: True to rename folders as well, False to not
            - dont_touch: list of names of files or folders to do not rename, by default it will contains the constant self._dont_touch

        return a tuple of two items:
            - 1: list of tuples. Each tuple contains the old name and the new name
            - 2: list of errors tuples (if errors occur else empty list), each tuple contains the item name and the error message
        """
        if not dont_touch: dont_touch = self._dont_touch
        content = self.get_content("all" if include_folder else "files") 
        #if there is more than one item and the pattern is a static string
        if len(content) > 1 and ("{}" not in new_name_pattern and "[]" not in new_name_pattern):
            #add an index at the end of name
            new_name_pattern += "[]"

        renamed = []
        errors = []

        for index, item in enumerate(content):
            if item.name in dont_touch:
                continue
            
            extension = path.splitext(item.name)[1]
            new_name = new_name_pattern.replace("[]", str(index))
            new_name = new_name.replace("{}", item.name)
            new_name += extension
            try:
                rename(item.path, item.path.replace(item.name, new_name))
                renamed.append((item.name, new_name))
            except Exception as e:
                errors.append(item.name, str(e))

        return (renamed, errors)

    
    def change_extensions(self, current:str, new:str, dont_touch:list=None) -> tuple:
        """Change the extension of all files that have [current] extension to the [new] extension

        Args:
            - current: the current extension
            - new: the new extension
            - dont_touch: list of names of files or folders to do not rename, by default it will contains the constant self._dont_touch

        return a tuple of two items:
            - 1: the count of total changed items (int)
            - 2: list of errors tuples (if errors occur else empty list), each tuple contains the item name and the error message
        """
        if not dont_touch: dont_touch = self._dont_touch
        #make sure that extensions have '.' at the beginning
        if current[0] != ".": current = "." + current
        if new[0] != ".": new = "." + new

        changed = 0
        errors = []

        #get all files with given extension(s)
        content = self.select_files(by="ext", value=current)
        for file in content:
            if file.name in dont_touch:
                continue
            
            try:
                #the name with the new extension
                new_name = path.splitext(file.name)[0] + new
                rename(file.path, file.path.replace(file.name, new_name))
                changed += 1
            except Exception as e:
                errors.append((file.name, str(e)))
        
        return (changed, errors)


