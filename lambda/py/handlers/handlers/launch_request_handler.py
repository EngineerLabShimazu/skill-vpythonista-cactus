# -*- coding: utf-8 -*-

import os
import datetime
import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_content
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective,
    BackButtonBehavior, BodyTemplate2)
from ssml_builder.core import Speech
from alexa import data
from alexa import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        last_watered_date = utils.get_last_watered_date(handler_input)

        height = utils.get_cactus_height(handler_input)

        speech_text = LaunchResponseCreator().create_response(
            height, last_watered_date, handler_input
        )
        cactus_image = utils.ImageGetter().get_image(
            utils.get_level(height), utils.select_scene()
        )
        logger.info(f'launch_h, cactus_image: {cactus_image}')
        ret_img = Image(sources=[ImageInstance(url=cactus_image)])

        primary_text = get_plain_text_content(
            primary_text="")

        if utils.supports_apl(handler_input):
            handler_input.response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate2(
                        back_button=BackButtonBehavior.VISIBLE,
                        image=ret_img, title=data.SKILL_NAME,
                        text_content=primary_text))
            )

        handler_input.response_builder.set_card(
            ui.StandardCard(
                title=data.get_standard_card_title(height),
                text=data.get_standard_card_text(height),
                image=ui.Image(
                    small_image_url=cactus_image,
                    large_image_url=cactus_image
                )
            )
        )

        should_end_session = True
        status = 'check_state'

        scene = get_scene(handler_input)
        if scene == 'water':
            should_end_session = False
            status = 'confirmation'
        elif scene == 'upsell':
            should_end_session = False
            status = 'isp_better_water'

        handler_input.attributes_manager.session_attributes[
            'status'] = status
        if should_end_session:
            return handler_input.response_builder.speak(speech_text).set_should_end_session(should_end_session).response
        return handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(should_end_session).response


class LaunchResponseCreator:
    def __init__(self):
        self.speech = Speech()

    def create_response(self, height, last_watered_date, handler_input):
        self.pre_response()

        if height == 0:
            return self.seed_response()

        self.base_launch_response(height)

        if utils.can_water(last_watered_date):
            return self.can_water_response(handler_input)

        return self.cannot_water_response(height, handler_input)

    def pre_response(self):
        if os.environ.get('AWS_LAMBDA_FUNCTION_VERSION') == '$LATEST':
            self.speech.add_text('デブです。')

    def seed_response(self):
        self.speech.add_text('そういえば、さぼてんの種を拾ったんですよね。'
                             '一緒に育てませんか？')
        return self.speech.speak()

    def base_launch_response(self, height):
        self.speech.add_text(f'はい、きみのサボテンはこちらです。'
                             f'全長は{height}ミリメートルです。')
        return self.speech.speak()

    def can_water_response(self, handler_input):
        speech = f'さぼてんに水をあげますか？'
        if utils.is_subscriptable(handler_input):
            # TODO BuyIntentHandlerに飛ばせるか、、、？
            # return GetFactHandler().handle(handler_input)
            speech = f'さぼてんに綺麗な水をあげますか？'
        self.speech.add_text(speech)
        return self.speech.speak()

    def cannot_water_response(self, height, handler_input):
        # TODO ISP対応 課金してなければアップセル
        if not utils.is_subscriptable(handler_input):
            self.speech.add_text(f'綺麗な水を購入して、さぼてんの成長をもっと早くしますか？')
        # 'さぼてんの形がどんどん変わっていくのを見るのって楽しいですよね。'
        else:
            tomorrow = self.speech.sub(value="明日", alias="あした", is_nested=True)
            self.speech.add_text(f'また{tomorrow}水やりしてくださいね。')
        return self.speech.speak()


def get_scene(handler_input):
    # 水をあげる
    if utils.can_water(utils.get_last_watered_date(handler_input)):
        return 'water'

    # 水は上げれないけど、課金する？
    if not utils.is_subscriptable(handler_input):
        return 'upsell'

    # 水も課金もできないので様子を見てsession終了
    return 'check_state'
