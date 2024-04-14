import requests
import json

def send_text(stt_text, stt_text_id, server_url):
    data = {"sttText": stt_text, "sttTextId": stt_text_id}
    response = requests.post(server_url + '/upload', data=data)
    print(response.json())

if __name__ == '__main__':
    server_url = 'http://localhost:8893'
    stt_text_id = 'a9d8621c-998d-4024-b15c-621aad526148'
    stt_text = "히터를 꺼줘"
    send_text(stt_text, stt_text_id, server_url)
