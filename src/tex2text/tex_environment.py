"""
* Written by CK
"""
import re
import sys

_TMPSTR_DISPLAY_EQ = '___DISPLAYEQ___'


def insert_eq_punctuation_mark(
    text: str,
    tmpstr_display_eq: str = _TMPSTR_DISPLAY_EQ
) -> str:
    match_eq_list = re.finditer( tmpstr_display_eq, text )
    offset = 0
    for match in match_eq_list:
        pos_eq_end   = match.end() + offset
        pos_next_str = pos_eq_end + 1

        if text[ pos_next_str ].islower():
            punctuation_mark = ','
        else:
            punctuation_mark = '.'

        text = text[ : pos_eq_end ] + punctuation_mark + text[ pos_eq_end: ]
        offset += len( punctuation_mark )

    return text


def remove_environment(
    text: str,
    eq_environment_names: list[str] = [],
    tmpstr_display_eq: str = _TMPSTR_DISPLAY_EQ
) -> str:

    def remove_str(
        text: str,
        removed_str: str,
        pos_start: int | None = None,
    ):
        str_len = len( removed_str )
        if pos_start is None:
            pos_start = text.find( removed_str )
            if pos_start == -1:
                print( '[error] remove_str' )
                print( f'"{remove_str}" is not found.' )
                sys.exit(1)

        return text[ : pos_start ] + text[ pos_start + str_len : ]

    pattern = r'\\begin{(.*?)}'
    env_names = re.findall( pattern, text )
    # pprint( env_names )

    for env_name in env_names:

        if env_name == 'document':
            continue

        env_begin_str = fr'\begin{{{env_name}}}'
        env_end_str   = fr'\end{{{env_name}}}'

        # env_str = re.findall( rf'\\begin{{{env_name}}}.*?\\end{{{env_name}}}',   text )
        # contents = re.findall( rf'\\begin{{{env_name}}}(.*?)\\end{{{env_name}}}', text )
        # text = remove_str( text, removed_str = env_str )

        pos_env_start = text.find( env_begin_str )
        pos_env_end   = text.find( env_end_str   )

        if pos_env_start == -1 or pos_env_end == -1:
            continue

        if pos_env_start > pos_env_end:
            print( '[error] remove_environment' )
            print( f'\\begin{{env}} or \\end{{env}} of "env = {env_name}" does not exist.' )
            sys.exit(1)

        # remove "\end{env_name}"
        text = remove_str( text, pos_start=pos_env_end, removed_str=env_end_str )


        #==============================================================#
        # nest
        #==============================================================#
        sub_pos_env_start = text[ : pos_env_end ].rfind( env_begin_str )
        if sub_pos_env_start != -1 and sub_pos_env_start > pos_env_start:
            pos_env_start = sub_pos_env_start


        env_content = text[ pos_env_start + len( env_begin_str ) : pos_env_end ]

        # remove "\begin{env_name}" and content
        text = remove_str( text, pos_start=pos_env_start, removed_str=env_begin_str )
        text = remove_str( text, pos_start=pos_env_start, removed_str=env_content )


        #==============================================================#
        # equation
        #==============================================================#
        for eqenv_name in eq_environment_names:
            if env_name != eqenv_name:
                continue
            text = text[ : pos_env_start ] + tmpstr_display_eq + text[ pos_env_start : ]


    pattern = r'\\begin{(.*?)}'
    env_names = re.findall( pattern, text )
    # pprint( env_names )

    return text