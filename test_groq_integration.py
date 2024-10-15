import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def test_groq_model():
    groq_client = ChatGroq(model="mixtral-8x7b-32768", api_key=os.environ.get('GROQ_API_KEY'))
    test_prompt = "Hello, can you introduce yourself?"

    try:
        response = groq_client.invoke(test_prompt)
        print(f"Groq model response: {response}")
        return True
    except Exception as e:
        print(f"Error testing Groq model: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_groq_model()
    print(f"Groq model test {'succeeded' if success else 'failed'}")
