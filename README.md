# WhatsApp Automation with Flask and Selenium

## Описание

Этот проект представляет собой API на Flask, который использует Selenium для автоматизации взаимодействия с веб-страницей [Green API](https://green-api.com/docs/). С помощью данного API вы можете отправлять сообщения, управлять уведомлениями и взаимодействовать с документацией API через веб-интерфейс.

## Установка

### Предварительные требования

- Убедитесь, что у вас установлен [Python 3.7 или выше](https://www.python.org/downloads/).
- Установите [Google Chrome](https://www.google.com/chrome/) на ваш компьютер.
- Убедитесь, что у вас установлен [ChromeDriver](https://sites.google.com/chromium.org/driver/) соответствующей версии Google Chrome.
- Установите [PostgreSQL](https://www.postgresql.org/download/) и создайте базу данных.

### Клонирование репозитория


### Настройка переменных окружения
# Конфигурация для Green API
GREEN_API_URL=https://7103.api.greenapi.com

# Конфигурация базы данных PostgreSQL
DB_NAME=название_базы_данных
HOST=localhost
USER=пользователь
PORT=5432
PASSWORD=ваш_пароль


```bash
git clone https://github.com/yourusername/WhatsAppAutomation.git
cd WhatsAppAutomation

Установка зависимостей
Создайте виртуальное окружение и активируйте его:

python -m venv venv
source venv/bin/activate  # На Linux или Mac
# venv\Scripts\activate  # На Windows

Установите необходимые пакеты:

pip install -r requirements.txt
```

### Настройка базы данных

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


### Установка дополнительных зависимостей для Selenium
```bash
pip install webdriver-manager
```
### Запуск проекта
```bash
flask run
```


Примеры запросов в Postman
1) GET /run-selenium

Метод: GET
URL: http://127.0.0.1:5000/run-selenium
Описание: Запускает Selenium скрипт, который открывает страницу Green API и выполняет автоматизацию.


2) POST /getSettings

Метод: POST
URL: http://127.0.0.1:5000/getSettings
Тело запроса (JSON):
```bash
{
  "idInstance": "ваш_id_instance",
  "apiTokenInstance": "ваш_api_token_instance"
}
```

3) POST /sendMessage

Метод: POST
URL: http://127.0.0.1:5000/sendMessage
Тело запроса (JSON):
```bash
{
  "idInstance": "ваш_id_instance",
  "apiTokenInstance": "ваш_api_token_instance",
  "phoneNumber": "ваш_номер_телефона",
  "message": "ваше сообщение"
}
```

4) POST /sendFileByUrl

Метод: POST
URL: http://127.0.0.1:5000/sendFileByUrl
Тело запроса (JSON):
```bash
{
  "idInstance": "ваш_id_instance",
  "apiTokenInstance": "ваш_api_token_instance",
  "phoneNumber": "ваш_номер_телефона",
  "fileUrl": "ссылка_на_файл"
}
```

5) DELETE /deleteNotification

Метод: DELETE
URL: http://127.0.0.1:5000/deleteNotification
Тело запроса (JSON):
```bash
{
  "idInstance": "ваш_id_instance",
  "apiTokenInstance": "ваш_api_token_instance",
  "receiptId": "id_уведомления"
}
```

Примечания
Убедитесь, что все необходимые зависимости установлены.
Если возникают проблемы с открытием браузера или взаимодействием с элементами, проверьте, установлены ли Chrome и ChromeDriver, и совпадают ли их версии.







