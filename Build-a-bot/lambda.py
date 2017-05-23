"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which looks up job descriptions from ETA's O*NET API.
"""
from __future__ import print_function
import json
import datetime
import time
import os
import dateutil.parser
import logging
import urllib
import urllib2
import xml.etree.ElementTree
import os
import base64




logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---

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


""" --- Functions that control the bot's behavior --- """


def learn_about_jobs(intent_request):
    """
    Performs dialog management and fulfillment for booking a hotel.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    career_name = intent_request['currentIntent']['slots']['JobName']
   
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    search_res = call_onet_service('mnm/search', {'keyword': career_name})
    onet_code = search_res.find('career').find('code').text
    career_res = call_onet_service('mnm/careers/' + onet_code + '/')
    onet_title = career_res.find('title').text
    speech_output = "On the job, " + onet_title + " will:"
    for task_el in career_res.find('on_the_job').findall('task'):
        speech_output += " " + task_el.text
            
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': speech_output
        }
    )



# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'LearnAboutJobs':
        return learn_about_jobs(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
