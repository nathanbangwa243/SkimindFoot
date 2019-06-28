
# tools
import collections

# skimind.gFunctions
from . import gFunctions

# skimind.config
from . import skiconfig

# container
import collections


#---------------------------------------------------------------------------
#    TABLE MATCHS
#---------------------------------------------------------------------------

@gFunctions.singleton
class Matchs:
    # table name {database}
    TABLE_NAME = "MATCHS"

    # feature prefix
    FEATURE_PREFIX = 'cote'

    def __init__(self):
        # database columns
        self.numlist = "numlist" 
        self.idmatch = "idmatch" 
        self.date = "date" 
        self.time = "time" 
        self.competition = "competition" 
        self.home = "home" 
        self.classhome = "classhome" 
        self.classvisitor = "classvisitor" 
        self.visitor = "visitor"
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        all_columns = [
                        *self.__dict__.values(),
                        *map(self.format_cote, range(1, 31))
        ]

        return all_columns
    
    def get_primary_key(self):
        """
            Clé primaire de la table
        """
        primary_key = [self.numlist, self.idmatch, self.date]

        return primary_key

    def format_cote(self, idcote:int):
        """
            Formate le nom d'un champ
        """

        if not(idcote > 0 and idcote <= 30):
            raise ValueError("la cote va de 1 a 30")
        
        return self.FEATURE_PREFIX + str(idcote)
    
    def get_features(self):
        """
            Retourne les colonnes realisatrices de taches
        """
        # realizable task features
        idfeatures = []

        for task in skiconfig.tasks_target:
            idfeatures += list(skiconfig.COTES_TARGET_DF.loc[task, :])
        
        # columns
        features = map(self.format_cote, idfeatures)

        features = list(features)

        return features
    
    def get_betid_from(self, task_name, class_id):
        """
            permet de traduire une classe en id pour le pari

            :param task_name: str
                le nom de la tache
            :param class_id: int
                l'id de la classe parmi les classes de la tache
                0 : cross
                1 : first
                3 : second
            :return: int
                1 - 30
        """
        class_id = int(class_id)
        class_name = skiconfig._targets[class_id]

        bet_id = skiconfig.COTES_TARGET_DF.loc[task_name, class_name]

        return bet_id
    
    

#---------------------------------------------------------------------------
#    TABLE DATASETS
#---------------------------------------------------------------------------

@gFunctions.singleton
class Datasets:
    # table name {database}
    TABLE_NAME = "DATASETS"

    def __init__(self):
        # matchs table
        matchs = Matchs()

        # database columns 
        self.numlist = matchs.numlist 
        self.idmatch = matchs.idmatch 
        self.date = matchs.date
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        
        return self.__dict__.values()


#---------------------------------------------------------------------------
#    TABLE PREDICTION
#---------------------------------------------------------------------------

@gFunctions.singleton
class Prediction:
    # table name
    TABLE_NAME = "PREDICTION"

    # prediction suffix
    PREDICTION_SUFFIX = 'predict'

    def __init__(self):
        # matchs table
        matchs = Matchs()

        # database columns 
        self.numlist = matchs.numlist 
        self.idmatch = matchs.idmatch 
        self.date = matchs.date
        self.normal_cross = "normal_cross" 
        self.normal_first = "normal_first" 
        self.normal_second = "normal_second" 
        self.normal_predict = "normal_predict" 
        self.first_mt_cross = "first_mt_cross" 
        self.first_mt_first = "first_mt_first" 
        self.first_mt_second = "first_mt_second" 
        self.first_mt_predict = "first_mt_predict" 
        self.second_mt_cross = "second_mt_cross" 
        self.second_mt_first = "second_mt_first" 
        self.second_mt_second = "second_mt_second" 
        self.second_mt_predict = "second_mt_predict" 
        self.mt_more_goal_cross = "mt_more_goal_cross" 
        self.mt_more_goal_first = "mt_more_goal_first" 
        self.mt_more_goal_second = "mt_more_goal_second" 
        self.mt_more_goal_predict = "mt_more_goal_predict" 
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        
        return self.__dict__.values()
    
    
    def get_predict_task_col(self, task_name:str):
        """
            rencoit la colonne prediction d'une tache
        """

        assert task_name in skiconfig.tasks_target

        # task name to lower case
        prediction_column = task_name.lower() + f"_{self.PREDICTION_SUFFIX}"

        return prediction_column
    
    @ staticmethod
    def get_class_name(bet_id):
        """
            renvoi le nom de la classe

            :param bet_id: int
                le numero du pari ex : 3
            :return: str
                la nature du pari ex: CROSS
        """

        for class_name in skiconfig.COTES_TARGET_DF.columns:
            if bet_id in skiconfig.COTES_TARGET_DF[class_name]:
                return class_name
    
    
    @staticmethod
    def get_task_probabilities_cols(task_name):
        """
            renvoit les colonnes probabilities d'une tache
        """

        task_name = task_name.lower()

        columns = map(lambda class_name: task_name + f"_{class_name.lower()}", skiconfig._targets)

        return list(columns)
    


            

#---------------------------------------------------------------------------
#    TABLE RESULTAT
#---------------------------------------------------------------------------

#@gFunctions.singleton : because besoin d'acceder a Resultat.TASK_TARGET
class Resultat:
    # table name
    TABLE_NAME = "RESULTAT"

    TASK_TAGET = {
        skiconfig.all_tasks.NORMAL         : "normalresult",
        skiconfig.all_tasks.HANDICAP01     : "handicap01_result",
        skiconfig.all_tasks.HANDICAP10     : "handicap10_result",
        skiconfig.all_tasks.FIRST_MT       : "first_mt_result",   # win before    45'
        skiconfig.all_tasks.SECOND_MT      : "second_mt_result",   # win after     45'
        skiconfig.all_tasks.MT_MORE_GOAL   : "mt_more_goal",    # mi-temps avec le plus de buts
    }

    CLASS_IDS = collections.namedtuple("CLASS_IDS", field_names=skiconfig._targets)
    CLASS_IDS = CLASS_IDS(*range(len(skiconfig._targets))) 

    def __init__(self):
        # matchs table
        matchs = Matchs()

        # database columns 
        self.numlist = matchs.numlist 
        self.idmatch = matchs.idmatch 
        self.date = matchs.date
        self.normal_home = "normal_home" 
        self.normal_visitor = "normal_visitor" 
        self.normalresult = Resultat.TASK_TAGET[skiconfig.all_tasks.NORMAL] 
        self.handicap01_home = "handicap01_home" 
        self.handicap01_visitor = "handicap01_visitor" 
        self.handicap01_result = Resultat.TASK_TAGET[skiconfig.all_tasks.HANDICAP01]
        self.handicap10_home = "handicap10_home" 
        self.handicap10_visitor = "handicap10_visitor" 
        self.handicap10_result = Resultat.TASK_TAGET[skiconfig.all_tasks.HANDICAP10]
        self.first_mt_home = "first_mt_home" 
        self.first_mt_visitor = "first_mt_visitor" 
        self.first_mt_result = Resultat.TASK_TAGET[skiconfig.all_tasks.FIRST_MT] 
        self.second_mt_home = "second_mt_home" 
        self.second_mt_visitor = "second_mt_visitor" 
        self.second_mt_result = Resultat.TASK_TAGET[skiconfig.all_tasks.SECOND_MT]
        self.wire15result = "wire15result" 
        self.wire25result = "wire25result" 
        self.wire35result = "wire35result" 
        self.first_mt_goal = "first_mt_goal" 
        self.second_mt_goal = "second_mt_goal" 
        self.mt_more_goal = Resultat.TASK_TAGET[skiconfig.all_tasks.MT_MORE_GOAL] 
        self.parity = "parity" 
        self.teamallgoal = "teamallgoal" 
        self.egality = "egality"
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """

        return self.__dict__.values()
    
    def get_labels_cols(self):
        """
            Return The labels columns
        """

        labels_columns = [
                            self.normalresult, 
                            self.first_mt_result,
                            self.second_mt_result,
                            self.mt_more_goal
                        ]
        return labels_columns

#---------------------------------------------------------------------------
#    TABLE TICKET
#---------------------------------------------------------------------------

@gFunctions.singleton
class Ticket:
    # table name
    TABLE_NAME = "TICKET"

    DEFAULT_MATCH_STATUS = 2 # pas encore commencé

    def __init__(self):
        # matchs table
        matchs = Matchs()
        # database columns
        self.idticket = "idticket"
        self.numlist = matchs.numlist 
        self.idmatch = matchs.idmatch 
        self.date = matchs.date
        self.predict = "predict"
        self.match_status = "match_status"# etat du match 
                                            # 0 : perdant                                # 1 : 
                                            # 1 : gagnant
                                            # 2 : pas encore commencé
                                            # 3 : en cours
                                            # 4 : terminé
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        
        return self.__dict__.values()
    
    
#---------------------------------------------------------------------------
#    TABLE TICKET_STATUS
#---------------------------------------------------------------------------

@gFunctions.singleton
class TicketStatus:
    # table name
    TABLE_NAME = "TICKET_STATUS" 

    DEFAULT_STATUS = 2 # pas encore commencé

    def __init__(self):
        # database columns
        self.idticket = "idticket" 
        self.uid = "uid" 
        self.date_begin = "date_begin" 
        self.time_begin = "time_begin" 
        self.date_close = "date_close" 
        self.time_close = "time_close" 
        self.cote = "cote" 
        self.probability = "probability" 
        self.status = "status" # etat du ticket 
                                # 0 : perdant                                # 1 : 
                                # 1 : gagnant
                                # 2 : pas encore commencé
                                # 3 : en cours
                                # 4 : terminé
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        
        return self.__dict__.values()

#---------------------------------------------------------------------------
#    TABLE USER_TICKET
#---------------------------------------------------------------------------

@gFunctions.singleton
class UserTicket:
    # table name
    TABLE_NAME = "USER_TICKET" 
    DEFAULE_NB_COPY = 1

    def __init__(self):
        # database columns
        self.uid = "uid" 
        self.idticket = "idticket" 
        self.bet_money = "bet_money" 
        self.win_money = "win_money"
        self.nb_copy = "nb_copy"
    
    def get_all_cols(self):
        """
            Return toutes les colonnes
        """
        
        return self.__dict__.values()

#---------------------------------------------------------------------------
#    MODEL TABLES OBJECTS
#---------------------------------------------------------------------------

datasets = Datasets()
matchs = Matchs()
prediction = Prediction()
resultat = Resultat()
ticket = Ticket()
ticketStatus = TicketStatus()
user_ticket = UserTicket()