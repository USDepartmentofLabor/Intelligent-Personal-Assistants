from __future__ import print_function
import urllib
import urllib2
import os
import json

# --------------- Helpers that call COS web services ---------------------------

def call_cos_service(api, params=None, query=None):
    url = 'https://api.careeronestop.org/v1/' + api + \
          '/' + os.environ['cos_web_api_userid'] + '/'
    
    def quoter(item):
        return urllib.quote_plus('{}'.format(item))
    
    if params is not None:
        url += '/'.join(map(quoter, params))
    if query is not None:
        url += '?' + urllib.urlencode(query)
    req = urllib2.Request(url)
    req.add_header('Authorization', 'Bearer ' + os.environ['cos_web_api_token'])
    req.add_header('Accept', 'application/json')
    response = urllib2.urlopen(req)
    resp_raw = response.read()
    return json.loads(resp_raw)

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

def build_permission_response(title, output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'permissions': [
                'read::alexa:device:all:address:country_and_postal_code'
            ]
        },
        'shouldEndSession': True
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def call_cos_for_ajc(zip_code):
    params = [ zip_code, 50, 0, 0, 0, 0, 'GEOCODE', 0, 0, 10 ]
    ajc_response = call_cos_service('ajcfinder', params)
    
    try:
      closest_ajc = ajc_response['OneStopCenterList'][0]
      speech_output = "Your closest American Job Center is " + \
                      closest_ajc['Distance'] + " miles away. " + \
                      closest_ajc['Name'] + "; " + \
                      closest_ajc['Address1'] + "; " + \
                      closest_ajc['City'] + ", " + \
                      closest_ajc['StateName'] + ". " + \
                      "Telephone: " + closest_ajc['Phone'] + "."
    except:
      speech_output = "I cannot find the closest Job Center right now. " + \
                      "Please try again later. " + \
                      "Goodbye."
    return speech_output

def get_closest_ajc_response(intent, session, eventContext):
    """ Returns the nearest AJC from CareerOneStop, using
        the ZIP code associated with the Alexa device.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    
    try:
      consent_token = eventContext['System']['user']['permissions']['consentToken']
      api_endpoint = eventContext['System']['apiEndpoint']
      device_id = eventContext['System']['device']['deviceId']
    except:
      consent_token = None
      api_endpoint = None
      device_id = None
    
    if consent_token and api_endpoint and device_id:
      url = api_endpoint + '/v1/devices/' + device_id + '/settings/address/countryAndPostalCode'
      req = urllib2.Request(url)
      req.add_header('Authorization', 'Bearer ' + consent_token)
      response = urllib2.urlopen(req)
      addr_data = json.loads(response.read())
      
      try:
        zip_code = addr_data['postalCode']
      except:
        zip_code = None
      
      if zip_code:
        speech_output = call_cos_for_ajc(zip_code)
      else:
        speech_output = "I cannot read your ZIP code right now. " + \
                        "Goodbye."
    else:
      speech_output = "I cannot read your ZIP code right now. " + \
                      "Please grant permission in the Alexa app. " + \
                      "Goodbye."
      
      ## DEBUG
      # speech_output = call_cos_for_ajc(90210)
      
      return build_response(session_attributes, build_permission_response(
          card_title, speech_output))
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the AJC Finder. " + \
                    "Please ask me, where is my closest Job Center?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me, where is my closest Job Center?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the AJC Finder."
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


def on_intent(intent_request, session, eventContext):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ClosestCenterIntent":
        return get_closest_ajc_response(intent, session, eventContext)
        # return get_on_the_job_response(intent, session)
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
    
    try:
      eventContext = event['context']
    except:
      eventContext = None
    
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
        return on_intent(event['request'], event['session'], eventContext)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
