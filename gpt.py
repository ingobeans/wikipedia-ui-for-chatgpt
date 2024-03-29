import requests, json

model = "gpt-3.5-turbo"
#model will always be gpt-3.5-turbo, regardless of this value. api overrides anyways

def get_resp(messages:list[dict],temperature:float=0.7,frequency_penalty:float=0.7,presence_penalty:float=0.7) -> str:
    url = "https://chat.mindtastik.com/php/api.php"
    messages_text = json.dumps(messages)
    headers = {
        "Host": "chat.mindtastik.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://chat.mindtastik.com",
        "Alt-Used": "chat.mindtastik.com",
        "Connection": "keep-alive",
        "Referer": "https://chat.mindtastik.com/?chat=AI+Chat+Pro",
        "Cookie": "PHPSESSID=o4cnferlstceg33behmulftua6",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    data = {
        "array_chat": messages_text,
        "employee_name": "AI Chatbot Pro",
        "model": model,
        "temperature": temperature,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
    }

    response = requests.post(url, data=data, headers=headers)
    response_text = response.text
    if not "data: " in response_text:
        raise Exception(f"No data in response.\n\nResponse Text: {response_text}")
    chunks = response_text.split('data: ')
    full = ""
    for chunk in chunks:
        if chunk.strip():
            try:
                chunk_data = json.loads(chunk.strip())
                if "error" in chunk_data:
                    raise Exception(f"Error in chunk_data: {chunk_data['message']}\n\nResponse Text: {response_text}")
                if "choices" in chunk_data:
                    content = chunk_data["choices"][0]["delta"].get("content", "")
                    full += content
            except:
                pass
    return full

def get_prompt(prompt:str) -> str:
    return get_resp([{"role":"user","content":prompt}])

def complete(text:str) -> str:
    return get_resp([{"role":"assistant","content":text}])
