#-*-coding:utf-8 -*-


# tensorflow
import tensorflow as tf

# scientifical tools
import numpy as np

import pandas as pd

# interfacedb
from ..interfacedb import modelTables

#---------------------------------------------------------------------------
#    PREPARATION DES ENTREES DU DEEP NEURAL NETWORK
#---------------------------------------------------------------------------
FEATURES_LIST = modelTables.matchs.get_features()

FEATURES_COLS_NORMALIZE = map(tf.feature_column.numeric_column, 
                            FEATURES_LIST
                            )
FEATURES_COLS_NORMALIZE = list(FEATURES_COLS_NORMALIZE)

print(f"FEATURES_LIST {FEATURES_LIST}")

#---------------------------------------------------------------------------
#    PREPARATION DES DONNEES
#---------------------------------------------------------------------------

class FilterDataFrame:
    def __init__(self, data_df, *args, **kwargs):
        self.data_df = data_df
        print(data_df.columns)
    
    def get_datas(self, task_target, select_label=True):
        print(self.data_df[['numlist', 'idmatch', 'date', 'cote1', 'home']])
        features = map(lambda feature_name: (feature_name, np.array(self.data_df[feature_name], dtype=float)), FEATURES_LIST)

        features = dict(features)

        labels = []

        if select_label:
            labels = np.array(self.data_df[modelTables.resultat.TASK_TAGET[task_target]], dtype=int)

        return (features, labels)
