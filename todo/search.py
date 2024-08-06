# bertrandterrier@codeberg.org/utilities/todo/search.py
#
# Script for the fuzzy search
#
# =========================================================================== #

import Levenshtein as lev
import pandas as pd

# =========================================================================== #

def fuzzy_search(query:str,search_space:dict[int:str],good_dist:int=1,max_dist:int=5) -> tuple[str,str]:
    """Fuzzy search.

    Args:
        query (str): Query with word or phrase to search for.
        search_space (dict[int,str]): Search space with integer for index as key and a string for the word(s) searched in.
        good_dist (int, optional): Very small distance of words to be included. Defaults to 1.
        max_dist (int, optional): Maximal distance of words to be included. Defaults to 5.

    Returns:
        tuple[list,list]: Good results and max distance results.
    """
    # Storage for results
    result = []
    good_result = []

    # Iterate threw text
    for idx,words in search_space.items():
        single_words = words.split(' ')
        for w in single_words:
            dist:float = lev.distance(query,words)
            
            if dist <= good_dist:
                good_result.append(idx)
            elif dist <= max_dist:
                result.append(idx)
    
    return (good_result,result)

def search_tasks(query:str,data:pd.DataFrame,columns:list) -> tuple[list,list]:
    """Search certain columns of a pandas DataFrame with tasks for a query.

    Args:
        query (str): Search query. Word(s) or phrase to search for.
        data (pd.DataFrame): Pandas DataFrame with tasks that will be searched for query.
        columns (list): List of columns that will be searched. If empty or None it will default to ':' for all.

    Returns:
        tuple[list,list]: _description_
    """
    results = []
    good_results = []

    # Check if columns list is empty or None
    if columns in [""," ",None]:
        columns = ":"

    # Get columns for search
    search_cols:pd.DataFrame = data[columns]

    # Iterate threw columns for search
    tmp_srch_dct = {}
    for col in search_cols.columns:
        # Add index and content to search space
        for row in range(search_cols.shape[0]):
            tmp_srch_dct[row] = f"{search_cols.loc[row,col]}"
        
        # Add search results for column to search results
        tmp_good_results,tmp_results = fuzzy_search(query=query
                                                    search_space=tmp_srch_dct
                                                    )
        good_results = good_results + tmp_good_results
        results = results + tmp_results

    return (good_results,results)