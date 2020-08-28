import cmp.visitor as visitor
from AST import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from AST import VarDeclarationNode, AssignNode, CallNode, BinaryNode
from AST import ConstantNumNode, VariableNode, InstantiateNode

from cmp.semantic import SemanticError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType, IntType
from cmp.semantic import Context, Scope

from TypeCollectorBuilder import TypeCollector, TypeBuilder

#Find Correct Loaction For This
WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'

class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable('self', self.current_type)
    
        for attr in self.current_type.attributes:
             scope.define_variable(attr.name, attr.type)
        
        for feature in node.features:
            self.visit(feature, scope.create_child())
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        
        for idx, typex in zip(self.current_method.param_names, self.current_method.param_types):
            scope.define_variable(idx, typex)
        for expr in node.body:
            self.visit(expr, scope)
        
        ret_type_decl = self.current_method.return_type 
        ret_type_expr = node.body[-1].computed_type
        if not ret_type_expr.conforms_to(ret_type_decl):
            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', ret_type_decl.name, 1).replace('%s', ret_type_expr.name, 1))
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        if node.id == 'self':
            self.errors.append("Identifier 'self' is already defined GLOBALLY")
        try:
            var_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.errors.append(err.text)
            var_type = ErrorType()
            
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        
        if not expr_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
        if scope.is_defined(node.id):
            self.errors.append(LOCAL_ALREADY_DEFINED.replace('%s', node.id, 1).replace('%s', self.current_method.name, 1))
        else:
            scope.define_variable(node.id, var_type)        
        node.computed_type = var_type    
        
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        if scope.is_defined(node.id):
            var = scope.find_variable(node.id)
            var_type = var.type
            
            self.visit(node.expr, scope)
            expr_type = node.expr.computed_type
            if expr_type is str:
                print(expr_type)
            
            if var.name == 'self':
                self.errors.append(SELF_IS_READONLY)
            elif not expr_type.conforms_to(var_type):
                self.errors.append(INCOMPATIBLE_TYPES.replace('%s', var_type.name, 1).replace('%s', expr_type.name, 1))
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.id, 1).replace('%s', self.current_method.name, 1))
            var_type = ErrorType()
        node.computed_type = var_type
    
    @visitor.when(CallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        obj_type = node.obj.computed_type
        
        try:
            method = obj_type.get_method(node.id)
            if len(node.args) == len(method.param_types):
                for arg, param_type in zip(node.args, method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type
                    if isinstance(arg_type, str):
                        print("aaa")
                        print(arg_type)
                        print("bbb")
                        
                    if not arg_type.conforms_to(param_type):
                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                 self.errors.append("Method", method.name, "only accepts",len(method.param_types),"arguments")
            ret_type = method.return_type
        
        except SemanticError as err:
            self.errors.append(err.text)
            ret_type = ErrorType()
            
        node.computed_type = ret_type
            
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        
        if not (left_type.conforms_to(IntType()) and right_type.conforms_to(IntType())):
            self.errors.append(INVALID_OPERATION.replace('%s', left_type.name, 1).replace('%s', right_type.name, 1))
            node_type = ErrorType()
        else:
            node_type = IntType()
        
        node.computed_type = node_type
            
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        node.computed_type = IntType()

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            var_type = var.type
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.lex, 1).replace('%s', self.current_method.name, 1))
            var_type = ErrorType()
        
        node.computed_type = var_type

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.lex)
        except SemanticError as err:
            self.errors.append(err.text)
            node_type = ErrorType()
            
        node.computed_type = node_type