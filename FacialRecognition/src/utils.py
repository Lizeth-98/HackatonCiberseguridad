# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:59:58 2024

@author: cs940
"""

import pickle

def save_pickle(data, filepath):
    """Guardar datos en formato pickle."""
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filepath):
    """Cargar datos en formato pickle."""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
