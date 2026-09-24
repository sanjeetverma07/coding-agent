from groq import Groq
from .config import LLM_SETTINGS

class LLM:
    def __init__(self):
        self.model = LLM_SETTINGS.MODEL_NAME
        self.temp= LLM_SETTINGS.TEMPERATURE
        self.max_tokens = LLM_SETTINGS.MAX_TOKENS
        self.stream = LLM_SETTINGS.STREAM
        self.reasoning_effort= LLM_SETTINGS.REASONING_EFFORT
        self.client = Groq(api_key=LLM_SETTINGS.MODEL_API_KEY)
        
    def chat(self,messages, tools=[], tool_choice="none"):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temp,
            reasoning_effort=self.reasoning_effort,
            stream=self.stream,
            tools=tools,
            tool_choice=tool_choice
        )
        return response.choices[0].message
# completion = client.chat.completions.create(
#     model="openai/gpt-oss-120b",
#     messages=[
#       {
#         "role": "user",
#         "content": ""
#       }
#     ],
#     temperature=1,
#     max_completion_tokens=2048,
#     top_p=1,
#     reasoning_effort="medium",
#     stream=True,
#     stop=None
# )

# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")
