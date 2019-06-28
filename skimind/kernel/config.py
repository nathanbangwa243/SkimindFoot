#-*-coding:utf-8 -*-


# collections
import collections

# tools
import pandas as pd

# os
import os



#---------------------------------------------------------------------------
#    CHECKPOINT FOLDER : LE DOSSIER D'ENREGISTREMENT DES CONFIGURATIONS DU DNN
#---------------------------------------------------------------------------
ENV_VAR = "SKI_KERNEL"

KERNEL_PATH = os.environ.get(ENV_VAR)

KERNEL_PATH = str(KERNEL_PATH)

if not(os.path.isdir(KERNEL_PATH)):
    message = (f"la variable d'environnement '{ENV_VAR}' contenant le path vers le kernel "
                "n'existe pas ou ne contient pas une valeur valide")
    raise ValueError(message)

PATH_MODEL_FOLDER = os.path.join(KERNEL_PATH, "checkPoint")

#---------------------------------------------------------------------------
#    ALL TASKS CONFIGURATION : Taches a realiser
#---------------------------------------------------------------------------

_tasks  = [
                "NORMAL",
                "HANDICAP01",
                "HANDICAP10",
                "FIRST_MT",
                "SECOND_MT",
                "MT_MORE_GOAL",
]

# object Task
all_tasks = collections.namedtuple(typename="Task", field_names=_tasks)(*_tasks)

#---------------------------------------------------------------------------
#    TASKS CONFIGURATION : Taches a realiser
#---------------------------------------------------------------------------

_tasks_target  = [
                all_tasks.NORMAL,
                all_tasks.FIRST_MT,
                all_tasks.SECOND_MT,
                all_tasks.MT_MORE_GOAL,
]

# object Task
tasks_target = collections.namedtuple(typename="Task", field_names=_tasks_target)(*_tasks_target)

#---------------------------------------------------------------------------
#    CLASSES POSSIBLE PAR TACHE
#---------------------------------------------------------------------------

_targets = [
                "CROSS",
                "FIRST",
                "SECOND"
]

targets = collections.namedtuple(typename="Target", field_names=_targets)(*_targets)

#---------------------------------------------------------------------------
#    BET IDS SELON CHAQUE CLASSE DE CHAQUE TACHE
#---------------------------------------------------------------------------

COTES_TARGET_DF = [
    # [cross, first, second][0, 1, 2]
    [3, 1, 2],      # normal
    [6, 4, 5],      # handicap01
    [9, 7, 8],      # handicap10
    [12, 10, 11],   # first_mt
    [15, 13, 14],   # second_mt
    [24, 22, 23]    # mt_more_goal
]

COTES_TARGET_DF = pd.DataFrame(
                                COTES_TARGET_DF, 
                                columns=_targets,
                                index=_tasks
                                )