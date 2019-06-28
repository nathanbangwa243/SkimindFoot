#-*-coding: utf-8 -*-

# interfacedb config
from . import config

# model columns
from . import modelColumns

# gFunctions
from . import gFunctions

# data science tools
import pandas as pd
import numpy as np

# datetime
import datetime 



# contient des methodes d'acces aux donnees
model_request = config.SqlRequestFunctions()

#---------------------------------------------------------------------------
#    DATA SERIALIZATION : 
#---------------------------------------------------------------------------

def serialize_datas(model_cols_fn, datas:list):
    """
        retourne les donnees(colonnes) necessaire a la realisation d'une tache
    """
    # colonnes 
    all_cols, selected_cols = model_cols_fn()

    # selected_columns without redondance
    selected_cols = list(set(selected_cols))

    # datas to numpy array
    datas = np.array(datas)

    datas_df = pd.DataFrame(data=datas, columns=all_cols)

    # suppression de doublures
    datas_df = gFunctions.pd_unique_cols(datas_df)

    return datas_df[selected_cols]


#---------------------------------------------------------------------------
#    LEARNING MODEL
#---------------------------------------------------------------------------

def get_training_datas():
    """
        retourne les donnees d'entrainnement
    """
    # datas 
    datas_df = model_request.get_training_datas()

    # data serialization
    datas_df = serialize_datas(
        model_cols_fn=modelColumns.get_training_datas_cols,
        datas=datas_df)

    return datas_df

#---------------------------------------------------------------------------
#    MATCHS
#---------------------------------------------------------------------------

def get_data_to_predict():
    """
        retourne les donnees necessaire a la prediction
    """
    date = datetime.datetime.now()

    date = date.date()
    
    # WARNING : delete
    date = str(date)

    # datas 
    datas_df = model_request.get_data_to_predict(date)

    # data serialization
    datas_df = serialize_datas(
        model_cols_fn=modelColumns.get_data_to_predict_cols,
        datas=datas_df)

    return datas_df



#---------------------------------------------------------------------------
#    PREDICTIONS
#---------------------------------------------------------------------------
def get_prediction_datas(date=None):
    """
        retourne les donnees predictes
    """

    if not date:
        # on prend partant de la date actuelle
        #date = datetime.datetime.now()
        pass

    date = config.TEST_DATE

    # datas 
    datas_df = model_request.get_prediction_datas(date)

    # data serialization
    datas_df = serialize_datas(
        model_cols_fn=modelColumns.get_prediction_datas_cols,
        datas=datas_df)

    return datas_df





