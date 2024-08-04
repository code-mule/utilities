# bertrandterrier@codeberg.org/utilities/todo/search.py

import Levenshtein as lev

def fz_search(query:str,text:str,max_dist:int=3):
    