from os.path import dirname, abspath

API_VERSION = 1

PROTOCOL = "http://"
HOST = "localhost"
PORT = dict(kernel=18986, web=8106)

ORG = "Nino-cunei"
REPO = "oldbabylonian"
CORPUS = "Old Babylonian Letters 1900-1600: Cuneiform tablets "
VERSION = "1.0.4"
RELATIVE = "tf"

DOI_TEXT = "10.5281/zenodo.2579207"
DOI_URL = "https://doi.org/10.5281/zenodo.2579207"

DOC_URL = f"https://github.com/{ORG}/{REPO}/blob/master/docs/"
DOC_INTRO = "about.md"
CHAR_URL = f"https://github.com/{ORG}/{REPO}/blob/master/docs/transcription.md"
CHAR_TEXT = "How TF features represent ATF"

FEATURE_URL = f"{DOC_URL}/transcription.md"

MODULE_SPECS = ()

ZIP = [REPO]

BASE_TYPE = "word"
CONDENSE_TYPE = "line"

NONE_VALUES = {None}

STANDARD_FEATURES = None  # meaning all loadable features

EXCLUDED_FEATURES = set()

NO_DESCEND_TYPES = {"lex"}

EXAMPLE_SECTION = "<code>P509373</code>"
EXAMPLE_SECTION_TEXT = "P509373"

SECTION_SEP1 = " "
SECTION_SEP2 = ":"

WRITING = "cun"
WRITING_DIR = "ltr"

FONT_NAME = "Santakku"
FONT = "Santakku.ttf"
FONTW = "Santakku.woff"

TEXT_FORMATS = {
    "layout-orig-rich": "layoutRich",
    "layout-orig-unicode": "layoutUnicode",
}

BROWSE_NAV_LEVEL = 2
BROWSE_CONTENT_PRETTY = False

VERSE_TYPES = None

LEX = None

TRANSFORM = None

CHILD_TYPE = dict(
    document="face",
    face="line",
    line={"word", "commentline"},
    word="sign",
    quad="sign",
    cluster="sign",
)

SUPER_TYPE = None

TYPE_DISPLAY = dict(
    document=dict(
        template="{pnumber}",
        bareFeatures="collection volume document docnote",
        features="",
        level=3, flow="col", wrap=False, stretch=False,
    ),
    face=dict(
        template="{face}",
        bareFeatures="object",
        features="",
        level=3, flow="col", wrap=False, strectch=False,
    ),
    line=dict(
        template="{lnno}",
        bareFeatures="",
        features="remarks translation@en",
        level=2, flow="row", wrap=True, strectch=True,
    ),
    cluster=dict(
        template="{type}",
        bareFeatures="",
        features="",
        level=2, flow="row", wrap=True, strectch=False,
    ),
    word=dict(
        template=True,
        bareFeatures="",
        features="",
        level=1, flow="row", wrap=False, strectch=True,
    ),
    sign=dict(
        template=True,
        bareFeatures="",
        features=(
            "collated remarkable question damage"
            " det uncertain missing excised supplied langalt"
            " comment remarks"
            " repeat fraction operator grapheme"
        ),
        level=0, flow="col", wrap=False, strectch=False,
    ),
)

INTERFACE_DEFAULTS = dict()

LINE_NUMBERS = dict(line="srcLnNum", face="srcLnNum", document="srcLnNum")


def deliver():
    return (globals(), dirname(abspath(__file__)))
