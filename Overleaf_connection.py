# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import typewrite
from pyautogui import hotkey
import time


def unpack_document(text_file):
    """
    Функция читает текстовый файл
    :param text_file: текстовый файл
    :return:текст файла
    """
    file = open(text_file, 'r')
    file_lines = file.read()
    return file_lines


def ol_open(text_file, email, password):
    """
    Функция открывает Overleaf, вводит логин и пароль, нажимает кнопку входа
    :return:
    """
    driver = webdriver.Chrome('/home/makyaro/.local/bin/chromedriver')  # Открываем браузер
    driver.get("http://www.overleaf.com/login")  # Открываем Overleaf

    email_box = driver.find_element_by_name('email')  # Ищем окно для ввода email
    email_box.send_keys(email)  # Вводим email

    password_box = driver.find_element_by_name('password')  # Ищем окно для ввода пароля
    password_box.send_keys(password)  # Вводим пароль

    login_button = driver.find_element_by_css_selector('div.actions')  # Ищем кнопку инициализации
    login_button.click()  # Нажимаем на кнопку

    new_project_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    'div.dropdown')))  # Ищем кнопку для создания нового проекта
    new_project_button.click()  # Нажимаем на кнопку и создаем проект

    project_type = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                            '/html/body/ul/li[1]/a')))  # Выбираем тип создаваемого проекта
    project_type.click()  # Создаем проект

    name_blank = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                    '/html/body/div[5]/div/div/div[2]/form/input')))  # Ищем поле для ввода названия проекта
    name_blank.send_keys('Name')  # Вводим название проекта

    create_project_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                '/html/body/div[5]/div/div/div[3]/button[2]')))  # Ищем кнопку для создания проекта
    create_project_button.click()  # Нажимаем на кнопку и создаем проект

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                '//*[@id="editor"]/div/div[2]')))
    time.sleep(1)  # Ожидание загрузки страницы
    hotkey('ctrl', 'a', 'delete')  # Удаление текста на странице
    time.sleep(1)
    text_list = unpack_document(text_file)  # Считывание файла
    time.sleep(1)
    typewrite(text_list)  # Печать исходного кода страницы

    time.sleep(10)  # Время для просмотра


#ol_open('0l_start_text.txt')

