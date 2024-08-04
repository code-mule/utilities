# bertrandterrier@codeberg.org/utilities/todo/main.py

# --------------------------------------------------------- #

from conf import get_conf,check_first_time,set_conf
from viz import btp,bt_inp
from tabulate import tabulate

import pandas as pd
import os
import argparse
import sys
import shutil

DIR_PATH:str = os.path.dirname(os.path.abspath(__file__))
CSV_TMPL_PATH:str = os.path.join(DIR_PATH,"files/template.csv")

LEGEND = {
    "?":"Show command legend",
    "+":"Add task",
    "-":"Finish task",
    "f":"Find task",
    "fs":"Show last search table",
    "s":"Show tasks [:OPEN|:all|:unfin]",
    "w":"Save changes",
    "q":"Quit ToDo",
    "wq":"Save changes and quit",
    "q!":"Force quit"
}

CHECK = ["x","q","q!","wq"]

UNFIN = "\033[31m✗\033[0m"
FIN = "\033[32m✔\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"
RE_ASCII = r"\[\d\dm\.+?\\033"

# ------------------------------------------------- #
def parse_cl_args():
    # Initialize parser
    parser = argparse.ArgumentParser(prog="To-Do")

    # Set arguments
    parser.add_argument(
        "-i",
        "--input",
        help="CSV file with format for To-Do-Application. Comp. 'files/template.csv'"
    )
    parser.add_argument(
        "-c",
        "--create",
        help="Create new CSV style from To-Do template."
    )
    parser.add_argument(
        "-s",
        "--set",
        help="Change settings. 'table:<tabulate-table-style> file:<my-default-file>'."
    )

    # Store arguments
    args = parser.parse_args()

    return args

class MyTasks:

    def __init__(self,data:pd.DataFrame):
        """Task object creating tabulate tables, allowing to add and delete tasks, save the new DataFrame, etc.

        Args:
            data (pd.DataFrame): DataFrame with CSV data.
        """
        self.df = data
        self.cols = list(data.columns)
 
        # Create printable table from DataFrame
        self.create_table()

        # Create category index
        self.cat_idx = {}
        for idx,cat in enumerate(list(self.df["type"].cat.categories.tolist())):
            self.cat_idx[idx] = f"{cat}"
        self.cat_idx["+"] = "NEW"
        self.cat_idx["-"] = "CANCEL"

        self.search_table = ""

    def create_table(self) -> tabulate:
        temp_df = self.df.copy()

        # Change int64 column to object type
        temp_df.importance = temp_df["importance"].astype("str")

        # Coloring tasks
        for row in range(temp_df.shape[0]):
            match temp_df.loc[row,"importance"]:
                case "0":
                    clr = BLUE
                case "2":
                    clr = YELLOW
                case "3":
                    clr = MAGENTA
                case _:
                    clr = ""

            temp_df.loc[row,"importance"] = f"{clr}{temp_df.loc[row,'importance']}{RESET}"
            temp_df.loc[row,"name"] = f"{clr}{temp_df.loc[row,'name']}{RESET}"
                
        # Mask finished/unifnished tasks
        mask_fin = temp_df.status == "fin"
        temp_df.loc[mask_fin,"status"] = FIN
        temp_df.loc[~mask_fin,"status"] = UNFIN

        self.table = tabulate(tabular_data=temp_df.loc[~mask_fin,:], 
                              headers="keys", 
                              tablefmt="pretty"
                              )
        self.table_all = tabulate(tabular_data=temp_df,
                                  headers="keys",
                                  tablefmt="pretty"
                                 )
        self.table_fin = tabulate(tabular_data=temp_df.loc[mask_fin,:],
                                  headers="keys",
                                  tablefmt="pretty"
                                  )
                                  
    
    def show(self,table_type:str="open") -> tabulate:
        """Prints/shows tabulate form of DataFrame

        Args:
            table_type (str, optional): [open|all|fin] Type of table to be 
                                        shown/printed. Defaults to "open".

        Returns:
            tabulate: Tabulate tables. [All tasks,open tasks,finished tasks]
        """
        match table_type:
            case "o"|"open"|"unfin"|"unfinished":
                temp_table = self.table
            case "f"|"fin"|"finished":
                temp_table = self.table_fin
            case "a"|"all":
                temp_table = self.table_all
            case _:
                btp(f"  {RED}{BOLD}-›ERROR","Unknown <table_type>.{RESET}")
            
        temp_table = self._printable_table(temp_table)
        print(temp_table)

        inp = bt_inp(prompt="")

        return inp
    
    def _printable_table(self,table:str) -> str:

        table = table.replace("\n","\n  ")
        table = f"  {table}"

        return table
   
    def create_task(self,command:str) -> str:
        """Creates a new task.

        Returns:
            str: [s:open] Returns return code for showing open tasks.
        """
        if len(command) >= 2:
            if command[1] == " ":
                command = command[2:]
            else:
                command = command[1:]
        else:
            name = bt_inp(prompt="<name>",
                          prefix="Choose task name" 
                          )

        if name in CHECK:
            return name
        
        category = bt_inp(prompt="<type>",prefix="Choose type of task.")
    
        if category in ["x","q","q!"]:
            return category
        
        importance = bt_inp(prompt="[0-3]",prefix="Set importance of task.")
        status = ""
        new_entry = [importance,name,category,status]

        # Add new row to dataframe
        self.df.loc[len(self.df)] = new_entry
        
        self.create_table() 
        return "s:open"
                     
    def save(self,path:str) -> str:
        self.df.to_csv(path, index=False)

        return "s:all"

    def _extract_search_command(self,command:str) -> tabulate:
        # Extract keyword
        if ":" in command:
            cols = command.split(":")
            f = cols[0]
            cols = cols[1:]

            if len(cols) <= 1:
                cols = cols
        
        else:
            f = command
            cols = ":"

        if f == "fs":
            return self.show_search_table()        
        else:
            return f,cols

    def find(self,inp:str):
        # Extract keyword, command
        keywords = inp.split(" ")
        command = keywords[0]
        keywords = keywords[1:]

        f,cols = self._extract_search_command(command=command)

        print(f)
        print(f"COLUMNS: {cols}")

        search_indeces_exact = []
        search_indeces_others = []
        # Searching DataFrame
        for row in range(self.df.shape[0]):
            for col in cols:
                # Assure that column is existing
                if not col in self.df.columns:
                    btp(f"{YELLOW}{BOLD}WARNING",f"{col} no valid category.{RESET}")
                    continue

                for key in keywords:
                    var = self.df.loc[row,col]
                    for esc_ascii in [BLUE,RED,YELLOW,GREEN,MAGENTA]:
                        var = var.replace(esc_ascii,"")
                    # Storing exact find
                    if key.strip().lower() == var.strip().lower():
                        search_indeces_exact.append(row)
                    
                    # Store none exact finds
                    elif key.strip().lower() in var.strip().lower() or var.strip().lower() in key.strip().lower():
                        search_indeces_others.append(row)

        # Clean lists from doubles and sort them
        search_indeces_others = list(set(search_indeces_others))
        search_indeces_exact = list(set(search_indeces_exact))               

        # Create result column
        temp_df = self.df.copy()
        temp_df["result"] = "-"

        for index_list,rslt in zip([search_indeces_exact,search_indeces_others],
                                   [f"{GREEN}EXACT{RESET}",f"FUZZY"]):
            if len(index_list) >= 2:
                temp_df.iloc[min(index_list):max(index_list)+1,-1] = rslt
            elif len(index_list) == 1:
                temp_df.iloc[index_list[0],-1] = rslt

        mask_no_find = temp_df.result == "-"
        temp_df = temp_df.loc[~mask_no_find,:]
        
        # Create table
        self.search_table = tabulate(tabular_data=temp_df,
                                headers="keys",
                                tablefmt="pretty"
                                )
        return
    
    def show_search_table(self) -> str:
        # Create printable search table        
        search_table = self.search_table.replace("\n","\n  ")
        search_table = f"  {search_table}"

        # Print search table
        print(search_table)

        inp = bt_inp(prompt="")

        return inp
         
    def show_legend(self) -> None:
        # Print legend
        inp = bt_inp(prompt="",
                     options=LEGEND
                     )
        return inp
    
    def fin_task(self,command:str) -> str:
        # Check if index already in command
        if len(command) >= 2:
            inp = command[1:].strip()
            
        else:
            # Prompt user to choose index
            inp = bt_inp("[idx]",prefix="Choose task to finish by index")
             
        # Check prompt input
        if inp.strip().isnumeric():
            if not int(inp) in self.df.index:
                print("Wrong index")
                print(self.df.index)
            self.df.iloc[int(inp),-1] = f"fin"
        else:
            btp("FAILURE","Entry index not found.")
        
        return "s:all"
        
def main():
    # Get input path
    args = parse_cl_args()

   # Check if settings file is existing
    check_first_time()

    # Get settings from config file
    def_file,tbl_style = get_conf()

    # Get path
    if not args.set == None:
        # Reset configuration file
        set_conf(args.set)
        
        # Get new settings
        configs = get_conf()
        print('  → Reset configuration file:')
        for elem in configs:
            print(f'    » {elem}')
        
        # End app
        sys.exit(4)
    elif not args.input == None:
        path:str = args.input
    elif not args.create == None:
        path:str = os.path.expanduser(args.create)
        shutil.copy2(CSV_TMPL_PATH,path)
    elif def_file == None:
        print(f"  {RED}{BOLD}-› ERROR.\n  → No input file provided.\n  → Aborting.{RESET}")
        sys.exit(3)
    elif not os.path.exists(def_file):
        print(f"  {RED}{BOLD}-› FAILURE.\n  → File {def_file} not found.\n  → Aborting.{RESET}")
        sys.exit(2)
    else:
        path:str = def_file


    ## Load DataFrame
    df = pd.read_csv(path)

    # Create category column
    df["type"] = df["type"].astype("category")

    # Create To-do-list-object
    todolist:MyTasks = MyTasks(df)

    # Create table of DataFrame
    todolist.create_table()

    # Start main loop
    exit_check = False
    opt = "s:open"
    fail_save = 0
    while exit_check == False:
        # Insert fail save
        fail_save =+ 1
        if fail_save >= 555:
            exit_check = True
            continue

        # Check if app should be quit
        if opt.lower().startswith("w") or opt.lower().endswith("w"):
            # Save dataframe
            todolist.df.to_csv(path, index=False)

            # Get writing command out of option storage
            opt = opt.lower().replace("w","")

            # Check if option variable is now empty
            if len(opt) <= 0:
                opt = "s:open"
                continue
        
        if opt.lower().startswith("f") or opt.lower().startswith("ff"):
            todolist.find(opt)
            opt = todolist.show_search_table()
            continue
        
        if opt.lower().startswith("-"):
            opt = todolist.fin_task(opt)
            todolist.create_table()
            continue

        if opt.lower().startswith("+"):
            opt = todolist.create_task(opt)
            continue
        # Match the option which menu to show
        match opt.lower():
            case "s"|"so"|"s:unfinished"|"s:open":
                opt = todolist.show(table_type="open")
            case "sa"|"s!"|"s:all":
                opt = todolist.show(table_type="all")
            case "sf"|"s:fin"|"s:finished":
                opt = todolist.show(table_type="fin")
            case "?":
                opt = todolist.show_legend()
            case "q"|"quit"|"exit"|"!":
                # Reload CSV as DataFrame
                df = pd.read_csv(path)

                # Check if changes were saved
                if not todolist.df.shape[0] == df.shape[0]:
                    print(f"  {RED}{BOLD}-› WARNING","Changes were not saved.","Use [wq] for save+exit or [q!] to force an exit.{RESET}")
                    opt = bt_inp("[wq|q!|<option>]")
                    continue
                else:
                    btp("Quitting ToDo")
                    exit_check = True
            case "q!":
                btp("Ending ToDo")
                exit_check = True
            case "!q":
                inp = bt_inp("[y|N]",prefix="Do you meant [q!]?")
                if inp.lower() in ["y","yes","yeah"]:
                    exit_check = True
                    continue
                else:
                    opt = "?"
            case "wq":
                todolist.df.to_csv(path, index=False)
                exit_check = True
            case _:
                print(f"  {YELLOW}{BOLD}-› WARNING","Unrecognized input.{RESET}")
                opt = "?"
    return

if __name__ == "__main__":
    main()
    sys.exit(0)