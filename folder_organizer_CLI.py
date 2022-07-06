from folder_organizer import FolderOrganizer
from typer import Typer
from rich.console import Console
from rich.table import Table

"""
TO-DO:
------
    - create helper method to show errors table [Done]
    - add comments and documentations to new commands (rename and change extensions) [Done]
"""

app = Typer()
console = Console()
organizer = FolderOrganizer()

#========== Commands description ==========#
COMMANDS = {
    "show-stats": "Display a table that contains general stats of folder content",
    "organize ext <folder name>": "Organize the folder by extensions and set new organized content in a folder with <folder name> name",
    "organize cat <folder name>": "Organize the folder by categories (you can edit categories from categories.json file) and set new organized content in a folder with (folder name) name",
    "rename <new name pattern>": "Rename all content in the folder.",
    "change-extension <current extension> <new extension>": "Change the extensions of all files with extension = <current extension> to the <new extension>"
}


#========== Helpers ==========#
def generate_rich_syntax(color:str, content:str, other:list=[]) -> str:
    return f"[{color} {' '.join(other)}]{content}[/{color} {' '.join(other)}]"


def handle_errors(errors:tuple) -> None:
    #if no errors
    if len(errors) == 0:
        console.print(generate_rich_syntax("green", "No Errors Occur!"))
    #there is errors
    else:
        console.print(generate_rich_syntax("red", f"{len(errors)} Errors Occur!"))
        #create table for errors
        table = Table(show_header=True, show_lines=True)
        table.add_column(generate_rich_syntax("red", "Item name", ["bold"]), justify="left", no_wrap=False)
        table.add_column(generate_rich_syntax("red", "Error message", ["bold"]), justify="left", no_wrap=False)
        for k, v in errors:
            table.add_row(generate_rich_syntax("red", k), generate_rich_syntax("red", str(v)))
        #output
        console.print(table)


#========== App commands ==========#
@app.command(short_help="Show all available commands")
def show_commands():
    table = Table(show_header=True, show_lines=True)
    table.add_column(generate_rich_syntax("white", "command", ["bold", "underline"]), justify="left")
    table.add_column(generate_rich_syntax("white", "action", ["bold", "underline"]), justify="left")

    for command, action in COMMANDS.items():
        table.add_row(generate_rich_syntax("white", ">>> " + command), generate_rich_syntax("white", action))
    
    console.print(table)


#=== Show folder stats ===#
@app.command(short_help="Show Stats of folder content")
def show_stats():
    stats = organizer.get_stats()
    #create table
    table = Table(show_header=True)
    table.add_column(generate_rich_syntax("green", "Total", ["bold"]))
    table.add_column(generate_rich_syntax("green", stats["Total"], ["bold"]))
    #set font color
    for k, v in stats.items():
        if k == "Total":
            continue
        if k == "folders":
            color = "yellow"
        elif k == "unknown":
            color = "red"
        else:
            color = "white"
        #add row
        table.add_row(generate_rich_syntax(color, k), generate_rich_syntax(color, v))

    #output
    console.print(table)


#=== Organize folder ===#
@app.command(short_help="Organize folder content by extensions or categories")
def organize(by:str, output_folder_name:str):
    if by == "ext":
        res = organizer.organize_by_extensions(output_folder_name)
        console.print(generate_rich_syntax("green", f"{res[0]} Sucessfully moved"))
    elif by == "cat":
        res = organizer.organize_by_categories(output_folder_name)
        console.print(generate_rich_syntax("green", f"{res[0]} Sucessfully moved"))
    else:
        console.print(generate_rich_syntax("red", "Invalid input! You can organize by extensions 'ext' or categories 'cat'."))
        return

    handle_errors(res[1])


#=== rename content ===#
@app.command(short_help="Rename folder content")
def rename(new_name_pattern:str):
    res = organizer.rename_content(new_name_pattern)
    console.print(generate_rich_syntax("green", f"{len(res[0])} Successfully renamed:", ["bold"]))
    handle_errors(res[1])


#=== change extensions ===#
@app.command(short_help="Change extension")
def change_extension(old:str, new:str):
    res = organizer.change_extensions(old, new)
    console.print(generate_rich_syntax("green", f"{res[0]} Successfully changed:", ["bold"]))
    handle_errors(res[1])



if __name__ == "__main__":
    app()