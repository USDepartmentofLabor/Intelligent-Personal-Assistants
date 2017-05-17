# AJC Finder Skill

## “Alexa, ask AJC Finder: where's my closest Job Center?”

This directory contains an Alexa Skill that returns the user's closest American Job Center. It obtains the user's location through the Alexa API, and finds AJCs through the [CareerOneStop Web API](https://www.careeronestop.org/Developers/WebAPI/web-api.aspx).

## Installation

This skill is based on the Python "favorite color" sample from Amazon, using AWS Lambda to host the code. This guide assumes you have set up Amazon developer account(s); if not, you may need to go through some registration steps first.

### Part 1: Lambda setup

1. In the [Lambda management console](https://console.aws.amazon.com/lambda/home), switch to the "US East (N. Virginia)" region if needed.

2. Create a new function based on the "alexa-skills-kit-color-expert-python" template.

3. At the "Configure triggers" section, click Next.

4. At the "Configure function" section, add a name (it doesn't matter what name you choose), then scroll down.

5. At the "Lambda function code" section, delete the sample code and paste in the code from `lambda.py` in this repo. Further down, create two environment variables, named `cos_web_api_userid` and `cos_web_api_token`. For the hackathon, contact Tom for credentials, or [sign up](https://www.careeronestop.org/Developers/WebAPI/registration.aspx) for an account. Then scroll down.

6. At the "Lambda function handler and role" section, under "Role" choose "Create new role from template(s)". Add a role name (it doesn't matter what name you choose) and add the "Simple Microservice permissions" template. Then click Next.

5. At the review screen, click "Create function" to finish the setup. Once it completes, take note of the **ARN** in the upper right corner -- you'll need that ID for the next step.

### Part 2: Alexa Skill setup

1. In the [Amazon developer console](https://developer.amazon.com/edw/home.html), click "Get Started" under "Alexa Skills Kit".

2. Click "Add a New Skill".

3. Fill out the Name and Invocation Name (the name you speak to Alexa) of the skill. I used "AJC Finder" and "AJC Finder" in my setup. Then click "Save" followed by "Next".

4. In the "Intent Schema" section, paste in the JSON from `intent-schema.json`.

5. In the "Sample Utterances" area, paste in the text from `sample-utterances.txt`. Then click "Next" and wait until the next screen loads.

6. In the "Endpoint" section, select the "AWS Lambda ARN" radio button. Click the "North America" checkbox. In the text field that appears, paste in the ARN you saved at the end of the Lambda setup. Then scroll down.

7. In the "Permissions" section, check "Device Address", then select "Country & Postal Code Only". Then click "Next".

### Part 3: Grant Permissions

1. Open the Alexa app on your iOS or Android device. From Home, navigate to "Skills", then "Your Skills", then "AJC Finder".

2. Click "Manage Settings" and enable the "Device Country and Postal Code" option.

Now your demo skill is ready to use. You need an Alexa device to try it; the simulator will not work. Try it by saying, "Alexa, ask AJC Finder where my closest Job Center is".

As a demo, error checking is almost nonexistent. It will prompt you to visit the Alexa app if permissions have not been granted.

