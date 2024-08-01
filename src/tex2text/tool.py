"""
* written by CK
"""
import re
import sys

TMPSTR_EXCEPT = '___EXCEPT___'

def replace_in_range(
    text: str,
    old: str,
    new: str,
    range_symbol_re: str = '\\"',
    range_symbol_except: str | None = None
):
    """
    * length of range_symbol_re (except escape symbol) must be 1
    * range_symbol_re:     for re.finditer
    * range_symbol_except: avoid searching
    """
    rs = range_symbol_re

    if range_symbol_except is not None:
        text = text.replace( range_symbol_except, TMPSTR_EXCEPT )

    positions = [ match.start() for match in re.finditer( rs, text ) ]
    if len( positions ) % 2 != 0:
        print( '[error] replace_in_range' )
        print( f'invalid number of {range_symbol_re}: {len( positions )}' )
        sys.exit(1)

    offset = 0
    for _pos_l, _pos_r in zip( positions[::2], positions[1::2] ):
        pos_l = _pos_l + offset
        pos_r = _pos_r + offset

        text_l, content, text_r = (
            text[ : pos_l+1 ],
            text[ pos_l+1 : pos_r ],
            text[ pos_r : ]
        )

        new_content = content.replace( old, new )

        text = text_l + new_content + text_r
        offset += len( new_content ) - len( content )


    if range_symbol_except is not None:
        text = text.replace( TMPSTR_EXCEPT, range_symbol_except )

    return text
