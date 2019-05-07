from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    time.sleep(3)  # Чуть-чуть подождем, чтобы не получить ошибку
    new_project_button = driver.find_element_by_css_selector('div.dropdown')  # Ищем кнопку создания нового проекта
    new_project_button.click()  # Нажимаем на кнопку и создаем проект
    time.sleep(3)  # Подождем, чтобы не получить ошибку
    project_type = driver.find_element_by_partial_link_text("Blank")  # Находим нужный вариант создания проекта
    project_type.click()  # Создаем проект
    time.sleep(4)  # Чуть-чуть подождем, чтобы избежать ошибки

ol_open()

