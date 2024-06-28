import asyncio

from fastapi import Request
from starlette.responses import StreamingResponse

from cbr_athena.athena__fastapi.routes.Routes__OpenAI import Routes__OpenAI
from cbr_athena.llms.chats.LLM__Chat_Completion__Resolve_Engine import LLM__Chat_Completion__Resolve_Engine
from cbr_athena.schemas.for_fastapi.GPT_Prompt_With_System_And_History import GPT_Prompt_With_System_And_History
from cbr_athena.schemas.for_fastapi.LLMs__Chat_Completion import LLMs__Chat_Completion

from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from osbot_fast_api.utils.Version import Version
from osbot_utils.utils.Misc import wait_for

ROUTES_PATHS__CONFIG = ['/config/status', '/config/version']

class Routes__Chat(Fast_API_Routes):
    tag : str = 'chat'

    def execute_llm_request(self, llm_chat_completion):
        llm_platform_engine = LLM__Chat_Completion__Resolve_Engine().map_provider(llm_chat_completion)
        if llm_platform_engine:
            return llm_platform_engine.execute_request()
        return 'no engine'

    async def handle_other_llms(self, llm_chat_completion: LLMs__Chat_Completion):
        return StreamingResponse(self.handle_other_llms__streamer(llm_chat_completion), media_type='text/event-stream"; charset=utf-8')

    async def handle_other_llms__streamer(self, llm_chat_completion: LLMs__Chat_Completion):
        async def simulated_api_call():                         # Simulating the response of the async API call
            user_data = llm_chat_completion.user_data or {}

            response =  self.execute_llm_request(llm_chat_completion)
            for chunk in response:
                await asyncio.sleep(0)                           # this is needed to trigger sending the data back (without it, we don't get streaming)
                yield chunk

        generator = simulated_api_call()
        async for answer in generator:
            if answer:
                yield f"{answer}\n"

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



