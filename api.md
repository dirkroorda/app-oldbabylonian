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
