from dotenv import load_dotenv
from openai import OpenAI
import os
import sys


def classify_email(sender_name, subject_line, *email_body_items):
    """
    Classifies an email using OpenAI's GPT-3 model.

    Args:
        sender_name: The name of the sender.
        subject_line: The subject line of the email.
        email_body: The body of the email.
        desired_classifications: A list of possible classifications for the email.

    Returns:
        The assistant's reply with the classified email type.
    """
    email_body = " ".join(email_body_items)
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

        # Combine the sender name, subject line, and email body into one sentence
        email_content = f"{sender_name}, {subject_line}: {email_body}"

        # Create a list of possible classifications
        Classifications = [
            os.getenv("JOB_APPLICATION_CONFIRMATION"),
            os.getenv("JOB_REJECTION"),
            os.getenv("JOB_OFFERED"),
            os.getenv("NEW_JOB_NOTIFICATION"),
            os.getenv("NOT_JOB_SPECIFIC_EMAIL"),
        ]
        content = f"""
        I want you to classify this email as one of the following: {', '.join(Classifications)}.
        Reply only with following words 
        `{os.getenv('JOB_APPLICATION_CONFIRMATION')}`, 
        `{os.getenv('JOB_REJECTION')}`, 
        `{os.getenv('JOB_OFFERED')}`, 
        `{os.getenv('NEW_JOB_NOTIFICATION')}` 
        and `{os.getenv('NOT_JOB_SPECIFIC_EMAIL')}` "
        """

        # Send the information to OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
                {"role": "system", "content": email_content},
            ],
        )

        # Get the assistant's reply
        assistant_reply = completion.choices[0].message.content

        # Return the assistant's reply with the classified email type
        return assistant_reply

    except Exception as e:
        print("Error", e)
        return "Error"

if __name__ == "__main__":
    # Extract the arguments from sys.argv
    sender_name, subject_line, *email_body = sys.argv[1:]
    email_body = " ".join(email_body)
    # Classify the email and print the assistant's reply
    classified_email_type = classify_email(sender_name, subject_line, email_body)
    print(classified_email_type)