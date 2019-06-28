#-*-coding:utf-8 -*-

from . import interfacedb

#---------------------------------------------------------------------------
#    TICKET CONFIGURATION
#---------------------------------------------------------------------------

CONST_TICKET_MATCH_MIN = 3   # nombre minimal
CONST_TICKET_MATCH_MAX = 12  # nombre maximal

BET_MONEY_MIN = 300 # montant minimal

DEFAULT_MARGIN_TIME = 10 # temps de tolerance (minutes)

PROBABILITY_COL = "probability"

PREDICTION_COL = interfacedb.modelTables.prediction.PREDICTION_SUFFIX

COTE_COL = interfacedb.modelTables.matchs.FEATURE_PREFIX

ID_TICKET_COL = interfacedb.modelTables.ticket.idticket

DEFAULT_NUMLIST = 77

MATCH_NODE = "matchs"
