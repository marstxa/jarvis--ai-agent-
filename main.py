import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key failed")

    client = genai.Client(api_key=api_key)

    # Generate response from agent
    response = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

    #Tokens 
    if response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Failed API request")


    print(f"Response:\n{response.text}") # Display response to terminal

if __name__ == "__main__":
    main()
