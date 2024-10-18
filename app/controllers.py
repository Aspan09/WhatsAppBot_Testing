from flask import jsonify, request
from .services import GreenAPIService
from flask import Blueprint
from .logger import logger


bp = Blueprint('whatsapp', __name__)


class WhatsAppController:
    def __init__(self, data):
        self.data = data
        self.id_instance = data.get('idInstance')
        self.api_token = data.get('apiTokenInstance')

    @classmethod
    def from_request(cls):
        """Создание экземпляра контроллера из данных запроса."""
        data = request.json
        if not data:
            raise ValueError("Нет данных в запросе")
        return cls(data)

    def validate(self, required_fields):
        """Проверка наличия обязательных полей."""
        missing_fields = [field for field in required_fields if not self.data.get(field)]
        if missing_fields:
            return False, f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
        return True, None

    async def get_settings(self):
        """Метод для получения настроек аккаунта."""
        if not self.id_instance or not self.api_token:
            return jsonify({"error": "idInstance and apiTokenInstance are required"}), 400

        try:
            response_data = await GreenAPIService.get_settings(self.id_instance, self.api_token)
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def send_message(self):
        phone_number = self.data.get('phoneNumber')
        message = self.data.get('message')

        if not phone_number:
            return {"error": "требуется phoneNumber"}, 400

        response_data, status_code = GreenAPIService.send_message(
            self.id_instance, self.api_token, phone_number, message
        )

        return response_data, status_code

    async def send_file_by_url(self):
        """Метод для отправки файла по URL."""
        valid, error = self.validate(['idInstance', 'apiTokenInstance', 'phoneNumber', 'fileUrl'])
        if not valid:
            logger.error(f"Ошибка: {error}")
            return jsonify({"error": error}), 400

        try:
            response_data, status_code = await GreenAPIService.send_file_by_url(
                self.id_instance,
                self.api_token,
                self.data.get('phoneNumber'),
                self.data.get('fileUrl')
            )

            if isinstance(response_data, dict) and "error" in response_data:
                logger.warning(f"Не удалось отправить файл: {response_data['error']}")
                return jsonify({"error": response_data['error']}), status_code

            return jsonify(response_data), status_code
        except Exception as e:
            logger.error(f"Ошибка в send_file_by_url: {str(e)}")
            return jsonify({"error": "Произошла ошибка при отправке файла."}), 500

    async def get_clients(self):
        try:
            clients = await GreenAPIService.get_clients()
            if clients is None:
                logger.error("Не удалось получить пользователей")
                return jsonify({"error": "Не удалось получить пользователей"}), 500
            clients_data = [{"id": client.id, "phone_number": client.phone_number} for client in clients]
            return jsonify(clients_data), 200
        except Exception as e:
            logger.error(f"Error in get_clients: {str(e)}")
            return jsonify({"error": str(e)}), 500

    async def get_notifications(self):
        try:
            notifications = GreenAPIService.get_notifications()
            if notifications is None:
                logger.error("Не удалось получить уведомления")
                return jsonify({"error": "Не удалось получить уведомления"}), 500
            notifications_data = [
                {
                    "id": notification.id,
                    "content": notification.content,
                    "file_url": notification.file_url,
                    "client_id": notification.client_id
                }
                for notification in notifications
            ]
            return jsonify(notifications_data), 200
        except Exception as e:
            logger.error(f"Error in get_notifications: {str(e)}")
            return jsonify({"error": str(e)}), 500

    async def delete_notification(self):
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')
        receipt_id = data.get('receiptId')

        if not id_instance or not api_token or not receipt_id:
            return jsonify({"error": "idInstance, apiTokenInstance, and receiptId are required"}), 400

        try:
            response_data = await GreenAPIService.delete_notification(id_instance, api_token, receipt_id)
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def receive_incoming_notifications(self):
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')

        if not id_instance or not api_token:
            return jsonify({"error": "idInstance and apiTokenInstance are required"}), 400

        response_data, status_code = GreenAPIService.receive_incoming_notifications(id_instance, api_token)
        return jsonify(response_data), status_code
