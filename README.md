# Folder Organizer CLI app
## Automate basic folder-organizing-tasks.
<hr>

### <u>Features:</u>
- show brief statistics on folder content
- Organize the folder content in 2 different way:
    - By extensions: set all files with same extension in one folder.
    - By categories: set group of extensions in one folder. <i>(check categories.json)</i>
<hr>

### <u>Get started:</u>
- install requirements:
    > pip3 install -r requirements.txt
- set the scripts in the folder that you want to organize <i>(in the same level of content)</i>
- open the treminal, you can check all commands using one of the following:
    > folder_organizer_CLI.py --help
    
    or

    > folder_organizer_CLI.py show-commands

<hr>

### <u>Show Folder content stats:</u>
To get an idea of the content of folder, run the following command:

> folder_organizer_CLI.py show-stats

```console
example of output using 'python folder_organizer_CLI.py show-stats' command:
```

![imgs](/imgs/show_stats.png)


### <u>Organize by Extensions</u>
To organize folder content by extensions, use the following command:
> folder_organizer_CLI.py organize ext [output folder name]
```console
example of output using 'python folder_organizer_CLI.py organize ext "Organized Folder"' command:
```
![imgs](/imgs/org_ext.png)

#### <u>Example of how it works:</u>
Folder structure before:
```console
working directory/                      
├─ note.txt
├─ 1m_monkey_image.png                          
├─ presentation.docx
├─ sub folder/                          
├─ cheat_sheet.txt
├─ categories.json
├─ folder_organizer.py
├─ folder_organizer_CLI.py
```

Folder structure after:
```console
working directory/
├─ Organized Folder/
│  ├─ Folders/
│  │  ├─ sub folder/
│  ├─ .docx/
│  │  ├─ presentation.docx
│  ├─ .png/
│  │  ├─ 1m_monkey_image.png
│  ├─ .txt/
│  │  ├─ cheat_sheet.txt
│  │  ├─ note.txt
├─ folder_organizer.py
├─ categories.json
├─ folder_organizer_CLI.py
```

### <u>Organize by Categories</u>
To organize folder content by categories, use the following command:
> folder_organizer_CLI.py organize cat [output folder name]
```console
Default categories:
{
    "programs": ["exe", "msi"],
    "documents": {
        "pdf": ["pdf", "PDF"],
        "notes": ["txt"]
    },
    "office": {
        "word": ["doc", "docx"],
        "excel": ["xls", "xlsx"],
        "power point": ["pptx"],
        "access": ["ACCDA", "ACCDB"]
    },
    "media": {
        "images": ["png", "gif", "JPEG", "jpeg"],
        "videos": ["mp4", "webm"],
        "audios": ["m4a", "mp3"]
    },
    "programming": {
        "scripts": ["py", "js", "cpp", "c", "php", "html", "css"],
        "db": ["sqlite", "db"],
        "readme": ["md"]
    },
    "zip": ["zip", "rar"]
}

```
> You can edit categories from categories.json file.

> ! multiple nested categories is not working yet :( 

#### <u>Example of how it works:</u>

Folder structure before:
```console
working directory/                      
├─ note.txt
├─ 1m_monkey_image.png                          
├─ presentation.docx
├─ sub folder/                          
├─ cheat_sheet.txt
├─ categories.json
├─ folder_organizer.py
├─ folder_organizer_CLI.py
```

Folder structure after:
```console
working directory/
├─ Organized Folder/
│  ├─ Folders/
│  │  ├─ sub folder/
│  ├─ Documents/
│  │  ├─ Notes/
│  │  │  ├─ note.txt
│  │  │  ├─ cheat_sheet.txt
│  ├─ Media/
│  │  ├─ Images/
│  │  │  ├─ 1m_monkey_image.png
│  ├─ Office/
│  │  ├─ Word/
│  │  │  ├─ presentation.docx
├─ folder_organizer.py
├─ categories.json
├─ folder_organizer_CLI.py
```

## <u>Optimizations:</u>
- You can avoid moving folders by changing the default value of <b>include_folders</b> argument in folder_organizer.py methods to False.
- You can change the files and folders that the script will never move by adding their names to the list in <b>_default_ignore_list</b> method in folder_organizer.py script.

