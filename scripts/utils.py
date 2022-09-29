from pathlib import Path
import h5py

def is_exist(path):
    if not h5py.is_hdf5(path):
        return False
    return True
