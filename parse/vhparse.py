# vhdl parser

import ply.lex as lex
import ply.yacc as yacc
from vhlex import VhdlLexer

# import all ast classes
from lcommon import *
from vhast import * 

class VhdlParser():

    instance = None

    def getVhdlParser():
        if VhdlParser.instance:
            return VhdlParser.instance
        VhdlParser.instance = VhdlParser()
        return VhdlParser.instance

    def __init__(self):
        # check singleton
        if self.instance:
            raise Exception("Singleton violation: VhdlParser")
        # set singleton
        self.instance = self

        self.rootScope = Scope(Symbol("_root"))
        self.curScope = self.rootScope
        self.curScope.add(self.curScope.name)     # root scope contains its own name Symbol

        # add keywords that can be used in place of a symbol to the _root scope
        self.rootScope.get('ALL')
        self.rootScope.get('OPEN')
        self.rootScope.get('NULL')
        self.rootScope.get('OTHERS')

        self.designFile = vhDesignFile(self.curScope)
        self.curScope.name.ast = self.designFile

        self.lexer = VhdlLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=True)

        self.error = 0

    def __del__(self):
        VhdlParser.instance = None
        del self.lexer

    def p_design_file_1(self, p):
        "design_file                    : design_units"
        p[0] = self.designFile
        p[0].units = p[1]

    def p_design_file_2(self, p):
        "design_file                    : empty"
        p[0] = []

    def p_design_units_1(self, p):
        "design_units                   : design_units design_unit"
        p[0] = p[1]
        p[0].append(p[2])

    def p_design_units_2(self, p):
        "design_units                   : design_unit"
        p[0] = [ p[1] ]

    def p_design_unit(self, p):
        "design_unit                    : context_clause library_unit"
        p[0] = p[2]
        p[0].context = p[1]

    def p_library_unit_1(self, p):
        "library_unit                   : primary_unit"
        p[0] = p[1]

    def p_library_unit_2(self, p):
        "library_unit                   : secondary_unit"
        p[0] = p[1]

    def p_primary_unit_1(self, p):
        "primary_unit                   : entity_decl"
        p[0] = p[1]

    def p_primary_unit_2(self, p):
        "primary_unit                   : config_decl"
        p[0] = p[1]

    def p_primary_unit_3(self, p):
        "primary_unit                   : package_decl"
        p[0] = p[1]

    def p_secondary_unit_1(self, p):
        "secondary_unit                 : architecture_body"
        p[0] = p[1]

    def p_secondary_unit_2(self, p):
        "secondary_unit                 : package_body"
        p[0] = None

    def p_entity_decl(self, p):
        "entity_decl                    : ENTITY"
        p[0] = None

    def p_config_decl(self, p):
        "config_decl                    : CONFIGURATION"
        p[0] = None

    def p_package_decl(self, p):
        "package_decl                   : PACKAGE symbol start_package_decl package_declarative_part end_package_decl SEMI"
        p[0] = p[3]
        p[0].sym = p[2]
        p[0].decls = p[4]
        p[0].sym.setLoc(p, 1, 6)
        #todo p[5] may be None or Symbol.  If Symbol, check that it is the same symbol as p[2]

    def p_start_package_decl(self, p):
        "start_package_decl             : IS"
        p[0] = vhPackageDecl(p[-1], self.curScope)     # creates a scope
        self.curScope = p[0].scope
        self.curScope.name.ast = p[0]

    def p_end_package_decl_1(self, p):
        "end_package_decl               : end_package_kw"
        p[0] = None

    def p_end_package_decl_2(self, p):
        "end_package_decl               : end_package_kw simple_name"
        p[0] = p[2]

    def p_end_package_kw(self, p):
        """end_package_kw               : end_scope
                                        | end_scope PACKAGE"""
        #todo check the package simple name against the name of the package
        p[0] = None

        p[0] = p[2]

    def p_end_scope(self, p):
        "end_scope                      : END"
        if self.curScope.outer:
            self.curScope = self.curScope.outer

    def p_architecture_body(self, p):
        "architecture_body              : ARCHITECTURE"
        p[0] = None

    def p_package_body(self, p):
        "package_body                   : PACKAGE BODY"
        p[0] = None

    def p_context_clause_1(self, p):
        "context_clause                 : context_items"
        if not p[1]:
            p[0] = None
            return
        p[0] = vhContextClause()
        p[0].addItems(p[1])

    def p_context_items_1(self, p):
        "context_items                  : context_items context_item"
        p[0] = p[1]
        p[0].extend(p[2])

    def p_context_items_2(self, p):
        "context_items                  : empty"
        p[0] = []

    def p_context_item_1(self, p):
        "context_item                   : library_clause"
        p[0] = p[1]

    def p_context_item_2(self, p):
        "context_item                   : use_clause"
        p[0] = p[1]

    def p_library_clause(self, p):
        "library_clause                 : LIBRARY logical_names SEMI"
        libs = []
        for sym in p[2]:
            libs.append(vhLibrary(sym))
        p[0] = libs

    def p_logical_names_1(self, p):
        "logical_names                  : logical_names ',' simple_name"
        p[0] = p[1]
        p[0].append(p[3])

    def p_logical_names_2(self, p):
        "logical_names                  : simple_name"
        p[0] = [ p[1] ]

    def p_use_clause(self, p):
        "use_clause                     : USE selected_names SEMI"
        p[0] = []
        for selected in p[2]:
            use = vhUse(selected)
            p[0].append(use)       

    def p_selected_names_1(self, p):
        "selected_names                 : selected_names ',' selected_name "
        p[0] = p[1]
        p[0].append(p[3])

    def p_selected_names_2(self, p):
        "selected_names                 : selected_name"
        p[0] = [ p[1] ]

    def p_package_declarative_part_1(self, p):
        "package_declarative_part       : package_declarative_part package_declarative_item"
        p[0] = p[1]
        p[0].append(p[2])

    def p_package_declarative_part_2(self, p):
        "package_declarative_part       : empty"
        p[0] = []

    def p_package_declarative_item(self, p):
        """package_declarative_item     : subprogram_decl
                                        | type_decl
                                        | subtype_decl
                                        | const_decl
                                        | signal_decl
                                        | var_decl
                                        | file_decl
                                        | alias_decl
                                        | component_decl
                                        | attr_decl
                                        | attr_spec
                                        | disconnect_spec
                                        | use_clause
                                        | group_template_decl
                                        | group_decl
                                        """
        p[0] = p[1]

    def p_type_decl(self, p):
        """type_decl                    : full_type_decl
                                        | incomplete_type_decl"""
        p[0] = p[1]

    def p_subtype_decl(self, p):
        "subtype_decl                   : SUBTYPE symbol IS subtype_indication SEMI"
        p[0] = vhSubtypeDecl(p[2], p[4])

    def p_const_decl(self, p):
        "const_decl                     : CONSTANT symbols ':' subtype_indication opt_assign_rhs SEMI"
        p[0] = [ p[1], p[2], p[4], p[5] ]

    def p_signal_decl(self, p):
        "signal_decl                    : SIGNAL symbols ':' subtype_indication opt_sig_kind_kw opt_vassign_rhs SEMI"
        p[0] = [ p[1], p[2], p[4], p[5], p[6] ]

    def p_var_decl(self, p):
        "var_decl                       : var_decl_start subtype_indication opt_vassign_rhs SEMI"
        p[0] = p[1]
        p[0].extend( [ p[2], p[3] ] )

    def p_var_decl_start_1(self, p):
        "var_decl_start                 : VARIABLE symbols ':'"
        p[0] = [ p[1], None, p[2] ]

    def p_var_decl_start_2(self, p):
        "var_decl_start                 : SHARED VARIABLE symbols ':'"
        p[0] = [ p[2], p[1], p[3] ]

    def p_file_decl(self, p):
        "file_decl                      : FILE symbols ':' subtype_indication file_open_info SEMI"
        p[0] = [ p[1], p[2], p[4], p[5] ]

    def p_alias_decl(self, p):
        "alias_decl                     : alias_decl_start name signature SEMI"
        p[0] = [ p[1], p[2], p[3], p[5], p[6] ]

    def p_alias_decl_start_1(self, p):
        "alias_decl_start              : ALIAS alias_designator ':' subtype_indication IS"
        p[0] = [ p[1], p[2], p[4] ]

    def p_alias_decl_start_2(self, p):
        "alias_decl_start              : ALIAS alias_designator subtype_indication IS"""
        p[0] = [ p[1], p[2], p[3] ]

    def p_component_decl(self, p):
        "component_decl                 : COMPONENT symbol start_component opt_is_kw generic_clause port_clause end_component SEMI"
        #todo match component name with component end name
        #todo p[0] = p[3]
        #todo add generics and ports to the component
        p[0] = [ p[1], p[2], p[5], p[6] ]

    def p_attr_decl(self, p):
        "attr_decl                      : attr_start ':' name SEMI"
        p[0] = vhAttributeDecl(p[1], p[3])

    def p_attr_spec(self, p):
        "attr_spec                      : attr_start OF entity_spec IS expr"  # attr_start here or need to use simple_name?
        p[0] = [ p[1] ]
        p[0].append([ p[3], p[5] ])
        
    def p_attr_start(self, p):
        "attr_start                     : ATTRIBUTE symbol"
        p[0] = p[2]
    
    def p_disconnect_spec(self, p):
        "disconnect_spec                : DISCONNECT signals_list ':' name AFTER expr SEMI"
        p[0] = [ p[1], p[2], p[4] ]

    def p_group_template_decl(self, p):
        "group_template_decl            : group_start IS '(' entity_class_entry_list ')'"
        p[0] = []
        p[0].extend(p[1])
        p[0].append(p[4])

    def p_group_decl(self, p):
        "group_decl                     : group_start name '(' group_constituent_list ')'"
        p[0] = []
        p[0].extend(p[1], p[3], p[5])

    def p_group_start(self, p):
        "group_start                    : GROUP symbol ':'"
        p[0] = [ p[1], p[2] ]

    def p_group_constituent_list_1(self, p):
        "group_constituent_list         : group_constituent_list ',' group_constituent"
        p[0] = p[1]
        p[0].append(p[3])

    def p_group_constituent_list_2(self, p):
        "group_constituent_list         : group_constituent"
        p[0] = [ p[1] ]

    def p_group_constituent(self, p):
        """group_constituent            : name
                                        | literal"""
        p[0] = p[1]

    def p_entity_class_entry_list_1(self, p):
        "entity_class_entry_list        : entity_class_entry_list ',' entity_class_entry"
        p[0] = p[1]
        p[0].append(p[3])

    def p_entity_class_entry_list_2(self, p):
        "entity_class_entry_list        : entity_class_entry"
        p[0] = p[1]

    def p_entity_class_entry_1(self, p):
        "entity_class_entry             : entity_class_kw BOX"
        p[0] = [ p[1], p[2] ]

    def p_entity_class_entry_2(self, p):
        "entity_class_entry             : entity_class_kw"
        p[0] = [ p[1], None ]

    def p_entity_class_kw(self, p):
        """entity_class_kw              : ENTITY
                                        | ARCHITECTURE
                                        | CONFIGURATION
                                        | PROCEDURE
                                        | FUNCTION
                                        | PACKAGE
                                        | TYPE
                                        | SUBTYPE
                                        | CONSTANT
                                        | SIGNAL
                                        | VARIABLE
                                        | COMPONENT
                                        | LABEL
                                        | LITERAL
                                        | UNITS
                                        | GROUP
                                        | FILE"""
        p[0] = p[1]

    def p_signals_list(self, p):
        """signals_list                 : symbols
                                        | others_symbol
                                        | all_symbol"""
        p[0] = p[1]

    def p_entity_spec(self, p):
        "entity_spec                    : entity_name_list ':' entity_class_kw"
        p[0] = [ p[1], p[2] ]

    def p_entity_names_list(self, p):
        """entity_name_list             : entity_names
                                        | others_symbol
                                        | all_symbol"""
        p[0] = p[1]

    def p_entity_names_1(self, p):
        "entity_names                   : entity_names ',' entity_name"
        p[0] = p[1]
        p[0].append(p[3])

    def p_entity_names_2(self, p):
        "entity_names                   : entity_name"
        p[0] = [ p[1] ]

    def p_entity_name_1(self, p):
        "entity_name                    : entity_tag signature"
        p[0] = [ p[1], p[3] ]

    def p_entity_name_2(self, p):
        "entity_name                    : entity_tag"
        p[0] = [ p[1], None ]

    def p_entity_tag(self, p):
        """entity_tag                   : simple_name
                                        | CHARLIT
                                        | operator_symbol"""
        p[0] = p[1]

    def p_start_component(self, p):
        "start_component                : empty"
        #todo create VhComponent ast
        #todo use the scope created in VhComponent to the set the current scope
        pass

    def p_opt_is_kw(self, p):
        """opt_is_kw                    : IS
                                        | empty"""
        pass

    def p_end_component_1(self, p):
        "end_component                  : end_scope COMPONENT"
        p[0] = None

    def p_end_component_2(self, p):
        "end_component                  : end_scope COMPONENT simple_name"
        p[0] = p[3]

    def p_generic_clause(self, p):
        "generic_clause                 : GENERIC formal_parameter_list"
        p[0] = p[1]

    def p_port_clause(self, p):
        "port_clause                    : PORT formal_parameter_list"
        p[0] = p[1]

    def p_interface_list_1(self, p):
        "interface_list                 : interface_list SEMI interface_element"
        p[0] = p[1]
        p[0] += p[3]

    def p_interface_list_2(self, p):
        "interface_list                 : interface_element"
        #interface_element returns a list
        p[0] = p[1]

    def p_interface_element(self, p):
        "interface_element              : interface_element_start opt_mode_kw subtype_indication opt_bus_kw opt_vassign_rhs"
        obj_class = p[1][0]
        syms = p[1][1]
        p[0] = []
        for sym in syms:
            elem = vhIfcElem(sym, p[3], p[5], obj_class, p[2], p[4])
            p[0].append(elem)

    def p_interface_element_start_1(self, p):
        "interface_element_start        : symbols ':'"
        p[0] = [ None, p[1] ]

    def p_interface_element_start_2(self, p):
        "interface_element_start         : obj_class_kw symbols ':'"
        p[0] = [ p[1], p[2] ]
    
    def p_obj_class_kw(self, p):
        """obj_class_kw                     : CONSTANT
                                            | SIGNAL
                                            | VARIABLE
                                            | FILE"""
        p[0] = p[1]

    def p_opt_mode(self, p):
        """opt_mode_kw                      : IN
                                            | OUT
                                            | INOUT
                                            | BUFFER
                                            | LINKAGE
                                            | empty"""
        p[0] = p[1]

    def p_opt_bus_kw(self, p):
        """opt_bus_kw                       : BUS
                                            | empty"""
        p[0] = p[1]

    def p_alias_designator(self, p):
        """alias_designator             : symbol
                                        | CHARLIT
                                        | operator_symbol"""
        p[0] = p[1]

    def p_file_open_info_1(self, p):
        "file_open_info                 : open_expr IS expr"
        p[0] = [ p[3], p[1] ]

    def p_file_open_info(self, p):
        "file_open_info                 : IS expr"
        p[0] = [ p[2], None ]

    def p_open_expr(self, p):
        "open_expr                      : OPEN expr"
        p[0] = p[2]

    def p_opt_sig_kind_kw(self, p):
        """opt_sig_kind_kw              : REGISTER
                                        | BUS
                                        | empty"""
        p[0] = p[1]

    def p_opt_vassign_rhs_1(self, p):
        "opt_assign_rhs                 : VASSIGN expr"
        p[0] = p[2]

    def p_opt_vassign_rhs(sefl, p):
        "opt_vassign_rhs                : empty"
        p[0] = p[1]
    
    def p_full_type_decl(self, p):
        "full_type_decl                : TYPE symbol IS type_def SEMI"
        p[0] = p[4]
        if type(p[0]) is list:
            breakpoint()
        p[0].setName(p[2])


    def p_incomplete_type_decl(self, p):
        "incomplete_type_decl           : TYPE symbol SEMI"
        p[0] = vhIncompleteType(p[2])
    
    def p_type_def(self, p):
        """type_def                     : scalar_type_def
                                        | composite_type_def
                                        | access_type_def
                                        | file_type_def
                                        | protected_type_def"""
        p[0] = p[1]
        
    def p_scalar_type_def(self, p):
        """scalar_type_def              : enum_type_def
                                        | constrained_type_def"""
        p[0] = p[1]

    def p_composite_type_def(self, p):
        """composite_type_def           : array_type_def
                                        | record_type_def"""
        p[0] = p[1]

    def p_access_type_def(self, p):
        "access_type_def                : ACCESS subtype_indication"
        p[0] = vhAccessType(subtype=p[2])

    def p_file_type_def(self, p):
        "file_type_def                  : FILE OF name"
        p[0] = vhFileDecl(p[3])
    
    def p_protected_type_def(self, p):
        """protected_type_def           : protected_type_decl
                                        | protected_type_body"""
        p[0] = p[1]
        
    # these array type productions allow partially constrained multi-dimensionals
    # this is not allowed, there needs to be a semantic check
    def p_array_type_def(self, p):
        "array_type_def                 : ARRAY bounds_def OF subtype_indication"
        p[0] = vhArrayType(p[2], p[4])

    def p_record_type_def(self, p):
        "record_type_def                : start_record element_decls end_record_def"
        #todo check end name vs type name
        p[0] = p[1]
        p[0].addElements(p[2])
        p[0].setName(p[3])

    def p_protected_type_decl(self, p):
        "protected_type_decl            : start_protected protected_type_list end_protected"
        #todo check end name vs type name
        p[0] = [ p[1], p[2], p[6] ]

    def p_protected_type_body(self, p):
        "protected_type_body            : start_protected_body protected_body_list end_protected_body"
        p[0] = [ p[1], p[2], p[3] ]

    def p_protected_kw(self, p):
        "start_protected                : PROTECTED"
        p[0] = vhProtectedType(None, self.curScope)
        p[-2].ast = p[0]
        self.curScope = p[0].scope

    def p_end_protected_1(self, p):
        "end_protected                  : end_scope PROTECTED"
        p[0] = None
    
    def p_end_protected_2(self, p):
        "end_protected                  : end_scope PROTECTED simple_name"
        p[0] = p[3]

    def p_protected_body(self, p):
        "start_protected_body           : PROTECTED BODY"
        p[0] = self.curScope.search(p[-2].name)
        if p[0]:
            self.curScope = p[0].scope
        #todo raise error protected type symbols is not found, continue

    def p_end_protected_body_1(self, p):
        "end_protected_body             : end_scope PROTECTED BODY"
        p[0] = None

    def p_end_protected_body(self, p):
        "end_protected_body             : end_scope PROTECTED BODY simple_name"
        p[0] = p[3]

    def p_protected_type_items_1(self, p):
        "protected_type_list           : protected_type_list protected_type_item"
        p[0] = p[1]
        p[0].append(p[1])

    def p_protected_type_items_2(self, p):
        "protected_type_list           : protected_type_item"
        p[0] = [ p[1] ]

    def p_protected_type_item(self, p):
        """protected_type_item          : subprogram_decl
                                        | attr_spec
                                        | use_clause"""
        p[0] = p[1]

    def p_protected_body_list_1(self, p):
        "protected_body_list           : protected_body_list protected_body_item"
        p[0] = p[1]
        p[0].append(p[2])

    def p_protected_body_list_2(self, p):
        "protected_body_list           : protected_body_item"
        p[0] = [ p[1] ]

    def p_protected_body_item(self, p):
        """protected_body_item          : subprogram_decl
                                        | subprogram_body
                                        | type_decl
                                        | subtype_decl
                                        | const_decl
                                        | var_decl
                                        | file_decl
                                        | alias_decl
                                        | attr_decl
                                        | use_clause
                                        | group_template_decl
                                        | group_decl"""
        p[0] = p[1]

    def p_start_record(self, p):
        "start_record                   : RECORD"
        p[0] = vhRecordType(p[-2], self.curScope)
        self.curScope = p[0].scope

    def p_end_record_def_1(self, p):
         "end_record_def              : end_scope RECORD"
         p[0] = None
    
    def p_end_record_scope_2(self, p):
         "end_record_def              : end_scope RECORD simple_name"
         p[0] = p[3]

    def p_element_decls_1(self, p):
        "element_decls                  : element_decls element_decl"
        p[0] = p[1]
        p[0].append(p[2])

    def p_element_decls_2(self, p):
        "element_decls                  : element_decl"
        p[0] = [ p[1] ]

    def p_element_decl(self, p):
        "element_decl                   : symbols ':' subtype_indication SEMI"
        p[0] = [ p[1], p[3] ]

    def p_bounds_def(self, p):
        "bounds_def                     : '(' bounds_list ')'"
        p[0] = p[2]

    def p_bounds_spec_1(sefl, p):
        "bounds_list                    : bounds_list ',' bound"
        p[0] = p[1]
        p[0].append(p[2])

    def p_bounds_spec_2(self, p):
        "bounds_list                    : bound"
        p[0] = [ p[1] ]

    def p_bound_1(self, p):
        """bound                        : index_subtype_def
                                        | index_constraint"""
        p[0] = p[1]

    def p_index_subtype_def(self, p):
        "index_subtype_def              : name RANGE BOX"
        p[0] = vhUnconstrainedRange(p[1])

    def p_enum_type_def(self, p):
        "enum_type_def                  : start_enum enum_lit_decls end_enum"
        p[0] = p[1]
        p[0].addLiterals(p[2])

    def p_end_enum_scope(self, p):
        "end_enum                       : ')'"
        if self.curScope.outer:
            self.curScope = self.curScope.outer

    def p_start_enum(self, p):
        "start_enum                     : '('"
        p[0] = vhEnumType(None, self.curScope)
        self.curScope = p[0].scope

    def p_enum_lits_decls_1(self, p):
        "enum_lit_decls                 : enum_lit_decls ',' enum_lit_decl"
        p[0] = p[1]
        p[0].append(p[3])

    def p_enum_lit_decls_2(self, p):
        "enum_lit_decls                 : enum_lit_decl"
        p[0] = [ p[1] ]

    def p_enum_lit_decl_1(self, p):
        "enum_lit_decl                  : symbol"
        p[0] = p[1]

    def p_enum_lit_decl_2(self, p):
        "enum_lit_decl                  : CHARLIT"
        p[0] = self.curScope.pget(p, 1)

    #these two handle integer, real, and physical ranges
    def p_constrained_type_def_1(self, p):
        "constrained_type_def           : range_constraint phys_units_spec"
        p[0] = p[2]
        p[0].constraint = p[1]

    def p_constrained_type_def_2(self, p):
        "constrained_type_def           : range_constraint"
        p[0] = vhConstrainedType(range=p[1])

    def p_phys_units_spec(self, p):
        "phys_units_spec                : start_units unit_list end_units"
        #todo check end name vs type name
        p[0] = p[1]
        p[0].name = p[3]
        p[0].addUnits(p[2])

    def p_start_units(self, p):
        "start_units                    : UNITS"
        p[0] = vhPhysicalType(self.curScope)
        self.curScope = p[0].scope

    def p_unit_list_1(self, p):
        "unit_list                      : symbol SEMI"
        p[0] = [ vhPhysicalUnit(p[1]) ]
    
    def p_unit_list_2(self, p):
        "unit_list                      : symbol SEMI sec_units"
        p[0] = [ vhPhysicalUnit(p[1]) ]
        p[0].extend(p[3])

    def p_end_units_1(self, p):
        "end_units                      : end_scope UNITS"
        p[0] = None

    def p_end_units_2(self, p):
        "end_units                      : end_scope UNITS simple_name"
        p[0] = p[3]

    def p_sec_units(self, p):
        "sec_units                      : sec_units unit_decl SEMI"
        p[0] = p[1]
        p[0].append(p[2])

    def p_sec_units_2(self, p):
        "sec_units                      : empty"
        p[0] = [ ]
    
    def p_unit_1(self, p):
        "unit_decl                      : symbol '=' simple_name"
        p[0] = vhPhysicalUnit(p[1], p[3]) 

    def p_unit_2(self, p):
        "unit_decl                      : symbol '=' abstract_lit simple_name"
        p[0] = vhPhysicalUnit(p[1], p[4], p[3])

    def p_constraint(self, p):
        """constraint                   : range_constraint
                                        | index_constraint"""
        p[0] = p[1]
    
    def p_index_constraint(self, p):
        "index_constraint               : '(' discrete_ranges ')'"
        p[0] = p[1]
    
    def p_discrete_ranges_1(self, p):
        "discrete_ranges                : discrete_ranges ',' discrete_range"
        p[0] = p[1]
        p[0].append(p[2])

    def p_discrete_ranges_2(self, p):
        "discrete_ranges                : discrete_range"
        p[0] = [ p[1] ]

    def p_range_constraint(self, p):
        "range_constraint               : RANGE expr"
        p[0] = p[2]
        if not p[2].isRange():
            raise SyntaxError(f"Expression found where a range or a range attribute is expected at line {p.lineno(2)}") 

    def p_range(self, p):
        "range                          : simple_expr direction simple_expr"
        p[0] = vhRange(p[1], p[2], p[3])

    def p_discrete_range(self, p):
        """discrete_range               : range
                                        | name"""
        p[0] = p[1]
    
    def p_subtype_indication(self, p):
        """subtype_indication           : unresolved_subtype_ind
                                        | resolved_subtype_ind"""      # type_mark
        p[0] = p[1]

    def p_type_constraint(self, p):
        "type_constraint                : name constraint"  # type_mark constraint
        p[0] = vhSubtypeIndication(p[1], p[2])

    def p_unresolved_subtype_ind_1(self, p):
        "unresolved_subtype_ind         : name"
        p[0] = vhSubtypeIndication(p[1])

    def p_unresolved_subtype_ind_2(self, p):
        "unresolved_subtype_ind         : type_constraint"
        p[0] = p[1]

    def p_resolved_subtype_ind(self, p):
        "resolved_subtype_ind          : name name"    # resolution_function_name type_mark
        p[0] = vhSubtypeIndication(p[2], res_func=p[1])

    def p_resolved_indication_2(self, p):
        "resolved_subtype_ind          : name type_constraint"     # resolution_function_name type_mark constraint
        p[0] = p[2]
        p[0].res_func = p[1]

    def p_direction(self, p):
        """direction                    : TO
                                        | DOWNTO"""
        p[0] = p[1]
    
    def p_name(self, p):
        """name                         : simple_name
                                        | selected_name
                                        | operator_string
                                        | applied_name
                                        | attribute_name"""
        p[0] = p[1]
        
         # dont use simple_name here, need to figure out the search scope using the prefix first, then lookup the symbol
    def p_suffix(self, p):
        """suffix                       : IDENT
                                        | CHARLIT
                                        | operator_string
                                        | all_symbol"""
        p[0] = p[1]

    def p_symbol(self, p):    # simple_name for declarations
        "symbol                         : IDENT"
        p[0] = self.curScope.find(p[1])     # search the local scope
        if p[0]:        
            print(f"Symbol '{p[0].name}' already exists in {self.curScope.name}, continuing..")
            return

        p[0] = Symbol(p[1])
        self.curScope.add(p[0])

    def p_symbols_1(self, p):
        "symbols                        : symbols ',' symbol"
        p[0] = p[1]
        p[0].append(p[3])

    def p_symbols_2(self, p):
        "symbols                        : symbol"
        p[0] = [ p[1] ]

    def p_simple_name(self, p):   # for references
        "simple_name                    : IDENT"
        syms = self.curScope.search(p[1])   # search all the Scope in the current stack
        if not syms:
            p[0] = self.curScope.pget(p, 1)
            print(f"Symbol '{p[0]}' at line {p[0].loc.sline}(column {p[0].loc.scol}) " +
                  "not found, creating and continuing.. ")
            return
    
        if len(syms) > 1:
            p[0] = syms[0]
            print(f"Ambiguous Symbol '{p[1]}' at line {p.lineno(1)}(column {start_column(p, 1)}), " +
                  "using the Symbol from the nearest scope.  This will error during semantic analysis.")
            return
    
        p[0] = syms[0]      # if we get here there is only 1 symbol in tuple, return it

    def p_operator_string(self, p):
        "operator_string                : STRLIT"
        syms = self.curScope.search(p[1])
        if not syms:
            p[0] = self.curScope.pget(p, 1)
            print(f"Symbol '{p[0]}' at line {p[0].loc.sline}(column {p[0].loc.scol}) " +
                  "not found, creating and continuing.. ")
            return
    
        if len(syms) > 1:
            p[0] = syms[0]
            print(f"Ambiguous Symbol '{p[1]}' at line {p[0].loc.sline}(column {p[0].loc.scol}), " +
                  "using the Symbol from the nearest scope.  This will error during semantic analysis.")
            return
    
        p[0] = syms[0]      # if we get here there is only 1 symbol in tuple, return it


    def p_operator_symbol(self, p):
        "operator_symbol                : STRLIT"
        p[0] = self.curScope.find(p[1])
        if p[0]:
            print(f"Symbol '{p[0].name}' already exists in {self.curScope.name}, continuing..")
            return
        
        p[0] = Symbol(p[1])
        self.curScope.add(p[0])

    def p_selected_name(self, p):
        "selected_name                  : prefix suffix"
        #todo create vhSelectedName()
        p[0] = []
        p[0].append(p[1])
        p[0].append(p[2])
        #todo, revert the curScope

    def p_prefix(self, p):
        "prefix                         : name '.'"
        #todo, use the prefix name to establish the curScope for suffix name lookup
        p[0] = p[1]

    def p_applied_name(self, p):
        "applied_name                   : name '(' association_list ')'"
        p[0] = [ p[1], p[3] ]

    def p_attribute_name_1(self, p):
        "attribute_name                 : name_tick attribute_symbol"
        p[0] = vhAttributeExpr(p[1][0], p[1][1], p[2])

    def p_attribute_name_2(self, p):
        "attribute_name                 : name_tick attribute_symbol aggregate"
        p[0] = vhAttributeExpr(p[1][0], p[1][1], p[2], p[3])

    def p_attribute_symbol(self, p):
        """attribute_symbol             : simple_name
                                        | RANGE"""
        p[0] = p[1]

    def p_expr(self, p):
        """expr                         : range
                                        | logicals"""
        p[0] = p[1]

    def p_logicals_1(self, p):
        "logicals                      : logicals logical_op relation"
        p[0] = p[1]
        if type(p[1]) is not vhBinaryExpr or p[1].precedence_level != vhBinaryExpr.precedence.get(p[2], -1):
            p[0] = vhBinaryExpr(p[1])
        p[0].addOperand(p[2], p[3])

    def p_logicals_2(self, p):
        "logicals                      : relation"
        p[0] = p[1]

    def p_logical_op(self, p):
        """logical_op                   : AND
                                        | OR
                                        | XOR
                                        | NAND
                                        | NOR
                                        | XNOR"""
        p[0] = p[1]

    def p_relation_1(self, p):
        "relation                       : shift_expr relational_op shift_expr"
        p[0] = vhBinaryExpr(p[1], p[2], p[3])

    def p_relation_2(self, p):
        "relation                       : shift_expr"
        p[0] = p[1]

    def p_relational_op(self, p):
        """relational_op                : '='
                                        | NE
                                        | '<'
                                        | LE
                                        | '>'
                                        | GE"""
        p[0] = p[1]

    def p_shift_expr_1(self, p):
        "shift_expr                     : simple_expr shift_op simple_expr"
        p[0] = vhBinaryExpr(p[1], p[2], p[3])

    def p_shift_expr_2(self, p):
        "shift_expr                     : simple_expr"
        p[0] = p[1]

    def p_shift_op(sefl, p):
        """shift_op                     : SLL
                                        | SRL
                                        | SLA
                                        | SRA
                                        | ROL
                                        | ROR"""
        p[0] = p[1]

    def p_simple_expr_1(self, p):
        "simple_expr                    : MINUS adding_exprs"
        p[0] = vhUnaryExpr(p[1], p[2])

    def p_simple_expr_2(self, p):
        "simple_expr                    : adding_exprs"
        p[0] = p[1]
    
    def p_adding_exprs_1(sefl, p):
        "adding_exprs                   : adding_exprs adding_op term"
        p[0] = p[1]
        if type(p[1]) is not vhBinaryExpr or p[1].precedence_level != vhBinaryExpr.precedence.get(p[2], -1):
            p[0] = vhBinaryExpr(p[1])
        p[0].addOperand(p[2], p[3])

    def p_adding_exprs_2(self, p):
        "adding_exprs                   : term"
        p[0] = p[1]

    def p_adding_op(self, p):
        """adding_op                    : '+'
                                        | MINUS
                                        | '&'"""
        p[0] = p[1]

    def p_term(self, p):
        "term                           : multiplying_exprs"
        p[0] = p[1]

    def p_multiplying_exprs_1(self, p):
        "multiplying_exprs              : multiplying_exprs multiplying_op factor"
        p[0] = p[1]
        if type(p[1]) is not vhBinaryExpr or p[1].precedence_level != vhBinaryExpr.precedence.get(p[2], -1):
            p[0] = vhBinaryExpr(p[1])
        p[0].addOperand(p[2], p[3])

    def p_multiplying_exprs_2(self, p):
        "multiplying_exprs              : factor"
        p[0] = p[1]

    def p_multiplying_op(self, p):
        """multiplying_op               : '*'
                                        | '/'
                                        | MOD
                                        | REM"""
        p[0] = p[1]

    def p_factor(self, p):
        """factor                       : exponent_exprs
                                        | unary_factor"""
        p[0] = p[1]

    def p_exponent_exprs_1(self, p):
        "exponent_exprs                 : exponent_exprs EXP primary"
        p[0] = p[1]
        if type(p[1]) is not vhBinaryExpr or p[1].precedence_level != VhBinaryExpr.precedence.get(p[2], -1):
            p[0] = vhBinaryExpr(p[1])
        p[0].addOperand(p[2], p[3])

    def p_exponent_exprs_2(self, p):
        "exponent_exprs                 : primary"
        p[0] = p[1]

    def p_unary_factor(self, p):
        """unary_factor                 : unary_factor_op primary"""
        p[0] = vhUnaryExpr(p[1], p[2])

    def p_unary_factor_op(self, p):
        """unary_factor_op              : ABS
                                        | NOT"""
        p[0] = p[1]

    def p_primary(self, p):
        """primary                      : name
                                        | literal
                                        | aggregate
                                        | allocator"""
        p[0] = p[1]

    def p_literal_1(self, p):
        """literal                        : numeric_lit
                                          | null_symbol"""
        p[0] = p[1]

    def p_literal_2(self, p):
        "literal                        : CHARLIT"
        p[0] = vhCharLiteral(p[1])

    def p_literal_3(self, p):
        "literal                        : BITSTRLIT"
        p[0] = vhBitStrLiteral(p[1])

    def p_numeric_lit_1(self, p):
        "numeric_lit                    : abstract_lit simple_name"
        p[0] = vhPhysicalLiteral(p[1], p[2])

    def p_numeric_lit_2(self, p):
        "numeric_lit                    : abstract_lit"
        p[0] = p[1]

    def p_abstract_lit(self, p):
        """abstract_lit                 : DECLIT
                                        | BASEDLIT"""
        p[0] = vhAbstractLiteral(p[1])

    def p_aggregate(self, p):
        "aggregate                      : '(' aggregate_elements ')'"
        p[0] = p[1]

    def p_qualified(self, p):
        "qualified                      : name_tick aggregate"
        if p[1][1]:
            raise SyntaxError(f"signature not allowed in qualified expression prefix at line {p.lineno(1)}" )
        p[0] = vhQualifiedExpr(p[1][0])

    def p_name_tick_1(self, p):
        "name_tick                      : name TICK"
        p[0] = ( p[1], None )

    def p_name_tick_2(self, p):
        "name_tick                      : name signature TICK"
        p[0] = ( p[1], p[2] ) 

    def p_allocator(self, p):
        "allocator                      : NEW new_subtype"
        p[0] = vhAllocator(p[2])

    def p_new_expr(self, p):
        """new_subtype                  : subtype_indication
                                        | qualified"""
        p[0] = p[1]

    def p_aggregate_elements_1(seff, p):
        "aggregate_elements               : aggregate_elements ',' aggregate_elem"
        p[0] = p[1]
        p[0].append(p[3])

    def p_aggregate_elements_2(self, p):
        "aggregate_elements               : aggregate_elem"
        p[0] = [ p[1] ] 
        
    def p_element_association_1(self, p):
        "aggregate_elem                 : choices ARROW expr"
        p[0] = [ p[1], p[3] ]

    def p_element_association_2(self, p):
        "aggregate_elem                 : expr"
        p[0] = p[1]

    def p_choices_1(self, p):
        "choices                       : choices '|' choice"
        p[0] = p[1]
        p[0].append(p[2])

    def p_choices_2(self, p):
        "choices                       : choice"
        p[0] = [ p[1] ]

    def p_choice(self, p):
        """choice                       : simple_expr
                                        | discrete_range
                                        | others_symbol"""
        p[0] = p[1]

    def p_signature_1(self, p):
        "signature                      : '[' signature_elements ']'"
        p[0] = p[2]

    def p_signature_2(self, p):
        "signature                    : '[' ']'"
        p[0] = [ None, None ]

    def p_signature_elements_1(self, p):
        "signature_elements             : type_marks return_type"
        p[0] = [ p[1], p[2] ]

    def p_signature_elements_2(self, p):
        "signature_elements             : type_marks"
        p[0] = [ p[1], None ]

    def p_signature_elements_3(sslf, p):
        "signature_elements             : return_type"
        p[0] = [ None, p[1] ]

    def p_type_marks_1(self, p):
        "type_marks                     : type_marks ',' name"
        p[0] = p[1]
        p[0].append(p[1])

    def p_type_marks_2(self, p):
        "type_marks                     : name"
        p[0] = [ p[1] ]

    def p_return_type(self, p):
        "return_type                    : RETURN name"
        p[0] = p[2]

    def p_association_list_1(self, p):
        "association_list               : association_list ',' association_element"
        p[0] = p[1]
        p[0].append(p[3])

    def p_association_list_2(self, p):
        "association_list               : association_element"
        p[0] = [ p[1] ]

    def p_association_element_1(self, p):
        "association_element            : expr ARROW actual_part"
        p[0] = [ p[1], p[3] ]

    def p_association_element_2(self, p):
        "association_element            : actual_part"
        p[0] = [ None, p[2] ]

    def p_actual_part(self, p):
        """actual_part                  : expr
                                        | open_symbol"""
        p[0] = p[1]

    def p_subprogram_decl_1(self, p):
        "subprogram_decl                : subprogram_decl_start SEMI"
        p[0] = p[1]

    def p_subprogram_decl_2(self, p):
        "subprogram_decl               : subprogram_decl_start subprogram_interface SEMI"
        p[0] = p[1]
        p[0].setInterface(p[2][0])
        if type(p[0]) is vhFunction:
            p[0].setReturnType(p[2][1])
        if self.curScope.outer:
            self.curScope = self.curScope.outer

    def p_subprogram_interface_1(self, p):
        "subprogram_interface           : formal_parameter_list return_type"
        p[0] = [ p[1], p[2] ]

    def p_subprogram_interface_2(self, p):
        "subprogram_interface           : formal_parameter_list"
        p[0] = [ p[1], None ]

    def p_subprogram_interface_3(self, p):
        "subprogram_interface           : return_type"
        p[0] = [ None, p[1] ]

    def p_formal_parameter_list(self, p):
        "formal_parameter_list                 : '(' interface_list ')'"
        p[0] = p[2]

    def p_subprogram_decl_start(self, p):
        """subprogram_decl_start        : procedure_start
                                        | function_start"""
        p[0] = p[1]
        self.curScope = p[0].ifc_symbols

    def p_procedure_start(self, p):
        "procedure_start                : PROCEDURE designator_symbol"
        p[0] = vhProcedure(p[2], self.curScope)

    def p_function_start_1(self, p):
        "function_start                 : FUNCTION designator_symbol"
        p[0] = vhFunction(p[2], self.curScope)

    def p_function_start_2(self, p):
        "function_start                 : purity FUNCTION designator_symbol"
        p[0] = vhFunction(p[3], self.curScope, p[1])

    def p_purity(self, p):
        """purity                       : PURE
                                        | IMPURE"""
        p[0] = p[1]
    
    def p_designator(self, p):
        """designator_symbol            : symbol
                                        | operator_symbol"""
        p[0] = p[1]
   
    def p_subprogram_body(self, p):
        "subprogram_body                : FUNCTION IS SEMI"
        p[0] = p[1]

    def p_all_symbol(self, p):
        "all_symbol                     : ALL"
        p[0] = self.rootScope.find(p[1])

    def p_open_symbol(self, p):
        "open_symbol                    : OPEN"
        p[0] = self.rootScope.find(p[1])

    def p_null_symbol(self, p):
        "null_symbol                    : NULL"
        p[0] = self.rootScope.find(p[1])

    def p_others_symbol(self, p):
        "others_symbol                  : OTHERS"
        p[0] = self.rootScope.find(p[1])

    def p_empty(self, p):
        "empty                          : "
        p[0] = None

    def p_error(self, t):
        if not t:
            print("There was a syntax error at the end of the file")
            return
        print(f"there was an error with '{t.value}' at {t.lineno}")

# end of production rules

    def parse(self, data):
        self.parser.parse(data, lexer=self.lexer.lexer)

    def popScope(self):
        if not self.curScope.outer:
            raise 


def parser_test():
    with open("../lib/vhdl/std/standard.vhd", 'r', encoding='utf-8', errors='ignore') as parse_std:
        parse_str = parse_std.read()

    with open("../lib/vhdl/std/textio.vhd", 'r', encoding='utf-8', errors='ignore') as parse_txtio:
        parse_str += parse_txtio.read()

    parser = VhdlParser.getVhdlParser()
    parser.parse(parse_str)

    print(parser.designFile)
    
if __name__ == "__main__":
    parser_test()
