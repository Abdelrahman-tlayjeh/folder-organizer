# Folder Organizer CLI app
## Automate basic folder-organizing-tasks.
<hr>

### <u>Features:</u>
- [Show folder stats](#show-folder-content-stats)
- Organize the folder content in 2 different way:
    - [By Extensions](#organize-by-extensions)
    - [By Categories](#organize-by-categories)
- [Bulk-rename](#rename-content)
- [Change Extension](#change-an-extension-to-another)
<hr>

### <u>Get started:</u>
- install requirements:
```console
pip3 install -r requirements.txt
```
- set the scripts and the JSON file in the folder that you want to organize <i>(in the same level of content)</i>
- open the terminal.

 you can check all commands using one of the following:
```console
python folder_organizer_CLI.py --help
```
or
```console
python folder_organizer_CLI.py show-commands
```
> use 'python3' on Linux or mac 


<hr>

## <u>Show Folder content stats:</u>
To see the count of different content types (extensions) in the folder:

```console
python folder_organizer_CLI.py show-stats
```

### Example of output:

![imgs](/imgs/show_stats.png)


## <u>Organize by Extensions</u>
To organize folder content by extensions:
```console
python folder_organizer_CLI.py organize ext "<output folder name>"
```
> replace <output folder name> by a valid folder name to be the folder that will contain all organized content.

### Example of output:
![imgs](/imgs/organize.png)

### Example of output (in case of errors):
![imgs](/imgs/organize_error.png)

### <u>Example of how it works:</u>
Before:
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

After:
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
To organize folder content by categories:
```console
python folder_organizer_CLI.py organize ext "<output folder name>"
```

```
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
        "codes": ["py", "js", "cpp", "c", "php", "html", "css"],
        "db": ["sqlite", "db"],
        "readme": ["md"]
    },
    "zip": ["zip", "rar"]
}

```
>The script can handle multiple nested categories.

### <u>Example of how it works:</u>

Before:
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

After:
```
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
## <u>Rename content</u>
To rename all the content of the folder:
```console
python folder_organizer_CLI.py rename "<name pattern>"
```
    There are two special characters that can be used in the pattern:
    - []: will be replaced by a unique number (index)
    - {}: will be replaced by the old name

### <u>Example of how it works:</u>

Before:
```
working directory/                      
├─ 10052022.txt
├─ 12052022.txt                          
├─ 18052022.txt
├─ 03062022.txt                          
├─ 12062022.txt
```
using:
> python folder_organizer_CLI.py rename "note_[]"

After:
```
working directory/                      
├─ note_0.txt
├─ note_1.txt                          
├─ note_2.txt
├─ note_3.txt                          
├─ note_4.txt
```

## <u>Change an extension to another</u>
To change one extension to another for all files:
```console
python folder_organizer_CLI.py change-extension "<current extension>" "<new extension>"
```

### <u>Example of how it works:</u>

Before:
```
working directory/                      
├─ 10052022.jpeg
├─ 12052022.jpeg                          
├─ 18052022.jpeg
├─ 03062022.jpeg                          
├─ note.txt                          
├─ 12062022.jpeg
```
using:
> python folder_organizer_CLI.py change-extension ".jpeg" ".png"

After:
```
working directory/                      
├─ 10052022.png
├─ 12052022.png                          
├─ 18052022.png
├─ 03062022.png                          
├─ note.txt                          
├─ 12062022.png
```
> the script behavior can be optimized as the need by changing some default values in the FolderOrganizer class (folder_organizer.py)
