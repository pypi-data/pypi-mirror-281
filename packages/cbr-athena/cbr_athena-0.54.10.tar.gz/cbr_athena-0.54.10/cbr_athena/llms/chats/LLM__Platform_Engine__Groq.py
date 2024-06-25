from cbr_athena.llms.chats.LLM__Platform_Engine import LLM__Platform_Engine
from cbr_athena.schemas.for_fastapi.LLMs__Chat_Completion import LLMs__Chat_Completion


class LLM__Platform_Engine__Groq(LLM__Platform_Engine):
    llm_platform       : str
    llm_provider       : str
    llm_model          : str
    llm_chat_completion: LLMs__Chat_Completion

    def is_provider_available(self):
        return False

    def execute_request(self):
        if self.is_provider_available():
            yield "Groq is available"
        else:
            yield "Groq is not available"