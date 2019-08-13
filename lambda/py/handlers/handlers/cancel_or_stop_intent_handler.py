# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from alexa import data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # TODO withShouldEndSession
        # type: (HandlerInput) -> Response
        speech_text = 'まいにちさぼてんをひらいてくれてありがとうございました。つぎはさぼてんに水を上げてくれると嬉しいです。'

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(data.SKILL_NAME, speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response
