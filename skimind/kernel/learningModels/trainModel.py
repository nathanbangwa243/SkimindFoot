#-*-coding: utf-8 -*-

# config
from . import config

# skimind.config
from .config import skiconfig

# preprocessing
from . import preprocessing

# tools
import tensorflow as tf
import pandas as pd

# system tools
import os

# train and prediction function (generator)
from . import trainEval

# interfacedb
from . import interfacedb

# checkpoint manager
from . import ckpt_manager

#eager execution
tf.enable_eager_execution()



#---------------------------------------------------------------------------
#    CONSTRUCTION DU DEEP NEURAL NETWORK
#---------------------------------------------------------------------------

def build_model(task_target):
    """
        construit un dnn selon les configurations propres a une tache

        :param task_target: str
                            le nom de la tache
        :param features_columns: list
                            types d'entree
                        
        :return: tf.estimator.DNNClassifier
    """

    #---------------------------------------------------------------------------
    #    CHECKPOINT DIRECTORY CONFIG
    #---------------------------------------------------------------------------

    model_dir = os.path.join(skiconfig.PATH_MODEL_FOLDER, task_target)

    
    if not os.path.exists(model_dir): # directory not exist
        os.makedirs(model_dir)  # create directory
   
    try:
        # builder
        neural_network = tf.estimator.DNNClassifier(feature_columns=preprocessing.FEATURES_COLS_NORMALIZE, # features types
                                                    hidden_units=config.HIDDEN_LAYERS,       # architecture
                                                    n_classes=config.NB_CLASSES, # classe
                                                    model_dir=model_dir
                                                    )
    except: # erreur de restoration du modele
        ckpt_manager.reboot_checkpoint()
        return None
    
    return neural_network

#---------------------------------------------------------------------------
#    ENTRAINNEMENT DU DEEP NEURAL NETWORK
#---------------------------------------------------------------------------

def train_model_if_possible(data_df:pd.DataFrame):
    """
        add knowledge to skimind
        :retrn: bool
    """

    if not list(data_df.values):
        # aucune nouvelle donnee a apprendre
        return True

    print(f"preprocessing build")
    # train (learning) request object
    request_train = preprocessing.FilterDataFrame(data_df)

    # shuffle constant
    CONST_BATCH_SIZE = data_df.shape[0] * 10

    for task in skiconfig.tasks_target:
        # data -> [[feautures_inputs, labels], features_columns]
        train_X, train_Y = request_train.get_datas(task_target=task, select_label=True)

        neural_network = build_model(task_target=task)

        # S'il ya eu reinitialisation des checkpoints
        if not neural_network:
            return False

        # training the neural_network
        neural_network = neural_network.train(input_fn=lambda:trainEval.train_input_fn(train_X=train_X, train_Y=train_Y, 
                                                                                    const_shuffle = CONST_BATCH_SIZE, 
                                                                                    batch_size=CONST_BATCH_SIZE), 
                                            steps=config.CONST_TRAINING_STEEP)
    
    return True