from flask import Blueprint
from .controllers import WhatsAppController
from .selenium_controller import run_selenium  # Импортируем функцию run_selenium


bp = Blueprint('main', __name__)

# Метод предназначен для получения файла code_context(с кодом) с помощью selenium
bp.add_url_rule('/run-selenium', 'run_selenium', run_selenium, methods=['GET'])

# Метод предназначен для получения текущих настроек аккаунта.
bp.add_url_rule('/getSettings', 'get_settings', WhatsAppController.get_settings, methods=['GET'])

# Метод предназначен для отправки текстового сообщения в личный или групповой чат.
bp.add_url_rule('/sendMessage', 'send_message', WhatsAppController.send_message, methods=['POST'])

# Метод предназначен для отправки файла, загружаемого по ссылке.
bp.add_url_rule('/sendFileByUrl', 'send_file_by_url', WhatsAppController.send_file_by_url, methods=['POST'])

# Получение входящих уведомлений
bp.add_url_rule('/receiveIncomingNotifications', 'receive_incoming_notifications',
                WhatsAppController.receive_incoming_notifications, methods=['POST'])

# Получение всех клиентов
bp.add_url_rule('/clients', 'get_clients', WhatsAppController.get_clients, methods=['GET'])

# Получение всех уведомлений
bp.add_url_rule('/notifications', 'get_notifications', WhatsAppController.get_notifications, methods=['GET'])

# Удаление уведомления
bp.add_url_rule('/deleteNotification', 'delete_notification',
                WhatsAppController.delete_notification, methods=['DELETE'])

