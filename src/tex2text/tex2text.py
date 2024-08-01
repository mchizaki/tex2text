"""
* Written by CK
"""
import re
import os
from dataclasses import dataclass, field

from .jsonc import read_jsonc
from .tex_command import (
    replace_command as _replace_command,
    replace_other   as _replace_other
)
from .tex_environment import (
    remove_environment         as _remove_environment,
    insert_eq_punctuation_mark as _insert_eq_punctuation_mark
)
from .tex_eq import replace_inline_eq as _replace_inline_eq


PROPS_JSONC = os.path.join(
    os.path.dirname( __file__ ),
    'tex2text-props.jsonc'
)

TMPSTR_DISPLAY_EQ = '___DISPLAYEQ___'
TMPSTR_NEWLINE    = '___NEWLINE___'
TMPSTR_NEWLINE2   = '___NEWLINE2___'
TMPSTR_PERCENT    = '___PERCENT___'
TMPSTR_DOLLAR     = '___DOLLAR___'

@dataclass
class TeX2TextProps():
    inline_eq_simplified           : bool = True
    inline_eq_len_thr              : int  = 30

    inline_eq_str                  : str  = 'inline-eq'
    display_eq_str                 : str  = r'\[display-eq\]'

    show                           : bool = False

    eq_environment_names           : list = field( default_factory = list )
    replaced_commands_with_content : list = field( default_factory = list )
    replaced_commands              : list = field( default_factory = list )
    replaced_math_symbols          : list = field( default_factory = list )
    removed_commands               : list = field( default_factory = list )
    removed_commands_with_content  : list = field( default_factory = list )


class TeX2Text():

    def __init__( self, props_jsonc = None ):

        props_dict = read_jsonc( PROPS_JSONC )

        if props_jsonc is not None:
            props_dict.update( **read_jsonc( props_jsonc ) )

        self.props = TeX2TextProps( **props_dict )


    #==============================================================#
    # tex2text method
    #==============================================================#
    def _replace_escape_symbols( self, text: str ) -> str:
        text = text.replace( '\\%', TMPSTR_PERCENT )
        text = text.replace( '\\$', TMPSTR_DOLLAR  )

        return text

    def tex2text_initialize( self, input_tex_file: str ) -> str:
        """
        * read file
        * add new line & remove comments
        """
        with open( input_tex_file, 'r' ) as infile:
            text = infile.read()
            text = self._replace_escape_symbols( text )
            read_lines = text.splitlines()

            # read_lines = infile.read().splitlines()

            new_line_cnt = 0
            percent_end = False
            text = ''

            for i, line in enumerate( read_lines ):
                # print( i )

                line = line.strip()

                #==============================================================#
                # start a new line & skip comment line
                #==============================================================#
                # new line
                if line == '':
                    if new_line_cnt == 0:
                        text += TMPSTR_NEWLINE
                    new_line_cnt += 1
                    # if no_str:
                    #     text += TMPSTR_NEWLINE
                    # no_str = True
                    percent_end = False
                    continue

                # skip comment line
                if line[0] == '%':
                    continue

                new_line_cnt = 0
                if line[0] != '.' or line[0] != ',' and not percent_end:
                    text += ' '

                #==============================================================#
                # remove comment
                #==============================================================#
                # "\%" is not a comment
                line = line.replace( r'\%', TMPSTR_PERCENT )
                if line.find( '%' ) == -1:
                    percent_end = False
                else:
                    percent_end = True
                line = re.sub( r'%.*', '', line )

                text += line

        return text


    def tex2text_main( self, text: str ) -> str:
        text = self.remove_environment( text )
        text = self.replace_inline_eq( text ) # after remove_environment
        text = self.replace_command( text )
        text = self.insert_eq_punctuation_mark( text )
        text = self.replace_other( text )
        return text


    def tex2text_finilize( self, text: str ) -> str:

        # remove extra spaces
        text = text.replace( f'{TMPSTR_NEWLINE} ',   TMPSTR_NEWLINE )
        text = re.sub      ( f'({TMPSTR_NEWLINE})+', TMPSTR_NEWLINE, text )

        # replace tmpstr
        text = text.replace( TMPSTR_NEWLINE,    '\n' )
        text = text.replace( TMPSTR_NEWLINE2,   '\n' )
        text = text.replace( TMPSTR_DISPLAY_EQ, self.props.display_eq_str )
        text = text.replace( TMPSTR_PERCENT,    '%' )
        text = text.replace( TMPSTR_DOLLAR,     '$' )

        return text


    #==============================================================#
    # procedures to replace & remove text
    #==============================================================#
    def remove_environment( self, text: str ) -> str:
        return _remove_environment(
            text,
            eq_environment_names = self.props.eq_environment_names,
            tmpstr_display_eq    = TMPSTR_DISPLAY_EQ
        )

    def replace_inline_eq( self, text: str ) -> str:
        return _replace_inline_eq(
            text,
            simplify         = self.props.inline_eq_simplified,
            replaced_symbols = self.props.replaced_math_symbols,
            str_eq           = self.props.inline_eq_str,
            eq_len_thr       = self.props.inline_eq_len_thr
        )

    def replace_command( self, text: str ) -> str:
        return _replace_command(
            text,
            show                           = self.props.show,
            replaced_commands              = self.props.replaced_commands,
            replaced_commands_with_content = self.props.replaced_commands_with_content,
            removed_commands               = self.props.removed_commands,
            removed_commands_with_content  = self.props.removed_commands_with_content,
            tmpstr_newline                 = TMPSTR_NEWLINE,
            tmpstr_newline2                = TMPSTR_NEWLINE2
        )

    def insert_eq_punctuation_mark( self, text: str ) -> str:
        return _insert_eq_punctuation_mark( text )

    def replace_other( self, text: str ) -> str:
        return _replace_other(
            text,
            show = self.props.show
        )
