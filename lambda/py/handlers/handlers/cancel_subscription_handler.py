import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.interfaces.connections import SendRequestDirective
from alexa import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CancelSubscriptionHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name('CancelSubscriptionIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        logger.info('In CancelSubscriptionHandler')

        in_skill_response = utils.in_skill_product_resposne(handler_input)
        if in_skill_response:
            product_category = 'better_water'
            product = [l for l in in_skill_response.in_skill_products
                       if l.reference_name == product_category]
            return handler_input.response_builder.add_directive(
                SendRequestDirective(
                    name='Cancel',
                    payload={
                        'InSkillProduct': {
                            'productId': product[0].product_id
                        }
                    },
                    token='correlationToken'
                )
            ).response
