#-*-coding: utf-8 -*-

# database structure
from . import modelTables


#---------------------------------------------------------------------------
#    LEARNING MODEL
#---------------------------------------------------------------------------

def get_training_datas_cols():
    """
        retourne les colonnes des donnees d'entrainnement

        :return: tuple(all_cols, selected_cols)
            :all_cols: les colonnes retournees par le model
            :selected_cols: colonnes necessaires
            
    """
    # colonnes retournees par la requetes {model}
    # Toutes les colonnes de {MATCHS, RESULTAT}
    all_cols = [*modelTables.matchs.get_all_cols(), *modelTables.resultat.get_all_cols()]

    # colonnes necessaires a la realisation d'une taches
    selected_cols = [
                        *modelTables.matchs.get_all_cols(), 
                        *modelTables.resultat.get_labels_cols()
                    ]

    
    return all_cols, selected_cols

#---------------------------------------------------------------------------
#    MATCHS
#---------------------------------------------------------------------------

def get_data_to_predict_cols():
    """
        retourne les colonnes des donnees a predire

        :return: tuple(all_cols, selected_cols)
            :all_cols: les colonnes retournees par le model
            :selected_cols: colonnes necessaires
            
    """
    # colonnes retournees par la requetes {model}
    # Toutes les colonnes de {MATCHS, RESULTAT}
    all_cols = [*modelTables.matchs.get_all_cols()]

    # colonnes necessaires a la realisation d'une taches
    # toutes les colonnes de la table MATCHS
    selected_cols = all_cols

    
    return all_cols, selected_cols


#---------------------------------------------------------------------------
#    PREDICTION
#---------------------------------------------------------------------------

def get_prediction_datas_cols():
    """
        retourne les colonnes des donnees predites

        :return: tuple(all_cols, selected_cols)
            :all_cols: les colonnes retournees par le model
            :selected_cols: colonnes necessaires
            
    """
    # colonnes retournees par la requetes {model}
    # Toutes les colonnes de {MATCHS, RESULTAT}
    all_cols = [*modelTables.matchs.get_all_cols(), *modelTables.prediction.get_all_cols()]

    # colonnes necessaires a la realisation d'une taches
    selected_cols = all_cols

    
    return all_cols, selected_cols
