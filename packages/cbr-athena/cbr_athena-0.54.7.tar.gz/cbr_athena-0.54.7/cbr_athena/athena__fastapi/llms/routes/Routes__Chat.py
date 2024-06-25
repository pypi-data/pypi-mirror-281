from fastapi import Request
from starlette.responses import StreamingResponse

from cbr_athena.athena__fastapi.routes.Routes__OpenAI import Routes__OpenAI
from cbr_athena.schemas.for_fastapi.GPT_Prompt_With_System_And_History import GPT_Prompt_With_System_And_History
from cbr_athena.schemas.for_fastapi.LLMs__Chat_Completion import LLMs__Chat_Completion

from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from osbot_fast_api.utils.Version import Version

ROUTES_PATHS__CONFIG = ['/config/status', '/config/version']

class Routes__Chat(Fast_API_Routes):

    def __init__(self, app):
        super().__init__(app, tag='chat')

    async def handle_other_llms(self, llm_chat_completion):
        async def streamer():
            async def simulated_api_call():                         # Simulating the response of the async API call
                user_data = llm_chat_completion.user_data
                responses = ['Here ', 'is ', 'the ', 'data received .....']
                for key, value in user_data.items():
                    responses.append(f'\n- {key} = {value}')
                for response in responses:
                    yield response

            generator = simulated_api_call()
            gpt_response = ''
            async for answer in generator:
                if answer:
                    gpt_response += answer
                    yield f"{answer}\n"
        return StreamingResponse(streamer(), media_type='text/event-stream"; charset=utf-8')

    async def completion(self, llm_chat_completion: LLMs__Chat_Completion, request: Request):
            routes_open_ai = Routes__OpenAI()
            user_data      = llm_chat_completion.user_data

            # for now use the code in routes_open_ai.prompt_with_system__stream which is already working for OpenAI
            if 'selected_platform' in user_data and user_data.get('selected_platform') != 'OpenAI (Paid)':
                return await self.handle_other_llms(llm_chat_completion)
            else:
                return await routes_open_ai.prompt_with_system__stream(llm_chat_completion, request)


    def setup_routes(self):
        self.router.post("/completion" )(self.completion )



