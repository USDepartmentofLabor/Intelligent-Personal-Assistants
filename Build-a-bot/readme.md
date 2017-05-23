# O*NET Demo Bot

## This is a demo of bot functionality based off of O*NET demo built in Lex.”

This directory contains a simple Lex Skill that calls [O*NET Web Services](https://services.onetcenter.org/). It returns the most important task statements for any of the 900+ careers in [My Next Move](https://www.mynextmove.org/).

## Installation

This skill is based on the Python "BookTrip" template from Amazon, using AWS Lambda to host the code. This guide assumes you have set up Amazon developer account(s); if not, you may need to go through some registration steps first.

### Part 1: Lambda setup

1. In the [Lambda management console](https://console.aws.amazon.com/lambda/home), switch to the "US East (N. Virginia)" region if needed.

2. Create a new function based on the "alexa-skills-kit-color-expert-python" template.

3. At the "Configure triggers" section, click Next.

4. At the "Configure function" section, add a name (it doesn't matter what name you choose), then scroll down.

5. At the "Lambda function code" section, delete the sample code and paste in the code from `lambda.py` in this repo. Further down, create two environment variables, named `onet_web_services_username` and `onet_web_services_password`. For the hackathon, contact Tom or Jeremiah for credentials, or [sign up](https://services.onetcenter.org/developer/signup) for an account. Then scroll down.

6. At the "Lambda function handler and role" section, under "Role" choose "Create new role from template(s)". Add a role name (it doesn't matter what name you choose) and add the "Simple Microservice permissions" template. Then click Next.

7. At the review screen, click "Create function" to finish the setup. Once it completes, take note of the **ARN** in the upper right corner -- you'll need that ID for the next step. Open a second browser, navigate back to the AWS Console - this time, open Lex.


### Part 2: Lex Skill setup

...coming soon...

