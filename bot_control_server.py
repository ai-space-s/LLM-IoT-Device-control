#%% Flask 서버
# json 형태로 stt 결과를 받아서 json 형태로 report를 반환
# 명령별 id를 받을 것
# api 구성으로 flask에서 threads로 작동

###############################################################################
from datetime import datetime
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from src.llm_templates import make_prompt, make_report_prompt
from src.switchbot_control import get_device_ids, return_to_action

###############################################################################
# openAI 설정
from src.load_config import load_config
config = load_config("./config.txt")

import os
# path 설정
os.chdir(config['BASE_PATH']) # your server base loc
if os.path.exists('./log') == False:
    os.mkdir('./log')


openai_key = config['OPENAI_KEY'] # openai_key 사전 정의
os.environ['OPENAI_API_KEY'] = openai_key
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    max_tokens=2048,  # 최대 토큰수
    model_name="gpt-3.5-turbo")  # 모델명

# switchbot 설정
token = config['TOKEN'] # 장비 토큰 사전 정의
secret = config['SECRET'] # 장비 키 사전 정의


###############################################################################
# flask app
app = Flask(__name__)
LOG_FOLDER = "./log"
app.config["LOG_FOLDER"] = LOG_FOLDER
@app.route("/upload", methods=["POST"])
def iot_run():
    timestr = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    report_text = ''
    # 처리
    try: 
        user_input_text = request.form["sttText"]
        input_id = request.form["sttTextId"]
        print('step 1', user_input_text, input_id)
        
        # 디바이스 정보 (switchbot 서버에서 응답이 안 오는 경우(500) 재시도를 위한 try-except)
        try: 
            device_ids = get_device_ids(token=token, secret=secret)
        except:
            device_ids = get_device_ids(token=token, secret=secret)
        device_names = list(device_ids.keys())
        print('step 2', device_ids, device_names)
        
        # 명령 해석
        llm_text = llm.invoke(make_prompt(user_input_text, device_names)).content
        print('step 3', llm_text)
        # 명령 수행 (switchbot 서버에서 응답이 안 오는 경우(500) 재시도를 위한 try-except)
        try:
            action_results = return_to_action(token, secret, device_ids, llm_text)
        except:
            action_results = return_to_action(token, secret, device_ids, llm_text)
        print('step 4', action_results)
        # 보고 생성
        report_text = llm.invoke(make_report_prompt(user_input_text, llm_text, action_results, "Korean")).content
        print('step 5', report_text)
        # 로그 생성
        log_path = os.path.join(app.config['LOG_FOLDER'], timestr + '.log')
        log_text = "사용자 명령: " + user_input_text + "\n" + \
                   "수행 명령: " + llm_text + "\n" + \
                   "결과 메세지: " + report_text + "\n"
        # 오류 상태        
        status = 10
        error_msg = None

    # 예외 처리
    except Exception as e:
        error_msg = str(e)
        # 로그 생성
        log_path = os.path.join(app.config['LOG_FOLDER'], 'ERROR_' + timestr + '.log')
        log_text = error_msg
        # 오류 상태
        status = 20

    # 반환        
    finally:
        # 결과 생성
        response_data = {"sttTextId": input_id,
                 'status': status,
                 'errorDesc': error_msg,
                 'result': report_text}
        # 로그 기록
        with open(log_path, 'a') as f:
            f.writelines(log_text)
    
        return jsonify(response_data)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(config['IP'], int(config['PORT']), app, threaded=True)