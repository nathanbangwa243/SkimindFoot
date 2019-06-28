# interface_db
from . import interfacedb

# os
import os
import shutil

# config
from . import config

from . import skiconfig

#---------------------------------------------------------------------------
#    REINITIALISATION
#---------------------------------------------------------------------------
def reboot_checkpoint():
    """
        S'il y a eu changement de configuration du reseau de neurone
        on refait l'entrainnement avec une nouvelle configuration
        tout en sauvegardant l'ancienne configuration
        on vide aussi la table DATASETS pour permettre l'entrainnement
        sur toutes les donnees disponibles.
    """
    # on sauvegarde les anciens checkpoints
    def backup_checkpoint():
        """
            Permet de faire un backup des checkpoint
        """
        # checkpoint folder tracking : exclude backup folder
        call_fn = (lambda folder: folder != config.BACKUP_CHECKPOINT)
        checkpoint_list = filter(call_fn, os.listdir(skiconfig.PATH_MODEL_FOLDER))

        # checkpoint folder path
        call_fn = (lambda folder: os.path.join(skiconfig.PATH_MODEL_FOLDER, folder))
        checkpoint_list = map(call_fn, checkpoint_list)

        # make backup folder if not exist
        if not os.path.exists(config.PATH_BACKUP_CHEKPOINT):
            os.makedirs(config.PATH_BACKUP_CHEKPOINT)
        

        # last backup
        list_backup = os.listdir(config.PATH_BACKUP_CHEKPOINT)
        last_backup = 0

        if list_backup:
            last_backup = list_backup[-1]

        # new backup
        new_backup_folder = int(last_backup) + 1
        new_backup_folder = str(new_backup_folder)
        new_backup_folder = os.path.join(config.PATH_BACKUP_CHEKPOINT, new_backup_folder)

        # make new backup folder
        os.mkdir(new_backup_folder)

        # move to backup
        for ck_folder in checkpoint_list:
            if os.path.isdir(ck_folder):
                shutil.move(ck_folder, new_backup_folder)
    try:
        # backup
        backup_checkpoint()
        
        # on vide la table datasets
        interfacedb.config.request_object.clean_datasets()
        
    except Exception as error:
        print("Error : ", error)
        return False 

    return True

#---------------------------------------------------------------------------
#    RESTORATION
#---------------------------------------------------------------------------
def restore_checkpoint():
    """
        Permet de restorer un checkpoint
    """
    pass