# bertrandterrier@codeberg.org/utilities/todo/search.py
#
# Script for the fuzzy search
#
# =========================================================================== #

import pandas as pd

# =========================================================================== #

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
        #tmp_good_results,tmp_results = fuzzy_search(query=query
                     #                               search_space=tmp_srch_dct
                      #                              )
        #good_results = good_results + tmp_good_results
        #results = results + tmp_results

    return 