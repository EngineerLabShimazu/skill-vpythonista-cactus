import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult
from alexa import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BuyResponseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Connections.Response')(handler_input) and
                handler_input.request_envelope.request.name == 'Buy')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        logger.info("In BuyResponseHandler")
        in_skill_response = utils.in_skill_product_resposne(handler_input)
        if in_skill_response:
            logger.info(f'in_skill_response {in_skill_response}')
            product_id = handler_input.request_envelope.request.payload.get(
                'productId'
            )
            product = [l for l in in_skill_response.in_skill_products
                       if l.product_id == product_id]
            if handler_input.request_envelope.request.status.code == '200':
                purchase_result = handler_input.request_envelope.request.payload.get(
                    'purchaseResult'
                )
                speech = '購入できませんでした。音声ショッピングの設定やお支払い方法をご確認ください。'
                ask = 'さぼてんの様子を確認しますか？'
                status = 'check_status'
                if utils.can_water(utils.get_last_watered_date(handler_input)):
                    ask = 'さぼてんに水をあげますか？'
                    status = 'confirmation'
                handler_input.attributes_manager.session_attributes[
                    'status'] = status
                if purchase_result == PurchaseResult.ACCEPTED.value:
                    speech = ('綺麗な水がアンロックされました。'
                              '次の水やりからさぼてんの成長が1.5倍になります。')
                elif purchase_result in PurchaseResult.DECLINED.value:
                    speech = ''
                elif purchase_result == PurchaseResult.ERROR.value:
                    speech = ('すみません。綺麗な水の定期購入は'
                              'うまく処理できませんでした。')
                elif purchase_result == PurchaseResult.ALREADY_PURCHASED.value:
                    # speech = '綺麗な水はすでに定期購入済みです。'
                    speech = ''
                elif purchase_result == PurchaseResult.NOT_ENTITLED.value:
                    speech = '購入済みなのでキャンセルできませんでした。'

                return handler_input.response_builder.speak(
                    speech + ask).ask(ask).response
        else:
            return handler_input.response_builder.speak(
                '購入処理でエラーが発生しました。'
                'もう一度試すか、カスタマーサービスにご連絡ください。'
            ).response
