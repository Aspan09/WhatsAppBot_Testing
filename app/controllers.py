from flask import jsonify, request
from .services import GreenAPIService
from flask import Blueprint

bp = Blueprint('whatsapp', __name__)


class WhatsAppController:
    @staticmethod
    async def get_settings():
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')

        if not id_instance or not api_token:
            return jsonify({"error": "idInstance and apiTokenInstance are required"}), 400

        try:
            response_data = await GreenAPIService.get_settings(id_instance, api_token)
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    async def send_message():
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')
        phone_number = data.get('phoneNumber')
        message = data.get('message')

        if not id_instance or not api_token or not phone_number:
            return jsonify({"error": "idInstance, apiTokenInstance, and phoneNumber are required"}), 400

        try:
            response_data = await GreenAPIService.send_message(id_instance, api_token, phone_number, message)
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    async def send_file_by_url():
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')
        phone_number = data.get('phoneNumber')
        file_url = data.get('fileUrl')

        if not id_instance or not api_token or not phone_number:
            return jsonify({"error": "idInstance, apiTokenInstance, and phoneNumber are required"}), 400

        try:
            response_data = await GreenAPIService.send_file_by_url(id_instance, api_token, phone_number, file_url)
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    async def delete_notification():
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

    @staticmethod
    async def get_clients():
        try:
            clients = GreenAPIService.get_clients()
            if clients is None:
                return jsonify({"error": "Could not fetch clients"}), 500
            clients_data = [{"id": client.id, "phone_number": client.phone_number} for client in clients]
            return jsonify(clients_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    async def get_notifications():
        try:
            notifications = GreenAPIService.get_notifications()
            if notifications is None:
                return jsonify({"error": "Could not fetch notifications"}), 500
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
            return jsonify({"error": str(e)}), 500

    @staticmethod
    async def receive_incoming_notifications():
        data = request.json
        id_instance = data.get('idInstance')
        api_token = data.get('apiTokenInstance')

        if not id_instance or not api_token:
            return jsonify({"error": "idInstance and apiTokenInstance are required"}), 400

        try:
            notification = await GreenAPIService.receive_incoming_notifications(id_instance, api_token)
            if notification:
                receipt_id = notification.get('receiptId')
                if receipt_id:
                    await GreenAPIService.delete_notification(id_instance, api_token, receipt_id)
            return jsonify(notification), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
