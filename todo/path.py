import os
from viz import btp

def search_correct_path(orig_dir=str):
    rest,part = os.path.split(orig_dir)

    btp(f'Not able to find DIR {orig_dir}.','Trying different paths...')
    print(f'Current path: {os.path.curdir}')
    counter=0
    sft_cntr = 333
    result = None
    ext_loop = False
    while len(rest) >= 1 and ext_loop == False:
        counter += 1

        if sft_cntr == counter:
            new_path = None
            break

        tmp_upper:str = part.upper()
        tmp_lower:str = part.lower()
        tmp_cptlz:str = part.capitalize()

        for tmp in [tmp_cptlz,tmp_lower,tmp_upper]:
            new_path = orig_dir.replace(part,tmp)
            
            if os.path.exists(new_path):
                print(f'  ::{new_path} -- MATCH')
                result = new_path
                ext_loop = True
                break
            else:
                print(f'  ::{new_path} -- no match')
            
        rest,part=os.path.split(rest)
    
    if result == None:
        return orig_dir
    else:
        return result