from os import scandir, path, DirEntry, remove, makedirs, rename, getcwd
from shutil import move
from json import load as load_json


class FolderOrganizer:
    def __init__(self) -> None:
        self._categories = self._load_categories()

    #========== Helpers methods ==========#
    def _get_file_extension(self, file:DirEntry) -> str:
        """return the extension of the given file or 'unknown' if the file has no extension"""
        extension = path.splitext(file.name)[1]
        return extension if extension else "Unknown"

    
    def _default_ignore_list(self, output_folder_name) -> list[str]:
        return [output_folder_name, "folder_organizer.py", "categories.json", "test.py", "folder_organizer_CLI.py"]
        

    def _safe_move(self, item:DirEntry, destination_path:str) -> tuple:
        """move the item to the destination and ensure that detination exists"""
        if not path.exists(destination_path):
            makedirs(destination_path)

        try:
            move(item.path, path.join(destination_path, item.name))
            return (True, )
        except Exception as e:
            return (False, e)
        
    #---- Helpers to read categories file ----#
    def _get_sub_categories(self, categories:dict) -> list:
        sub_categories = []
        for k, v in categories.items():
            if type(v) is list:
                sub_categories.extend(v)
            else:
                sub_categories.extend(self._get_sub_categories(v))
        return sub_categories

    
    def _load_categories(self) -> dict:
        with open("categories.json", "r") as f:
            categories = load_json(f)
        #add 'all' key for each category has sub-categories
        for k, v in categories.items():
            if type(v) is list:
                continue
            categories[k]["all"] = self._get_sub_categories(v)
        return categories

    
    def _get_category(self, item:DirEntry, categories:dict=None) -> 'str|list[str]|None':
        if not categories: categories = self._categories

        if extension := self._get_file_extension(item)[1: ]: #extension without '.'
            for category, extensions in categories.items():
                if type(extensions) is list:
                    if extension in extensions:
                        return category
                    continue
                
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
        """return statistics of the Folder content"""
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
    def organize_by_extensions(self, output_folder_name, include_folders:bool=True, ignore:list[str]=None) -> tuple:
        if not ignore: ignore = self._default_ignore_list(output_folder_name)
        content = self.get_content("all" if include_folders else "files")

        moved = 0
        errors = []

        for item in content:
            if item.name in ignore:
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
                errors.append((item.path, response[1]))

        #finish
        return (moved, errors)

    
    def organize_by_categories(self, output_folder_name, include_folders:bool=True, ignore:list[str]=None) -> tuple:
        if not ignore: ignore = self._default_ignore_list(output_folder_name)
        content = self.get_content("all" if include_folders else "files")

        moved = 0
        errors = []

        for item in content:
            if item.name in ignore:
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
                    errors.append((item.path, response[1]))
                continue
            
            #many sub-categories
            if type(category) is list:
                response = self._safe_move(item, path.join(output_folder_name, *list(map(lambda c: c.title(), category))))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.path, response[1]))
                continue

            #unknown category
            if category is None:
                response = self._safe_move(item, path.join(output_folder_name, "Other"))
                if response[0]:
                    moved += 1
                else:
                    errors.append((item.path, response[1]))
            
        #finish
        return (moved, errors)