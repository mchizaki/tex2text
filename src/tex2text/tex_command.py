"""
* Written by CK
"""
import re
from dataclasses import dataclass
SHOW = True
TMPSTR_NEWLINE  = '___NEWLINE___'
TMPSTR_NEWLINE2 = '___NEWLINE2___'

@dataclass
class ReplacedCommand():
    old: str
    new: str

@dataclass
class ReplacedCommandWithContent():
    cmd: str
    new_fmt: str
    prefix: str | None = None


def replace_command(
    text: str,
    show: bool = SHOW,
    replaced_commands:              list[list] = [],
    replaced_commands_with_content: list[dict] = [],
    removed_commands:               list[str]  = [],
    removed_commands_with_content:  list[str]  = [],
    tmpstr_newline:                 str        = TMPSTR_NEWLINE,
    tmpstr_newline2:                str        = TMPSTR_NEWLINE2
) -> str:
    """
    replaced_commands = [
        [ 'old1', 'new1' ], [ 'old2', 'new2' ], ...
    ]
    replaced_commands_with_content = [
        {
            'cmd'     : 'cite',
            'new_fmt' : '[*]'
        },
        {
            'cmd'     : 'cite',
            'new_fmt' : '[*]',
            'prefix'  : 'Ref. '
        },
        ...
    ]
    """

    if show: print()
    for command in replaced_commands:
        command = ReplacedCommand( old = command[0], new = command[1] )

        _len = len( text )
        text = text.replace( command.old, command.new )

        if _len != len( text ):
            if show: print( f' > "{command.old}" => "{command.new}"' )


    if show: print()
    for command in replaced_commands_with_content:
        command = ReplacedCommandWithContent( **command )

        if command.prefix is None:
            prefix = ''
        else:
            prefix = command.prefix

        match_list = re.finditer(
            prefix + r'\\' + command.cmd + r'{.*?}',
            text
        )
        offset = 0
        for match in match_list:
            pos_content_start = match.start() + len(prefix) + offset
            pos_content_stop  = match.end() + offset

            content_w_cmd = text[ pos_content_start : pos_content_stop ]
            content = re.findall(
                r'\\' + command.cmd + r'{(.*?)}',
                content_w_cmd
            )[0]
            replaced_content = command.new_fmt.format(
                content  = content,
                newline  = tmpstr_newline,
                newline2 = tmpstr_newline2
            )

            text = text[ : pos_content_start ] + replaced_content + text[ pos_content_stop : ]
            offset += len( replaced_content ) - len( content_w_cmd )

            if show: print( f' > "{prefix}{content_w_cmd}" => "{prefix}{replaced_content}"' )


    #==============================================================#
    # other commands => removed
    #==============================================================#
    if show: print()
    for command in removed_commands_with_content:
        match_list = re.finditer(
            r'\\' + command + '{.*?}',
            text
        )
        offset = 0
        for i, match in enumerate( match_list ):
            pos_content_start = match.start() + offset
            pos_content_stop  = match.end()   + offset
            content = text[ pos_content_start : pos_content_stop ]

            # cmd = re.findall( r'\\(.*?){', content )[0]
            # if cmd not in removed_commands_with_content:
            #     continue

            # skip if content is in inline equation
            cnt_dollar = text[ : pos_content_start ].count( '$' )
            if cnt_dollar % 2 != 0:
                print( 'skip', command, content )
                continue

            text = text[ : pos_content_start ] + text[ pos_content_stop : ]
            offset -= len( content )
            if show and i == 0: print( f' > remove "\\{command}{{***}}"' )


    for command in removed_commands:
        match_list = re.finditer( rf'\\{command}', text )

        offset = 0
        for i, match in enumerate( match_list ):
            pos_content_start = match.start() + offset
            pos_content_stop  = match.end()   + offset
            content = text[ pos_content_start : pos_content_stop ]

            # skip if content is in inline equation
            # cnt_dollar = text[ : pos_content_start ].count( '$' )
            # if cnt_dollar % 2 != 0:
            #     continue

            text = text[ : pos_content_start ] + text[ pos_content_stop : ]
            offset -= len( content )

            if show and i == 0:
                print( f'> remove "{content}"' )

    return text


def replace_other(
    text: str,
    show: bool = SHOW
) -> str:
    text = text.replace( ' ,', ',' )
    text = text.replace( ' .', '.' )
    text = text.replace( '[ $', '[$' )
    text = text.replace( '( $', '($' )
    text = text.replace( '$ ]', '$]' )
    text = text.replace( '$ )', '$)' )
    text = text.replace( ',  ', ', ' )
    text = text.replace( '.  ', '. ' )

    # text = text.replace( '{', '' )
    # text = text.replace( '}', '' )

    text = text.replace( '--', '–' )

    text = re.sub( '\s+', ' ', text )


    # quotation
    if show: print()
    match_list = re.finditer( r"``.*?''", text )
    delta_offset = len( '""' ) - len( "``''" )
    offset = 0
    for match in match_list:
        pos_content_start = match.start() + offset
        pos_content_stop  = match.end() + offset
        content = text[ pos_content_start+2 : pos_content_stop-2 ]

        text = text[ : pos_content_start ] + f'"{content}"' + text[ pos_content_stop : ]
        offset += delta_offset
        if show: print( f' > ``{content}\'\' => \"{content}\"' )

    match_list = re.finditer( r"`.*?'", text )
    delta_offset = len( "''" ) - len( "`'" )
    offset = 0
    for match in match_list:
        pos_content_start = match.start() + offset
        pos_content_stop  = match.end() + offset
        content = text[ pos_content_start+1 : pos_content_stop-1 ]

        text = text[ : pos_content_start ] + f"'{content}'" + text[ pos_content_stop : ]
        offset += delta_offset
        if show: print( f' > `{content}\' => \'{content}\'' )

    return text