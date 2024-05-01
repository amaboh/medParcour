import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

class LLMService:
    def __init__(self):
        vertexai.init(project=GOOGLE_PROJECT_ID, location="us-central1")
        self.chat_model = ChatModel.from_pretrained("chat-bison")

    def generate_response(self, prompt):
        parameters = {
            "temperature": 0.8,
            "max_output_tokens": 256,
            "top_p": 0.95,
            "top_k": 40,
        }

        chat = self.chat_model.start_chat(
            context="My name is Med_Ai. You are a healthcare assistant, knowledgeable about keeping track of health records.",
            examples=[
                InputOutputTextPair(
                    input_text="I'm not feeling fine",
                    output_text="Have you taken your medication today?",
                ),
            ],
        )

        responses = chat.send_message_streaming(message=prompt, **parameters)
        generated_response = ""
        for response in responses:
            generated_response += response.text
        return generated_response