from __future__ import print_function
import urllib2
import json
import difflib

LINODE_URL = ''
ALEXA_APP_ID = ''

STOP_NAMES = {
    'Eighth': 184,
    'Sixth': 281,
    'Fourteenth': 309,
    'Union Square': 309,
    'Union': 309,
    'Square': 309,
    'Third': 140,
    'First': 139,
    'Bedford': 138,
    'Lorimer': 5,
    'Graham': 263,
    'Grand': 264,
    'Montrose': 265,
    'Morgan': 259,
    'Jefferson': 260,
    'Dekalb': 261,
    'Mrytle Wyckoff': 262,
    'Wyckoff Mrytle': 262,
    'Mrytle': 262,
    'Halsey': 258,
    'Wilson': 394,
    'Moffat':394,
    'Aberdeen': 393,
    'Brodway': 26,
    'Brodway Junction': 26,
    'Junction': 26,
    'Fulton': 26,
    'Atlantic': 396,
    'Snediker': 396,
    'Sutter': 395,
    'Livonia': 288,
    'New Lots': 397,
    'East one hundred and fifth': 400,
    'one hundred and fifth': 400,
    'Turnbul': 400,
    'Canarsie': 399,
    'Rockaway': 399,
    'Glenwood': 399,
    'Metropolitan Lorimer': 5,
    'Lorimer Metropolitan': 5,
    'Metropolitan': 5,
}

STOP_NAMES_LIST = [
    'Eighth',
    'Sixth',
    'Fourteenth',
    'Union Square',
    'Union',
    'Square',
    'Third',
    'First',
    'Bedford',
    'Lorimer',
    'Graham',
    'Grand',
    'Montrose',
    'Morgan',
    'Jefferson',
    'Dekalb',
    'Mrytle Wyckoff',
    'Wyckoff Mrytle',
    'Mrytle',
    'Halsey',
    'Wilson',
    'Moffat',
    'Aberdeen',
    'Brodway',
    'Brodway Junction',
    'Junction',
    'Fulton',
    'Atlantic',
    'Snediker',
    'Sutter',
    'Livonia',
    'New Lots',
    'East one hundred and fifth',
    'one hundred and fifth',
    'Turnbul',
    'Canarsie',
    'Rockaway',
    'Glenwood',
    'Metropolitan Lorimer',
    'Lorimer Metropolitan',
    'Metropolitan',
]

STOP_SAY = {
    184: "8th Avenue, 14th Street",
    281: "6th Avenue, 14th Street",
    309: "14 Street, Union Square",
    140: "6rd Avenue, 14th Street",
    139: "1st Avenue, 14th Street",
    138: "Bedford Avenue, North 7th Street",
    5: "Lorimer Street, Metropolitan Avenue",
    263: "Graham Avenue, Metropolitan Avenue",
    264: "Grand Street, Bushwick Avenue",
    265: "Montrose Avenue, Bushwick Avenue",
    259: "Morgan Avenue, Harrison Place",
    260: "Jefferson Street, Wyckoff Avenue",
    261: "DeKalb Avenue, Wyckoff Avenue",
    262: "Myrtle Wyckoff Avenues",
    258: "Halsey Street, Wyckoff Avenue",
    394: "Wilson Avenue, Moffat Street",
    393: "Bushwick Avenue, Aberdeen Street",
    26: "Broadway Junction, Fulton Street",
    396: "Atlantic Avenue, Snediker Avenue, Van Sinderen Avenue",
    395: "Sutter Avenue, Van Sinderen Avenue",
    288: "Livonia Avenue, Van Sinderen Avenue",
    397: "New Lots Avenue, Van Sinderen Avenue",
    400: "East 105 Street, Turnbull Avenue",
    399: "Canarsie-Rockaway Parkway, Glenwood Road",
}


DIRECTIONS = {
    'West': 'N',
    'East': 'S',
    'North': 'N',
    'South': 'S',
    'Manhattan': 'N',
    'Brooklyn': 'S',
    'Eight': 'N',
    'Eight Ave': 'N',
    'Eighth': 'N',
    'Eighth Ave': 'N',
    'Canarsie Rockaway': 'S',
    'Canarsie Rockaway Parkway': 'S',
    'Canarsie': 'S',
    'Rockaway Parkway': 'S',
}

DIRECTIONS_LIST = [
    'West',
    'East',
    'North',
    'South',
    'Manhattan',
    'Brooklyn',
    'Eight',
    'Eight Ave',
    'Eighth',
    'Eighth Ave',
    'Canarsie Rockaway',
    'Canarsie Rockaway Parkway',
    'Canarsie',
    'Rockaway Parkway',
]

class Speech:
    def trainTime(self, say, repeat):
        session_attributes = {'trainTime': True}
        card_title = "The L Train"
        speech_output = say
        should_end_session = True
        reprompt_text = ""
        return build_response(
            session_attributes, 
            build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
        )
        
    def getStation(self, say, repeat):
        session_attributes = {'getStation': True}
        session_attributes = {}
        card_title = "The L Train"
        speech_output = say
        should_end_session = False
        reprompt_text = "I could not find that station, what is the name of your L station again?"

        if repeat:
            speech_output = reprompt_text

        return build_response(
            session_attributes, 
            build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
        )
    
    def getDirection(self, say, repeat):
        session_attributes = {'getDirection': True}
        card_title = "The L Train"
        speech_output = say
        should_end_session = False
        reprompt_text = "I dont understand that direction, what direction do you travel on the L train again?"

        if repeat:
            speech_output = reprompt_text

        return build_response(
            session_attributes, 
            build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
        )

    def intro(self, say, repeat):
        session_attributes = {'intro': True}
        card_title = "Welcome To the L Train"
        speech_output = "What is the station you would like train times for? For example: Jefferson Street Or Union Square."
        if say:
            speech_output = say
        should_end_session = False
        reprompt_text = "I could not find that station, what is the name of your L station again?"

        if repeat:
            speech_output = reprompt_text
        
        return build_response(
            session_attributes, 
            build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
        )

def lambda_handler(event, context):
    if (event['session']['application']['applicationId'] !=
            ALEXA_APP_ID):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    query = "%s?user=%s" % (LINODE_URL, str(session['user']['userId']))
    data = json.loads(urllib2.urlopen(query).read())
    speech = Speech()
    try:
        say = data['say']
    except:
        say = ""
    return getattr(speech, data['function'])(say, False)

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    print("------intent_name------>")
    print(intent_name)
    print(intent_request)

    print("------ session ---------")
    print(session)

    user_id = session['user']['userId']
    if intent_name == "SaveTrainStation":
        try:
            station = intent_request['intent']['slots']['TrainStation']['value']
            station = difflib.get_close_matches(station, STOP_NAMES_LIST)[0]
            station = STOP_NAMES[station]
            query = '%s?user=%s&station=%s' % (LINODE_URL, user_id, station)
        except:
            query = '%s?user=%s' % (LINODE_URL, user_id)
    elif intent_name == 'SaveTrainDirection':
        try:
            direction = intent_request['intent']['slots']['TrainDirection']['value']
            direction = difflib.get_close_matches(direction, DIRECTIONS_LIST)[0]
            direction = DIRECTIONS[direction]
            query = '%s?user=%s&direction=%s' % (LINODE_URL, user_id, direction)
        except:
            query = '%s?user=%s' % (LINODE_URL, user_id)
    else:
        query = '%s?user=%s' % (LINODE_URL, user_id)

    print("QUERY ------->")
    print(query)

    data = json.loads(urllib2.urlopen(query).read())
    speech = Speech()
    try:
        say = data['say']
    except:
        say = ""

    print("Call Speech ----->")
    print(data['function'])
    print(say)

    repeat = False
    if 'attributes' in session and data['function'] in session['attributes']:
        repeat = True

    return getattr(speech, data['function'])(say, repeat)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    pass

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    print("build_speechlet_response build_speechlet_response build_speechlet_response ---->")
    print(title)
    print(output)
    
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': str(title),
            'content': str(output),
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
