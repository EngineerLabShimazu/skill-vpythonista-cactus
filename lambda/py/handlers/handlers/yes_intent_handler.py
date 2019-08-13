# -*- coding: utf-8 -*-

import datetime
import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_content
from ask_sdk_model import ui
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective,
    BackButtonBehavior, BodyTemplate2)
from ssml_builder.core import Speech
from alexa import data
from alexa import utils
from handlers.buy_handler import BuyHandler
from decimal import Decimal


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # TODO separate water handler and CheckStatus
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        status = handler_input.attributes_manager.session_attributes.get('status')
        attr = handler_input.attributes_manager.persistent_attributes
        
        if status == 'confirmation':
            before_height = attr.get('height')
            in_skill_response = utils.in_skill_product_resposne(handler_input)
            logger.info(f'in_skill_response: {in_skill_response}')
            grow_rate_of_up = 1.0
            if utils.is_subscriptable(handler_input):
                grow_rate_of_up = 1.5
            grow = utils.get_grow_value() * Decimal(grow_rate_of_up)
            grow_height = before_height + grow if before_height else grow
            attr['height'] = grow_height
            attr['last_watered_date'] = str(datetime.date.today())
            handler_input.attributes_manager.persistent_attributes = attr
            handler_input.attributes_manager.save_persistent_attributes()

            speech = Speech()
            speech.audio(utils.get_sound_url(data.SOUND_FLOWER))
            if not before_height:
                speech.add_text(f"""
                <say-as interpret-as="interjection">わ〜い</say-as>。
                とっても可愛いですね！
                全長は{grow_height}ミリメートルです。
                明日の様子も楽しみですね。
                """)
            else:
                speech.add_text(f"""
                水やりが終わりました。
                {grow}ミリ成長しました！
                全長は{grow_height}ミリメートルです。
                明日も成長が楽しみですね。
                """)
            speech_text = speech.speak()

            cactus_image = utils.ImageGetter().get_image(
                utils.get_level(grow_height), utils.select_scene()
            )
            ret_img = Image(sources=[ImageInstance(url=cactus_image)])
            title = data.SKILL_NAME
            primary_text = get_plain_text_content(
                primary_text="")

            if utils.supports_apl(handler_input):
                handler_input.response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate2(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=ret_img, title=title,
                            text_content=primary_text
                        ))).set_should_end_session(True)

            handler_input.response_builder.set_card(
                ui.StandardCard(
                    title=data.get_standard_card_title(grow_height),
                    text=data.get_standard_card_text(grow_height),
                    image=ui.Image(
                        small_image_url=cactus_image,
                        large_image_url=cactus_image
                    )
                )
            )

            return handler_input.response_builder.speak(speech_text).response
        elif status == 'check_status':
            height = utils.get_cactus_height(handler_input)
            speech = Speech()
            speech.add_text(f'全長は{height}ミリメートルです。'
                            f'明日も成長が楽しみですね。')
            speech_text = speech.speak()
            cactus_image = utils.ImageGetter().get_image(
                utils.get_level(height), utils.select_scene()
            )
            ret_img = Image(sources=[ImageInstance(url=cactus_image)])
            primary_text = get_plain_text_content(primary_text='')

            if utils.supports_apl(handler_input):
                handler_input.response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate2(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=ret_img, title=data.SKILL_NAME,
                            text_content=primary_text
                        )
                    )
                ).set_should_end_session(True)

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
            return handler_input.response_builder.speak(speech_text).response
        elif status == 'isp_better_water':
            return BuyHandler().handle(handler_input)
        else:
            speech_text = data.ERROR_SESSION_END_MESSAGE

            handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(data.SKILL_NAME, speech_text)).set_should_end_session(
            True)

            return handler_input.response_builder.response
