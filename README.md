# SwitchBot을 이용한 IoT 컨트롤

스위치봇과 OpenAI를 이용한 IoT 컨트롤 예제입니다. 기본적으로 flask를 이용한 서버의 형태로 작동하며, 텍스트 명령 또는 음성으로부터 Speech-To-Text 모델을 이용하여 생성된 텍스트 명령을 수신받아 지정된 장비에 대한 조작을 수행하고, 텍스트로 결과를 반환합니다. 등록되어 있는 SwitchBot의 장비를 자동으로 탐색하여 명령을 수행하도록 되어있습니다.

# requirements
flask

langchain

langchain-openai

python-switchbot

werkzeug

# 사용 방법

## 1) 빠른 실행
config.txt 내에 경로 및 API key, IP 등의 환경 설정을 수행

bot_control_server.py 를 실행

## 2) config.txt 구성 
config.txt는 다음의 구조로 이루어져 있습니다. 실행환경에 맞게 각 해당되는 값을 따옴표 없이 문자열로 기록합니다.

※ OpenAI와 SwitchBot의 key는 각각 다음의 정보를 참조합니다.

OpenAI API: https://platform.openai.com/docs/overview

SwitchBot API: https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#introduction

    # Config
    OPENAI_KEY= your_open_api_key_here
    TOKEN= your_switchbot_token_here
    SECRET= your_switchbot_key_here
    BASE_PATH= your_base_path_of_this_project_here
    IP= your_host_ip_here
    PORT= your_host_port_here

## 3) API 입출력 구성
본 예제는 Flask Server의 형태로 명령 텍스트의 입출력을 수행합니다. 입출력 모두 JSON의 형태로 이루어지며 다음과 같이 구성됩니다. 

    입력
    {"sttText": 입력 명령 텍스트(String), 
    "sttTextId": 입력 명령 텍스트의 식별용 고유 ID(String)}

    출력
     {"sttTextId": 입력 명령 텍스트의 식별용 고유 ID(String),
    'status': 처리 상태(Int). 정상인 경우 10, 오류인 경우 20 반환,
    'errorDesc': 오류 발생 시  오류 메세지(String). 없는 경우 None,
    'result': 실행 결과 텍스트(String). 입력 명령 내용과 그에 따른 실행 결과를 문장으로 반환}

send_sample.py를 이용하여 입력 API 및 결과 수신 예제를 확인해볼 수 있습니다.


## 4) 명령 추가 
SwitchBot 장비에 따라 수행할 수 있는 명령을 추가하기 위해서는 ① src/llm_templates.py의 make_prompt 함수와 ②  src/switchbot_control.py의 return_to_action 함수를 이용합니다. make_prompt 함수에서는 장비에 따른 행동 종류를 텍스트의 리스트 형태로 추가하고, return_to_action 함수에서는 추가된 행동 텍스트와 그에 맞는 SwitchBot 수행 명령을 매칭합니다.

지원되는 SwitchBot 장비별 명령에 대해서는 다음을 참고합니다.

python-switchbot 문서: https://github.com/jonghwanhyeon/python-switchbot

SwitchBot API 문서: https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#send-device-control-commands
