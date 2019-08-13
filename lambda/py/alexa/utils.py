import os
import random
import datetime
from alexa import data
from ask_sdk_model.services.monetization import (
    EntitledState, PurchasableState, InSkillProductsResponse, Error,
    InSkillProduct)


def get_level(height):
    if height <= 0:
        return 0
    if height <= 5:
        return 1
    if height <= 20:
        return 2
    if height <= 40:
        return 3
    if height <= 100:
        return 4
    if height <= 250:
        return 5
    if height <= 600:
        return 6
    return 7


def select_scene():
    return random.choice(data.scenes.get('events'))


class ImageGetter:
    def __init__(self, kind='chris'):
        self.kind = kind

    def get_image(self, level, scene):
        if level <= 0:
            return os.path.join(
                data.S3_BUCKET_URL, 'images', data.CACTUS_SEED_IMAGE_01
            )

        image_name = f'{self.kind}0{level}'
        if scene and scene != 'normal':
            image_name = image_name + f'_{scene}'

        image_file_name = f'{image_name}.png'
        return os.path.join(
            data.S3_BUCKET_URL, 'images', self.kind, image_file_name
        )


def get_sound_url(sound_name):
    return os.path.join(
        data.S3_BUCKET_URL, 'sounds', sound_name
    )


def supports_apl(handler_input):
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.supported_interfaces, 'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False


def in_skill_product_resposne(handler_input):
    # type: (HandlerInput) -> Union[InSkillProductsResponse, Error]
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)


def get_grow_value():
    return random.choices(
        list(data.growth_range.keys()), data.growth_range.values()
    )[0]


def is_product(product):
    """Is the product list not empty."""
    # type: (List) -> bool
    return bool(product)


def is_entitled(product):
    """Is the product in ENTITLED state."""
    # type: (List) -> bool
    return (is_product(product) and
            product[0].entitled == EntitledState.ENTITLED)


def is_subscriptable(handler_input):
    in_skill_response = in_skill_product_resposne(handler_input)
    if in_skill_response:
        subscription = [
            l for l in in_skill_response.in_skill_products
            if l.reference_name == "better_water"]
        if is_entitled(subscription):
            return True
    return False


def can_water(last_watered_date):
    if last_watered_date != str(datetime.date.today()):
        return True
    return False


def get_last_watered_date(handler_input):
    attributes = handler_input.attributes_manager.persistent_attributes
    return attributes.get('last_watered_date')


def get_cactus_height(handler_input):
    attributes = handler_input.attributes_manager.persistent_attributes
    if isinstance(attributes, dict):
        return attributes.get('height', 0)
    return 0
