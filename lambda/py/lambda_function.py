# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import os
from ask_sdk.standard import StandardSkillBuilder
from handlers.launch_request_handler import LaunchRequestHandler
from handlers.buy_handler import BuyHandler
from handlers.buy_response_handler import BuyResponseHandler
from handlers.upsell_response_handler import UpsellResponseHandler
from handlers.cancel_subscription_handler import CancelSubscriptionHandler
from handlers.cancel_response_handler import CancelResponseHandler
from handlers.yes_intent_handler import YesIntentHandler
from handlers.no_intent_handler import NoIntentHandler
from handlers.help_intent_handler import HelpIntentHandler
from handlers.cancel_or_stop_intent_handler import CancelOrStopIntentHandler
from handlers.session_ended_request_handler import SessionEndedRequestHandler
from handlers.catch_all_exception_handler import CatchAllExceptionHandler

table_name = 'cactus'
if os.environ.get('AWS_LAMBDA_FUNCTION_VERSION') == '$LATEST':
    table_name = 'cactus-dev'
sb = StandardSkillBuilder(table_name=table_name, auto_create_table=True)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CancelResponseHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())

# ISP
sb.add_request_handler(BuyHandler())
sb.add_request_handler(BuyResponseHandler())
sb.add_request_handler(UpsellResponseHandler())
sb.add_request_handler(CancelSubscriptionHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
