from urllib.parse import urljoin

import requests

from cbr_athena.llms.chats.LLM__Platform_Engine import LLM__Platform_Engine
from cbr_athena.llms.providers.open_router.LLM__Open_Router import LLM__Open_Router
from cbr_athena.schemas.for_fastapi.LLMs__Chat_Completion import LLMs__Chat_Completion
from osbot_utils.testing.Logging import Logging
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import from_json_str


class LLM__Platform_Engine__Open_Router(LLM__Platform_Engine):
    llm_platform       : str
    llm_provider       : str
    llm_model          : str
    llm_chat_completion: LLMs__Chat_Completion
    llm_open_router    : LLM__Open_Router

    def is_provider_available(self):
        if self.llm_open_router.api_key:
            return True
        return False

    def post_request(self, url, json, headers=None):
        try:
            response = requests.post(url, headers=headers, json=json, stream=True)
            for line in response.iter_lines():
                if line:
                    raw_data = line.decode('utf-8')
                    if raw_data.startswith('data: {'):
                        json_line = raw_data[5:]
                        json_data = from_json_str(json_line)
                        choice = json_data.get('choices')[0]
                        yield choice.get('delta').get('content')
        except Exception as error:
            yield f"Error fetching Open Router data : {error}"


    def execute_request(self):
        logging = Logging().enable_log_to_console()
        if self.is_provider_available():
            user_prompt = self.llm_chat_completion.user_prompt
            self.llm_open_router.add_message__user(user_prompt)

            messages = self.llm_open_router.messages
            post_data = { 'headers': { 'Authorization': f'Bearer {self.llm_open_router.api_key}',
                                       'Content-Type': 'application/json'},
                        'json': { 'messages': messages, 'model': self.llm_model,
                                  "stream" : True},
                        'url': 'https://openrouter.ai/api/v1/chat/completions' }
            response  = self.post_request(**post_data)
            for item in response:
                yield item
        else:
            yield "Open router is not available"
