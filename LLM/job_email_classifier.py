import sys
import constants as const
import largeLanguageModel as llm

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
        # Combine the sender name, subject line, and email body into one sentence
        email_content = f"From: {sender_name} Subject: {subject_line} Body: {email_body}"

        content = f"""
        You are job email classifiers, I want you to classify this email as one of the following: {', '.join(const.Classifications)}.
        Also Find following details from data provided: Company Name and Job Role.
        If company name not found return `unknown name`.
        If job role not found return `software engineer`.
        Reply only with comma separated values of classified type, company name, job role.
        """
        assistant_reply = llm.request(content, email_content)

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
