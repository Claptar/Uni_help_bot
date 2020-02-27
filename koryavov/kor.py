import requests

SEM = 0
TASK = 0

def kor_page(sem_num, zad_num):
    url = f'https://mipt1.ru/1_2_3_4_5_kor.php?sem={sem_num}&zad={zad_num}'
    res = requests.get(url)
    res.encoding = 'cp1251'
    text = res.text
    z = f'Задача {zad_num} найдена в Корявове на странице'
    if z in text:
        return text[text.find(z):text.find(z) + len(z) + 5]
    elif 'Задача не найдена' in text:
        return 'Задача не найдена в Корявове!'
    elif "Укажите номер задачи корректно!":
        return "Укажите номер задачи корректно!"
