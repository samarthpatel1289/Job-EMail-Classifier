from dotenv import load_dotenv
from openai import OpenAI
import os
import sys

def request(user_message, system_message):
    """
    Classifies an email using OpenAI's GPT-3 model.

    Args:
        user_message : Data sent by user,

    Returns:
        The assistant's reply with the classified email type.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Access the OpenAI API key from the environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        # Check if the API key is available
        if not api_key:
            return "Error"

        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key)

        # Send the information to OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                },
                {
                    "role": "system",
                    "content": system_message
                },
            ],
            temperature=0.4
        )

        # Get the assistant's reply
        assistant_reply = completion.choices[0].message.content

        # Return the assistant's reply with the classified email type
        return assistant_reply

    except Exception as e:
        print("Error", e)
        return "Error"

if __name__ == "__main__":
    # Classify the email and print the assistant's reply
    user_message, system_message = sys.argv[1:]
    response = request(user_message, system_message)
    print(response)
