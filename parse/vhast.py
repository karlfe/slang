# classes to represent the abstract syntax tree for vhdl

# Symbols begin life during parsing as simple name strings
# The strings get converted to Symbols during semantic processing

from abc import ABC
from lcommon import *

class vhDesignFile():
    def __init__(self, scope, filepath=""): # designUnits expects a list
        self.filepath = filepath
        self.scope = scope
        self.units = []

    def __str__(self):
        return self.decompile()
    
    def decompile(self):
        result = f"\n-- file: {self.filepath}\n\n"
        for unit in self.units:
            result += unit.decompile() + "\n\n"
        return result

    def __repr__(self):
        return self.dumpInternals()
    
    def dumpInternals(self):
        result = f"vhDesignFile(filepath={self.filepath},\n "
        result += "\tscope=" + self.scope.dumpInternals() + ", "
        first = '[ '
        result += "units="
        for unit in self.units:
            result += first
            first = ", "
            result += unit.dumpInternals(1)
        result += " ])"
        return result

# base class for primary and secondary units
class vhDesignUnit(ABC):
    def __init__(self, name, outerScope, context=None):
        self.name = name
        self.context = context
        self.scope = Scope(name, outerScope)


class vhPackageDecl(vhDesignUnit):
    def __init__(self, name, outerScope):
        super().__init__(name, outerScope)
        self.decls = []

    def __str__(self):
        return self.decompile()
    
    def __repr(self):
        return self.dumpInternals()
    
    def decompile(self, indent=0):
        result = ""
        if self.context:
            result += str(self.context) + "\n\n"
        result += f"package {str(self.name)} is\n"
        for decl in self.decls:
            result += decl.decompile(indent+1)     # design units are always indent 0, these decls are always indent 1
        result += f"end package {str(self.name)};\n\n"
        return result
    
    def dumpInternals(self, indent=0):
        result = "vhPackageDecl(sym=" + repr(self.sym)
        result += ", context=" + repr(self.context)
        result += ", scope=" + repr(self.scope)
        pfx = ", decls=[ "
        for decl in self.decls:
            result += pfx + repr(decl)
            pfx = ", "
        result += " ])"
        return result


class vhContextClause():
    def __init__(self):
        self.libs = {}
        self.uses = {}
        self.loc = FileLocation(-1,-1)

    def __str__(self):
        return self.decompile()
    
    def __repr__(self):
        return self.dumpInternals()
    
    def decompile(self):
        result = ""
        for lib in self.libs.values():
            result += str(lib)
        for use in self.uses.values():
            result += str(use)
        return result
    
    def dumpInternals(self):
        result = "vhContextClause(libs="
        pre = '['
        for lib in self.libs.values():
            result += pre + repr(lib)
            pre = ','
        result += "], uses="
        pre = '['
        for use in self.uses.values():
            result += pre + repr(use)
        result += "], " + repr(self.loc) + ')'
        return result
    
    def addItems(self, items):
        for item in items:
            item.addToContext(self)
    
    def addUse(self, use):
        key = use.selected
        if not type(key) is str:
            key = str(key)
        if not key in self.uses:
            self.uses[key] = use

    def addLibrary(self, lib):
        key = lib.logical.decompile()
        if not key in self.libs:
            self.libs[key] = lib

class vhUse():
    def __init__(self, selected):
        self.selected = selected    # for now a list of symbols
    
    def __str__(self):
        return self.decompile()
    
    def __repr__(self):
        return self.dumpInternals()
    
    def decompile(self):
        names = list(str(sym) for sym in self.selected[0])
        names.append(str(self.selected[1]))
        result = "USE " + '.'.join(names) + ";\n"
        return result
    
    def dumpInternals(self):
        result = f"Use(selected={str(self.selected)})"
        return result

    def addToContext(self, context):
        context.addUse(self)


class vhLibrary():
    def __init__(self, sym):
        self.logical = sym       # a symbol or 'ALL'
        self.physical = None     # a string, the path to the library folder

    def __str__(self):
        return self.decompile()
    
    def __repr__(self):
        return self.dumpInternals()
    
    def decompile(self):
        result = f"LIBRARY {str(self.logical)};\n"
        return result
    
    def dumpInternals(self):   
        result = f"Library(logical={str(self.logical)}, physical={str(self.physical)})"
        return result

    def addToContext(self, context):
        context.addLibrary(self)


class vhExpr(ABC):
    def __init__(self):
        pass

    def isRange(self):
        return False;


class vhRange(vhExpr):
    def __init__(self, left, dir, right):
        self.left = left
        self.dir = dir
        self.right = right

    def isRange(self):
        return True
    
    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{self.left} {self.dir} {self.right}"


class vhUnconstrainedRange(vhExpr):
    def __init__(self, bounds_subtype):
        self.bounds_subtype = bounds_subtype
    
    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{str(self.bounds_subtype)} range <>"

class vhUnaryExpr(vhExpr):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{self.op}{self.operand}"

    
class vhBinaryExpr(vhExpr):
    precedence = { 'AND' : 0, 'OR' : 0, 'NAND' : 0, 'NOR' : 0, 'XOR' : 0, 'XNOR' : 0,
                   '=' : 1, '/=' : 1, '<' : 1, '<=' : 1, '>' : 1, '>=' : 1,
                   'SLL' : 2, 'SRL' : 2, 'SLA' : 2, 'SRA' : 2, 'ROL' : 2, 'ROR' : 2,
                   '+' : 3, '-' : 3, '&' : 3,
                   # unary '+' and unary '-' should not be referenced here
                   '*' : 5, '/' : 5, 'MOD' : 5, 'REM' : 5,
                   '**' : 6 # ABS and NOT are unary operators
                  }
    def __init__(self, left, op=None, right=None):
        super().__init__()
        self.operands = [ left ]
        self.precedence_level = -1
        assert not (op ^ right), "both op and right must be set or neither"

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = f"({str(self.operands[0])}"
        for opn in self.operands[1:]:
            result += f" {opn[0]} {opn[1]}"
        result += ")"
        return


    def addOperand(self, op, operand):
        if self.precedence_level == -1:
            self.precedence_level = vhBinaryExpr.precedence[op]
        else:
            assert self.precedence_level == vhBinaryExpr.precedence.get(op, -1), "Unexpected precedence level in vgBinaryExpr"
        self.operands.append( (op, operand) )


class vhAbstractLiteral(vhExpr):
    def __init__(self, lit):
        self.literal = lit

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return str(self.literal)


class vhPhysicalLiteral(vhAbstractLiteral):
    def __init__(self, lit, unit):
        super().__init__(lit)
        self.unit = unit


class vhQualifiedExpr(vhExpr):
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr


class vhAttributeExpr(vhExpr):
    def __init__(self, pfx_name, pfx_sig, attr_name, arg=None):
        self.pfx_name = pfx_name
        self.pfx_sig = pfx_sig
        self.attr_name = attr_name
        self.arg = arg

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = str(self.pfx_name)
        if self.pfx_sig:
            result += str(self.pfx_sig)
        result += f"'{str(self.attr_name)}"
        if self.arg:
            result += f"({str(self.arg)})"
        return result

    def isRange(self):
        aname = str(self.attr_name).upper()
        return aname == 'RANGE' or aname == 'REVERSE_RANGE'


class vhAllocator(vhExpr):
    def __init__(self, subtype):
        self.subtype = subtype


class vhSubtypeIndication(vhExpr):
    def __init__(self, type_mark, constraints=None, res_func=None):
        self.type_mark = type_mark
        self.res_func = res_func
        # if constraints is a list, type is an array, otherwise it is a scalar
        self.constraints = constraints

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = ""
        if self.res_func:
            result += str(self.res_func) + " "
        result += str(self.type_mark)
        if not self.constraints:
            return result
        
        if type(self.constraints) is list:  # index constraint
            pfx = "("
            for constraint in self.constraints:
                result += pfx + str(constraint)
                pfx = ", "
            result += ")"
            return result
        
        if self.constraints.isRange():
            result += " range " + str(self.constraints)
        return result


class vhDecl(ABC):
    def __init__(self, sym=None):
        self.name = sym
        if sym:
            sym.ast = self
        
    def setName(self, sym):
        if self.name and sym != self.name:
            msg = f"start and end names don't match ({self.name} at {self.name.loc.sline}) "
            msg += f"and ({sym.name } at {sym.name.loc.sline})"
            return False
        self.name = sym
        sym.ast = self
        return True


class vhSubtypeDecl(vhDecl):
    def __init__(self, sym, subtype):
        super().__init__(sym)
        self.subtype = subtype

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(indent)}subtype {str(self.name)} is {str(self.subtype)};\n"


class vhConstrainedType(vhDecl):
    def __init__(self, sym=None, range=None):
        super().__init__(sym)
        self.range = range

    def setConstraint(range):
        self.range = range

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(indent)}type {str(self.name)} is range {str(self.range)};\n"


# class vhIntType(vhConstrainedType):
#     def __init__(self, sym=None, range=None):
#         super().__init__(sym, range)
#         #todo check that the range bounds are ints


# class vhFloatType(vhConstrainedType):
#     def __init__(self, sym=None, range=None):
#         super().__init__(sym, range)
#         #todo check that the the range bounds are floats


class vhIncompleteType(vhDecl):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(indent)}type {str(self.name)};\n"


# base class for decls that have their own symbol set
class vhScopeDecl(vhDecl):
    def __init__(self, sym=None, scope=None):
        super().__init__(sym)
        self.scope = scope

    def setScope(self, scope, override=False):
        assert override or not self.scope, "Scope is already set in vhScopeDecl"
        if override or not self.scope:
            scope.outer = self.ifc_symbols
            self.scope = scope


class vhEnumType(vhScopeDecl):
    def __init__(self, sym, outer):
        # EnumScope is specialized scope that is both a LocalScope (it does not search the outer scopes)
        # and that uses case        scope = 
        super().__init__(sym, Scope(sym, outer))
        # enumerants are visible at declaration scppe 
        outer.public_subscopes.append(self.scope)

    def __str__(self):
        return self.decompile()

    def decompile(self, indent=0):
        result = f"{indentPrefix(indent)}type {str(self.name)} is "
        pfx = "( "
        for sym in self.scope.symbols.values():
            result += pfx + str(sym)
            pfx = ", "
        result += " );\n"
        return result
    
    def __repr__(self):
        return self.dumpInternals()
    
    def dumpInternals(self):
        result = "VhEnumType(name=" + str(self.name)
        result += ", scope=" + repr(self.scope)
        result += ")"
        return result

    def addLiterals(self, lits):
        self.literals = lits


class vhPhysicalUnit(vhDecl):
    def __init__(self, unit, ref_unit=None, multiplier=1):
        unit.ast = self
        self.unit = unit
        self.multiplier = multiplier
        self.ref_unit = ref_unit

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = f"{indentPrefix(indent)}{str(self.unit)}"
        if self.ref_unit:
            result += f" = {self.multiplier} {str(self.ref_unit)}"
        result += ";\n"
        return result


class vhPhysicalType(vhScopeDecl):
    def __init__(self, outer, constraint=None, units=None):
        super().__init__(None, Scope(None, outer))
        # units are visible at declaration scope
        outer.public_subscopes.append(self.scope)
        self.constraint = constraint
        self.units = units

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = f"{indentPrefix(indent)}type {str(self.name)} is range {str(self.constraint)}\n"
        result += f"{indentPrefix(indent+1)}units\n"
        for unit in self.units:
            result += unit.decompile(indent+2)
        result += f"{indentPrefix(indent+1)}end units {str(self.name)};\n"
        return result

    def setName(self, sym):
        error = super().setName(sym)
        assert not self.scope.name or sym == self.scope.name, "different scope symbol already set"
        self.scope.name = sym
        sym.ast = self
        return error

    def addUnits(self, units):
        self.units = units


class vhArrayType(vhDecl):
    def __init__(self, ranges, elem_type):
        super().__init__()
        self.ranges = ranges
        self.elem_type = elem_type

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = f"{indentPrefix(indent)}type {str(self.name)} is array ("
        for range in self.ranges:
            result += range.decompile(indent)
        result += f") of {str(self.elem_type)};\n"
        return result


class vhRecordType(vhScopeDecl):
    def __init__(self, sym, outer):
        super().__init__(sym, Scope(sym, outer))
        # do not add to outer.public_subscopes, fields are only visible in the context of a record object

    def addElements(self, elements):
        self.elements = elements


class vhProtectedType(vhScopeDecl):
    def __init__(self, sym, outer):
        super().__init__(sym, Scope(sym, outer))
        # do not add to outer.public_subscopes, protected subprograms and attributes are only visible in the context of a protected object

    def addDecls(self, decls):
        self.decls = decls

    def addBody(self, body):
        self.body = body


class vhAttributeDecl(vhDecl):
    def __init__(self, sym, type_mark):
        super().__init__(sym)
        self.type_mark = type_mark

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(indent)}attribute {str(self.name)} : {str(self.type_mark)};\n"


class vhAccessType(vhDecl):
    def __init__(self, subtype, sym=None):
        super().__init__(sym)
        self.subtype = subtype

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(indent)}type {str(self.name)} is access {str(self.subtype)};\n"
    

class vhFileDecl(vhDecl):
    def __init__(self, subtype, sym=None):
        super().__init__(sym)
        self.subtype = subtype

    def __str__(self):
        return self.decompie()
    
    def decompile(self, indent=0):
        return f"{indentPrefix(index)}type {str(self.name)} is file of {str(self.subtype)};\n"


class vhIfcElem(vhDecl):
    def __init__(self, sym, subtype, default=None, obj_class='CONSTANT', mode='IN', bus=None):
        super().__init__(sym)
        self.subtype = subtype
        self.default = default 
        self.obj_class = obj_class
        self.mode = mode
        self.bus = bus

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = ""
        if self.obj_class:
            result = str(self.obj_class) + " "
        result += str(self.name) + " : "
        if self.mode:
            result += str(self.mode) + " "
        result += str(self.subtype)
        if self.bus:
            result += " " + str(self.bus)
        if self.default:
            result += " := " + str(self.default)
        return result       
        

class vhSubprogram(vhScopeDecl):
    def __init__(self, sym, outer):
        super().__init__(sym, SymbolTable(outer))
        self.ifc_symbols = self.scope
        # do not add to outer.public_subscopes, the interface formals are only visible in the context of a subprogram call
        self.scope = None # do not create a declaration scope until a body is seen.
        self.ifc = []   
        self.body = None

    def setInterface(self, ifc):
        self.ifc = ifc

    def setBody(self, body):
        self.body = body

class vhFunction(vhSubprogram):
    def __init__(self, sym, outer, purity='PURE'):
        super().__init__(sym, outer)
        self.purity = purity
        self.return_type = None

    def __str__(self):
        return self.decompile()
    
    def decompile(self, indent=0):
        result = indentPrefix(indent)
        if self.purity == 'IMPURE':
            result += "impure "
        result += f"function {str(self.name)}"
        if self.ifc:
            pfx = '('
            for formal in self.ifc:
                result += pfx + str(formal)
                pfx = '; '
            result += ")"

        result += " returns " + str(self.return_type)
        if self.body:
            result += f"\n{indentPrefix(indent)}begin\n"
            for stmt in self.body:
                result += stmt.decompile(indent+1)
            result += f"{indentPrefix(indent)}end function {str(self.sym)}"
        result += ";\n"
        return result

    def setReturnType(self, rtype):
        self.return_type = rtype  # rtype is expected to be a symbol, can it be an anonymous subtype?


class vhProcedure(vhSubprogram):
    def __init__(self, sym, outer):
        super().__init__(sym, outer)

    

