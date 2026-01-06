import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key failed")

    client = genai.Client(api_key=api_key)

    #Get user input
    user_input = argparse.ArgumentParser(description="Chatbot Jarvis")
    user_input.add_argument("user_prompt", type=str, help="User Prompt")
    user_args = user_input.parse_args() # To access args.user_prompt and write our prompt to the terminal

    # History of prompts
    message_history = [types.Content(role="user", parts=[types.Part(text=user_args.user_prompt)])]
    
    # Generate response from agent
    response = client.models.generate_content(model="gemini-2.5-flash", contents=message_history)

    #Tokens 
    if response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Failed API request")


    print(f"Response:\n{response.text}") # Display response to terminal

if __name__ == "__main__":
    main()
