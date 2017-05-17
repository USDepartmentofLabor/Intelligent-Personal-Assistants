from __future__ import print_function
import urllib
import urllib2
import xml.etree.ElementTree
import os
import base64

# -------------- Helpers for O*NET Web Services --------------------------------

def add_onet_authorization(req):
    auth_str = os.environ['onet_web_services_username'] + \
               ':' + \
               os.environ['onet_web_services_password']
    req.add_header('Authorization', 'Basic ' + \
                   base64.b64encode(auth_str))

def call_onet_service(path, params=None):
    url = 'https://services.onetcenter.org/ws/' + path
    if params is not None:
        url += '?' + urllib.urlencode(params)
    req = urllib2.Request(url)
    add_onet_authorization(req)
    response = urllib2.urlopen(req)
    return xml.etree.ElementTree.fromstring(response.read())


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_on_the_job_response(intent, session):
    """ Reads tasks from the requested career.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Career' in intent['slots'] and intent['slots']['Career']['value']:
        career_name = intent['slots']['Career']['value']
        
        search_res = call_onet_service('mnm/search', {'keyword': career_name})
        onet_code = search_res.find('career').find('code').text
        career_res = call_onet_service('mnm/careers/' + onet_code + '/')
        onet_title = career_res.find('title').text
        
        card_title = "What " + onet_title + " do on the job"
        speech_output = "On the job, " + onet_title + " will:"
        for task_el in career_res.find('on_the_job').findall('task'):
            speech_output += " " + task_el.text
    else:
        speech_output = "I didn't understand that career. " \
                        "Please try again."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the O*NET Demo skill. " \
                    "Please ask me about a career by saying, " \
                    "what does an architect do?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me about a career by saying, " \
                    "what does an architect do?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the O*NET Demo skill."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "OnTheJobIntent":
        return get_on_the_job_response(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent: " + intent_name)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
