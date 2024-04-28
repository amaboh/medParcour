from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class ConversationHandler:
    def __init__(self):
        model_name = "distilgpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)
        self.llm = HuggingFacePipeline(pipeline=pipe)
        
        self.template = """
        User: {user_input}
        Conversation History:
        {conversation_history}
        Assistant: """
        self.prompt = PromptTemplate(
            input_variables=["user_input", "conversation_history"],
            template=self.template,
        )
        self.conversation = ConversationChain(
            llm=self.llm, 
            prompt=self.prompt,
            verbose=True,
            memory=ConversationBufferMemory(input_key='user_input', memory_key='conversation_history')
        )

    def generate_response(self, user_input):
        response = self.conversation.predict(user_input=user_input)
        return response