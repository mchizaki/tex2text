"""
* Written by CK
"""
import re
import sys
import numpy as np
# try:
#     import numpy as np
# except:
#     pass
from dataclasses import dataclass

STR_INLINE_EQ   = 'inline-eq'
_TMPSTR_DOLLAR = '___DOLLAR___'

@dataclass
class ReplacedCommand():
    old: str
    new: str


def remove_duplicated_bracket( eq: str ) -> str:
    l_positions = np.array([ match.start() for match in re.finditer( '{', eq ) ])
    r_positions = np.array([ match.start() for match in re.finditer( '}', eq ) ])

    num_brackets = len( l_positions )
    if num_brackets != len( r_positions):
        print( '[error] remove_duplicated_bracket' )
        print( 'The numbers of "{" and "}" do not match.' )
        sys.exit(1)

    pairs = np.zeros([ num_brackets, 2 ], dtype=int )
    for i, r_pos in enumerate( r_positions ):
        delta = r_pos - l_positions
        pos_index,  = np.where( delta == np.min( delta[ delta > 0 ] ) )[0]
        l_pos       = l_positions[ pos_index ]
        l_positions = np.delete( l_positions, pos_index  )

        pairs[ i, : ] = np.array([ l_pos, r_pos ])
    # pprint( pairs )

    offset = 0
    for i in range( num_brackets - 1 ):
        pair = pairs[ i, : ]

        _pairs = pairs[ i+1:, : ]
        delta = pair - _pairs

        where = (
            np.sum( delta, axis=1 ) == 0
        ) & (
            np.abs( delta[ :, 0 ] ) == 1
        )
        _pairs = _pairs[ where, : ]

        if len( _pairs ) == 0:
            continue

        _pair = _pairs[0]

        # outer bracket
        outer_l = min( pair[0], _pair[0] ) + offset
        outer_r = max( pair[1], _pair[1] ) + offset

        eq = eq[ : outer_l ] + eq[ outer_l+1 : outer_r ] + eq[ outer_r+1 : ]
        offset -= 2

    # print( offset )

    return eq


def simplify_eq(
    eq: str,
    replaced_symbols: list[list] = []
) -> str:

    for symbol in replaced_symbols:
        symbol = ReplacedCommand( old = symbol[0], new = symbol[1] )
        eq = eq.replace( symbol.old, symbol.new )

    eq = remove_duplicated_bracket( eq )
    eq = ''.join( eq.split() )

    return eq


def replace_inline_eq(
    text: str,
    simplify:         bool = True,
    replaced_symbols: list[list] = [],
    str_eq:           str  = STR_INLINE_EQ,
    eq_len_thr:       int  = 20
) -> str:
    """
    after remove environment
    """
    positions = [ match.start() for match in re.finditer( r'\$', text ) ]

    if len( positions ) % 2 != 0:
        print( '[error] replace_inline_eq' )
        print( f'invalid number of "$" for inline equations: {len(positions)}' )
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

        if simplify:
            new_content = simplify_eq(
                eq               = content,
                replaced_symbols = replaced_symbols
            )
            if len( new_content ) > eq_len_thr:
                new_content = str_eq
        else:
            new_content = str_eq

        text = text_l + new_content + text_r
        offset += len( new_content ) - len( content )

    return text
