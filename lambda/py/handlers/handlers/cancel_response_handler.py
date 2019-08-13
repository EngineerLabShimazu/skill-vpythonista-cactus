import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult
from alexa import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CancelResponseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Connections.Response')(handler_input) and
                handler_input.request_envelope.request.name == 'Cancel')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        logger.info('In CancelResponseHandler')
        in_skill_response = utils.in_skill_product_resposne(handler_input)
        product_id = handler_input.request_envelope.request.payload.get(
            'productId')

        if in_skill_response:
            product = [l for l in in_skill_response.in_skill_products
                       if l.product_id == product_id]
            logger.info(f'Product = {product}')
            if handler_input.request_envelope.request.status.code == '200':
                purchase_result = handler_input.request_envelope.request.payload.get(
                    'purchaseResult'
                )
                # purchasable = product[0].purchasable

                speech = 'さぼてんの様子を確認しますか？'
                status = 'check_status'
                if utils.can_water(utils.get_last_watered_date(handler_input)):
                    speech = 'さぼてんに水をあげますか？'
                    status = 'confirmation'

                if purchase_result == PurchaseResult.ACCEPTED.value:
                    # TODO if can_water さぼてんに水をあげますか？ else さぼてんの様子を確認しますか？
                    # speech = '綺麗な水のサブスクリプションのキャンセルに成功しました。'
                    pass
                if purchase_result == PurchaseResult.DECLINED.value:
                    speech = '分かりました。'
                if purchase_result == PurchaseResult.NOT_ENTITLED.value:
                    speech = '綺麗な水を購入しますか？'
                    status = 'isp_better_water'
                    pass
                handler_input.attributes_manager.session_attributes[
                    'status'] = status
                if speech:
                    return handler_input.response_builder.speak(
                        speech).set_should_end_session(False).response
            else:
                logger.log(f'Connections.Response indicated failure. '
                           f'Error: {handler_input.request_envelope.request.status.message}')
                return handler_input.response_builder.speak(
                    'キャンセル処理でエラーが発生しました。'
                    'もう一度試すか、カスタマーサービスにご連絡ください。'
                ).response
