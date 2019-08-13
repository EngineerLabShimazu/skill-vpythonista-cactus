import os
import ssml_builder

SKILL_NAME = 'まいにちさぼてん'
SEED_MESSAGE = 'そういえば、さぼてんの種を拾ったんですよね。一緒に育てませんか？'
WELCOME_MESSAGE = 'はい、きみのサボテンはこちらです。'
HELP_MESSAGE = 'さぼてんを育てるスキルです。さぼてんに水をあげますか？'
ERROR_SESSION_END_MESSAGE = '問題がありました。スキルを終了します'
CACTUS_SEED_IMAGE_01 = 'seeds/cactus_seed.png'

_S3_URL = 'https://vpythonista.s3-ap-northeast-1.amazonaws.com'
_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
S3_BUCKET_URL = os.path.join(_S3_URL, _BUCKET_NAME)

SOUND_FLOWER = 'flower.mp3'

scenes = {
    'events': [
        'normal',
        'birds'
    ],
    'weather': [
        'rain'
    ],
    'bonus': [
        'flower'
    ]
}

growth_range = {
    4: 5,
    5: 50,
    6: 30,
    7: 10,
    8: 5
}


def get_standard_card_title(height):
    if height <= 0:
        return 'さぼてん の 種'
    return 'さぼてん'


def get_standard_card_text(height):
    if height <= 0:
        return'どんな さぼてん に育つのだろう。わくわく。'
    return f'{height}㎜'
