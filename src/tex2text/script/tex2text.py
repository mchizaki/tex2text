#!/usr/bin/env python
"""
* Written by CK
"""
import argparse

from tex2text import TeX2Text

parser = argparse.ArgumentParser(
    description = 'convert tex to plain text.'
)

parser.add_argument(
    '-i', '--input-tex',   type=str, required=True,
    help = 'path of input tex file'
)
parser.add_argument(
    '-o', '--output-text', type=str, required=True,
    help = 'path of output text file'
)
parser.add_argument(
    '-p', '--props-jsonc', type=str, default=None,
    help = 'path of props jsonc file'
)

args = parser.parse_args()

input_tex_file  = args.input_tex
output_txt_file = args.output_text


def main():
    tex2Text = TeX2Text( args.props_jsonc )
    text = tex2Text.tex2text_initialize( input_tex_file )
    text = tex2Text.tex2text_main( text )
    text = tex2Text.tex2text_finilize( text )

    with open( output_txt_file, 'w' ) as outfile:
        outfile.write( text )


if __name__ == '__main__':
    main()
