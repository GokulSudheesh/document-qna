from langchain_nvidia_ai_endpoints import ChatNVIDIA
from core.config import Settings

client = ChatNVIDIA(
    model="mistralai/mistral-7b-instruct-v0.2",
    api_key=Settings.NVIDIA_API_KEY,
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    disable_streaming=True,

)

for chunk in client.stream([{"role": "user", "content": "hello there"}]):
    print(chunk.content, end="")
