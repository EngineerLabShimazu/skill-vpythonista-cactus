# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import ui
from ask_sdk_core.response_helper import get_plain_text_content
from ask_sdk_model.interfaces.display import (
    ImageInstance, Image, RenderTemplateDirective,
    BackButtonBehavior, BodyTemplate2)
from ssml_builder.core import Speech
from alexa import data
from alexa import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        height = attr.get('height', 0)

        speech = Speech()
        speech.add_text('次は水を上げて欲しいな。楽しみに待っています。')
        speech_text = speech.speak()

        cactus_image = utils.ImageGetter().get_image(
            utils.get_level(height), utils.select_scene()
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
                        text_content=primary_text))).set_should_end_session(True)

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
