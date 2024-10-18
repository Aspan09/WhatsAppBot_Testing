from flask import Blueprint, jsonify, request
from .controllers import WhatsAppController
from .selenium_controller import SeleniumRunner
from .logger import logger


bp = Blueprint('main', __name__)


def create_controller():
    """Функция для создания экземпляра WhatsAppController из данных запроса."""
    try:
        controller = WhatsAppController.from_request()
        return controller
    except ValueError as e:
        logger.error(f"Ошибка при создании контроллера: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Ошибка при создании контроллера")
        return jsonify({"error": f"Внутренняя ошибка сервера: {e}"}), 500


# Метод для получения файла code_context с помощью selenium
@bp.route('/run-selenium', methods=['GET'])
def run_selenium_route():
    try:
        runner = SeleniumRunner()
        return runner.run()
    except Exception as e:
        logger.exception("Ошибка в run-selenium")
        return jsonify({"error": f"Не удалось выполнить Selenium-скрипт: {e}"}), 500


# Метод для получения текущих настроек аккаунта
@bp.route('/getSettings', methods=['POST'])
async def get_settings():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.get_settings()
            if response.status_code == 200:
                logger.info("Настройки успешно получены")
            else:
                logger.warning("Не удалось получить настройки")
            return response
        except Exception as e:
            logger.exception("Ошибка в getSettings")
            return jsonify({"error": f"Не удалось получить настройки: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Метод для отправки текстового сообщения
@bp.route('/sendMessage', methods=['POST'])
async def send_message_route():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response, status_code = await controller.send_message()
            if status_code == 200:
                logger.info("Сообщение успешно отправлено")
            else:
                logger.warning("Не удалось отправить сообщение")
            return jsonify(response), status_code
        except Exception as e:
            logger.exception("Ошибка в sendMessage")
            return jsonify({"error": f"Не удалось отправить сообщение: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Метод для отправки файла, загружаемого по ссылке
@bp.route('/sendFileByUrl', methods=['POST'])
async def send_file_by_url():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.send_file_by_url()
            return response
        except Exception as e:
            logger.exception("Ошибка в sendFileByUrl")
            return jsonify({"error": f"Не удалось отправить файл: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Получение входящих уведомлений
@bp.route('/receiveIncomingNotifications', methods=['POST'])
async def receive_incoming_notifications():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.receive_incoming_notifications()
            if response.status_code == 200:
                logger.info("Уведомления успешно получены")
            else:
                logger.warning("Не удалось получить уведомления")
            return response
        except Exception as e:
            logger.exception("Ошибка в receiveIncomingNotifications")
            return jsonify({"error": f"Не удалось получить уведомления: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Получение всех клиентов
@bp.route('/clients', methods=['GET'])
async def get_clients_route():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.get_clients()
            return response
        except Exception as e:
            logger.exception("Ошибка в getClients")
            return jsonify({"error": f"Не удалось получить пользователей: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Получение всех уведомлений
@bp.route('/notifications', methods=['GET'])
async def get_notifications():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.get_notifications()
            return response
        except Exception as e:
            logger.exception("Ошибка в getNotifications")
            return jsonify({"error": f"Не удалось получить уведомление: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller


# Получения одного входящего уведомления из очереди уведомлений.
@bp.route('/receiveNotifications', methods=['GET'])
def receive_notifications():
    data = request.args.to_dict()
    controller = WhatsAppController(data)
    return controller.receive_incoming_notifications()


# Удаление одного входящего уведомления из очереди уведомлений.
@bp.route('/deleteNotification', methods=['DELETE'])
async def delete_notification():
    controller = create_controller()
    if isinstance(controller, WhatsAppController):
        try:
            response = await controller.delete_notification()
            return response
        except Exception as e:
            logger.exception("Ошибка в deleteNotification")
            return jsonify({"error": f"Не удалось удалить уведомление: {e}"}), 500
    else:
        logger.error("Контроллер не создан")
        return controller

