from os.path import dirname, abspath

PROTOCOL = 'http://'
HOST = 'localhost'
PORT = dict(
    kernel=18986,
    web=8106,
)

OPTIONS = (
    ('lineNumbers', False, 'checkbox', 'linen', 'show line numbers'),
)

ORG = 'Nino-cunei'
REPO = 'oldbabylonian'
CORPUS = 'Old Babylonian Letters 1900-1600: Cuneiform tablets '
VERSION = '1.0.4'
RELATIVE = 'tf'

DOI_TEXT = '10.5281/zenodo.2579207'
DOI_URL = 'https://doi.org/10.5281/zenodo.2579207'

DOC_URL = f'https://github.com/{ORG}/{REPO}/blob/master/docs/'
DOC_INTRO = 'about.md'
CHAR_URL = f'https://github.com/{ORG}/{REPO}/blob/master/docs/transcription.md'
CHAR_TEXT = 'How TF features represent ATF'

FEATURE_URL = f'{DOC_URL}/transcription.md'

MODULE_SPECS = ()

ZIP = [REPO]

CONDENSE_TYPE = 'line'

NONE_VALUES = {None}

STANDARD_FEATURES = None  # meaning all loadable features

EXCLUDED_FEATURES = set()

NO_DESCEND_TYPES = {'lex'}

EXAMPLE_SECTION = '<code>P509373</code>'
EXAMPLE_SECTION_TEXT = 'P509373'

SECTION_SEP1 = ' '
SECTION_SEP2 = ':'

DEFAULT_CLS = 'txtn'
DEFAULT_CLS_ORIG = 'txtp'

FORMAT_CSS = dict(
    unicode='txtu',
    rich='txtr',
    full='txtp',
    plain='txtp',
)

CLASS_NAMES = None

FONT_NAME = 'Santakku'
FONT = 'Santakku.ttf'
FONTW = 'Santakku.woff'

TEXT_FORMATS = {
    'layout-orig-rich': 'layoutRich',
    'layout-orig-unicode': 'layoutUnicode',
}

BROWSE_NAV_LEVEL = 2
BROWSE_CONTENT_PRETTY = False


def deliver():
  return (globals(), dirname(abspath(__file__)))
