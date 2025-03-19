import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set the OpenAI API key from your environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("API key is not set properly. Check your .env loading and API key value.")

def get_embeddings(text, model="text-embedding-3-small"):
    # Fetch embeddings using a currently supported model
    response = openai.Embedding.create(
        input=text,
        model=model  # Updated model
    )
    return response['data']

def main():
    text1 = "I am sitting at my dining table to feed my kid."
    text2 = "I got a logarithmic table to establish the feed."

    embeddings1 = get_embeddings(text1)
    embeddings2 = get_embeddings(text2)

    print("Embeddings from text1:", embeddings1[0]['embedding'][:10])
    print("Embeddings from text2:", embeddings2[0]['embedding'][:10])

if __name__ == "__main__":
    main()
