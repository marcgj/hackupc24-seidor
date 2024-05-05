# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import json
import pdf_gen
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Shop Assistant, How can I help you today?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask me where things are located! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloNameIntentHandler(AbstractRequestHandler):
    """Handler for Hello Name Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Obtener el nombre del slot "nombre"
        request = handler_input.request_envelope.request
        name = request.intent.slots["name"].value
        
        # Construir el saludo personalizado
        speak_output = f"Hi {name}, nice to meet you."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class ApiTestIntentHandler(AbstractRequestHandler):
    """Handler for Api testing."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ApiTestIntent")(handler_input)

    def handle(self, handler_input):
        # Hacer la solicitud GET a Google
        response = requests.get("https://www.google.com")
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            speak_output = "La API está funcionando correctamente."
        else:
            speak_output = "Hubo un problema al conectar con la API."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Hey Hey Hey little darling tell me what you need")
                .response
        )


class SearchItemIntentHandler(AbstractRequestHandler):
    """Search Items in the warehouse"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SearchItem")(handler_input)
        
    def handle(self, handler_input):
        # Hacer la solicitud GET a la API
        response = requests.get("http://194.164.171.6:8080/warehouse", params={"name": handler_input.request_envelope.request.intent.slots["ItemName"].value})
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                # Si hay un solo objeto, obtener su ubicación
                item = data[0]
                product_name = item["product"]["name"]
                location_name = item["locations"][0]["location"]["name"]
                aisle = item["locations"][0]["location"]["location_name"]
                speak_output = f"The {product_name} can be found at {location_name} in {aisle}."
            elif len(data) > 1:
                # Si hay más de un objeto, decir los nombres de los artículos encontrados
                item_names = [item["product"]["name"] for item in data]
                item_names_str = ", ".join(item_names)
                speak_output = f"More than one item found. The items found are: {item_names_str}. Please tell me which item you want."
                handler_input.attributes_manager.session_attributes["items"] = data
                # Guardar los artículos en los atributos de la sesión para usarlos más tarde
                handler_input.attributes_manager.session_attributes["asked_for_item"] = True
            else:
                speak_output = "No item found with that name."
        else:
            speak_output = "There was a problem connecting to the API."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What else can I help you with?")
                .response
        )

class SearchItemByDescriptionIntentHandler(AbstractRequestHandler):
    """Search Items in the warehouse"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SearchByDescription")(handler_input)
        
    def handle(self, handler_input):
        # Hacer la solicitud GET a la API
        response = requests.get("http://194.164.171.6:8080/warehouse", params={"description": handler_input.request_envelope.request.intent.slots["itemDescription"].value})
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            data = response.json()
            if len(data) == 1:
                # Si hay un solo objeto, obtener su ubicación
                item = data[0]
                product_name = item["product"]["name"]
                location_name = item["locations"][0]["location"]["name"]
                aisle = item["locations"][0]["location"]["location_name"]
                speak_output = f"The {product_name} can be found at {location_name} in {aisle}."
            elif len(data) > 1:
                # Si hay más de un objeto, decir los nombres de los artículos encontrados
                item_names = [item["product"]["name"] for item in data]
                item_names_str = ", ".join(item_names)
                speak_output = f"More than one item found. The items found are: {item_names_str}. Please tell me which item you want."
                handler_input.attributes_manager.session_attributes["items"] = data
                # Guardar los artículos en los atributos de la sesión para usarlos más tarde
                handler_input.attributes_manager.session_attributes["asked_for_item"] = True
            else:
                speak_output = "No item found with that name."
        else:
            speak_output = "There was a problem connecting to the API."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("How can I help you")
                .response
        )

class SelectItemByNumberIntentHandler(AbstractRequestHandler):
    """Handler for selecting item by number."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SelectItemByNumber")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Obtener el número del slot "orderOfItem"
        request = handler_input.request_envelope.request
        order_of_item = request.intent.slots["orderOfItem"].value
        
        # Verificar si el número es válido y dentro del rango de artículos devueltos
        session_attr = handler_input.attributes_manager.session_attributes
        items = session_attr.get("items", [])
        if items and order_of_item.isdigit() and 1 <= int(order_of_item) <= len(items):
            selected_item_index = int(order_of_item) - 1
            item = items[selected_item_index]
            product_name = item["product"]["name"]
            location_name = item["locations"][0]["location"]["name"]
            aisle = item["locations"][0]["location"]["location_name"]
            speak_output = f"The {product_name} can be found at {location_name} in {aisle}."
        else:
            speak_output = "Invalid item number. Please choose a valid number."
        
        items = []
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What else can I do for you?")
                .response
        )


class AddToInvoiceIntentHandler(AbstractRequestHandler):
    """Handler for adding item to invoice."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddToInvoice")(handler_input)

    def handle(self, handler_input):
        request = handler_input.request_envelope.request
        itemqty = request.intent.slots["itemqty"].value
        itemid = request.intent.slots["itemid"].value

        if itemqty is None:
            itemqty = 1
        
        data = {
            "id": 0,
            "item_id": str(itemid),
            "quantity": int(itemqty),
            "served": False
        }

        # Hacer la solicitud POST a la API
        response = requests.post("http://194.164.171.6:8080/list", json=data)
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            speak_output = "Item added to the invoice successfully."
        else:
            speak_output = "There was a problem connecting to the API."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Do you want more products?")
                .response
        )


class FinishInvoiceIntentHandler(AbstractRequestHandler):
    """Handler for adding item to invoice."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FinishInvoice")(handler_input)

    def handle(self, handler_input):
        print("boo")
        response = requests.get("http://194.164.171.6:8081/createpdf")
        return (
            handler_input.response_builder
                .speak("You should receive the invoice in your Telegram soon. Thank you for shopping with us.")
                .ask("What else can I help you with?")
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
        speak_output = "See you Soon!"

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
        speech = "Hmm, I'm not sure. You can say ask me where is an Item or to start a invoice. What would you like to do?"
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

sb.add_request_handler(HelloNameIntentHandler())
sb.add_request_handler(ApiTestIntentHandler())
sb.add_request_handler(SearchItemIntentHandler())
sb.add_request_handler(SelectItemByNumberIntentHandler())
sb.add_request_handler(AddToInvoiceIntentHandler())
sb.add_request_handler(SearchItemByDescriptionIntentHandler())
sb.add_request_handler(FinishInvoiceIntentHandler())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()