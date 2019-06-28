#-*-coding: utf-8 -*-

# interfacedb
from . import interfacedb

# gFunctions
from . import gFunctions

# tools
import pandas as pd
import numpy as np

# config
from . import config



def get_ticket_columns():
    columns = [
        *interfacedb.modelTables.matchs.get_primary_key(),
        interfacedb.modelTables.matchs.time,
        interfacedb.modelTables.matchs.home,
        interfacedb.modelTables.matchs.visitor,
    ]
    
    return columns

def get_datas(task_list:list, margin_time:int):
    """
    """

    datas_df = interfacedb.modelRequest.get_prediction_datas()

    # colonnes predictions des taches selectionnnées
    predictions_columns = map(interfacedb.modelTables.prediction.get_predict_task_col, task_list)
    predictions_columns = list(predictions_columns)

    def transforme_class_to_betid():
        """
            transforme les classe en bet_id
        """
        nonlocal datas_df
        nonlocal predictions_columns

        for index_task, pred_cols in enumerate(predictions_columns):
            # task name
            task_name = task_list[index_task]

            datas_df[pred_cols] = [interfacedb.modelTables.matchs.get_betid_from(task_name, class_id) 
                                        for class_id in datas_df[pred_cols]]            



    def filter_best_prediction():
        """

        """
        nonlocal datas_df
        nonlocal predictions_columns

        def get_probabilities_cols():
            columns = []

            for task_name in task_list:
                columns += interfacedb.modelTables.prediction.get_task_probabilities_cols(task_name)
            
            return columns

        probabilities_columns = get_probabilities_cols()

        target_datas = {
            config.COTE_COL: [],
            config.PROBABILITY_COL: [],
            config.PREDICTION_COL: []
        }

        for index in datas_df.index:
            # les probabilities
            probabilities = datas_df.loc[index, probabilities_columns]
            probabilities = list(probabilities.values)
            
            # meilleur probability
            best_probability = max(probabilities)

            # task probabilities column
            index_prob = probabilities.index(best_probability)

            task_prob_name = probabilities_columns[index_prob]

            # task name
            task_names = filter(lambda task: task.lower() in task_prob_name, task_list)
            task_names = list(task_names)
            best_task_name = task_names[0]

            # best prediction
            best_pred_cols = interfacedb.modelTables.prediction.get_predict_task_col(best_task_name)
            best_prediction = datas_df.loc[index, best_pred_cols]

            # best cote
            cote_cols = interfacedb.modelTables.matchs.format_cote(best_prediction)

            best_cote = datas_df.loc[index, cote_cols]

            # add datas
            target_datas[config.COTE_COL].append(best_cote)
            target_datas[config.PROBABILITY_COL].append(best_probability)
            target_datas[config.PREDICTION_COL].append(best_prediction)
        
        # ticket columns
        ticket_columns = get_ticket_columns()

        # donnees importantes
        datas_df = datas_df[ticket_columns]

        # add cote prediction probability columns
        datas_df[config.COTE_COL] = target_datas[config.COTE_COL]
        datas_df[config.PREDICTION_COL] = target_datas[config.PREDICTION_COL]
        datas_df[config.PROBABILITY_COL] = target_datas[config.PROBABILITY_COL]


    transforme_class_to_betid()
    filter_best_prediction()
    
    return datas_df


