from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import typewrite
from pyautogui import hotkey
import time


def ol_open():
    """
    Функция открывает Overleaf, вводит логин и пароль, нажимает кнопку входа
    :return:
    """
    driver = webdriver.Chrome('/home/makyaro/.local/bin/chromedriver')  # Открываем браузер
    driver.get("http://www.overleaf.com/login")  # Открываем Overleaf

    email_box = driver.find_element_by_name('email')  # Ищем окно для ввода email
    email_box.send_keys('klykin-2@yandex.ru')  # Вводим email

    password_box = driver.find_element_by_name('password')  # Ищем окно для ввода пароля
    password_box.send_keys('wallacedesouza8')  # Вводим пароль

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

    time.sleep(4)  # Подождем, чтобы страница успела загрузиться
    hotkey('ctrl', 'a')  # Выделим весь текст
    hotkey('delete')  # Удалим все
    typewrite('Hello world')  # Просто тест
    time.sleep(10)  # Время для просмотра


ol_open()

