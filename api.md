# Linking

## A.cdli()

```python
A.cdli(document, linkText=None, asString=False)
```

### Description
Produces a link to a document page on CDLI,
to be placed in an output cell.

### document
`document` is either a node of type `document`
or a P-number of a document.

### linkText
You may provide the text to be displayed as the link.
If you do not provide any,
the P-number of the document will be used.

### asString 
Instead of displaying the result directly in the output of your
code cell in a notebook, you can also deliver the HTML as string,
just say `asString=True`.

## A.getSource()

```python
A.getSource(node, nodeType=None, lineNumbers=False)
```

### Description
Delivers the transcription source of nodes that correspond to the
ATF source line level.

### node
`node` must have a type in `document`, `face`, `line`.

### nodeType
If `nodeType` is passed, only source lines of this type are returned.

### lineNumbers
`lineNumbers`: if `True`, add line numbers to the result,
these numbers say where the source line occurs in the source file.

### TF from ATF conversion
The conversion of ATF to Text-Fabric has saved the original source lines and
their line numbers in the features `srcLn` and `srcLnNum` respectively. This
function makes use of those features.
# Display

All display functions (`plain()`, `pretty()`, `table()`, `show()` etc
accept the additional option:

## lineNumbers

`lineNumbers` indicates whether corresponding line numbers in the
ATF source should be displayed.

# Sections

## Sections in documents

Text-Fabric supports up to 3 section levels in general.
The Old Babylonian corpus uses 2 of them for *documents* and *faces*.

## Consider search

Text-Fabric [Search](../Use/Search.md) is a generic and powerful mechanism for information retrieval.
In most cases it is easier to extract nodes by search than by hand-written
code using the functions here.
