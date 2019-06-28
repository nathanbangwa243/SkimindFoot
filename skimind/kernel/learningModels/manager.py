#-*-coding: utf-8 -*-


from .prediction import SkiPrediction

# config
from ..interfacedb import modelRequest 
from .. import interfacedb

# tools
import pandas as pd

# gFunctions
from . import gFunctions

# train model
from . import trainModel

# datetime
import datetime


#---------------------------------------------------------------------------
#    EVALUATION DU MODEL
#---------------------------------------------------------------------------

def find_prediction():
    """
        Lance le processus d'evaluation (prediction)
    """

    datas = interfacedb.modelRequest.get_data_to_predict()

    def save_prediction(predictions_df):
        for enr in predictions_df.values:
            enr = list(enr)

            # 3nregistrement dans la data base
            interfacedb.config.request_object.save_prediction(enr)


    if list(datas.values):
        # deep neural network
        ski_prediction = SkiPrediction()

        ski_prediction.start(data_df=datas)

        save_prediction(ski_prediction.predictions)


#---------------------------------------------------------------------------
#    VERIFIE LES PREDICTIONS ET ENTRAINE LE MODEL SI NECESSAIRE
#---------------------------------------------------------------------------

def verify_prediction_and_trainmodel():
    print("sdbjhsbjhdsbfbfblbfdbfknlfkdjkfnkf", modelRequest)
    datas = interfacedb.modelRequest.get_training_datas()

    print(f"trainiing_datas : {datas.shape}")

    def save_datasets(dataset):
        for enr in dataset.values:
            enr = list(enr)

            # 3nregistrement dans la data base
            interfacedb.config.request_object.save_datasets(enr)

    if list(datas.values):
        datas_for_datasets = datas[interfacedb.modelTables.matchs.get_primary_key()]
        print(f"launch training model if possible : {len(datas)}")
        # model training
        trainModel.train_model_if_possible(datas)

        save_datasets(datas_for_datasets)
    
    find_prediction()



