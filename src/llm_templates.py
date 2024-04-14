# 질문 템플릿 형식 정의
def make_prompt(user_input_text, device_names):
    prompt = "Determine ① 'what action' the user intends by ② 'what device' based on the input ⓐ " + \
                "and return your answer in the python dictionary form ⓑ with in a python list form. " + \
                "While making returns, choose the intended device item ② among ⓒ and the action ① among ⓓ. " + \
                "If the action ① or device ② is not in ⓒ or ⓓ, return None. " + \
                "If two or more orders are given, make as many returns as orders. " + \
                "ⓐ " + str(user_input_text) + "\n" + \
                "ⓑ {'device': ②, 'action': ①}\n" + \
                "ⓒ " + str(device_names) + "\n" + \
                "ⓓ ['turn on', 'turn off', 'get status']" # 디바이스에 따라 행동 종류를 추가
    return prompt


# 결과 텍스트 형식 정의
def make_report_prompt(user_input_text, llm_text, action_results, language):
    prompt = "ⓐ " + str(user_input_text) + "are the orders the user gave at the beginning. " + \
            "ⓑ " + str(llm_text) + " are the commands out of ⓐ which the home manager, your role, performed because of ⓐ. " + \
            "ⓒ " + str(action_results) + " are the preformed results of ⓑ. " + \
            f"You are a home manager. Make a spoken report based on information ⓐ, ⓑ, ⓒ in {language} with polite manners. " + \
            "Within your report you need to clarify what orders are given, what the home manager did, and what the outcomes are."

    return prompt