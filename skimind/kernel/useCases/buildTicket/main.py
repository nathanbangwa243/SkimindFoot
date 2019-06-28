#-*-coding: utf-8 -*-

# config
from . import config

# interfacedb
from .import interfacedb

# dataFilter
from . import dataFilter

# global config
from . import skiconfig

# gFunctions
from . import gFunctions

# tools
import pandas as pd
import numpy as np


class BuildTicket(object):
    def __init__(self, bet_money, win_money, *args, **kwargs):
        self.bet_money = bet_money
        self.win_money = win_money

        self.meta_data = pd.DataFrame()
    
    def save_ticket(self, idticket, bet_money=None, uid=interfacedb.config.DEFAULT_UID):
        """
            Permet de sauvegarder un Ticket

            :idticket: int
                le numero du ticket
        """

        assert list(self.meta_data.values) != None

        if not bet_money:
            bet_money = self.bet_money
        
        # requete a la database
        requestObject = interfacedb.config.request_object


        def save_as_user_ticket(uid):
            nonlocal bet_money
            nonlocal data_ticket_df
            nonlocal idticket

            userTicket = interfacedb.modelTables.user_ticket

            global_cote = data_ticket_df[config.COTE_COL].product()

            # montant à gagner
            win_money = int(global_cote * bet_money)


            data_to_push = {
                userTicket.uid: [uid],
                userTicket.idticket: [idticket],
                userTicket.bet_money: [bet_money],
                userTicket.win_money: [win_money],
                userTicket.nb_copy : [userTicket.DEFAULE_NB_COPY],
            }

            data_to_push = pd.DataFrame(data_to_push)
            columns_order = userTicket.get_all_cols()

            data_to_push = list(data_to_push.loc[0, columns_order])

            # push
            requestObject.save_user_ticket(data_to_push)


        def save_as_ticket_status(uid):
            nonlocal data_ticket_df
            nonlocal idticket

            ticketStatus = interfacedb.modelTables.ticketStatus

            date_column = interfacedb.modelTables.matchs.date
            time_column = interfacedb.modelTables.matchs.time

            all_date = data_ticket_df[date_column]
            all_time = data_ticket_df[time_column]

            cote = data_ticket_df[config.COTE_COL].product()
            cote = round(cote, 2)

            probability = data_ticket_df[config.PROBABILITY_COL].mean()
            probability = round(probability, 2)
            

            data_to_push = {
                ticketStatus.idticket: [idticket],
                ticketStatus.uid: [uid],
                ticketStatus.date_begin: [all_date.min()],
                ticketStatus.time_begin: [all_time.min()],
                ticketStatus.date_close: [all_date.max()],
                ticketStatus.time_close: [all_time.max()],
                ticketStatus.cote: [cote],
                ticketStatus.probability: [probability],
                ticketStatus.status: [ticketStatus.DEFAULT_STATUS]
            }

            data_to_push = pd.DataFrame(data_to_push)

            
            columns_order = ticketStatus.get_all_cols()

            data_to_push = data_to_push.loc[0, columns_order]

            data_to_push = list(data_to_push)
            
            requestObject.save_ticket_status(data_to_push)


        # Global Ticket Datas
        filter_vector = self.meta_data[config.ID_TICKET_COL] == idticket

        data_ticket_df = self.meta_data[filter_vector]

        # ticket columns & datas for table TICKET
        columns = interfacedb.modelTables.ticket.get_all_cols()
        data_push_df = data_ticket_df.loc[:, columns]

        # Ticket Saving
        for tab_list in list(data_push_df.values):
            # save data
            requestObject.save_ticket(tab_list)
        
        save_as_ticket_status(uid)
        save_as_user_ticket(uid)
    
    def get_bet_columns(self):
        modelTables = interfacedb.modelTables
        selected_column = [
            modelTables.matchs.idmatch,
            #modelTables.matchs.date,
            #modelTables.matchs.time,
            modelTables.matchs.home,
            modelTables.matchs.visitor,
            modelTables.matchs.FEATURE_PREFIX, #cote
            modelTables.prediction.PREDICTION_SUFFIX, #predict
            #config.PROBABILITY_COL,
        ]

        return selected_column

    
    def data_to_display(self):
        """
            :return: dict
                    {
                        idticket:{
                            numlist_col: numlist,
                            config.PROBABILITY_COL: global_probability,
                            modelTables.user_ticket.bet_money: self.bet_money,
                            modelTables.user_ticket.win_money: win_money,
                            config.MATCH_NODE:
                            [
                                get_bet_columns()
                            ]
                        }
                    }
        """

        if not list(self.meta_data.values):
            self.find_tickets()

        response = dict()

        modelTables = interfacedb.modelTables

        numlist_col = modelTables.matchs.numlist

        
        
        selected_columns = self.get_bet_columns()

        for idticket in self.meta_data[config.ID_TICKET_COL].values:

            selected_vector = self.meta_data[config.ID_TICKET_COL] == idticket
            sub_datas_df = self.meta_data[selected_vector]


            numlist = list(sub_datas_df[numlist_col].values)[0]

            global_probability = sub_datas_df[config.PROBABILITY_COL].apply(float).mean()
            global_probability = round(global_probability, 3)

            global_cote = sub_datas_df[config.COTE_COL].apply(float).product()
            global_cote = round(global_cote, 3)

            win_money = int(global_cote * self.bet_money)

            matchs_list = sub_datas_df[selected_columns].values

            # init node
            response[idticket] = {
                numlist_col: numlist,
                config.PROBABILITY_COL: global_probability,
                modelTables.user_ticket.bet_money: self.bet_money,
                modelTables.user_ticket.win_money: win_money,
                config.MATCH_NODE: matchs_list
            }

        return response

    def find_tickets(self, task_list=[], margin_time=5, check_numlist=True):
        if not task_list: # all tasks
            task_list = list(skiconfig.tasks_target)

        datas_df = dataFilter.get_datas(task_list, margin_time)

        # add idticket column
        datas_df[config.ID_TICKET_COL] = 0

        # add match_status column
        datas_df[interfacedb.modelTables.ticket.match_status] = interfacedb.modelTables.ticket.DEFAULT_MATCH_STATUS

        # numlist col
        numlist_col = interfacedb.modelTables.matchs.numlist

        # idmatch cols
        idmatch_col = interfacedb.modelTables.matchs.idmatch

        # idticket
        current_idTicket = 1234

        def track_all_tickets(sub_datas_df):
            nonlocal datas_df
            nonlocal current_idTicket

            # this numlist
            numlist = sub_datas_df[numlist_col][0]

            # global filter : vector
            numlist_vector = datas_df[numlist_col] == numlist
            numlist_vector = list(numlist_vector)

            def choose_matchs():
                """
                    Permet de trouver les meilleurs matchs
                    pouvant constituer un ticket

                    :return: list
                        la liste des idmatch choisis
                """

                nonlocal sub_datas_df

                cote_global = 1
                idmatch_selected = []

                idmatch_col = interfacedb.modelTables.matchs.idmatch

                for index in sub_datas_df.index:
                    # montant atteint et on a au moins le nombre requis des matchs
                    if not(cote_global * self.bet_money < self.win_money) and len(idmatch_selected) >= config.CONST_TICKET_MATCH_MIN:
                        break
                    
                    if len(idmatch_selected) == config.CONST_TICKET_MATCH_MAX:
                        break
                    
                    match_cote = sub_datas_df.loc[index, interfacedb.modelTables.matchs.FEATURE_PREFIX]
                    match_cote = float(match_cote)
                    if match_cote > 1:
                        # add matchs
                        idmatch = sub_datas_df.loc[index, idmatch_col]
                        idmatch_selected.append(idmatch)

                        cote_global *= match_cote
                
                return idmatch_selected



            while len(sub_datas_df.values) >= config.CONST_TICKET_MATCH_MIN:
                list_idmatchs = choose_matchs()

                idmatch_vector = map(lambda idmatch: idmatch in list_idmatchs, datas_df[idmatch_col])
                idmatch_vector = list(idmatch_vector)

                selected_vector = np.logical_and(numlist_vector, idmatch_vector)

                datas_df.loc[selected_vector, config.ID_TICKET_COL] = current_idTicket

                current_idTicket += 1

                # deleted 
                idmatch_vector = map(lambda idmatch: False if idmatch in list_idmatchs else True, sub_datas_df[idmatch_col])
                
                idmatch_vector = list(idmatch_vector)

                sub_datas_df = sub_datas_df[idmatch_vector]



        # numlist list
        all_numlist = datas_df[numlist_col]
        all_numlist = set(all_numlist)
        
        response = list()

        if check_numlist:
            for numlist in all_numlist:
                # select data where numlist == numlist and drop numlist columns
                vector_selected = datas_df[numlist_col] == numlist
                df_temp = datas_df[vector_selected]

                # sort unascending
                df_temp = df_temp.sort_values(by=config.PROBABILITY_COL, ascending=False)

                track_all_tickets(df_temp)
            
        else:
            datas_df[numlist_col] = config.DEFAULT_NUMLIST
            # sort unascending
            df_temp = datas_df.sort_values(by=config.PROBABILITY_COL, ascending=False)
            track_all_tickets(df_temp)

        
        self.meta_data = datas_df

        return self.data_to_display()
        
    
