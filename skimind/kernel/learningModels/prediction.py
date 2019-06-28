#-*-coding: utf-8 -*-


# tools
import pandas as pd

import numpy as np

import tensorflow as tf

# training and evaluation
from . import trainEval
from . import trainModel

# preprocessing
from . import preprocessing

# interfacedb
from . import interfacedb

# config
from . import config

# global config
from . import skiconfig


class SkiPrediction:
    def __init__(self, *args, **kwargs):
        self.list_predictions = list()
    
    def add_predictions(self, predictions, task_target):
        """
            ajoute les predictions au data frame

            :param predictions: list
                                la liste des predictions -> contain dict
            
            :param task_target: str
                                l'id de la tache a realiser
            
            :action impact: self.predictions 
        """

        # les classes possibles pour la tache task_target
        colums = [[] for _ in range(len(skiconfig.targets))]

        # best class columns
        colums.append([])

        for pred_dict in predictions:
            # add best class
            colums[-1].append(pred_dict[config.TF_CLASS_IDS_KEY][0])

            # class probabilities
            for index, prob in enumerate(pred_dict[config.TF_PROBABILITIES_KEY]):
                prob = np.around(prob * 100, 1)
                colums[index].append(prob)
            
        
        for index, cols in enumerate(colums):
            # add colums to the dataframe : predictions
            self.predictions[f"{task_target}{index}"] = cols
    
    
    def start(self, data_df):
        print("start prediction")
        # predictions request object 
        request_prediction = preprocessing.FilterDataFrame(data_df)

        # init dataframe with matchs infos
        self.predictions = data_df[interfacedb.modelTables.matchs.get_primary_key()]


        # shuffle constant

        for task in skiconfig.tasks_target:
                
            # data -> [feutures_inputs, labels] -> prediction
            features, _ = request_prediction.get_datas(task_target=task, select_label=False)

            # builder
            neural_network = trainModel.build_model(task_target=task)

            if not neural_network:
                return False

            # predictions : geneartor
            predictions = neural_network.predict(input_fn=lambda:trainEval.eval_input_fn(train_X=features, train_Y=None, 
                                                                                        batch_size=config.CONST_BATCH_SIZE
                                                                                    )
                                                )

            # add prediction
            predictions = list(predictions)

            self.add_predictions(predictions=predictions, task_target=task)
            
        return True
    
