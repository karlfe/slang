# vhdl lexer

import ply.lex as lex
import vhtokens

class VhdlLexer():
    def __init__(self, **kwargs):
        self.tokens = vhtokens.vh_tokens + tuple(vhtokens.vh2000_reserved.values())
        self.reserved = vhtokens.vh2000_reserved

        self.lexer = lex.lex(object=self, **kwargs)
        self.lexer.lineStart = 0

    #multi-character token rules -- no action
    t_BASEDLIT = r'1?[0-9][#][0-9a-fA-F](_?[0-9a-fA-F])*(\.[0-9a-fA-F](_?[0-9a-fA-F])*)?[#]([eE][+-]?[0-9](_?[0-9])*)?'
    t_CHARLIT = r'\'.\''

    t_DECLIT = r'[0-9](_?[0-9])*(\.[0-9](_?[0-9])*)?([eE][+-]?[0-9](_?[0-9])*)?'
    t_STRLIT = r'".*?"'  
    # todo:  this rule doesn't support embedded '"'
    #        nor does it support the alternative quote character '%'

    # two character token rules -- no action
    t_ARROW = r'=>'
    t_BOX = r'<>'
    t_EXP = r'\*\*'
    t_GE = r'>='
    t_LE = r'<='
    t_NE = r'/='

    t_VASSIGN = r':='

    # one character token rules -- no action
    literals = "&|,:/.+>[(<*+])="
    # todo: replacement characters for '|', '#'

    t_ignore = " \t"
    t_TICK = r"'"
    t_SEMI = r';'
    # ';' ('SEMI') has a specific token because there are end of line actions that can be taken

    # token rules with actions
    def t_COMMENT(self, t):
        r'--.*'
        # skip comments
        pass

    # '-' ('MINUS') not in literals above because it is also the character that
    # starts a comments and literals are recognized first.  By using a specific
    # token for the '-' character vs. a literal, comments are recognized first.
    # Any other '-' then is recognized as the 'MINUS' token
    def t_MINUS(self, t):
        r'-'
        return t

        # match BITSTRLIT first since it starts with a letter like an IDENT
    def t_BITSTRLIT(self, t):
        r'([bB]"[0-1](_?[0-1])*?")|([oO]"[0-7](_?[0-7])*?")|([xX]"[0-9a-fA-F](_?[0-9a-fA-F])*?")'
        return t

    def t_IDENT(self, t):
        r'(_*[a-zA-Z]([_a-zA-Z0-9])*)|(\\.*?\\)'
        # This rule is permissive: it allows idents with repeated and trailing underscores
        # to allow internal names in lexical analysis. Legal ident names must be checked
        # during semantic analysis.  This rule requires at least 1 letter before any number.
        t.type = self.reserved.get(t.value.lower(), 'IDENT')
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.lineStart = t.lexpos + 1

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # end of token rules

    def test(self, data):
        self.lexer.input(data)
        for token in self.lexer:
            print(token)



def tokens_to_test():
    # testing string with many different tokens
    test_str = r'1 3 12.2 -137.987 1004.987654E12 x"189AbDdF" b"1010" O"01234567" '
    test_str += r"name name1 _name10 name_1_0 \this is an extended id\ 'a' 'Z' '&' => = := >= ** "
    test_str += '"+" "**" __this__is____an_internal__name__ _9 _p9-- this is a comment\n'
    test_str += '"this is a string" 2#1010#E10 16#9Ac7# -- this is a comment\n'
    test_str += '>:/+'

    #for token in vhtokens.vh2000_reserved.values():
    #    test_str += token + '\n'

    return test_str

def tokens_to_test2():
    test_str = "package standard is\n"
    test_str += "end package standard;"
    return test_str

def tokens_test(data):
    lexer = VhdlLexer()
    lexer.test(data)

if __name__ == '__main__':
    tokens_test(tokens_to_test())
    tokens_test(tokens_to_test2())
