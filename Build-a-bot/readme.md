# O*NET ChatBot Demo

## This is a demo of ChatBot functionality built in Lex - based off of O*NET Alexa Skill demo.”

This directory contains a simple Lex Skill that calls [O*NET Web Services](https://services.onetcenter.org/). It returns the most important task statements for any of the 900+ careers in [My Next Move](https://www.mynextmove.org/).

## Installation

This skill is based on the "BookTrip" template from Amazon, using AWS Lambda to host the code. This guide assumes you have set up Amazon developer account(s); if not, you may need to go through some registration steps first.

### Part 1: Lambda setup

1. In the [Lambda management console](https://console.aws.amazon.com/lambda/home), switch to the "US East (N. Virginia)" region if needed.

2. Create a new function based on the "lex-book-trip-python" template.

3. At the "Configure triggers" section, click Next.

4. At the "Configure function" section, add a name (it doesn't matter what name you choose), and description - then scroll down.

5. At the "Lambda function code" section, delete the sample code and paste in the code from `lambda.py` in this repo. Further down, create two environment variables, named `onet_web_services_username` and `onet_web_services_password`. For the hackathon, contact Tom or Jeremiah for credentials, or [sign up](https://services.onetcenter.org/developer/signup) for an account. Then scroll down.

6. At the "Lambda function handler and role" section, under "Role" choose "Create new role from template(s)". Add a role name (it doesn't matter what name you choose) and add the "Simple Microservice permissions" template. Then click Next.

7. At the review screen, click "Create function" to finish the setup. Once it completes, open a second browser, navigate back to the AWS Console - this time, open Lex.


### Part 2: Lex Skill setup

1. From the Lex Bots page, "Create" a new bot.

2. At the Create your Lex bot page, base your bot off of "BookTrip", give your bot a name, and select the approrpriate response to the Child-directed question.

3. Once your bot is finished creating, in the Editor Tab, find your bot name with the gray down arrow next to it - be sure that you are on "Latest" in order to make changes.

4. Enter the utterances that would invoke your intent.

5. Add the slot(s) you need to handle the variables you will need to execute your skill.

6. Under the Fullfillment section, select AWS Lambda Function and select the function you built in Part 1.

7. Save your Intent.

8. Build your bot.

9. After it builds successfully, you can test your chatbot with the built in Test Bot.
