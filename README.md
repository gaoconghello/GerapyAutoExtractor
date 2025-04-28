# Gerapy Auto Extractor

> 本项目是 fork 自 [GerapyAutoExtractor 原项目](https://github.com/Gerapy/GerapyAutoExtractor)。感谢原作者 [Qingcai Cui](https://github.com/cuiqingcai) 的贡献！

---

## Fork 说明

本仓库 fork 的原因：
- 为了适配最新版本的 scikit-learn
- 增加了一些网站的样本用于训练

主要修改内容：
- 使用 scikit-learn 最新版本进行训练
- 扩充了样本数据集以提升模型泛化能力

## 工具脚本使用说明

### 训练分类器 (train_classifier.py)

这个脚本用于训练和验证网页分类器，可以识别列表页和详情页。

**使用方法:**
```bash
# 只验证现有模型的准确率
python train_classifier.py

# 重新训练模型并验证准确率
python train_classifier.py --train
```

**参数说明:**
- `--train`: 使用此参数时会重新训练分类器模型，否则只验证现有模型的准确率

### 获取HTML (fetch_html.py)

这个脚本用于从URL获取HTML内容并保存到数据集目录中，支持批量获取。

**使用方法:**
```bash
# 获取单个URL的HTML内容
python fetch_html.py https://example.com/news/12345

# 批量处理list.txt和detail.txt中的URL
python fetch_html.py

# 将获取的HTML保存到测试目录
python fetch_html.py --test
```

**参数说明:**
- 第一个参数可以是要获取的单个URL，默认会保存为详情页类型
- `--test`: 使用此参数时，HTML会被保存到datasets/test目录下，方便进行测试验证而不影响训练数据

**URL文件格式:**
- datasets/list.txt: 每行一个URL，用于获取列表页
- datasets/detail.txt: 每行一个URL，用于获取详情页


如需了解原项目详情，请访问上方原项目链接。


![Python package](https://github.com/Gerapy/GerapyAutoExtractor/workflows/Python%20package/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gerapy-auto-extractor)
![PyPI](https://img.shields.io/pypi/v/gerapy-auto-extractor)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gerapy-auto-extractor)
![License](https://img.shields.io/badge/license-Apache%202-blue)

This is the Auto Extractor Module for [Gerapy](https://github.com/Gerapy/Gerapy), You can also use it separately.

You can use this package to distinguish between list page and detail page, and we can use it to extract
`url` from list page and also extract `title`, `datetime`, `content` from detail page without any XPath or Selector.

It works better for Chinese News Website than other scenarios.

Introduction: [Introduction](https://www.v2ex.com/t/687948)

## Installation

You can use this command to install this package:

```
pip3 install gerapy-auto-extractor
```

## Usage

Below are the methods this package implemented:

### Extraction of List Page

For list page, you can use `extract_list` method to extract the main list urls and their titles.

### Extraction of Detail Page

For detail page, you can use `extract_title` method to extract title, use `extract_content` method to extract content,
use `extract_datetime` method to extract datetime.

Also you can use `extract_detail` method to extract all above attrs, results are joined as a json.

### Classification of List/Detail Page

You can use `is_list` or `is_detail` method to distinguish if this page is list page or detail page, the type of returned result is `bool`.
Also you can use `probability_of_list` or `probability_of_detail` method to get the probability of the classification of this page, the type of returned result is `float`.

Usage example:

```python
from gerapy_auto_extractor import extract_list, extract_detail, is_detail, is_list, probability_of_detail, probability_of_list
from gerapy_auto_extractor.helpers import content, jsonify

html = content('samples/list/sample.html')
print(jsonify(extract_list(html)))

html = content('samples/detail/sample.html')
print(jsonify(extract_detail(html)))

html = content('samples/detail/sample.html')
print(probability_of_detail(html), probability_of_list(html))
print(is_detail(html), is_list(html))

html = content('samples/list/sample.html')
print(probability_of_detail(html), probability_of_list(html))
print(is_detail(html), is_list(html), )
```

HTML files can be found in [samples](./samples).

Below are outputs:

```
[
  {
    "title": "山东通报\"苟晶事件\"：15人被处理部分事实有反转",
    "url": "http://news.163.com/20/0703/13/FGK7NCOR0001899O.html"
  },
  {
    "title": "胡锡进：香港这仗就是要让华盛顿明白，它管多了",
    "url": "https://news.163.com/20/0702/19/FGI8IUEP0001899O.html"
  },
  {
    "title": "山东一校长为儿子伪造档案11岁开始领国家工资",
    "url": "https://news.163.com/20/0702/21/FGIENBGS0001899O.html"
  },
  {
    "title": "大理西洱河又现\"鱼腾\"奇景市民沿岸围观有人徒手抓",
    "url": "https://news.163.com/20/0704/03/FGLOFC3P0001875P.html"
  },
  {
    "title": "陈国基被任命为香港特别行政区国安委秘书长",
    "url": "https://news.163.com/20/0702/12/FGHFAVS200018AOQ.html"
  },
  {
    "title": "孙力军等6名中管干部被查上半年反腐数据说明啥？",
    "url": "https://news.163.com/20/0703/00/FGIPQ11D0001899O.html"
  },
  {
    "title": "香港特区政府严厉谴责暴徒恶行全力支持警队严正执法",
    "url": "https://news.163.com/20/0702/09/FGH801750001899O.html"
  }
]

0.9990605314033392 0.0009394685966607814
True False
0.033477426883441685 0.9665225731165583
False True
```

Just for Beta.

Needs more effort to improve.

---


## Reference

### Paper

* [面向不规则列表的网页数据抽取技术的研究](http://www.cnki.com.cn/Article/CJFDTotal-JSYJ201509023.htm)
* [基于文本及符号密度的网页正文提取方法](https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2019&filename=GWDZ201908029&v=MDY4MTRxVHJXTTFGckNVUkxPZmJ1Wm5GQ2poVXJyQklqclBkTEc0SDlqTXA0OUhiWVI4ZVgxTHV4WVM3RGgxVDM=)
* [基于块密度加权标签路径特征的Web新闻在线抽取](https://kns.cnki.net/kcms/detail/detail.aspx?filename=PZKX201708010&dbcode=CJFQ&dbname=CJFD2017&v=)
* [基于DOM树和视觉特征的网页信息自动抽取](http://www.cnki.com.cn/Article/CJFDTOTAL-JSJC201310069.htm)

### Project

* [GeneralNewsExtractor](https://github.com/kingname/GeneralNewsExtractor)
* [Readability](https://github.com/buriy/python-readability)

## Citing 

If you use Gerapy Auto Extractor in your research or project, please add a reference using the following BibTeX entry.

```
@misc{cui2020gerapy,
  author =       {Qingcai Cui},
  title =        {Gerapy Auto Extractor},
  howpublished = {\url{https://github.com/Gerapy/GerapyAutoExtractor}},
  year =         {2020}
}
```

