
import cmp.visitor as visitor

from AST import ProgramNode, ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode
from cmp.semantic import SemanticError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType
from cmp.semantic import Context

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
        
        self.class_tree = dict()
        self.roots = []
        self.class_count = 0
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.context.create_type('Int')
        for class_def in node.declarations:
            self.visit(class_def)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
            self.class_count += 1
            if node.parent:
                try:
                    self.class_tree[node.parent].append(node.id)
                except KeyError:
                    self.class_tree[node.parent] = [node.id]
            else: self.roots.append(node.parent)
                
        except SemanticError as err:
            self.errors.append(err.text)

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_def in node.declarations:
            self.visit(class_def)
#         try:
#             self.context.get_type('Main').get_method('main')
#         except SemanticError as err:
#             self.errors.append("Class \'Main\' and method \'main\' were not found.")
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except SemanticError as err:
                self.errors.append(err.text)
        
        for feature in node.features:
            self.visit(feature)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.errors.append(err.text)
            attr_type = ErrorType()
            
        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as err:
            self.errors.append(err.text)
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        try:
            ret_type = self.context.get_type(node.type) if node.type != 'Void' else VoidType()
        except SemanticError as err:
            self.errors.append(err.text)
            ret_type = ErrorType()
            
        params_type = []
        params_name = []
        for p_name, p_type in node.params:
            try:
                params_type.append(self.context.get_type(p_type))
            except SemanticError as err:
                params_type.append(ErrorType())
                self.errors.append(err.text)
            params_name.append(p_name)
            
        try:
            self.current_type.define_method(node.id, params_name, params_type, ret_type)
        except SemanticError as err:
            self.errors.append(err.text)