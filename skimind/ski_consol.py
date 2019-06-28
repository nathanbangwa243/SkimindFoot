# skimind kernel
import kernel

# os
import os

# scientifical tools
import pandas as pd

# global config
from kernel import config as skiconfig


#---------------------------------------------------------------------------
#    TICKET BUILDER
#---------------------------------------------------------------------------
import sqlite3

class DataBaseConnector:
    database = os.path.join(
                kernel.config.KERNEL_PATH, 
                "interfacdedb")
    database = os.path.join(database, "skimind.db")

    def __init__(self):
        self.connexion = sqlite3.connect(self.database)
        self.cursor = self.connexion.cursor()

    def close(self):
        self.cursor.close()
        self.connexion.close()
    

#db_obj = DataBaseConnector()

#---------------------------------------------------------------------------
#    SQLALCHEMY
#---------------------------------------------------------------------------
import sqlalchemy as db
from kernel.interfacedb import modelTables

database = os.path.join(
                skiconfig.KERNEL_PATH, 
                "interfacedb")
                
database = os.path.join(database, "skimind.db")

engine = db.create_engine(f"sqlite:///{database}")

connection = engine.connect()

metadata = db.MetaData()

# TABLES

table_datasets = db.Table(modelTables.datasets.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_matchs = db.Table(modelTables.matchs.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_prediction = db.Table(modelTables.prediction.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_resultat = db.Table(modelTables.resultat.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_ticket = db.Table(modelTables.ticket.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_ticketstatus = db.Table(modelTables.ticketStatus.TABLE_NAME, metadata, autoload=True, autoload_with=engine)
table_userticket = db.Table(modelTables.user_ticket.TABLE_NAME, metadata, autoload=True, autoload_with=engine)

#---------------------------------------------------------------------------
#    INTERFACEDB REQUEST
#---------------------------------------------------------------------------

# READ
def get_training_datas():
    table_matchs_nid = db.select(
                            [table_matchs.columns.numlist, 
                            table_matchs.columns.idmatch, 
                            table_matchs.columns.date]
                            )
    table_datasets_nid = db.select(
                            [table_datasets.columns.numlist, 
                            table_datasets.columns.idmatch, 
                            table_datasets.columns.date]
                            )
    match_except_datasets = table_matchs_nid.except_(table_datasets_nid)

    numlist_in_match_except_datasets = table_matchs.columns.numlist.in_(db.select([match_except_datasets.columns.numlist]))
    
    idmatch_in_match_except_datasets = table_matchs.columns.idmatch.in_(db.select([match_except_datasets.columns.idmatch]))
    
    date_in_match_except_datasets = table_matchs.columns.date.in_(db.select([match_except_datasets.columns.date]))
    

    condition = db.and_(
                    numlist_in_match_except_datasets,
                    idmatch_in_match_except_datasets,
                    date_in_match_except_datasets,
                    table_matchs.columns.numlist == table_datasets.columns.numlist,
                    table_matchs.columns.idmatch == table_datasets.columns.idmatch,
                    table_matchs.columns.date == table_datasets.columns.date
                    )

    query = db.select([table_matchs, table_resultat])
    
    query = query.where(condition)
    
    result_proxy = connection.execute(db.select([table_matchs]))

    
    datas = result_proxy.fetchall()

    return datas

def get_data_to_predict(date):
    #query  = ifacedb.get_data_to_predict_sql(date)
    table_matchs_nid = db.select(
                            [table_matchs.columns.numlist, 
                            table_matchs.columns.idmatch, 
                            table_matchs.columns.date]
                            )
    table_prediction_nid = db.select(
                            [table_prediction.columns.numlist, 
                            table_prediction.columns.idmatch, 
                            table_prediction.columns.date]
                            )
    match_except_prediction = table_matchs_nid.except_(table_prediction_nid)

    numlist_in_match_except_prediction = table_matchs.columns.numlist.in_(db.select([match_except_prediction.columns.numlist]))
    
    idmatch_in_match_except_prediction = table_matchs.columns.idmatch.in_(db.select([match_except_prediction.columns.idmatch]))
    
    date_in_match_except_prediction = table_matchs.columns.date.in_(db.select([match_except_prediction.columns.date]))
    

    condition = db.and_(
                    numlist_in_match_except_prediction,
                    idmatch_in_match_except_prediction,
                    date_in_match_except_prediction,
                    table_matchs.columns.date >= date
                    )

    query = db.select([table_matchs])
    
    query = query.where(condition)
    
    result_proxy = connection.execute(match_except_prediction)

    
    datas = result_proxy.fetchall()

    return datas

def get_prediction_datas(date):
    #query  = ifacedb.get_predictions_sql(date)
    query = db.select([table_matchs, table_prediction])
    condition = db.and_(
                    table_matchs.columns.numlist == table_prediction.columns.numlist,
                    table_matchs.columns.idmatch == table_prediction.columns.idmatch,
                    table_matchs.columns.date == table_prediction.columns.date,
                    table_prediction.columns.date >= date
                    )
    query = query.where(condition)
    
    result_proxy = connection.execute(query)

    
    datas = result_proxy.fetchall()

    return datas

# INSERT
def save_prediction(datas):
    print(f"insert prediction done : {len(datas)}")
    query = db.insert(table_prediction, values=datas)
    result_proxy = connection.execute(query)

def save_datasets(datas):
    print(f"datasets save done : {len(datas)}")
    query = db.insert(table_datasets, values=datas)
    result_proxy = connection.execute(query)

def save_ticket(datas):
    print(f"ticket infos save done : {datas}")
    query = db.insert(table_ticket, values=datas)
    result_proxy = connection.execute(query)

def save_ticket_status(datas):
    print(f"ticket status save done : {datas}")
    query = db.insert(table_ticketstatus, values=datas)
    result_proxy = connection.execute(query)

def save_user_ticket(datas):
    print(f"user ticket save done : {datas}")
    query = db.insert(table_userticket, values=datas)
    result_proxy = connection.execute(query)

def save_matchs(datas):
    print("datas matchs saves done : ", datas)
    query = db.insert(table_matchs, values=datas)
    result_proxy = connection.execute(query)

def save_resultat(datas):
    print("datas resultat saves done : ", datas)
    query = db.insert(table_resultat, values=datas)
    result_proxy = connection.execute(query)

# DELETE
def clean_datasets():
    query = "DELETE FROM DATASETS"
    query = db.delete(table_datasets)
    result_proxy = connection.execute(query)


#---------------------------------------------------------------------------
#    INTERFACEDB REQUEST CONFIGURATION
#---------------------------------------------------------------------------
from kernel.interfacedb import config as ifdb_conf

# DATASETS
ifdb_conf.request_object.get_training_datas = get_training_datas
ifdb_conf.request_object.save_datasets = save_datasets

# DATAS PREDICTION
ifdb_conf.request_object.get_data_to_predict = get_data_to_predict
ifdb_conf.request_object.save_prediction  = save_prediction

ifdb_conf.request_object.get_prediction_datas = get_prediction_datas

# ticket
ifdb_conf.request_object.save_ticket = save_ticket
ifdb_conf.request_object.save_user_ticket = save_user_ticket
ifdb_conf.request_object.save_ticket_status = save_ticket_status

# clean datasets
ifdb_conf.request_object.clean_datasets = clean_datasets
#print(ifdb_conf.request_object.get_prediction_datas().shape)

# save matchs
ifdb_conf.request_object.save_matchs = save_matchs
ifdb_conf.request_object.save_resultat = save_resultat


#---------------------------------------------------------------------------
#    TICKET BUILDER
#---------------------------------------------------------------------------
def display_ticket(bet_money, win_money):
    from kernel.useCases.buildTicket import main as build_ticket

    builder = build_ticket.BuildTicket(
        bet_money=bet_money, win_money=win_money
        ) 
    tickets = builder.data_to_display()

    columns = builder.get_bet_columns()

    for ticket, dict_datas in tickets.items():
        head_msg = (f"\nTicket {ticket} "
                    f"numlist : {dict_datas['numlist']} "
                    f"probability : {dict_datas['probability']}%\n"
                    f"bet money : {dict_datas['bet_money']}FC "
                    f"win money : {dict_datas['win_money']}FC\n"
                    )

        print(head_msg)
        
        matchs_df = dict_datas['matchs']

        index = map(lambda ind: f"{ind+1}e PARI", range(len(matchs_df)))

        matchs_df = pd.DataFrame(matchs_df, columns=columns, index=index)

        print(matchs_df, '\n')

    
    

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-a", 
                        "--action",
                        help="use case",
                        dest="action",
                        type=str,
                        default="buildticket"
                        )

    #---------------------------------------------------------------------------
    #    TICKET BUILDER options
    #---------------------------------------------------------------------------

    parser.add_option("-m", 
                        "--betmoney",
                        help="bet money",
                        dest="bet_money",
                        type=int,
                        default=300)

    parser.add_option("-w", 
                        "--winmoney",
                        help="win money money",
                        dest="win_money",
                        type=int,
                        default=5000)

    parser.add_option("-c", 
                        "--checknumlist",
                        help="boolean check numlist",
                        dest="check_numlist",
                        type=int,
                        default=True
                        )
    #---------------------------------------------------------------------------
    #    OPTOPARSE MANAGEMENT
    #---------------------------------------------------------------------------
    import collections

    options, args = parser.parse_args()
    
    usecases_list = [
                        "buildticket"
                    ]
    
    actions = collections.namedtuple("Action", 
                        field_names=usecases_list)
    actions = actions(*usecases_list)


    if options.action not in usecases_list:
        parser.print_help()
    
    if options.action == actions.buildticket:
        pass
        display_ticket(bet_money=options.bet_money,win_money=options.win_money)


#---------------------------------------------------------------------------
#    CLOSE DATABASE CONNEXION
#---------------------------------------------------------------------------
