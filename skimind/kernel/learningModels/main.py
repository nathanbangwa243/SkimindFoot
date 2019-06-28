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

# config
from . import config

# checkpoint manager
from . import ckpt_manager


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

        response = ski_prediction.start(data_df=datas)

        if not response:
            return response

        save_prediction(ski_prediction.predictions)
    
    return True


#---------------------------------------------------------------------------
#    VERIFIE LES PREDICTIONS ET ENTRAINE LE MODEL SI NECESSAIRE
#---------------------------------------------------------------------------

def verify_prediction_and_trainmodel():
    
    if config.config_changed():
        reboot_status = ckpt_manager.reboot_checkpoint()

        if reboot_status:
            config.save_config()
        else:
            return "Erreur : ckpt_manager"

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
        response = trainModel.train_model_if_possible(datas)

        if not response:
            verify_prediction_and_trainmodel()

        save_datasets(datas_for_datasets)
    
    prediction_saved = find_prediction()

    if not prediction_saved:
        verify_prediction_and_trainmodel()



