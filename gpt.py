import requests
import json

class GPT():
    def __init__(self, API_key):
        self.API_key = API_key

    def generate_chat_completion(self, user_prompt, system_prompt, model='gpt-4-1106-preview', response_format={ "type": "json_object" }, temperature=1, max_tokens=None):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.API_key}',
        }

        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'response_format':response_format
        }

        if max_tokens is not None:
            data['max_tokens'] = max_tokens

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f'Error {response.status_code}: {response.text}')