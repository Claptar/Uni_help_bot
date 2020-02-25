import psycopg2
import pandas as pd
import os

USER = os.environ['USER']
PASS = os.environ['PASS']
HOST = os.environ['TABLE_HOST']
DATABASE = os.environ['DATABASE']


def insert_data(chat_id, group_num, course):
    global USER, HOST, DATABASE, PASS
    """
    В таблицу с названием CHEL6I добавляются данные пользователя
    :param chat_id: id чата бота с пользователем
    :param group_num: номер учебной группы пользователя
    :param course: номер курса пользователя
    :return:
    """
    con = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASS,
        host=HOST,
        port="5432")
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO CHEL6I (CHAT_ID, GROUP_NUM, COURSE) VALUES ({chat_id}, '{group_num}', {course})"
    )
    con.commit()
    con.close()


def read_data():
    """
    Возвращает pandas dataframe с данными всех пользователей
    :return:
    """
    global USER, HOST, DATABASE, PASS
    con = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASS,
        host=HOST,
        port="5432")
    cursor = con.cursor()
    data = pd.read_sql("SELECT * FROM CHEL6I", con, index_col=0)
    con.close()
    return data


def update_course(chat_id, course):
    """
    Обновляет курс пользователя, по его chat_id
    :param chat_id: id чата бота с пользователем
    :param course:  новый номер курса пользователя
    :return:
    """
    global USER, HOST, DATABASE, PASS
    con = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASS,
        host=HOST,
        port="5432")
    cur = con.cursor()
    cur.execute(f"UPDATE CHEL6I set COURSE = {course} where CHAT_ID = {chat_id}")
    con.commit()
    con.close()


def update_group_num(chat_id, group_num):
    """
    Обновляет курс пользователя, по его chat_id
    :param chat_id: id чата бота с пользователем
    :param group_num: новый номер группы пользователя
    :return:
    """
    global USER, HOST, DATABASE, PASS
    con = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASS,
        host=HOST,
        port="5432")
    cur = con.cursor()
    cur.execute(f"UPDATE CHEL6I set GROUP_NUM = '{group_num}' where CHAT_ID = {chat_id}")
    con.commit()
    con.close()


def create_table():
    """
    Создает таблицу с название CHEL6I
    :return:
    """
    global USER, HOST, DATABASE, PASS
    con = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASS,
        host=HOST,
        port="5432")
    cur = con.cursor()
    cur.execute('''CREATE TABLE CHEL6I  
         (CHAT_ID INT PRIMARY KEY NOT NULL,
         GROUP_NUM TEXT NOT NULL,
         COURSE INT);''')
    con.commit()
    con.close()
