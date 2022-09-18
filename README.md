# Rouge-Chinese
*A full Python librarie for the ROUGE metric in Chinese Language Task [(paper)](http://www.aclweb.org/anthology/W04-1013).*

专用于计算中文rouge指标的python库。
### Difference

This library based on the [code](https://github.com/pltrdy/rouge) from pltrdy. Using the original code to compute rouge score in Chinese would meet some problems. For example, the stack overflow issue would occur and the Chinese sentences are not splited correctly. This code solves these problems and generates more accurate and "official" rouge scores in Chinese NLP tasks.

1. Changed the sentence cutting mechanism. Original code would split sentences only by '.'. The rouge-chinese would split sentences regarding Chinese punctuation in a more logical way.
2. Optimized memory usage in rouge-L score calculation. The new code did not generate longest common sequence since most of users did not need it. This part would be extremely memory costly since it contains iterative algorithm which would create lots of stacks. The new code could calculate the length of the longest common sequence without generating them. 
3. More accurate rouge scores. The original code replaced 'official' rouge-L scores with union rouge-L scores, which would certainly give users different results. Thanks to the memory optimization, the new code could give users 'official' rouge scores.

### 不同点

rouge-chinese库基于[rouge](https://github.com/pltrdy/rouge)库，针对中文NLP任务做出了改进。使用原始的rouge库计算中文的rouge score会遇到一些问题，例如，会产生栈溢出以及占据过大内存的问题（长文章甚至会占据数十GB），以及不计算union rouge score时不支持对中文文章的分句。新的rouge-chinese库不仅从根源上解决了这些问题，优化了算法，rouge-chinese库还舍弃了默认的rouge score近似指标union rouge score，转而通过优化后的算法提供用户最原始、准确和官方的rouge score指标。

1. 改进了中文的分句机制。原始的rouge库只根据'.'进行分句。rouge-chinese库除了英文标点外，还对中文的常见分句标点（。！？...）进行了囊括。
2. 优化了rouge-L score计算中的内存占用。rouge-chinese库计算rouge-L score时不再需要生成最长子序列，就可以直接计算出最长子序列的长度，并得出最终的rouge-L score。最长子序列的生成是算法中内存消耗最大的一块，由于其中含有递归算法，他会占用大量的栈，尤其是在遇到长文章时，容易导致内存溢出或栈溢出的问题。rouge-chinese库成功的绕过了这一步骤。
3. 更准确和官方的rouge scores。由于先前的rouge库算法存在内存占用过大的问题，因此他们使用分句后计算union rouge score的方法来近似实际的rouge score，但这会带来一定的误差，部分情况误差较大。由于我们成功解决了内存占用过大的问题，新算法支持计算出最准确，最原始和最官方的rouge score。

## Quickstart
### Clone & Install
```
pip install rouge-chinese
```
or:
```shell
git clone https://github.com/Isaac-JL-Chen/rouge_chinese.git
cd rouge_chinese
python setup.py install
# or
pip install -U .
```


### Use it as a library

###### Score 1 sentence

```python
from rouge_chinese import Rouge
import jieba # you can use any other word cutting library

hypothesis = "###刚刚发声，A股这种情况十分罕见！大聪明逆市抄底330亿，一篇研报引爆全球，市场逻辑生变？"
hypothesis = ' '.join(jieba.cut(hypothesis)) 

reference = "刚刚过去的这个月，美股总市值暴跌了将近6万亿美元（折合人民币超过40万亿），这背后的原因可能不仅仅是加息这么简单。最近瑞士信贷知名分析师Zoltan Polzsar撰写了一篇极其重要的文章，详细分析了现有世界秩序的崩坏本质以及美国和西方将要采取的应对策略。在该文中，Zoltan Polzsar直指美国通胀的本质和其长期性。同期，A股市场亦出现了大幅杀跌的情况。"
reference = ' '.join(jieba.cut(reference))

rouge = Rouge()
scores = rouge.get_scores(hypothesis, reference)
```

*Output:*

```json
[
  {
    "rouge-1": {
      "f": 0.4786324739396596,
      "p": 0.6363636363636364,
      "r": 0.3835616438356164
    },
    "rouge-2": {
      "f": 0.2608695605353498,
      "p": 0.3488372093023256,
      "r": 0.20833333333333334
    },
    "rouge-l": {
      "f": 0.44705881864636676,
      "p": 0.5277777777777778,
      "r": 0.3877551020408163
    }
  }
]
```

*Note: "f" stands for f1_score, "p" stands for precision, "r" stands for recall.*

###### Score multiple sentences
```python
import json
from rouge_chinese import Rouge

# Load some sentences
with open('./tests/data.json') as f:
  data = json.load(f)

hyps, refs = map(list, zip(*[[d['hyp'], d['ref']] for d in data]))
rouge = Rouge()
scores = rouge.get_scores(hyps, refs)
# or
scores = rouge.get_scores(hyps, refs, avg=True)
```

*Output (`avg=False`)*: a list of `n` dicts:

```
[{"rouge-1": {"f": _, "p": _, "r": _}, "rouge-2" : { .. }, "rouge-l": { ... }}]
```


*Output (`avg=True`)*: a single dict with average values:

```
{"rouge-1": {"f": _, "p": _, "r": _}, "rouge-2" : { ..     }, "rouge-l": { ... }}
``` 

###### Score two files (line by line)
Given two files `hyp_path`, `ref_path`, with the same number (`n`) of lines, calculate score for each of this lines, or, the average over the whole file. 

```python
from rouge_chinese import FilesRouge

files_rouge = FilesRouge()
scores = files_rouge.get_scores(hyp_path, ref_path)
# or
scores = files_rouge.get_scores(hyp_path, ref_path, avg=True)
```

### Use it from the shell (JSON Output)
```
$rouge -h
usage: rouge_chinese [-h] [-f] [-a] hypothesis reference

Rouge Metric Calculator

positional arguments:
  hypothesis  Text of file path
  reference   Text or file path

optional arguments:
  -h, --help  show this help message and exit
  -f, --file  File mode
  -a, --avg   Average mode

```

e.g. 


```shell
# Single Sentence
rouge_chinese "### 刚刚 发声 ， A股 这种 情况 十分 罕见 ！ 大 聪明 逆市 抄底 330 亿 ， 一篇 研报 引爆 全球 ， 市场 逻辑 生变 ？" \
      "刚刚 过去 的 这个 月 ， 美股 总 市值 暴跌 了 将近 6 万亿美元 （ 折合 人民币 超过 40 万亿 ） ， 这 背后 的 原因 可能 不仅仅 是 加息 这么 简单 。 最近 瑞士 信贷 知名 分析师 Zoltan   Polzsar 撰写 了 一篇 极其重要 的 文章 ， 详细分析 了 现有 世界秩序 的 崩坏 本质 以及 美国 和 西方 将要 采取 的 应对 策略 。 在 该文 中 ， Zoltan   Polzsar 直指 美国 通胀 的 本质 和 其 长期性 。 同期 ， A股 市场 亦 出现 了 大幅 杀跌 的 情况 。"

# Scoring using two files (line by line)
rouge_chinese -f ./tests/hyp.txt ./ref.txt

# Avg scoring - 2 files
rouge_chinese -f ./tests/hyp.txt ./ref.txt --avg
```