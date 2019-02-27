import os

from tf.core.helpers import htmlEsc, mdEsc
from tf.applib.helpers import dh
from tf.applib.display import prettyPre, getFeatures
from tf.applib.highlight import hlRep
from tf.applib.api import setupApi
from tf.applib.links import outLink
from atf import Atf

TEMP_DIR = '_temp'
REPORT_DIR = 'reports'

COMMENT_FEATURES = '''
  comment
  remarks
'''.strip().split()

ATF_TYPES = set('''
    sign
    cluster
'''.strip().split())


URL_FORMAT = (
    'https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID={}'
)


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
    L = api.L
    F = api.F
    if type(n) is str:
      pNum = n
    else:
      refNode = n if F.otype.v(n) == 'document' else L.u(n, otype='document')[0]
      pNum = F.catalogId.v(refNode)

    title = None if _noUrl else ('to CDLI main page for this document')
    linkText = pNum if text is None else text
    url = '#' if _noUrl else URL_FORMAT.format(pNum)
    target = '' if _noUrl else None

    result = outLink(
        linkText,
        url,
        title=title,
        className=className,
        target=target,
        passage=pNum,
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

    nType = F.otype.v(n)
    result = passage
    if _asApp:
      nodeRep = f' <a href="#" class="nd">{n}</a> ' if d.withNodes else ''
    else:
      nodeRep = f' *{n}* ' if d.withNodes else ''

    if nType == 'sign':
      rep = F.atf.v(n)
      rep = hlRep(app, rep, n, d.highlights)
      if isLinked:
        rep = app.webLink(n, text=rep, _asString=True)
      result = f'{rep}{nodeRep}'
    else:
      lineNumbersCondition = d.lineNumbers
      if nType == 'line':
        src = F.srcLn.v(n) or ''
        rep = (
            src
            if src else (
                mdEsc(htmlEsc(f'{nType} {F.ln.v(n)}'))
                if secLabel else
                ''
            )
        )
        lineNumbersCondition = d.lineNumbers
      elif nType == 'face':
        rep = mdEsc(htmlEsc(f'{nType} {F.face.v(n)}'))
      elif nType == 'document':
        rep = mdEsc(htmlEsc(f'{nType} {F.pnumber.v(n)}')) if secLabel else ''
      rep = hlRep(app, rep, n, d.highlights)
      result = app._addLink(
          n,
          rep,
          nodeRep,
          isLinked=isLinked,
          lineNumbers=lineNumbersCondition,
      )

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
    sortNodes = api.sortNodes
    otypeRank = api.otypeRank

    bigType = False
    if d.condenseType is not None and otypeRank[nType] > otypeRank[d.condenseType]:
      bigType = True

    (hlClass, hlStyle) = hlAtt

    heading = ''
    featurePart = ''
    commentsPart = app._getComments(
        n,
        firstSlot,
        lastSlot,
        **options,
    )
    children = ()

    if bigType:
      children = ()
    elif nType == 'document':
      children = L.d(n, otype='face')
    elif nType == 'face':
      children = L.d(n, otype='line')
    elif nType == 'line':
      children = sortNodes(set(L.d(n, otype='sign')))
    elif nType == 'cluster':
      children = sortNodes(set(L.d(n, otype='sign')))

    if nType == 'document':
      heading = htmlEsc(F.catalogId.v(n))
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
      heading = htmlEsc(app._getLineNum(n))
      className = 'line'
      theseFeats = ('srcLnNum', ) if d.lineNumbers else ()
      featurePart = getFeatures(
          app,
          n,
          theseFeats,
          **options,
      )
    elif nType == 'cluster':
      heading = F.type.v(n)
    elif nType == slotType:
      featurePart = F.atf.v(n) + getFeatures(app, n, (), **options)
      if not outer and F.type.v(n) == 'empty':
        return

    if outer:
      typePart = app.webLink(n, text=f'{nType} {heading}', _asString=True)
    else:
      typePart = heading

    isCluster = nType == 'cluster'
    extra = 'b' if isCluster else ''
    label = f'''
    <div class="lbl {className}{extra}">
        {typePart}
        {nodePart}
    </div>
''' if typePart or nodePart else ''

    if isCluster:
      if outer:
        html.append(f'<div class="contnr {className} {hlClass}" {hlStyle}>')
      html.append(label)
      if outer:
        html.append(f'<div class="children {className}">')
    else:
      html.append(
          f'''
<div class="contnr {className} {hlClass}" {hlStyle}>
    {label}
    <div class="meta">
        {featurePart}
        {commentsPart}
    </div>
'''
      )
    if not isCluster:
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
    if isCluster:
      html.append(
          f'''
    <div class="lbl {className}e {hlClass}" {hlStyle}>
        {typePart}
        {nodePart}
    </div>
'''
      )
      if outer:
        html.append('</div></div>')
    else:
      if children:
        html.append('''
    </div>
''')
      html.append('''
</div>
''')

  def _getLineNum(app, n):
    api = app.api
    F = api.F
    col = F.col.v(n) or ''
    primeCol = "'" if F.primecol.v(n) else ''
    colNum = f'{col}{primeCol}'

    ln = F.ln.v(n) or ''
    primeLn = "'" if F.primeln.v(n) else ''
    lnNum = f'{ln}{primeLn}'

    sep = ':' if colNum and lnNum else ''
    return f'{colNum}{sep}{lnNum}'

  def _getComments(
      app,
      n,
      firstSlot,
      lastSlot,
      **options,
  ):
    api = app.api
    Fs = api.Fs
    comments = []
    for kind in COMMENT_FEATURES:
      cmt = Fs(kind).v(n)
      if cmt:
        cmt = cmt.replace('\n', '<br/>')
        comments.append(f'<div class="{kind}">{cmt}</div>')
    return ''.join(comments)
