import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UpsellResponseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Connections.Response')(handler_input) and
                handler_input.request_envelope.request.name == 'Upsell')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        logger.info('In UpsellResponseHandler')

        if handler_input.request_envelope.request.status.code == '200':
            if handler_input.request_envelope.request.payload.get('purchaseResult') == PurchaseResult.DECLINED.value:
                speech = '綺麗な水を購入する必要があります。詳細を聞きますか？'
                reprompt = speech
                return handler_input.response_builder.speak(speech).ask(reprompt).response

        else:
            logger.log(f'Connections.Response indicated failure. Error: {handler_input.request_envelope.request.status.message}')
            speech = ('アップセルリクエストの処理中にエラーが発生しました。'
                      'もう一度やり直すか、お問い合わせください。')
            return handler_input.response_builder.speak(speech).response
