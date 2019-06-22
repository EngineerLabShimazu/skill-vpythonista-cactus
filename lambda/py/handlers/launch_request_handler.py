from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from alexa import data
from ask_sdk_model import ui


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = data.WELCOME_MESSAGE

        # height = getHeight()
        # image = getImage(height)

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title="ことだまさぼてん",
                text=speech_text,
                # image=ui.Image(
                #     small_image_url=small_url,
                #     large_image_url=large_url
                # )
            )
        ).ask(speech_text)
        return handler_input.response_builder.response
