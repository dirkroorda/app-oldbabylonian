from tf.applib.app import loadModule
from tf.applib.api import setupApi


def notice(app):
    if int(app.api.TF.version.split(".")[0]) <= 7:
        print(
            f"""
Your Text-Fabric is outdated.
It cannot load this version of the TF app `{app.appName}`.
Recommendation: upgrade Text-Fabric to version 8.
Hint:

    pip3 install --upgrade text-fabric

"""
        )


MODIFIERS = """
    collated
    remarkable
    question
    damage
    uncertain
    missing
    excised
    supplied
""".strip().split()


class TfApp(object):
    def __init__(app, *args, **kwargs):
        atf = loadModule(*args[0:2], "atf")
        atf.atfApi(app)
        setupApi(app, *args, **kwargs)
        notice(app)

    def fmt_layoutRich(app, n):
        return app._wrapHtml(n, "r")

    def fmt_layoutUnicode(app, n):
        return app._wrapHtml(n, "u")

    def _wrapHtml(app, n, kind):
        api = app.api
        F = api.F
        Fs = api.Fs
        typ = F.type.v(n)
        after = (F.afteru.v(n) if kind == "u" else F.after.v(n)) or ""
        if typ == "empty":
            material = '<span class="empty">∅</span>'
        elif typ == "comment" or typ == "commentline":
            material = f'<span class="comment">{F.comment.v(n)}</span>'
        elif typ == "unknown":
            partR = Fs("reading" + kind).v(n) or ""
            if partR:
                partR = f'<span class="r">{partR}</span>'
            partG = Fs("grapheme" + kind).v(n) or ""
            if partG:
                partG = f'<span class="g">{partG}</span>'
            material = f'<span class="uncertain">{partR}{partG}</span>'
        elif typ == "ellipsis":
            material = f'<span class="missing">{Fs("grapheme" + kind).v(n)}</span>'
        elif typ == "reading":
            material = f'<span class="r">{Fs("reading" + kind).v(n)}</span>'
        elif typ == "grapheme":
            material = f'<span class="g">{Fs("grapheme" + kind).v(n)}</span>'
        elif typ == "numeral":
            if kind == "u":
                material = F.symu.v(n)
            else:
                part = f'<span class="r">{Fs("reading" + kind).v(n) or ""}</span>'
                partG = Fs("grapheme" + kind).v(n) or ""
                if partG:
                    partG = f'<span class="g">{partG}</span>'
                part = f"{part}{partG}"
                material = f'<span class="quantity">{F.repeat.v(n) or ""}{F.fraction.v(n) or ""}</span>⌈{part}⌉'
        elif typ == "complex":
            partR = f'<span class="r">{Fs("reading" + kind).v(n) or ""}</span>'
            partG = f'<span class="g">{Fs("grapheme" + kind).v(n) or ""}</span>'
            operator = (
                f'<span class="operator">{Fs("operator" + kind).v(n) or ""}</span>'
            )
            material = f"{partR}{operator}⌈{partG}⌉"
        else:
            material = Fs("sym" + kind).v(n)
        clses = " ".join(cf for cf in MODIFIERS if Fs(cf).v(n))
        if clses:
            material = f'<span class="{clses}">{material}</span>'
        if F.det.v(n):
            material = f'<span class="det">{material}</span>'
        if F.langalt.v(n):
            material = f'<span class="langalt">{material}</span>'
        return f"{material}{after}"
