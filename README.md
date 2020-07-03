# ChineseWordSegmentation
Chinese word segmentation algorithm without corpus

## Usage
```
from wordseg import WordSegment
doc = u'十四是十四四十是四十，十四不是四十，四十不是十四'
ws = word_segmentation(doc, max_word_len=2, min_aggregation=1, min_entropy=0.5)
ws.segSentence(doc)
```
