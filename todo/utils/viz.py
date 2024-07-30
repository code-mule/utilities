# bertrandterrier@codeberg.org/utilities/todo/utils/viz.py

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
    if not options == None:
        for idx,opt in options.items():
            print(f'  -{idx}- {opt}')
        print('')

    if not prefix == None:
        print(f"  › {prefix}")

    inp:str = input(f"  {prompt} » ")

    return inp