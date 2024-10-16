from flask import Blueprint, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

bp = Blueprint('selenium', __name__)


def run_selenium():
    try:
        chrome_options = Options()
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chrome_options.add_argument("--start-maximized")  # Открыть окно в максимальном размере
        # chrome_options.add_argument("--headless")  # Закомментируйте для отладки
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")  # Отключение GPU
        chrome_options.add_argument("--remote-debugging-port=9222")  # Удаленное отладочное подключение

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get("https://green-api.com/docs/")

        # Ожидание для "Документация API"
        documentation_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[@for="__nav_2_3"]'))
        )
        documentation_tab.click()

        time.sleep(2)

        # Ожидание для "Отправка"
        send_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[@for="__nav_2_3_3"]'))
        )
        send_tab.click()

        time.sleep(2)

        # Ожидание и клик по тексту "Отправить текст"
        send_message_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="api/sending/SendMessage/"]'))
        )
        send_message_link.click()

        time.sleep(2)

        # Найти элемент <code> и скопировать его содержимое
        code_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, '__code_6'))
        )
        code_text = code_element.text  # Получаем текст из элемента <code>

        # Сохранить текст в .txt файле
        with open("code_content.txt", "w") as file:
            file.write(code_text)

        driver.quit()

        return jsonify({"message": "Selenium script executed successfully!"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
