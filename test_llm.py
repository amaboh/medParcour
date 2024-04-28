import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(response_validation=False)

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

prompt = "Hello."
print(get_chat_response(chat, prompt))

prompt = "What is the capital of Nigeria"
print(get_chat_response(chat, prompt))

prompt = "Who was their first president?"
print(get_chat_response(chat, prompt))