# Folder Organizer CLI app
## Automate basic folder-organizing-tasks.
<hr>

### <u>Features:</u>
- Show the counts of the different content types in the folder. 
- Organize the folder content in 2 different way:
    - By extensions: set all files with same extension in one folder.
    - By categories: set all files with same categort in one folder. <i>(check categories.json)</i>
<hr>

### <u>Get started:</u>
- install requirements:
```console
pip3 install -r requirements.txt
```
- set the scripts and the JSON file in the folder that you want to organize <i>(in the same level of content)</i>
- open the terminal, you can check all commands using one of the following:
```console
folder_organizer_CLI.py --help
```
or
```console
folder_organizer_CLI.py show-commands
```
    

<hr>

## <u>Show Folder content stats:</u>
To get an idea about the count of different content types in the  folder, run the following command:

```console
python folder_organizer_CLI.py show-stats
```
> use 'python3' on linux or mac 

### Example of output:

![imgs](/imgs/show_stats.png)


## <u>Organize by Extensions</u>
To organize folder content by extensions, use the following command:
```console
python folder_organizer_CLI.py organize ext '{output folder name}'
```
> replace {output folder name} by a valid folder name to be the folder that will contain all organized content.

### Example of output:
![imgs](/imgs/org_ext.png)

### <u>Example of how it works:</u>
Folder tree before:
```
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

Folder tree after:
```
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

## <u>Organize by Categories</u>
To organize folder content by categories, use the following command:
```console
python folder_organizer_CLI.py organize ext '{output folder name}'
```

>The script can handle multiple nested categories.

```console
Default categories.json content:
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
### <u>Example of how it works:</u>

Folder tree before:
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

Folder tree after:
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

> the script behavior can be optimized as the need by changing some default values in the FolderOrganizer class (folder_organizer.py)
