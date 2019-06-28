# excel reader
import xlrd

# system tools
import os

# datetime
import pandas as pd

# regular expression
import re

# copy
import copy


def extract_metadatas(metadatas, is_betfile=True):
        """
            suppression du caractere versus
            remplacement des donnees vides (-)
            transformation des cotes en float
        """

        def serialize_data(data, isclass=False):
            # lowercase
            data =  str(data).lower()

            # replace comma by fullstop
            data = data.replace(",", ".")

            # remplacement de -, x par 0
            try:
                if is_betfile:
                    data = float(data)
                
                else:
                    data =  int(data)
            except:
                data = 0
            
            finally:
                if isclass:
                    data = int(data)
            
            return data
        
        def move_datas_bet(cotes):
            # copy
            new_cotes = copy.deepcopy(cotes)
            
            # --> index des cotes a mover
            index_to_move = [1, 4, 7, 10, 13, 22]

            #--> arrangement des new_cotes
            for index in index_to_move:
                new_cotes[index], new_cotes[index + 1] = new_cotes[index + 1], new_cotes[index]
            
            return new_cotes
        
        new_metadatas = copy.deepcopy(metadatas)


        for index in range(len(new_metadatas)):
            # idmatch
            idmatch = new_metadatas[index][0]

            idmatch = int(idmatch)

            new_metadatas[index][0] = idmatch

            # classement_A classement_B
            class_a = new_metadatas[index][4]
            class_b = new_metadatas[index][6]

            new_metadatas[index][4] = serialize_data(class_a, isclass=True)
            new_metadatas[index][6] = serialize_data(class_b, isclass=True)

            # cote ou resultat
            datas = new_metadatas[index][8:]

            datas = map(serialize_data, datas)

            datas = list(datas)

            if is_betfile:
                datas = move_datas_bet(datas)

            new_metadatas[index][8:] = datas

            # deletion of versus symbole
            del new_metadatas[index][5]

        return new_metadatas


def extract_datas(filename:str):
    def is_matchs_datas(tablist):
        """
            Verifie si une liste contient les donnees de pari
        """

        try:
            date = tablist[1].value

            date_list = re.findall("\d\d[-/]\d\d[-/]\d{2,4}",date)

            if not date_list:
                raise ValueError("le tableau ne contient aucune date")

        except:
            return False
    
        return True
    
    def get_values(tablist):
        datas = map(lambda data: data.value, tablist)

        datas = list(datas)

        return datas

    # 
    workbook = xlrd.open_workbook(filename)

    # sheets
    sheets = workbook.sheets()

    metadatas = list()

    for sheet in sheets:
        for row in sheet.get_rows():
            if is_matchs_datas(row):
                # serialisation des donnees
                row = get_values(row)

                # ajout
                metadatas.append(row)
    
    return metadatas
            
        


def pdf_process(filename:str, is_betfile=True):
    metadata = extract_datas(filename)

    metadata = extract_metadatas(metadata, is_betfile=is_betfile)

    print(metadata[0:2])

# test
filename = "C:\\Users\\RMB PC\\Downloads\\long.xlsx"
pdf_process(filename)