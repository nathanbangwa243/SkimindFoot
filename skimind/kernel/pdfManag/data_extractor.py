import tabula

# warning : from . import tools
from . import tools

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

def extract_datas(filename):
    def arange_values(cotes_tab):
        cotes_list = copy.deepcopy(cotes_tab)

        # transformation en lower
        cotes_list = map(lambda cote: str(cote).lower(), cotes_list)
        cotes_list = list(cotes_list)

        # transformation en string
        cotes_string = " ".join(cotes_list)

        # double space exclued
        cotes_string = cotes_string.replace("  ", " ")

        # separation des cotes
        cotes_list = cotes_string.split(" ")

        # exclusion des valeurs 'nan'
        cotes_list = filter(lambda cote: cote != 'nan', cotes_list)
        cotes_list = list(cotes_list)

        return cotes_list

    meta_df = tabula.read_pdf(filename, pages='all')

    metadatas = list()

    for tab_list in meta_df.values:
        tab_list = list(tab_list)
        
        if tools.is_matchs_datas(tab_list):
            cotes = tab_list[8:]

            cotes = arange_values(cotes)

            print(len(cotes))

            tab_list = [*tab_list[:8], *cotes]

            metadatas.append(tab_list)
    return metadatas

def pdf_data_process(filename:str, is_betfile=True):
    metadata = extract_datas(filename)

    metadata = extract_metadatas(metadata, is_betfile=is_betfile)

    return metadata
    
