#-*-conding: utf-8 -*-

""""""

# tools
import pandas as pd



def now():
    """
        acces a l'heure et a la date actuelle

        :return: str
                'date time'
    """

    

    response = pd.datetime.today()

    response = f'{response.day}-{response.month}-{response.year} {response.hour}:{response.minute}'
    
    # WARNING : trouver une fonction qui ffait ca mieux
    response = '25-10-2018 10:10'

    return response

def now_date():
    """"""
    # today
    date = pd.to_datetime(now(), format='%d-%m-%Y')

    return f'{date.day}-{date.month}-{date.year}'


def add_margin_time(date_time, margin_time):
    """
        ajout d'une marge a une heure

        :param date_time: str 
        :param margin_time: int
                                {minutes}
        :return: pd.to_datetime
    """
    print(f"date time jhgfdsghfvdjhf : {date_time}")
    # date_time
    date_time = pd.to_datetime(date_time)

    # add margin time
    minute = date_time.minute + margin_time

    date_time = pd.to_datetime(f'{date_time.day}-{date_time.month}-{date_time.year} {date_time.hour}:{minute}')

    return date_time