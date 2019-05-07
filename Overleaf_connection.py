from selenium import webdriver


def ol_open():
    """
    Функция открывает Overleaf, вводит логин и пароль, нажимает кнопку входа
    :return:
    """
    driver = webdriver.Chrome('/home/makyaro/.local/bin/chromedriver')
    driver.get("http://www.overleaf.com/login")
    email_box = driver.find_element_by_name('email')
    email_box.send_keys('klykin-2@yandex.ru')
    password_box = driver.find_element_by_name('password')
    password_box.send_keys('wallacedesouza8')
    login_button = driver.find_element_by_css_selector('div.actions')
    login_button.click()


ol_project_create()