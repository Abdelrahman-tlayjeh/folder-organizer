from folder_organizer import FolderOrganizer
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()
organizer = FolderOrganizer()

#========== Commands ==========#
COMMANDS = {
    "show-stats": "Show you a table that contains statistics of the folder content",
    "organize ext (folder name)": "Organize the folder by extensions and set new organized content in a folder with (folder name) name",
    "organize cat (folder name)": "Organize the folder by categories (you can edit categories from categories.json file) and set new organized content in a folder with (folder name) name"
}



#========== Helpers ==========#
def generate_rich_syntax(color:str, content:str, other:list=[]) -> str:
    return f"[{color} {' '.join(other)}]{content}[/{color} {' '.join(other)}]"


#========== App commands ==========#
@app.command()
def show_commands():
    table = Table(show_header=True, show_lines=True)
    table.add_column(generate_rich_syntax("white", "command", ["bold", "underline"]), justify="left")
    table.add_column(generate_rich_syntax("white", "action", ["bold", "underline"]), justify="left")

    for command, action in COMMANDS.items():
        table.add_row(generate_rich_syntax("white", ">>> " + command), generate_rich_syntax("white", action))
    
    console.print(table)


@app.command(short_help="Show Stats of Folder content")
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


@app.command(short_help="Organize folder content by extensions")
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

    #if no errors
    if len(res[1]) == 0:
        console.print(generate_rich_syntax("green", "0 Errors occurs"))
    #there is errors
    else:
        console.print(generate_rich_syntax("red", f"{len(res[1])} Errors occurs!"))
        #create table for errors
        table = Table(show_header=True, show_lines=True)
        table.add_column(generate_rich_syntax("red", "Item Path", ["bold"]), justify="left", no_wrap=False)
        table.add_column(generate_rich_syntax("red", "Error message", ["bold"]), justify="left", no_wrap=False)
        for k, v in res[1]:
            table.add_row(generate_rich_syntax("red", k), generate_rich_syntax("red", str(v)))
        #output
        console.print(table)


if __name__ == "__main__":
    app()