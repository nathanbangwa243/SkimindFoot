#-*-coding: utf-8 -*-


# skimind.config
from . import skiconfig

# os
import os

# files
import json

#---------------------------------------------------------------------------
#    Checkpoint backup
#---------------------------------------------------------------------------
BACKUP_CHECKPOINT = "BACKUP"
PATH_BACKUP_CHEKPOINT = os.path.join(skiconfig.PATH_MODEL_FOLDER, BACKUP_CHECKPOINT)

#---------------------------------------------------------------------------
#    DEEP NEURAL NETWORK CONFIGURATION
#---------------------------------------------------------------------------
CONFIG_FILE = os.path.join(skiconfig.PATH_MODEL_FOLDER,"config.json")

LAYERS = 50  # nombre de neurones par couche
NEURAL = 20  # nombre de couches cachées 

NB_CLASSES = 3 # nombre de classe

HIDDEN_LAYERS = [NEURAL for _ in range(LAYERS)]

CONST_BATCH_SIZE = 100

CONST_TRAINING_STEEP = 1000


#---------------------------------------------------------------------------
#    DEEP NEURAL NETWORK CONFIGURATION
#---------------------------------------------------------------------------

TF_PROBABILITIES_KEY = "probabilities"
TF_CLASS_IDS_KEY     = "class_ids"


#----------------------------------------------------------------------------
# SAVE CONFIG
#----------------------------------------------------------------------------
def save_config():
    datas = {
        "LAYERS": LAYERS,
        "NEURAL": NEURAL
    }

    with open(CONFIG_FILE, 'w') as fp:
        try:
            datas = json.dumps(datas)
            fp.write(datas)
        except Exception:
            return False
    
    return True

def config_changed():
    # create file if does not exist
    if not os.path.exists(CONFIG_FILE):
        save_config()

    # save config
    with open(CONFIG_FILE, 'r') as fp:
        try:
            datas = json.load(fp)
        except Exception:
            return False

    datas = dict(datas)

    if datas["LAYERS"] == LAYERS and datas['NEURAL'] == NEURAL:
        return False
    
    else:
        return True

    