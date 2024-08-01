"""
* Written by CK
"""
import re
import json
from .tool import replace_in_range

TMPSTR_DOUBLE_SLASH  = '___DOUBLE_SLASH___'
TMPSTR_COMMENT_START = '___CSTART___'
TMPSTR_COMMENT_END   = '___CEND___'


def read_jsonc( filepath: str ) -> dict:
    with open( filepath, 'r', encoding='utf-8' ) as f:
        text = f.read()

    common_props = dict(
        range_symbol_re     = '\\"',
        range_symbol_except = '\\"'
    )

    # //, /*, */ in " " is not the comment symbol
    text = replace_in_range(
        text,
        old = '//',
        new = TMPSTR_DOUBLE_SLASH,
        **common_props
    )
    text = replace_in_range(
        text,
        old = '/*',
        new = TMPSTR_COMMENT_START,
        **common_props
    )
    text = replace_in_range(
        text,
        old = '*/',
        new = TMPSTR_COMMENT_END,
        **common_props
    )

    text = re.sub( r'/\*[\s\S]*?\*/|//.*', '', text )

    text = text.replace( TMPSTR_DOUBLE_SLASH,  '//' )
    text = text.replace( TMPSTR_COMMENT_START, '/*' )
    text = text.replace( TMPSTR_COMMENT_END,   '*/' )

    json_obj = json.loads( text )
    return json_obj
