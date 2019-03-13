import os

from tf.core.helpers import mdhtmlEsc, htmlEsc, mdEsc
from tf.applib.helpers import dh
from tf.applib.display import prettyPre, getFeatures
from tf.applib.highlight import hlText, hlRep
from tf.applib.api import setupApi
from tf.applib.links import outLink
from atf import Atf

TEMP_DIR = '_temp'
REPORT_DIR = 'reports'

DOCUMENT = 'document'
FACE = 'face'
LINE = 'line'
CLUSTER = 'cluster'
WORD = 'word'
SIGN = 'sign'

ATF_TYPES = set('''
    sign
    cluster
'''.strip().split())

COMMENTLINE = 'commentline'

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

MODIFIERS = FLAG_FEATURES + CLUSTER_FEATURES[1:-1]

SIGN_FEATURES = FLAG_FEATURES + CLUSTER_FEATURES + COMMENT_FEATURES + CONTENT_FEATURES

URL_FORMAT = (
    'https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID={}'
)

SECTION = {DOCUMENT, FACE, LINE}


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
      title = f'show this {DOCUMENT} on CDLI'
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

  def fmt_layoutRich(app, n):
    return app._wrapHtml(n, 'r')

  def fmt_layoutUnicode(app, n):
    return app._wrapHtml(n, 'u')

  def _wrapHtml(app, n, kind):
    api = app.api
    F = api.F
    Fs = api.Fs
    typ = F.type.v(n)
    after = (F.afteru.v(n) if kind == 'u' else F.after.v(n)) or ''
    if typ == 'empty':
      material = '<span class="empty">∅</span>'
    elif typ == 'comment' or typ == 'commentline':
      material = f'<span class="comment">{F.comment.v(n)}</span>'
    elif typ == 'unknown':
      partR = Fs("reading" + kind).v(n) or ''
      if partR:
        partR = f'<span class="r">{partR}</span>'
      partG = Fs("grapheme" + kind).v(n) or ''
      if partG:
        partG = f'<span class="g">{partG}</span>'
      material = f'<span class="uncertain">{partR}{partG}</span>'
    elif typ == 'ellipsis':
      material = f'<span class="missing">{Fs("grapheme" + kind).v(n)}</span>'
    elif typ == 'reading':
      material = f'<span class="r">{Fs("reading" + kind).v(n)}</span>'
    elif typ == 'grapheme':
      material = f'<span class="g">{Fs("grapheme" + kind).v(n)}</span>'
    elif typ == 'numeral':
      if kind == 'u':
        material = F.symu.v(n)
      else:
        part = f'<span class="r">{Fs("reading" + kind).v(n) or ""}</span>'
        partG = Fs("grapheme" + kind).v(n) or ''
        if partG:
          partG = f'<span class="g">{partG}</span>'
        part = f'{part}{partG}'
        material = (
            f'<span class="quantity">{F.repeat.v(n) or ""}{F.fraction.v(n) or ""}</span>⌈{part}⌉'
        )
    elif typ == 'complex':
      partR = f'<span class="r">{Fs("reading" + kind).v(n) or ""}</span>'
      partG = f'<span class="g">{Fs("grapheme" + kind).v(n) or ""}</span>'
      operator = f'<span class="operator">{Fs("operator" + kind).v(n) or ""}</span>'
      material = f'{partR}{operator}⌈{partG}⌉'
    else:
      material = Fs("sym" + kind).v(n)
    classes = ' '.join(cf for cf in MODIFIERS if Fs(cf).v(n))
    if classes:
      material = f'<span class="{classes}">{material}</span>'
    if F.det.v(n):
      material = f'<span class="det">{material}</span>'
    if F.langalt.v(n):
      material = f'<span class="langalt">{material}</span>'
    return f'{material}{after}'

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
    T = api.T

    nType = F.otype.v(n)
    result = passage
    if _asApp:
      nodeRep = f' <a href="#" class="nd">{n}</a> ' if d.withNodes else ''
    else:
      nodeRep = f' <i>{n}</i> ' if d.withNodes else ''

    rep = ''
    text = ''
    if nType == SIGN:
      text = hlText(app, [n], d.highlights, fmt=d.fmt)
    elif nType == WORD:
      text = hlText(app, L.d(n, otype=SIGN), d.highlights, fmt=d.fmt)
    elif nType in SECTION:
      if secLabel and d.withPassage:
        sep1 = app.sectionSep1
        sep2 = app.sectionSep2
        label = (
            '{}'
            if nType == DOCUMENT else
            f'{{}}{sep1}{{}}'
            if nType == FACE else
            f'{{}}{sep1}{{}}{sep2}{{}}'
        )
        rep = label.format(*T.sectionFromNode(n))
        rep = mdhtmlEsc(rep)
        rep = hlRep(app, rep, n, d.highlights)
        if isLinked:
          rep = app.webLink(n, text=f'{rep}&nbsp;', _asString=True)
      else:
        rep = ''
      if nType == LINE:
        text = hlText(app, L.d(n, otype=SIGN), d.highlights, fmt=d.fmt)
      elif nType == FACE:
        rep += mdhtmlEsc(f'{nType} {F.face.v(n)}') if secLabel else ''
      elif nType == DOCUMENT:
        rep += mdhtmlEsc(f'{nType} {F.pnumber.v(n)}') if secLabel else ''
      rep = hlRep(app, rep, n, d.highlights)
      if text:
        text = hlRep(app, text, n, d.highlights)
    else:
      rep = hlText(app, L.d(n, otype=SIGN), d.highlights, fmt=d.fmt)
    lineNumbersCondition = d.lineNumbers
    if text:
      tClass = display.formatClass[d.fmt].lower()
      text = f'<span class="{tClass}">{text}</span>'
      rep += text
    rep = app._addLink(
        n,
        rep,
        nodeRep,
        isLinked=isLinked and nType not in SECTION,
        lineNumbers=lineNumbersCondition,
    )
    result += rep

    if _asString or _asApp:
      return result
    dh(result)

  def _addLink(app, n, rep, nodeRep, isLinked=None, lineNumbers=True):
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
    isHtml = options.get('fmt', None) in app.textFormats

    bigType = (
        not d.full
        and
        d.condenseType is not None and otypeRank[nType] > otypeRank[d.condenseType]
    )

    (hlClass, hlStyle) = hlAtt

    heading = ''
    featurePart = ''
    children = ()

    if bigType:
      children = ()
    elif nType == DOCUMENT:
      children = L.d(n, otype=FACE)
    elif nType == FACE:
      children = L.d(n, otype=LINE)
    elif nType == LINE:
      children = tuple(
          c
          for c in L.d(n)
          if F.otype.v(c) == WORD or F.type.v(c) == COMMENTLINE
      )
    elif nType == WORD:
      children = L.d(n, otype=SIGN)
    elif nType == CLUSTER:
      children = L.d(n, otype=SIGN)

    isText = False

    if nType == DOCUMENT:
      heading = htmlEsc(F.pnumber.v(n))
      heading += ' '
      heading += getFeatures(
          app,
          n,
          ('collection', 'volume', 'docnumber', 'docnote'),
          plain=True,
          **options,
      )
    elif nType == FACE:
      heading = htmlEsc(F.face.v(n))
      featurePart = getFeatures(
          app,
          n,
          ('object',),
          **options,
      )
    elif nType == LINE:
      heading = htmlEsc(F.lnno.v(n))
      className = LINE
      theseFeats = ('remarks', 'translation@en')
      if d.lineNumbers:
        theseFeats = ('srcLnNum',) + theseFeats
      featurePart = getFeatures(
          app,
          n,
          theseFeats,
          **options,
      )
    elif nType == CLUSTER:
      heading = F.type.v(n)
      featurePart = getFeatures(
          app,
          n,
          (),
          **options,
      )
    elif nType == WORD:
      isText = True
      text = T.text(n, fmt=d.fmt, descend=True)
      heading = text if isHtml else htmlEsc(text)
      featurePart = getFeatures(
          app,
          n,
          (),
          **options,
      )
    elif nType == slotType:
      isText = True
      text = T.text(n, fmt=d.fmt)
      heading = text if isHtml else htmlEsc(text)
      featurePart = getFeatures(
          app,
          n,
          SIGN_FEATURES,
          withName=True,
          **options,
      )
      if not outer and F.type.v(n) == 'empty':
        return

    tClass = display.formatClass[d.fmt].lower() if isText else app.defaultCls
    heading = f'<span class="{tClass}">{heading}</span>'

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
