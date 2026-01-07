import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key failed")

    client = genai.Client(api_key=api_key)

    #Get user input
    user_input = argparse.ArgumentParser(description="Chatbot Jarvis")
    user_input.add_argument("user_prompt", type=str, help="User Prompt")
    user_input.add_argument("--verbose", action="store_true", help="Enable verbose output") # Verbose flag for briefer less noise outputs
    user_args = user_input.parse_args() # To access args.user_prompt and write our prompt to the terminal

    # History of prompts
    message_history = [types.Content(role="user", parts=[types.Part(text=user_args.user_prompt)])]

    # Generate response from agent
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message_history,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            ),     
    )

    # Check for function calls

    if not response.function_calls is None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    if user_args.verbose is True: #Check if verbose flag is true
        print(f"User prompt: {user_args.user_prompt}")

        #Tokens
        if response.usage_metadata is not None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("Failed API request")
    else:
        print(f"Response:\n{response.text}") # Display response to terminal

if __name__ == "__main__":
    main()
