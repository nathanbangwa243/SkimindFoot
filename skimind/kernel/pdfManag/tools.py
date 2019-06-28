# regular expression module
import re

# config
from . import config

# pdf
import PyPDF2


def is_matchs_datas(tablist):
        """
            Verifie si une liste contient les donnees de pari
        """

        try:
            date = tablist[1]

            date_list = re.findall("\d\d[-/]\d\d[-/]\d{2,4}",date)

            if not date_list:
                raise ValueError("le tableau ne contient aucune date")

        except Exception as err:
            return False
    
        return True

def serialize_date_format(date:str, date_format:str):
    def complet_DMY():
        nonlocal date_tab

        day_month = map(lambda value: value if len(value) == 1 else f"0{value}", date_tab[:-1])

        date_tab[:-1] = list(day_month)

        date_tab[-1] = date_tab[-1] if len(date_tab[-1]) == 4 else f"20{date_tab[-1]}" 

    date_temp = str(date)

    if date_format == config.DEFAULT_FORMAT:
        return date
    
    date_tab = date_temp.split("-")
    
    if date_format == 'MM-DD-YYYY':
        date_tab[0], date_tab[1] = date_tab[1], date_tab[0]
    
    elif date_format == 'YYYY-MM-DD':
        date_tab.reverse()

    # serialyze 
    complet_DMY()

    date_temp = "-".join(date_tab)

    return date_temp


def count_pages(filename:str):
    pages_nb = 1

    with open(filename, 'rb') as fp:
        pdf_reader = PyPDF2.PdfFileReader(fp)

        pages_nb = pdf_reader.numPages
    
    return pages_nb


