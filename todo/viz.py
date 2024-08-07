# bertrandterrier@codeberg.org/utilities/todo/utils/viz.py

def get_prefix(dlevel:int=0) -> str:
    """Create a prefix for indent level in terminal.

    Args:
        dlevel (int, optional): Level of indentation. Defaults to 0.

    Returns:
        str: Prefix string for level of indentation.
    """
    # Create prefix
    dpref:str = f"{dlevel*'o'}»"

    return dpref

def btp(*args, now:bool=True) -> str:
    """Visually differing printing style from normal command lines

    Args:
        now (bool, optional): Determine if arguments are printed directly, or just be returned. Defaults to True.

    Returns:
        str: _description_
    """
    result = ""
    for arg in args:
        lines = arg.split('\n')
        for l in lines:
            l = f"  › {l}"
            result = result + l + "\n"

            if now == True:
                print(l)
    
    return result

def bt_inp(prompt:str,options:dict[str:str]=None, prefix:str=None):
    # Print option list if provided
    if not options == None:
        for idx,opt in options.items():
            # Create white space
            space = (4-len(str(idx))) * " "
            print(f'{space} [{idx}] {opt}')
        print('')

    if not prefix == None:
        print(f"  › {prefix}")

    inp:str = input(f"  {prompt} » ")

    return inp