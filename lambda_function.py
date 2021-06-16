# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model import Response, Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_core.utils import get_dialog_state
from ask_sdk_model import DialogState
from random import randrange

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "What are you looking for?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SearchPlaceIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SearchPlaceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        poi_name = slots["PlaceName"].value
        
        
        # api key will expire in an hour 
        api_key = 'ESJCQ7HePpH4c9gCYrIYbv4VOeoZqx_2DTlVp3iiyLM'
        url = 'https://discover.search.hereapi.com/v1/discover?at=37.78592,-122.40074&limit=1&apikey={api_key}&q={poi_name}'.format(poi_name=poi_name, api_key = api_key)
        
        r = requests.get(url)
        res = r.json()
        poi_name = res['items'][0]['title']
        poi_address = res['items'][0]['address']['city']
        
        poi_lat = str(res['items'][0]['position']['lat'])
        poi_lng = str(res['items'][0]['position']['lng'])
        poi_coord = str(poi_lat) + "," + str(poi_lng)
        poi_category = res['items'][0]['categories'][0]['name']
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["center_area"] = str(poi_coord)
        session_attr["api_key"] = str(api_key)
        session_attr["poi_name"] = str(poi_name)
        
        speak_output = "hello"
        
        if poi_category not in ['Railway Station','Taxi Stand', 'Light Rail']:
            speak_output = "I was able to find {poi_name}. It is in {poi_address}. By the way, you can ask for similar places around {poi_name}. Just say 'explore'".format(poi_name=poi_name, poi_address=poi_address)
            session_attr["category"] = str(poi_category)
        else:
            random_integer = randrange(0,2)
            speak_output_list = []
            category_list = []
            speak_output_list.append("I was able to find {poi_name}. It is in {poi_address}. There seems to be few things to see around the train station. Just say 'explore'".format(poi_name=poi_name, poi_address=poi_address))
            category_list.append("Tourist Attractions")
            speak_output_list.append("I was able to find {poi_name}. It is in {poi_address}. There seems to be few good places to eat around the train station. Just say 'explore'".format(poi_name=poi_name, poi_address=poi_address))
            category_list.append("Restaurants")
            session_attr["category"] = str(category_list[random_integer])
            speak_output = speak_output_list[random_integer]
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class RecommendIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RecommendIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        poi_coord = session_attr["center_area"]
        poi_category = session_attr["category"] 
        poi_name = session_attr["poi_name"] 
        api_key = session_attr["api_key"]
        
        url = 'https://discover.search.hereapi.com/v1/discover?at={poi_coord}&limit=5&apikey={api_key}&q={poi_category}'.format(poi_coord=str(poi_coord), poi_category=poi_category,api_key=api_key)
        
        r = requests.get(url)
        res = r.json()
        
        poi_name1 = res['items'][1]['title']
        poi_name2 = res['items'][2]['title']
        poi_name3 = res['items'][3]['title']
        poi_name4 = res['items'][4]['title']
        poi_street1 = res['items'][1]['address']['street']
        poi_street2 = res['items'][2]['address']['street']
        poi_street3 = res['items'][3]['address']['street']
        poi_street4 = res['items'][4]['address']['street']
        
        speak_output = "Here are few {poi_category}s around {poi_name}. One,  {poi_name1} on {poi_street1}, two, {poi_name2} on {poi_street2}, three, {poi_name3} on {poi_street3}, four, {poi_name4} on {poi_street4}.".format(poi_name=poi_name, poi_category=poi_category, poi_name1 = poi_name1, poi_name2=poi_name2, poi_name3=poi_name3, poi_name4=poi_name4, poi_street1=poi_street1, poi_street2=poi_street2,poi_street3=poi_street3,poi_street4=poi_street4)
        # speak_output = "hello"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RecommendIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(SearchPlaceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()