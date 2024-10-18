from flask import Blueprint, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .logger import logger


bp = Blueprint('selenium', __name__)


class SeleniumRunner:
    def __init__(self):
        """Инициализация SeleniumRunner и настройка опций для драйвера."""
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Настройка драйвера Chrome с необходимыми параметрами."""
        chrome_options = Options()
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def open_page(self, url):
        """Открытие страницы по заданному URL."""
        try:
            self.driver.get(url)
            logger.info(f"Открыта страница: {url}")
        except Exception as e:
            logger.error(f"Ошибка при открытии страницы: {str(e)}")
            raise

    def click_element(self, xpath):
        """Клик по элементу, найденному по XPath."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            logger.info(f"Клик по элементу: {xpath}")
        except Exception as e:
            logger.error(f"Ошибка при клике по элементу {xpath}: {str(e)}")
            raise

    def get_code_text(self, element_id):
        """Получение текста из элемента <code> по его ID."""
        try:
            code_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            code_text = code_element.text
            logger.info(f"Текст из элемента {element_id} успешно получен")
            return code_text
        except Exception as e:
            logger.error(f"Ошибка при получении текста из элемента {element_id}: {str(e)}")
            raise

    def save_to_file(self, text, file_path):
        """Сохранение текста в файл."""
        try:
            with open(file_path, "w") as file:
                file.write(text)
            logger.info(f"Текст успешно сохранен в файл: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении в файл {file_path}: {str(e)}")
            raise

    def quit_driver(self):
        """Закрытие драйвера."""
        if self.driver:
            self.driver.quit()
            logger.info("Драйвер успешно закрыт")

    def run(self):
        """Основной метод выполнения скрипта Selenium."""
        try:
            # Открытие страницы
            self.open_page("https://green-api.com/docs/")

            # Переходы по вкладкам
            self.click_element('//label[@for="__nav_2_3"]')  # Документация API
            time.sleep(2)
            self.click_element('//label[@for="__nav_2_3_3"]')  # Отправка
            time.sleep(2)
            self.click_element('//a[@href="api/sending/SendMessage/"]')  # Отправить текст
            time.sleep(2)

            # Получение текста из элемента <code> и сохранение его в файл
            code_text = self.get_code_text('__code_6')
            self.save_to_file(code_text, "code_content.txt")

            return jsonify({"message": "Selenium-скрипт успешно выполнен!"}), 200
        except Exception as e:
            logger.exception("Ошибка при выполнении Selenium скрипта")
            return jsonify({"error": str(e)}), 500
        finally:
            self.quit_driver()

