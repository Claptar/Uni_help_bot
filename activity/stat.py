import psycopg2 as pg
import pandas.io.sql as psql
from datetime import datetime
import pandas as pd
import os

DBNAME = os.environ['DATABASE']
USER = os.environ['USER']
PASS = os.environ['PASS']
HOST = os.environ['HOST']


def uniqe_users_per_day(day):
    """
    Функция возвращает количество уникальных пользователей за день (сегодняшний или вчерашний)
    :return:
    """
    connection = pg.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASS}")
    dataframe = psql.read_sql('SELECT * FROM actions', connection)
    if day == 'За сегодня':
        today = dataframe[dataframe['date_time'].dt.date == datetime.now().date()]
        return today['user_id'].unique().size
    elif day == 'За вчера':
        yesterday = dataframe[dataframe['date_time'].dt.date == (datetime.now() - pd.Timedelta(days=1)).date()]
        return yesterday['user_id'].unique().size
