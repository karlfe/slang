# AST classes shared in different parsers

from abc import ABC
from vhlex import VhdlLexer

class FileLocation():
    def __init__(self, sline, scol, eline=-1, ecol=-1):
        self.sline = sline
        self.scol = scol
        if eline >= 0:
            self.eline = eline
        if ecol >= 0:
            self.ecol = ecol

    def __repr__(self):
        return self.dumpInternals()
    
    def dumpInternals(self):
        result = f"FileLocation(sline={self.sline}, scol={self.scol}"
        if hasattr(self, 'eline') and self.eline >= 0:
            result += f", eline={self.eline}"
        if hasattr(self, 'ecol') and self.ecol >= 0:
            result += f", ecol={self.ecol}"
        result += ")"
        return result

class Symbol():
    def __init__(self, name, fLoc=None):
        self.name = name
        self.loc = fLoc
        self.ast = None  # the defining object: design units, declarations
        self.defn = None

    def __str__(self):
        return self.decompile()
        
    def decompile(self):
        return self.name
       
    def __repr__(self):
        return self.dumpInternals()
        
    def dumpInternals(self, indent=0):
        result = "Symbol("
        result += 'name="' + self.name + '", '
        result += "loc=" + self.loc.__repr__()
        if self.ast:
            result += ", ast=<decl>"
        if self.defn:
            result += ", defn=<definition>"
        result += ")"
        return result

    def setLoc(self, p, sidx, eidx=-1):
        eline = -1
        ecol = -1
        sline = p.lineno(sidx)
        scol = start_column(p, sidx)
        if eidx != -1:
            eline = p.lineno(eidx)
            ecol = end_column(p, eidx) 
        self.loc = FileLocation(sline, scol, eline, ecol)


class SymbolTable():     # does this need to be concrete?  are there unnamed scopes in Vhdl?
    def __init__(self, outer=None):
        # outer is a single SymbolTable or a vhContextClause
        self.outer = outer
        self.symbols = {}
    
    def add(self, sym):
        key = str(sym)  # escaped names, character literals, and string literals use case-sensitive lookup
        if key[0] != '"' and key[0] != "'" and key[0] != '\\':
            # identifier names use case-insensitive lookup
            key = key.lower()
        self.symbols[key] = sym

    def find(self, name):
        key = name  # escaped names, character literals, and string literals use case-sensitive lookup
        if key[0] != '"' and key[0] != "'" and key[0] != '\\':
            # identifier names use case-insensitive lookup
            key = key.lower()
        sym = self.symbols.get(key, None)  # dict.get() not SymbolTable.get()
        return sym
    
    def get(self, name):
        sym = self.find(name)
        if sym:
            return sym
        sym = Symbol(name)
        self.add(sym)
        return sym
    
    # get symbol data using the yacc production and the production index
    def pget(self, p, idx):
        sym = self.find(p[idx])
        if sym:
            return sym   
        sym = Symbol(p[idx], FileLocation(p.lineno(idx), start_column(p, idx)))
        self.add(sym)
        return sym

    def search(self, name):
        syms = []
        sym = self.find(name)
        if sym:
            syms.append(sym)
        if self.outer:
            syms += self.outer.search(name)
        return syms


# a Scope is named symbol table.  The name is represented by the symbol of the 
# the design_unit name, subprogram name, or record name which introduces the scope
class Scope(SymbolTable):
    def __init__(self, nameSym, outer=None):
        super().__init__(outer)
        self.name = nameSym
        self.public_subscopes = []
     
    # the next two are for simple form (name only) internal dumping
    def __str__(self):
        return self.name.__str__()
    
    def decompile(self):
        return self.__str__()

    def __repr__(self):
        return self.dumpInternals()
    
    def dumpInternals(self, indent=0):
        result = "Scope("
        result += "name=" + self.name.__str__() + ", "
        result += "outer=" + self.outer.__str__() + ", "
        result += "symbols=" + self.symbols.__str__() + ", "
        pfx = "public_subscopes=["
        for scope in self.public_subscopes:
            result += pfx + str(scope)
            pfx = ", "
        result += "])"
        return result
    
    # override SymbolTable.search()
    def search(self, name):
        syms = []
        sym = self.find(name)
        if sym:
            syms.append(sym)
        for scope in self.public_subscopes:
            sym = scope.find(name)
            if sym:
                syms.append(sym)
        if self.outer:
            syms += self.outer.search(name)
        return syms

    
# utility functions
def end_column(p, idx):
    return p.lexpos(idx) - p.lexer.lineStart - 1

def start_column(p, idx):
    """Compute column given the current line start (saved in the lexer)
       and the token lexical position"""
    return end_column(p, idx) - len(p[idx]) + 1   

def indentPrefix(indent):
    result = ""
    for ii in range(0,indent):
        result += "    "
    return result
