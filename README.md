# Folder Organizer CLI app
## Automate basic folder-organizing-tasks.
<hr>

### <u>Features:</u>
- show brief statistics on folder content
- Organize the folder content in 2 different way:
    - By extension: set all files with same extension in on folder.
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

![img4readme](/img4readme/shoe_stats.png)


### <u>Organize by Extensions</u>
To organize folder content by extensions, use the following command:
> folder_organizer_CLI.py organize ext [output folder name]
```console
example of output using 'python folder_organizer_CLI.py organize ext "Organized Folder"' command:
```
![img4readme](/img4readme/org_ext.png)


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


