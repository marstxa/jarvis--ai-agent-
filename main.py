import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

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

    while True:
    # 1. Generate content
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message_history,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),     
        )
        
        # Extract function calls from the response        
        function_calls = []
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_calls.append(part.function_call)

        # 2. Check if we found any function calls
        if function_calls:
            if user_args.verbose:
                print(f"Model requested {len(function_calls)} function(s)...")

            # Append the model's full response (thoughts + function calls) to history
            message_history.append(response.candidates[0].content)

            # 3. Execute all requested functions
            for function_call in function_calls:
                # Execute the specific function
                function_result_content = call_function(function_call, verbose=user_args.verbose)
                
                # Append the RESULT to the history
                message_history.append(function_result_content)
                
                if user_args.verbose:
                    # Accessing the result part for printing (safely)
                    try:
                        result_data = function_result_content.parts[0].function_response.response
                        print(f" -> Function Result: {result_data}")
                    except:
                        print(f" -> Function Result: [Complex Data]")

            # --- FREE TIER SAFETY ---
            # Not guaranteed to be perfect, but helps avoid hitting rate limits
            # Pause for 2 seconds to avoid hitting the "50 Requests Per Minute" limit
            if user_args.verbose:
                print("Pausing for 4 seconds to respect rate limits...")
                time.sleep(50) # Change to 50 seconds if you hit limits frequently
            
            # 4. Loop back to send results to the model
            continue
        
        # 5. No function calls? We have a text response.
        else:
            if response.text:
                print(f"Response:\n{response.text}")
                break
            else:
                print("Error: Model returned empty response.")
                break

if __name__ == "__main__":
    main()
