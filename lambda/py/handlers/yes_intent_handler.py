# -*- coding: utf-8 -*-

import datetime
import logging

from ask_sdk.standard import StandardSkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.response_helper import get_plain_text_content

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import StandardCard
from ask_sdk_model import Response

from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective,
    BackButtonBehavior, BodyTemplate2)

from ssml_builder.core import Speech

from alexa import data
from alexa import utils

sb = StandardSkillBuilder(table_name="cactus", auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        status = handler_input.attributes_manager.session_attributes.get('status')
        attr = handler_input.attributes_manager.persistent_attributes
        
        if status == 'confirmation':
            before_height = attr.get('height')
            grow = 5
            grow_height = before_height + grow if before_height else grow
            attr['height'] = grow_height
            attr['last_watered_date'] = str(datetime.date.today())
            handler_input.attributes_manager.persistent_attributes = attr
            handler_input.attributes_manager.save_persistent_attributes()

            speech = Speech()
            speech.audio('https://vpythonista.s3-ap-northeast-1.amazonaws.com/cactus/sounds/flower.mp3')
            speech.add_text('水やりが終わりました。') 
            speech.add_text('身長は{}センチメートルです。'.format(str(grow_height)))
            speech.add_text('明日も水を上げてくださいね。スキルを終了します。')
            speech_text = speech.speak()

            images = {
                0: data.CACTUS_CHRIS_IMAGE_01,
                5: data.CACTUS_CHRIS_IMAGE_01,
                10: data.CACTUS_CHRIS_IMAGE_02,
                15: data.CACTUS_CHRIS_IMAGE_03,
                20: data.CACTUS_CHRIS_IMAGE_04,
                25: data.CACTUS_CHRIS_IMAGE_05,
                30: data.CACTUS_CHRIS_IMAGE_06,
                35: data.CACTUS_CHRIS_IMAGE_07
            }
            img = images.get(grow_height, data.CACTUS_CHRIS_IMAGE_07)

            ret_img = Image(sources=[ImageInstance(url=img)])
            title = data.SKILL_NAME
            primary_text = get_plain_text_content(
                primary_text="")

            handler_input.response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate2(
                        back_button=BackButtonBehavior.VISIBLE,
                        image=ret_img, title=title,
                        text_content=primary_text))).set_should_end_session(True)

            return handler_input.response_builder.speak(speech_text).response
        else:
            speech_text = data.ERROR_SESSION_END_MESSAGE

            handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(data.SKILL_NAME, speech_text)).set_should_end_session(
            True)

            return handler_input.response_builder.response
