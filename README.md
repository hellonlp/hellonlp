# word_segmentation
Chinese word segmentation algorithm without corpus

## Usage
```
from word_segmentation import get_words
content = '北京比武汉的人口多，但是北京的天气没有武汉的热，武汉有热干面，北京有北京烤鸭'
words = get_words(content, max_word_len=2, min_aggregation=1, min_entropy=0.5)
print(words)
```
