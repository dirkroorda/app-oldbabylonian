from os.path import dirname, abspath

API_VERSION = 1

PROVENANCE_SPEC = dict(
    org="Nino-cunei",
    repo="oldbabylonian",
    version="1.0.4",
    doi="10.5281/zenodo.2579207",
    corpus="Old Babylonian Letters 1900-1600: Cuneiform tablets ",
)

DOCS = dict(
    docPage="about",
    featureBase="{docBase}/transcription{docExt}",
    featurePage="",
    charUrl="{docBase}/programs/mapReadings.ipynb",
    charText="mapping from readings to UNICODE",
    webBase="https://cdli.ucla.edu",
    webUrl="/search/search_results.php?SearchMode=Text&ObjectID=<1>",
    webHint="Show this document on CDLI",
)

DATA_DISPLAY = dict(
    writing="akk",
    textFormats={
        "layout-orig-rich": "layoutRich",
        "layout-orig-unicode": "layoutUnicode",
    },
)

TYPE_DISPLAY = dict(
    document=dict(
        featuresBare="collection volume document docnote", lineNumber="srcLnNum",
    ),
    face=dict(featuresBare="object", lineNumber="srcLnNum"),
    line=dict(
        features="remarks translation@en",
        children={"word", "commentline"},
        lineNumber="srcLnNum",
    ),
    cluster=dict(template="{type}", children="sign", stretch=False),
    word=dict(template=True, base=True, wrap=False),
    sign=dict(
        features=(
            "collated remarkable question damage"
            " det uncertain missing excised supplied langalt"
            " comment remarks"
            " repeat fraction operator grapheme"
        ),
    ),
)

INTERFACE_DEFAULTS = dict(lineNumbers=False)


def deliver():
    return (globals(), dirname(abspath(__file__)))
