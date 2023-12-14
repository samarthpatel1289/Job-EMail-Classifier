# Job Email Classifier

## Overview

This project utilizes OpenAI's GPT-3 model to classify job-related emails, aiming to simplify the job hunting process. The Job Email Classifier takes three main inputs: the sender's name, the subject line of the email, and the email body. It then uses these inputs to classify the email into one of several predefined categories. The possible classifications include:

- **Job Application Confirmation**: Email confirming the submission of a job application.
  
- **Job Rejection**: Email notifying the recipient that their job application has been rejected.

- **Job Under Consideration**: Email indicating that the job application is still under consideration.

- **Job Offered**: Email extending a job offer to the recipient.

- **New Job Notification**: Email notifying the recipient about a new job opportunity.

- **Not Job Specific Email**: Generic email that does not fall into any of the specific job-related categories.

## Usage

To use the Job Email Classifier, follow these steps:

1. Provide the sender's name, subject line, and email body as input parameters.
2. Specify the desired classifications as a list of possible categories.
3. Receive the assistant's reply, which includes the classified email type.

## Environment Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/job-email-classifier.git```

2. Rename the demo.env file to .env and configure it with your OpenAI GPT-3 API key

    ```
    mv demo.env .env 
    ```

- Open the .env file and replace YOUR_API_KEY with your actual GPT-3 API key

3. Install Requirements

    ```
    pip install -r requirements.txt
    ```

4. Run the application

    ```
    python job_email_classifier.py "<SENDER>" "<SUBJECT>" "<EMAIL BODY 1>"...<EMAIL BODY N>
    ```

## Important Note

Make sure to handle your GPT-3 API key securely and avoid sharing it publicly. 👀

Feel free to contribute to and enhance this project. If you encounter any issues or have suggestions for improvement, please open an issue on the GitHub repository.

Happy job hunting. 🚀

Feel Free to Customize it Further or Add more Classifiers. 