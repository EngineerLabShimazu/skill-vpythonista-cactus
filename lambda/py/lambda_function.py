# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
from ask_sdk.standard import StandardSkillBuilder
from handlers.launch_request_handler import LaunchRequestHandler
from handlers.yes_intent_handler import YesIntentHandler
from handlers.help_intent_handler import HelpIntentHandler
from handlers.cancel_or_stop_intent_handler import CancelOrStopIntentHandler
from handlers.session_ended_request_handler import SessionEndedRequestHandler
from handlers.catch_all_exception_handler import CatchAllExceptionHandler

sb = StandardSkillBuilder(table_name="cactus", auto_create_table=True)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
