#-coding: utf-8 -*-


# tools
import pandas as pd
import numpy as np

# interfacedb
from . import interfacedb

# datetime
import datetime


class HomeView:
    DATE_TIME_COL = 'datetime'
    MATCH_STATUS = 'status' # etat du match
                            # started
                            # nostarted
    STARTED = 'STARTED'
    NOSTARTED = 'NOSTARTED'

    def __init__(self):
        # les metasdatas
        self.metadata = interfacedb.modelRequest.get_prediction_datas()
        
        matchs_table = interfacedb.modelTables.matchs

        def add_datetime_column():

            self.metadata[matchs_table.date] = pd.to_datetime(self.metadata[matchs_table.date])

            all_dates = self.metadata[matchs_table.date]
            all_times = self.metadata[matchs_table.time]

            all_dates = [str(date.date()) for date in all_dates]

            datetime_list = map(lambda date_time: pd.to_datetime(f"{date_time[0]} {date_time[1]}"), zip(all_dates, all_times))

            datetime_list = list(datetime_list)

            self.metadata[self.DATE_TIME_COL] = datetime_list

        
        add_datetime_column()

        # init status
        self.metadata[self.MATCH_STATUS] = self.NOSTARTED

        self.metadata = self.metadata[self.get_selected_columns()]
    
    def get_selected_columns(self):
        matchs_table = interfacedb.modelTables.matchs

        columns = [
            matchs_table.numlist,
            matchs_table.idmatch,
            self.DATE_TIME_COL,
            matchs_table.home,
            matchs_table.visitor,
        ]

        predictions_columns = interfacedb.modelTables.prediction.get_all_cols()

        filter_fn = (lambda column: column not in [*columns, matchs_table.date])

        predictions_columns = filter(filter_fn, predictions_columns)

        columns += [*predictions_columns, self.MATCH_STATUS]

        return columns

    
    def filter_datas(self, by_idmatch=True, by_datetime=False):

        matchs_table = interfacedb.modelTables.matchs
        
        def check_status():
            date_time = datetime.datetime.now()

            date_filter_vector = self.metadata[self.DATE_TIME_COL] >= date_time

            status = map(lambda boolean: self.NOSTARTED if boolean else self.STARTED, date_filter_vector)

            status = list(status)

            self.metadata[self.MATCH_STATUS] = status
            
        
        check_status()

        modelTables = interfacedb.modelTables

        numlist_col = modelTables.matchs.numlist

        # colonnes a afficher
        selected_columns = self.get_selected_columns()

        # delete numlist column
        selected_columns.remove(numlist_col)

        # response 
        response = dict()

        for numlist in self.metadata[numlist_col]:
            numlist_vector = self.metadata[numlist_col] == numlist

            sub_metadata = self.metadata[numlist_vector]

            sub_metadata = sub_metadata.loc[:, selected_columns]

            if by_idmatch:
                filter_colum = matchs_table.idmatch

            elif by_datetime:
                filter_colum = self.DATE_TIME_COL
            
            sub_metadata = sub_metadata.sort_values(by=filter_colum, ascending=True)

            response[numlist] = sub_metadata.values

        return response
        
