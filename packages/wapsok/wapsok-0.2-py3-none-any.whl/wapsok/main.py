import requests
import socket

def send_to_discord(webhook_url, message):
    pc_name = socket.gethostname()

    ip_address = socket.gethostbyname(pc_name)

    full_message = f"{message}\nPC Name: {pc_name}\nIP Address: {ip_address}"
    payload = {
        "content": full_message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code