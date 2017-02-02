# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import random

PRESIDENTS = [("first","George Washington"),
("second","John Adams"),
("third","Thomas Jefferson"),
("fourth","James Madison"),
("fifth","James Monroe"),
("sixth","John Quincy Adams"),
("seventh","Andrew Jackson"),
("eighth","Martin Van Buren"),
("ninth","William Harrison"),
("tenth","John Tyler"),
("eleventh","James Polk"),
("twelfth","Zachary Taylor"),
("thirteenth","Millard Fillmore"),
("fourteenth","Franklin Pierce"),
("fifteenth","James Buchanan"),
("sixteenth","Abraham Lincoln"),
("seventeenth","Andrew Johnson"),
("eighteenth","Ulysses Grant"),
("nineteenth","Rutherford Hayes"),
("twentieth","James Garfield"),
("twenty first","Chester Arthur"),
("twenty second","Grover Cleveland"),
("twenty third","Benjamin Harrison"),
("twenty fourth","Grover Cleveland"),
("twenty fifth","William McKinley"),
("twenty sixth","Theodore Roosevelt"),
("twenty seventh","William Taft"),
("twenty eighth","Woodrow Wilson"),
("twenty ninth","Warren Harding"),
("thirtieth","Calvin Coolidge"),
("thirty first","Herbert Hoover"),
("thirty second","Franklin Roosevelt"),
("thirty third","Harry Truman"),
("thirty fourth","Dwight Eisenhower"),
("thirty fifth","John Kennedy"),
("thirty sixth","Lyndon Johnson"),
("thirty seventh","Richard Nixon"),
("thirty eighth","Gerald Ford"),
("thirty ninth","Jimmy Carter"),
("fortieth","Ronald Reagan"),
("forty first","George Bush"),
("forty second","Bill Clinton"),
("forty third","George Bush"),
("forty fourth","Barack Hussein Obama"),
("forty fifth","Donald Trump")]

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests
    to this function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.2277a42d-2ad9-4789-beac-821641d31f32"):
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
    """Called when the session starts"""

    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they
    want.
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill"""

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # handle yes/no intent after the user has been prompted
    if 'attributes' in session.keys() and 'user_prompted_to_continue' in session['attributes'].keys():
        del session['attributes']['user_prompted_to_continue']
        if intent_name == 'AMAZON.NoIntent':
            return handle_finish_session_request(intent, session)
        elif intent_name == "AMAZON.YesIntent":
            return handle_repeat_request(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "DontKnowIntent":
        return handle_dont_know_request(intent, session)
    if intent_name == "AnswerIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AnswerOnlyIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "DidntUnderstandIntent":    
        return handle_didnt_understand_request(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# ------- Skill specific business logic -------

ANSWER_COUNT = 1
GAME_LENGTH = 15
CARD_TITLE = " Presidents Flash Cards "  # Be sure to change this for your skill.

# --------------- Functions that control the skill's behavior -------------


def get_welcome_response():
    """
    If we wanted to initialize the session to have some attributes we could
    add those here
    """
    game_questions = populate_game_questions()

    current_questions_index = 0

    spoken_question = " Who was the " + PRESIDENTS[game_questions[current_questions_index]][0] + " President of the United States?"
    reprompt_text = spoken_question
    
    speech_output = ("Let's test your knowledge of the United States Presidents! I will ask you " +
                     str(GAME_LENGTH) + " questions, try to get as many right" +
                     "as you can. Just say the answer. Let's begin. " + spoken_question)
    should_end_session = False

    attributes = {"speech_output": reprompt_text,
                  "reprompt_text": reprompt_text,
                  "current_questions_index": current_questions_index,
                  "questions": game_questions,
                  "score": 0,
                  "correct_answer_text": PRESIDENTS[game_questions[current_questions_index]][1]
                  }
    return build_response(attributes, build_speechlet_response(
        CARD_TITLE, speech_output, reprompt_text, should_end_session))


def populate_game_questions():
    game_questions = []
    index_list = []
    index = len(PRESIDENTS)

    if GAME_LENGTH > index:
        raise ValueError("Invalid Game Length")

    for i in range(0, index):
        index_list.append(i)

    # Pick GAME_LENGTH random questions from the list to ask the user,
    # make sure there are no repeats
    game_questions = random.sample(index_list, GAME_LENGTH)

    return game_questions


def handle_didnt_understand_request(intent, session):
    attributes = {}
    should_end_session = False
    speech_output = "Sorry, I don't understand? Could you repeat that?"

    if 'attributes' in session.keys() and 'questions' in session['attributes'].keys():
        reprompt_text = session['attributes']["reprompt_text"]
        attributes = session['attributes']
        attributes[speech_output] = speech_output
    else:
        reprompt_text = speech_output
        attributes = {"speech_output": reprompt_text,
                      "reprompt_text": reprompt_text,
                      }

    return build_response(attributes, build_speechlet_response(CARD_TITLE,
                                                               speech_output, reprompt_text, should_end_session))


def handle_dont_know_request(intent, session):
    attributes = {}
    should_end_session = False

    if 'attributes' in session.keys() and 'questions' not in session['attributes'].keys():
        # If the user responded with an answer but there is no game
        # in progress ask the user if they want to start a new game.
        # Set a flag to track that we've prompted the user.
        attributes['user_prompted_to_continue'] = True
        speech_output = "There is no game in progress. " \
                        "Do you want to start a new game?"
        reprompt_text = speech_output
        return build_response(attributes, build_speechlet_response(CARD_TITLE,
                                                                   speech_output, reprompt_text, should_end_session))
    else:
        game_questions = session['attributes']['questions']
        current_score = session['attributes']['score']
        current_questions_index = session['attributes']['current_questions_index']
        correct_answer_text = session['attributes']['correct_answer_text']


        speech_output_analysis = ("The correct answer is " +
                                      correct_answer_text + ".")

        # if current_questions_index is 4, we've reached 5 questions
        # (zero-indexed) and can exit the game session
        if current_questions_index == GAME_LENGTH - 1:
            speech_output = (speech_output_analysis + "You got "
                             + str(current_score) + " out of " + str(GAME_LENGTH)
                             + " questions correct. Thank you for learning Flash"
                               " Cards with Alexa!")
            reprompt_text = None
            should_end_session = True
            return build_response(session['attributes'],
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text,
                                                           should_end_session))
        else:
            current_questions_index += 1
            spoken_question = "Who was the " + PRESIDENTS[game_questions[current_questions_index]][0] + " President of the United States?"

            reprompt_text = spoken_question
            speech_output = (speech_output_analysis +
                             " Your score is " +
                             str(current_score) + reprompt_text)
            attributes = {"speech_output": reprompt_text,
                          "reprompt_text": reprompt_text,
                          "current_questions_index": current_questions_index,
                          "questions": game_questions,
                          "score": current_score,
                          "correct_answer_text": PRESIDENTS[game_questions[current_questions_index]][1]
                          }

            return build_response(attributes,
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text,
                                                           should_end_session))

def handle_answer_request(intent, session):
    attributes = {}
    should_end_session = False
    #answer_slot_valid = is_answer_slot_valid(intent)

    if 'attributes' in session.keys() and 'questions' not in session['attributes'].keys():
        # If the user responded with an answer but there is no game
        # in progress ask the user if they want to start a new game.
        # Set a flag to track that we've prompted the user.
        attributes['user_prompted_to_continue'] = True
        speech_output = "There is no game in progress. " \
                        "Do you want to start a new game?"
        reprompt_text = speech_output
        return build_response(attributes, build_speechlet_response(CARD_TITLE,
                              speech_output, reprompt_text, should_end_session))
    else:
        game_questions = session['attributes']['questions']
        current_score = session['attributes']['score']
        current_questions_index = session['attributes']['current_questions_index']
        correct_answer_text = session['attributes']['correct_answer_text']

        speech_output_analysis = None
        if intent['slots']['Answer']['value'].lower() == correct_answer_text.lower():
            current_score += 1
            speech_output_analysis = "correct. "
        else:
            speech_output_analysis = "wrong. "
            speech_output_analysis = (speech_output_analysis +
                                      "The correct answer is " +
                                      correct_answer_text)

        # if current_questions_index is 4, we've reached 5 questions
        # (zero-indexed) and can exit the game session
        if current_questions_index == GAME_LENGTH - 1:
            speech_output = (speech_output_analysis + "You got "
                             + str(current_score) + " out of " + str(GAME_LENGTH)
                             + " questions correct. Thank you for learning Flash"
                             " Cards with Alexa!")
            reprompt_text = None
            should_end_session = True
            return build_response(session['attributes'],
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text, should_end_session))
        else:
            current_questions_index += 1
            spoken_question = "Who was the " + PRESIDENTS[game_questions[current_questions_index]][0] + " President of the United States?"


            reprompt_text = spoken_question
            speech_output = (speech_output_analysis +
                             " Your score is " +
                             str(current_score) + '. ' + reprompt_text)
            attributes = {"speech_output": reprompt_text,
                          "reprompt_text": reprompt_text,
                          "current_questions_index": current_questions_index,
                          "questions": game_questions,
                          "score": current_score,
                          "correct_answer_text": PRESIDENTS[game_questions[current_questions_index]][1]
                          }

            return build_response(attributes,
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text,
                                                           should_end_session))


def handle_repeat_request(intent, session):
    """
    Repeat the previous speech_output and reprompt_text from the
    session['attributes'] if available else start a new game session
    """
    if 'attributes' not in session or 'speech_output' not in session['attributes']:
        return get_welcome_response()
    else:
        attributes = session['attributes']
        speech_output = attributes['speech_output']
        reprompt_text = attributes['reprompt_text']
        should_end_session = False
        return build_response(attributes,
                              build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session))


def handle_get_help_request(intent, session):
    attributes = {}
    card_title = "Presidents Flash Cards"
    reprompt_text = ""
    speech_output = ""

    if 'attributes' in session.keys() and 'questions' in session['attributes'].keys():
        attributes = session['attributes']
        speech_output = ("You can answer by saying the first and last name of the President, or, "+
                         "if you don't know the answer, you can say: I don't know. " +
                         "If you didn't hear me, you can ask me to repeat the question. " +
                         "You can also say stop to quit.")
        reprompt_text = attributes['reprompt_text']
    else:
        speech_output = ("You can begin a game by saying start a new game, or, "
                         "you can say stop... What can I help you with?")
        reprompt_text = "What can I help you with?"
        attributes = {"speech_output": reprompt_text,
                      "reprompt_text": reprompt_text,
                      }
    should_end_session = False
    return build_response(attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



def handle_finish_session_request(intent, session):
    """
    End the session with a message
    if the user wants to quit the game
    """
    attributes = session['attributes']
    reprompt_text = None
    speech_output = "Okay, we can study again later!"
    should_end_session = True
    return build_response(attributes,
                          build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session))


def is_answer_slot_valid(intent):
    if 'Answer' in intent['slots'].keys() and 'value' in intent['slots']['Answer'].keys():
        return True
    else:
        return False


# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }