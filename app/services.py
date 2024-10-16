import httpx
from . import db
from dotenv import load_dotenv
import os
from .models import Notification, Client

load_dotenv()


class GreenAPIService:
    BASE_URL = os.getenv('GREEN_API_URL')

    @staticmethod
    async def get_settings(id_instance, api_token):
        try:
            url = f"{GreenAPIService.BASE_URL}/waInstance{id_instance}/getSettings/{api_token}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            return {"error": str(e)}, 500

    @staticmethod
    async def send_message(id_instance, api_token, phone_number, message):
        try:
            url = f"{GreenAPIService.BASE_URL}/waInstance{id_instance}/sendMessage/{api_token}"
            payload = {
                "chatId": f"{phone_number.strip()}@c.us",
                "message": message
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            # Сохраняем уведомление в базе данных
            client = GreenAPIService.get_or_create_client(phone_number)
            notification = Notification(
                client_id=client.id,
                content=message,
            )
            db.session.add(notification)
            db.session.commit()

            return response.json(), 200

        except httpx.RequestError as e:
            return {"error": str(e)}, 500

    @staticmethod
    async def send_file_by_url(id_instance, api_token, phone_number, file_url):
        try:
            url = f"{GreenAPIService.BASE_URL}/waInstance{id_instance}/sendFileByUrl/{api_token}"
            payload = {
                "chatId": f"{phone_number.strip()}@c.us",
                "urlFile": file_url,
                "fileName": "file_name"
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            # Сохраняем уведомление в базе данных
            client = GreenAPIService.get_or_create_client(phone_number)
            notification = Notification(
                client_id=client.id,
                content=file_url,
                file_url=file_url
            )
            db.session.add(notification)
            db.session.commit()

            return response.json(), 200

        except httpx.RequestError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_or_create_client(phone_number):
        try:
            client = Client.query.filter_by(phone_number=phone_number).first()
            if not client:
                client = Client(phone_number=phone_number)
                db.session.add(client)
                db.session.commit()
            return client
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_clients():
        try:
            return Client.query.all()
        except Exception as e:
            print(f"Error fetching clients: {str(e)}")
            return None

    @staticmethod
    def get_notifications():
        try:
            return Notification.query.all()
        except Exception as e:
            print(f"Error fetching notifications: {str(e)}")
            return None

    @staticmethod
    async def receive_incoming_notifications(id_instance, api_token):
        url = f"{GreenAPIService.BASE_URL}/waInstance{id_instance}/receiveNotification/{api_token}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def delete_notification(id_instance, api_token, receipt_id):
        url = f"{GreenAPIService.BASE_URL}/waInstance{id_instance}/deleteNotification/{api_token}/{receipt_id}"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url)
            response.raise_for_status()
            return response.json()

