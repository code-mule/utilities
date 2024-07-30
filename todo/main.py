# bertrandterrier@codeberg.org/utilities/todo/main.py

from utils.viz import btp,bt_inp
from tabulate import tabulate

import pandas as pd

class MyTasks:
    def __init__(self,data:pd.DataFrame):
        self.df = data
        self.cols = list(data.columns)
        
        # Create printable table from DataFrame
        self.create_table()

        # Create category index
        self.cat_idx = {}
        for idx,cat in enumerate(list(self.df["type"].cat.categories.tolist())):
            cat[idx] = f"{cat}"
        self.cat_idx["+"] = "NEW"
        self.cat_idx["-"] = "CANCEL"

    def create_table(self):
        self.table = tabulate(tabular_data=self.df, headers="Keys", TableFormat="pretty")
    
    def show(self):
        print(self.table)

        waiter = self.check(bt_inp(prompt="[-|x|?|<action>]"))
        match waiter.lower():
            case "x"|"-":
                return waiter
            case "+"|"new"|"new task":
                return self.create_task
            case "f"|"find"|"search":
                return self.search_task()
            case _:
                btp("Input not recognized.")
                return 0

    def store_task(self):

        usr_inp:str = bt_inp("[<idx>|<name>]",
               prefix="Choose task to store as \"finished\" by index or name:")

        if usr_inp.isnumeric() == True:
            usr_inp = int(usr_inp)

            try:
                self.df.drop(index=usr_inp)
            except:
                btp("Not possible.")
        
        else:
            btp("You have to use index (number) to store task as finished.")
        
        self.create_table()

        return
    
    def create_task(self):
        name = self.check(bt_inp(prompt="Name of task"))
        if name in ["-","x"]:
            return name

        importance = self.check(bt_inp(prompt="[<0-3>]", 
                            prefix="Choose importance of task",
                            options={
                                0:"Projects of interest",
                                1:"Nothing special",
                                2:"Important",
                                3:"Very urgent."
                            }))
        if importance in ["x","-"]:
            return importance 

        # Check level of importance
        match importance:
            case 0:
                clr = "\033[32m"
            case 2:
                clr = "\033[33m"
            case 3:
                clr = "\033[31m"

        importance = f"{clr}{importance}\033[0m"
        name = f"{clr}{name}\033[0m" 

        category = self.check(bt_inp(prompt="[<idx>]",
                                options=self.cat_idx
                                ))
        if category in ["x","-"]:
            return category
        
        note = self.check(bt_inp(prompt="",
                      prefix="Add a note [opt.]"
                      ))
        if note in ["x","-"]:
            return note
        
        new_entry = [name,category,note,importance]

        # Add new row to dataframe
        self.df.loc[len(self.df)] = new_entry
        self.create_table()
    
        return 0
                
    def check(self,prompt:str) -> int|str:
        """Check a prompt string and check if another menu should be activated.

        Args:
            prompt (str): The prompt to be checked.

        Returns:
            str|int: [0|1] Return code. If one, current menu should be killed. Otherwise the string itself will be returned.
        """
        return_code = 1
        match prompt.lower():
            case "!"|"x":
                return 2
            case "-"|"return"|"c"|"cancel":
                return 1
            case "?":
                self.help()
                return 0
            case _:
                return 0