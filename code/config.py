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

EXAMPLE_SECTION = "<code>P509373</code>"
EXAMPLE_SECTION_TEXT = "P509373"

DATA_DISPLAY = dict(
    writing="cun",
    textFormats={
        "layout-orig-rich": "layoutRich",
        "layout-orig-unicode": "layoutUnicode",
    },
)

TYPE_DISPLAY = dict(
    document=dict(
        featuresBare="collection volume document docnote", lineNumber="srcLnNum",
    ),
    face=dict(featuresBare="object", lineNumber="srcLnNum",),
    line=dict(
        features="remarks translation@en",
        children={"word", "commentline"},
        lineNumber="srcLnNum",
    ),
    cluster=dict(template="{type}", children="sign", stretch=False,),
    word=dict(template=True, base=True, wrap=False,),
    sign=dict(
        features=(
            "collated remarkable question damage"
            " det uncertain missing excised supplied langalt"
            " comment remarks"
            " repeat fraction operator grapheme"
        ),
    ),
)

INTERFACE_DEFAULTS = dict(lineNumbers=False,)


def deliver():
    return (globals(), dirname(abspath(__file__)))
