
import numpy as np
import pandas as pd


def singleton(classe:object):
    """
        Decorateur permettant d'avoir une classe singleton
        {une classe ayant qu'une seule instance}
    """
    instances = {}

    def manage(*arg, **kwargs):
        if classe not in instances:
            instances[classe] = classe(*arg, **kwargs)
        
        return instances[classe]
    
    return manage

def pd_init_index(df_index):
    """
        cette function renvoit les indices d'initialisations d'un data_frame

        :param df_index: pd.index like list

        :return: np.array
    """
    return np.arange(len(df_index))

def pd_unique_cols(datas_df:pd.DataFrame):
    """
        permet d filtre les colonnes d'un DataFrame 
        en eliminant les doublons

        :return: pd.DataFrame
    """
    # colonnes uniques
    selected_cols = []

    # nouvelles colonnes
    new_cols = []

    # nombre de doublons
    count_cols = {}

    # existe de doublons
    double_cols = list(set(datas_df)) != list(datas_df.columns)
    
    if double_cols:
        for cols in datas_df.columns:
            if cols not in new_cols:
                new_cols.append(cols)
                # add unique copy
                selected_cols.append(cols)
                count_cols[cols] = 1
            else:
                # add all others copy
                cols_add = cols + str(count_cols[cols])
                new_cols.append(cols_add)
                count_cols[cols] += 1
        
        datas_df.columns = new_cols

        return datas_df[selected_cols]

    return datas_df

