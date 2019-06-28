#-*-coding: utf-8 -*-

""""""

# global config
from .. import config as skiconfig

# global config
from ..interfacedb import fields as iface_db_fields



def class_to_betid(task_target, class_target):
    """
        permet de traduire la classe en idbet afin de faciliter le pari

        :param task_target: str
                            le nom (id) de la tache a realiser
        :param class_target: int
                            la classe fournit par le dnn
        
        :return: int
    """
    # COTES_TARGET : dict
    return skiconfig.COTES_TARGET[task_target][class_target]

def betid_to_class_name(betid):
    """
        transforme un betid en class name

        :param betid: int

        :return: str
                ex: betid = 23, return 'SECOND'
    """
    
    if betid in skiconfig.CLASS_FIELD_TARGET[skiconfig.CROSS]:
        return skiconfig.CROSS
    
    elif betid in skiconfig.CLASS_FIELD_TARGET[skiconfig.FIRST]:
        return skiconfig.FIRST

    elif betid in skiconfig.CLASS_FIELD_TARGET[skiconfig.SECOND]:
        return skiconfig.SECOND


def task_to_dbfield(task_target):
    """
        permet de traduire le nom d'une tache en un champ correspondant de la table prediction

        :param task_target: str
                        le nom de la tache a realiser
    """

    return task_target.replace('-', '_').lower()


def task_to_predict_cols(task_target):
    """
        permet de formater le nom de la colonne predition d'une tache

        :param task_target: str
                        le nom de la tache

                        ex : normal_predict
    """

    return f"{task_to_dbfield(task_target)}_{iface_db_fields.PREDICT_SUFFIX}"

