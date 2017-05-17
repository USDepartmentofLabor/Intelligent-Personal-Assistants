# O*NET Demo Alexa Skill

## “Alexa, ask O*NET Demo: what does an architect do?”

This directory contains a simple Alexa Skill that calls [O*NET Web Services](https://services.onetcenter.org/). It returns the most important task statements for any of the 900+ careers in [My Next Move](https://www.mynextmove.org/).

## Installation

This skill is based on the Python "favorite color" sample from Amazon, using AWS Lambda to host the code. This guide assumes you have set up Amazon developer account(s); if not, you may need to go through some registration steps first.

### Part 1: Lambda setup

1. In the [Lambda management console](https://console.aws.amazon.com/lambda/home), switch to the "US East (N. Virginia)" region if needed.

2. Create a new function based on the "alexa-skills-kit-color-expert-python" template.

3. At the "Configure triggers" section, click Next.

4. At the "Configure function" section, add a name (it doesn't matter what name you choose), then scroll down.

5. At the "Lambda function code" section, delete the sample code and paste in the code from `lambda.py` in this repo. Further down, create two environment variables, named `onet_web_services_username` and `onet_web_services_password`. For the hackathon, contact Tom or Jeremiah for credentials, or [sign up](https://services.onetcenter.org/developer/signup) for an account. Then scroll down.

6. At the "Lambda function handler and role" section, under "Role" choose "Create new role from template(s)". Add a role name (it doesn't matter what name you choose) and add the "Simple Microservice permissions" template. Then click Next.

5. At the review screen, click "Create function" to finish the setup. Once it completes, take note of the **ARN** in the upper right corner -- you'll need that ID for the next step.

### Part 2: Alexa Skill setup

1. In the [Amazon developer console](https://developer.amazon.com/edw/home.html), click "Get Started" under "Alexa Skills Kit".

2. Click "Add a New Skill".

3. Fill out the Name and Invocation Name (the name you speak to Alexa) of the skill. I used "O*NET Demo" and "oh net demo" in my setup. Then click "Save" followed by "Next".

4. In the "Intent Schema" section, paste in the JSON from `intent-schema.json`.

5. In the "Custom Slot Types" section, at the "Enter Type" field type "LIST_OF_CAREERS". In the "Enter Values" area, paste in the text from `slot-LIST_OF_CAREERS.txt`. Then click "Add".

6. In the "Sample Utterances" area, paste in the text from `sample-utterances.txt`. Then click "Next" and wait until the next screen loads.

7. In the "Endpoint" section, select the "AWS Lambda ARN" radio button. Click the "North America" checkbox. In the text field that appears, paste in the ARN you saved at the end of the Lambda setup. Then click "Next".

Now your demo skill is ready to use. If you have an Alexa device linked to your Amazon account, you can try out the skill by saying, "Alexa, ask O*NET Demo what an architect does". If you don't have a device, you can use the Service Simulator on the page you reached after the last step. Type in "what does an architect do" and click "Ask O\*NET Demo".



