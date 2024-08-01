# tex2text
TeXファイルをテキストファイルに変換する。



## Installation

```
$ pip install git+https://github.com/mchizaki/tex2text.git
```


アンインストール：

```
$ pip uninstall tex2text
```


## Usage

```
usage: tex2text.py [-h] -i INPUT_TEX -o OUTPUT_TEXT [-p PROPS_JSONC]

convert tex to plain text.

options:
  -h, --help            show this help message and exit
  -i INPUT_TEX, --input-tex INPUT_TEX
                        path of input tex file
  -o OUTPUT_TEXT, --output-text OUTPUT_TEXT
                        path of output text file
  -p PROPS_JSONC, --props-jsonc PROPS_JSONC
                        path of props jsonc file
```

### サンプルファイル

```
📂tests/
├── 📄sample.tex
├── 📄tex2text-props.tex
└── 📄test.sh
```
