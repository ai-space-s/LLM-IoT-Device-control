from switchbot import SwitchBot

# 디바이스 미리 확인
def get_device_ids(token, secret):
    switchbot = SwitchBot(token=token, secret=secret)
    devices = switchbot.devices()
    device_ids = {'None':None}
    for device in devices:
        device_ids[device.name] = device.id
    return device_ids

# switchbot 명령 수행 함수 정의
def return_to_action(token, secret, device_ids, llm_text):
    parsed_dict = eval(llm_text)
    action_results = [] # 행동 반환 결과
    for pdict in parsed_dict:
        # 적합한 장치/행동 선택이 없는 경우
        if None or 'None' in pdict.values():
            action_results.append('proper device does not exist for your command.')
    
        # 적합한 장치/행동 선택이 있는 경우
        else:
            switchbot = SwitchBot(token=token, secret=secret)
            device_id = device_ids[pdict['device']]
            device = switchbot.device(id=device_id)
            
            if 'status' in pdict['action']:
                response = device.status()
                del response['device_id'], response['hub_device_id']
                
            elif pdict['action'] == 'turn on':
                if device.status()['power'] == 'off':
                    response = device.command('turn_on') # 실제로 response가 발생하는지 확인 필요
                else:
                    response = f"{pdict['device']} is already on." # response가 있는 경우 response 포맷과 텍스트 포맷을 맞출 필요
            elif pdict['action'] == 'turn off': 
                if device.status()['power'] == 'on':
                    response = device.command('turn_off') # 실제로 response가 발생하는지 확인 필요
                else:
                    response = f"{pdict['device']} is already off." # response가 있는 경우 response 포맷과 텍스트 포맷을 맞출 필요
            action_results.append(response)
    return action_results