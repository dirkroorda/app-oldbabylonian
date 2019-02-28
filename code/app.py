import os

from tf.core.helpers import htmlEsc, mdEsc
from tf.applib.helpers import dh
from tf.applib.display import prettyPre, getFeatures
from tf.applib.highlight import hlText, hlRep
from tf.applib.api import setupApi
from tf.applib.links import outLink
from atf import Atf

TEMP_DIR = '_temp'
REPORT_DIR = 'reports'

ATF_TYPES = set('''
    sign
    cluster
'''.strip().split())

COMMENT_FEATURES = '''
  comment
  remarks
'''.strip().split()

CONTENT_FEATURES = '''
  repeat
  fraction
  operator
  grapheme
'''.strip().split()

FLAG_FEATURES = '''
    collated
    remarkable
    question
    damage
'''.strip().split()

CLUSTER_FEATURES = '''
    det
    uncertain
    missing
    excised
    supplied
    langalt
'''.strip().split()

SIGN_FEATURES = FLAG_FEATURES + CLUSTER_FEATURES + COMMENT_FEATURES + CONTENT_FEATURES

URL_FORMAT = (
    'https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID={}'
)

SECTION = {'document', 'face', 'line'}


class TfApp(Atf):

  def __init__(app, *args, _asApp=False, lgc=False, check=False, silent=False, **kwargs):
    setupApi(app, *args, _asApp=_asApp, lgc=lgc, check=check, silent=silent, **kwargs)

    app.tempDir = f'{app.repoLocation}/{TEMP_DIR}'
    app.reportDir = f'{app.repoLocation}/{REPORT_DIR}'

    if not _asApp:
      for cdir in (app.tempDir, app.reportDir):
        os.makedirs(cdir, exist_ok=True)

  def webLink(app, n, text=None, className=None, _asString=False, _noUrl=False):
    api = app.api
    T = api.T

    (pNum, face, lnno) = T.sectionFromNode(n, fillup=True)
    passageText = app.sectionStrFromNode(n)
    href = '#' if _noUrl else URL_FORMAT.format(pNum)
    if text is None:
      text = passageText
      title = 'show this document on CDLI'
    else:
      title = passageText
    if _noUrl:
      title = None
    target = '' if _noUrl else None

    result = outLink(
        text,
        href,
        title=title,
        className=className,
        target=target,
        passage=passageText,
    )
    if _asString:
      return result
    dh(result)

  def _plain(
      app,
      n,
      passage,
      isLinked,
      _asString,
      secLabel,
      **options,
  ):
    display = app.display
    d = display.get(options)

    _asApp = app._asApp
    api = app.api
    F = api.F
    L = api.L

    nType = F.otype.v(n)
    result = passage
    if _asApp:
      nodeRep = f' <a href="#" class="nd">{n}</a> ' if d.withNodes else ''
    else:
      nodeRep = f' *{n}* ' if d.withNodes else ''

    isText = d.fmt is None or '-orig-' in d.fmt
    if nType == 'sign':
      rep = hlText(app, [n], d.highlights, fmt=d.fmt)
    elif nType in SECTION:
      if nType == 'line':
        rep = hlText(app, L.d(n, otype='sign'), d.highlights, fmt=d.fmt)
      elif nType == 'face':
        rep = mdEsc(htmlEsc(f'{nType} {F.face.v(n)}')) if secLabel else ''
      elif nType == 'document':
        rep = mdEsc(htmlEsc(f'{nType} {F.pnumber.v(n)}')) if secLabel else ''
      rep = hlRep(app, rep, n, d.highlights)
      isText = False
    else:
      rep = hlText(app, L.d(n, otype='sign'), d.highlights, fmt=d.fmt)
    lineNumbersCondition = d.lineNumbers
    tClass = display.formatClass[d.fmt].lower() if isText else 'trb'
    rep = f'<span class="{tClass}">{rep}</span>'
    rep = app._addLink(
        n,
        rep,
        nodeRep,
        isLinked=isLinked,
        lineNumbers=lineNumbersCondition,
    )
    result += rep

    if _asString or _asApp:
      return result
    dh(result)

  def _addLink(app, n, rep, nodeRep, isLinked=True, lineNumbers=True):
    F = app.api.F
    if isLinked:
      rep = app.webLink(n, text=rep, _asString=True)
    theLine = ''
    if lineNumbers:
      theLine = mdEsc(f' @{F.srcLnNum.v(n)} ')
    return f'{rep}{nodeRep}{theLine}'

  def _pretty(
      app,
      n,
      outer,
      html,
      firstSlot,
      lastSlot,
      **options,
  ):
    display = app.display
    d = display.get(options)

    goOn = prettyPre(
        app,
        n,
        firstSlot,
        lastSlot,
        d.withNodes,
        d.highlights,
    )
    if not goOn:
      return
    (
        slotType,
        nType,
        className,
        boundaryClass,
        hlAtt,
        nodePart,
        myStart,
        myEnd,
    ) = goOn

    api = app.api
    F = api.F
    L = api.L
    T = api.T
    otypeRank = api.otypeRank

    bigType = False
    if d.condenseType is not None and otypeRank[nType] > otypeRank[d.condenseType]:
      bigType = True

    (hlClass, hlStyle) = hlAtt

    heading = ''
    featurePart = ''
    children = ()

    if bigType:
      children = ()
    elif nType == 'document':
      children = L.d(n, otype='face')
    elif nType == 'face':
      children = L.d(n, otype='line')
    elif nType == 'line':
      children = L.d(n, otype='word')
    elif nType == 'word':
      children = L.d(n, otype='sign')
    elif nType == 'cluster':
      children = L.d(n, otype='sign')

    if nType == 'document':
      heading = htmlEsc(F.pnumber.v(n))
      heading += ' '
      heading += getFeatures(
          app,
          n,
          ('collection', 'volume', 'docnumber', 'docnote'),
          plain=True,
          **options,
      )
    elif nType == 'face':
      heading = htmlEsc(F.face.v(n))
      featurePart = getFeatures(
          app,
          n,
          ('object',),
          **options,
      )
    elif nType == 'line':
      heading = htmlEsc(F.lnno.v(n))
      className = 'line'
      theseFeats = ('comment', 'remarks', 'translation@en')
      if d.lineNumbers:
        theseFeats = ('srcLnNum',) + theseFeats
      featurePart = getFeatures(
          app,
          n,
          theseFeats,
          **options,
      )
    elif nType == 'cluster':
      heading = F.type.v(n)
      featurePart = getFeatures(
          app,
          n,
          (),
          **options,
      )
    elif nType == 'word':
      heading = T.text(n, fmt=d.fmt, descend=True)
      featurePart = getFeatures(
          app,
          n,
          (),
          **options,
      )
    elif nType == slotType:
      heading = T.text(n, fmt=d.fmt)
      featurePart = getFeatures(
          app,
          n,
          SIGN_FEATURES,
          withName=True,
          **options,
      )
      if not outer and F.type.v(n) == 'empty':
        return

    if outer:
      typePart = app.webLink(n, text=f'{nType} {heading}', _asString=True)
    else:
      typePart = heading

    label = f'''
    <div class="lbl {className}">
        {typePart}
        {nodePart}
    </div>
''' if typePart or nodePart else ''

    html.append(
        f'''
<div class="contnr {className} {hlClass}" {hlStyle}>
    {label}
    <div class="meta">
        {featurePart}
    </div>
'''
    )
    if children:
      html.append(f'''
    <div class="children {className}">
''')

    for ch in children:
      app._pretty(
          ch,
          False,
          html,
          firstSlot,
          lastSlot,
          **options,
      )
    if children:
      html.append('''
    </div>
''')
    html.append('''
</div>
''')
