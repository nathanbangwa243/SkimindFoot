#-*-coding: utf-8 -*-

# regular expressions module
import re as reg

def find_int_in_str(string=None):
    """
    trouver les nombres entiers dans une chaine de caractere
    en ignorant les signes
    
    :param string: str
    
    :reutrn: ['float', 'float', ...]

    """
    response = []
    if string: # si la chaine n'est pas vide
        response = reg.findall("([0.0-9.9]+)", string) # on cherche les floatants

    return  [float(integer) for integer in response]