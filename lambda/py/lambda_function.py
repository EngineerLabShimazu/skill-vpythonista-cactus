# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from handlers.launch_request_handler import LaunchRequestHandler
from handlers.hello_world_intent_handler import HelloWorldIntentHandler
from handlers.help_intent_handler import HelpIntentHandler
from handlers.cancel_or_stop_intent_handler import CancelOrStopIntentHandler
from handlers.session_ended_request_handler import SessionEndedRequestHandler
from handlers.catcfh_all_exception_handler import CatchAllExceptionHandler

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
