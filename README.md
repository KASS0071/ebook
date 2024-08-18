# 1.配备工具
## 1.1 python
·PyMuPDF
## 1.2 latex（texlive）
·可能需要下载语言包（如中文宏包）

·转换为pdf需要下载xelatex或pdftex工具
# 2.文件注释
_**insert**_：用于根据关键字添加分页符 换行符 段落格式 章节标题加粗等

_**bm**_；bookmark 在pdf中添加书签 （cpbm效果一致）

_**dl**_：delete line 在有下述情况时删除换行（出错率较高谨慎使用）
<img width="664" alt="截屏2024-08-18 22 58 16" src="https://github.com/user-attachments/assets/5ded06e6-f64e-475e-978d-01bf4773f2b2">

_**dbl**_；delete blank line 在上图情况下删除空行（出错率较高谨慎使用）

_**由于通过关键词添加内容，可能会误加，建议检查**_

# 3.操作流程
## 3.1下载文本
  例：从Project Gutenberg上下载西游记
      
      wget ‘https://www.gutenberg.org/cache/epub/23962/pg23962.txt’
## 3.2 添加基本格式 
按需使用[dl](https://github.com/KASS0071/ebook/blob/main/25559%20fin/dl.py)  [dbl](https://github.com/KASS0071/ebook/blob/main/24042/dbl.py)

使用insert

  [insert1](https://github.com/KASS0071/ebook/blob/main/23818/insert02.py) 按章回加分页符，加分行符，段落前空两格，章节标题加粗并在后面添加空行
  
  [insert2](https://github.com/KASS0071/ebook/blob/main/23910/insert.py) 按章回加分页符，加分行符，段落前空两格，章节标题加粗并在后面添加空行，在此基础上在“但见，有诗为证,詩曰, 正是，寫道"关键词后空行
  
  [insert3](https://github.com/KASS0071/ebook/blob/main/25327/insert.py) 按章回加分页符，加分行符，段落前空两格，章节标题加粗 **居中** 并在后面添加空行

  [insert4](https://github.com/KASS0071/ebook/blob/main/52280/insert.py) 分卷版

## 3.3 编写tex文件并生成pdf

现有的latex文件均支持中文，可以随意使用一个改变作者和书名用于生成

    xelatex ？？？.tex

根据提示输入txt文件名生成pdf
## 3.4 检查pdf是否有排版错误
## 3.5 添加书签
运行[cpbm](https://github.com/KASS0071/ebook/blob/main/23910/cpbm.py) 章回

