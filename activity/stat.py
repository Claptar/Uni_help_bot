import psycopg2 as pg
import pandas.io.sql as psql
from datetime import datetime
import pandas as pd
import os

DBNAME = os.environ['DATABASE']
USER = os.environ['USER']
PASS = os.environ['PASS']
HOST = os.environ['HOST']


def activity_data():
    """
    Функция возвращает dataframe с активностью пользователей
    :return:
    """
    connection = pg.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASS}")
    return psql.read_sql('SELECT * FROM actions', connection)


def uniqe_users(time):
    """
    Функция возвращает количество уникальных пользователей за день (сегодняшний или вчерашний)
    :return:
    """
    connection = pg.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASS}")
    dataframe = activity_data()
    if time == 'За сегодня':
        today = dataframe[dataframe['date_time'].dt.date == datetime.now().date()]
        return today['user_id'].unique().size
    elif time == 'За вчера':
        yesterday = dataframe[dataframe['date_time'].dt.date == (datetime.now() - pd.Timedelta(days=1)).date()]
        return yesterday['user_id'].unique().size
    elif time == 'За неделю':
        week = dataframe[dataframe['date_time'].dt.date > (datetime.now() - pd.Timedelta(days=7)).date()]
        return week['user_id'].unique().size


def frequency_of_use():
    """
    Функция возращает Series файл с частотой использования функций
    :return:
    """
    dataframe = activity_data()
    week = dataframe[dataframe['date_time'] > (datetime.now() - pd.Timedelta(days=7))]
    frequency = week['command_name'].value_counts()
    return str(frequency).split('\n')[:-1:]
