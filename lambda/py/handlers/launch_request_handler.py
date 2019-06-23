# -*- coding: utf-8 -*-

import logging

from ask_sdk.standard import StandardSkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import StandardCard
from ask_sdk_model import Response

from ssml_builder.core import Speech

from alexa import data
from alexa import utils

sb = StandardSkillBuilder(table_name="cactus", auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        attr = handler_input.attributes_manager.persistent_attributes
        try:
            attr['height']
        except NameError:
            height = 0
        else:
            height = attr['height']

        speech = Speech()
        speech.add_text(data.WELCOME_MESSAGE)
        speech.add_text('身長は{}センチメートルです。'.format(str(height)))
        speech.add_text('さぼてんに水をあげますか？')
        speech_text = speech.speak()


        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(data.SKILL_NAME, speech_text)).set_should_end_session(
            False)

        # set confirmation status
        handler_input.attributes_manager.session_attributes['status'] = 'confirmation'
        
        return handler_input.response_builder.response