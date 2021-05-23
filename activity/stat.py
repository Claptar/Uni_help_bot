import psycopg2 as pg
import pandas.io.sql as psql
from datetime import datetime
import pandas as pd
import os

DBNAME = os.environ["DATABASE"]
USER = os.environ["USER"]
PASS = os.environ["PASS"]
HOST = os.environ["HOST"]


def activity_data():
    """
    Функция возвращает dataframe с активностью пользователей
    :return:
    """
    connection = pg.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASS}")
    return psql.read_sql("SELECT * FROM actions", connection)


def get_user_list():
    """
    Функция возвращает список из chat_id всех пользователей
    :return: numpy array
    """
    connection = pg.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASS}")
    df = psql.read_sql('SELECT chat_id FROM "User"', connection)
    return df["chat_id"].values


def uniqe_users(time):
    """
    Функция возвращает количество уникальных пользователей за день (сегодняшний или вчерашний)
    :return:
    """
    dataframe = activity_data()
    if time == "За сегодня":
        today = dataframe[
            (dataframe["date_time"].dt.date == datetime.now().date())
            & (dataframe["user_id"] != 310115323)
            & (dataframe["user_id"] != 296254699)
        ]
        return today["user_id"].unique().size
    elif time == "За вчера":
        yesterday = dataframe[
            (
                dataframe["date_time"].dt.date
                == (datetime.now() - pd.Timedelta(days=1)).date()
            )
            & (dataframe["user_id"] != 310115323)
            & (dataframe["user_id"] != 296254699)
        ]
        return yesterday["user_id"].unique().size
    elif time == "За неделю":
        week = dataframe[
            (
                dataframe["date_time"].dt.date
                > (datetime.now() - pd.Timedelta(days=7)).date()
            )
            & (dataframe["user_id"] != 310115323)
            & (dataframe["user_id"] != 296254699)
        ]
        return week["user_id"].unique().size


def frequency_of_use():
    """
    Функция возращает Series файл с частотой использования функций
    :return:
    """
    dataframe = activity_data()
    week = dataframe[
        (dataframe["date_time"] > (datetime.now() - pd.Timedelta(days=7)))
        & (dataframe["user_id"] != 310115323)
        & (dataframe["user_id"] != 296254699)
    ]
    frequency = week["command_name"].value_counts()
    return str(frequency).split("\n")[:-1:]
