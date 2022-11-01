from pathlib import Path
import h5py

def is_exist(path):
    if not h5py.is_hdf5(path):
        return False
    return True

def list_add(list1, list2):
    if len(list1) == len(list2):
        for i in range(len(list1)):
            list1[i] = list1[i] + list2[i]
        return list1
    else:
        raise Exception('The length of the list should be the same.')
    
