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
    noneValues={None},
    sectionSep1=" ",
    sectionSep2=":",
    writing="cun",
    writingDir="ltr",
    fontName="Santakku",
    font="Santakk.ttf",
    fontw="Santakku.woff",
    textFormats={
        "layout-orig-rich": "layoutRich",
        "layout-orig-unicode": "layoutUnicode",
    },
    browseNavLevel=2,
    browseContentPretty=False,
)

TYPE_DISPLAY = dict(
    document=dict(
        template="{pnumber}",
        featuresBare="collection volume document docnote",
        children="face",
        lineNumber="srcLnNum",
        level=3, flow="col", wrap=False, stretch=False,
    ),
    face=dict(
        template="{face}",
        featuresBare="object",
        children="line",
        lineNumber="srcLnNum",
        level=3, flow="col", wrap=False, strectch=False,
    ),
    line=dict(
        template="{lnno}",
        features="remarks translation@en",
        children={"word", "commentline"},
        condense=True,
        lineNumber="srcLnNum",
        level=2, flow="row", wrap=True, strectch=True,
    ),
    cluster=dict(
        template="{type}",
        children="sign",
        level=2, flow="row", wrap=True, strectch=False,
    ),
    word=dict(
        template=True,
        children="sign",
        base=True,
        level=1, flow="row", wrap=False, strectch=True,
    ),
    sign=dict(
        template=True,
        features=(
            "collated remarkable question damage"
            " det uncertain missing excised supplied langalt"
            " comment remarks"
            " repeat fraction operator grapheme"
        ),
        level=0, flow="col", wrap=False, strectch=False,
    ),
)

INTERFACE_DEFAULTS = dict(
    lineNumbers=False,
)


def deliver():
    return (globals(), dirname(abspath(__file__)))
