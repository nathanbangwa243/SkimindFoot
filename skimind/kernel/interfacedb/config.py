#-*-coding: utf-8 -*-


"""
    Configuration des requetes
"""

# gFunction tools
from . import gFunctions



TEST_DATE = "25-10-2018" # WARNING

#---------------------------------------------------------------------------
#    JOUEUR PAR DEFAUT
#---------------------------------------------------------------------------

DEFAULT_UID = "skimindAI"

#---------------------------------------------------------------------------
#    CLASSE SINGLETON CONTENANT LES REQUETES (MODEL)
#---------------------------------------------------------------------------

@gFunctions.singleton
class SqlRequestFunctions(object):
    def __init__(self, *args, **kwargs):
        #---------------------------------------------------------------------------
        #    DESCRIPTION : get_training_datas
        # RETOURNE TOUTES LES DONNEES DE LA TABLE MATCHS ET DE LA TABLE RESULTAT
        # ET NE FIGURANT PAS ENCORE DANS LA TABLE DATASETS
        # 
        # RESUME : RETOURNE LES DONNEES NON ENCORE APPRISES PAR LE MODEL
        #---------------------------------------------------------------------------
        
        self.get_training_datas = lambda:object # last : learning.get_data_allschema : False
        
        #---------------------------------------------------------------------------
        #    DESCRIPTION : get_data_to_predict
        # RETOURNE TOUTES LES DONNEES DE LA TABLE MATCHS SUPERIEURE OU EGALE A UNE DATE
        # ET NE FIGURANT PAS ENCORE DANS LA TABLE PREDICTION
        #
        # RESUME : RETOURNE LES DONNEES A PREDIRE
        #---------------------------------------------------------------------------
    
        self.get_data_to_predict = lambda date : object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : get_prediction_datas
        # RETOURNE TOUTES LES DONNEES DE LA TABLE MATCHS ET DE LA TABLE PREDICTION
        # SUPERIEURS OU EGALES A UNE DATE
        #---------------------------------------------------------------------------
    
        self.get_prediction_datas = lambda date : object # last : learning.get_data_allschema : False
        
        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_prediction
        # PERMET DE SAUVEGARDER (AJOUTER) UN ENREGISTREMENT DANS LA TABLE PREDICTION
        #---------------------------------------------------------------------------
        self.save_prediction = lambda datas: object
    
        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_datasets
        # PERMET DE SAUVEGARDER (AJOUTER) UN ENREGISTREMENT DANS LA TABLE DATASEST
        #---------------------------------------------------------------------------
        self.save_datasets = lambda datas: object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_ticket
        #---------------------------------------------------------------------------
        self.save_ticket = lambda datas: object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_user_ticket
        #---------------------------------------------------------------------------
        self.save_user_ticket = lambda datas: object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_ticket_status
        #---------------------------------------------------------------------------
        self.save_ticket_status = lambda datas: object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : clean_datasets
        # permet de supprimer tous les enregistrements de la table DATASETS
        #---------------------------------------------------------------------------
        self.clean_datasets = lambda:None

        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_matchs
        # PERMET DE SAUVEGARDER (AJOUTER) UN ENREGISTREMENT DANS LA TABLE MATCH
        #---------------------------------------------------------------------------
        self.save_matchs = lambda datas: object

        #---------------------------------------------------------------------------
        #    DESCRIPTION : save_resultat
        # PERMET DE SAUVEGARDER (AJOUTER) UN ENREGISTREMENT DANS LA TABLE RESULTAT
        #---------------------------------------------------------------------------
        self.save_resultat = lambda datas: object

        
        
# contient des methodes d'acces aux donnees
request_object = SqlRequestFunctions()