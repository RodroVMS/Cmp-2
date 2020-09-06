from cmp.pycompiler import Grammar

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

class BlockNode(ExpressionNode):
    def __init__(self, body):
        self.body = body

class IfDeclarationNode(ExpressionNode):
    def __init__(self, ifexpr, thenexpr, elseexpr):
        self.ifexpr = ifexpr
        self.thenexpr = thenexpr
        self.elseexpr = elseexpr

class WhileDeclarationNode(ExpressionNode):
    def __init__(self, whileexpr, bodyexpr):
        self.whileexpr = whileexpr
        self.bodyexpr = bodyexpr

class LetDeclarationNode(ExpressionNode):
    def __init__(self, letvars, expr):
        self.letvars = letvars
        self.expr = expr

class CaseDeclarationNode(ExpressionNode):
    def __init__(self, expr, casevars):
        self.expr = expr
        self.casevars = casevars       

class IsVoidDeclarationNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args):
        self.obj = obj
        self.id = idx
        self.args = args

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ConstantNumNode(AtomicNode):
    pass
class ConstantStringNode(AtomicNode):
    pass
class VariableNode(AtomicNode):
    pass
class InstantiateNode(AtomicNode):
    pass
class PlusNode(BinaryNode):
    pass
class MinusNode(BinaryNode):
    pass
class StarNode(BinaryNode):
    pass
class DivNode(BinaryNode):
    pass

class LesserNode(BinaryNode):
    pass
class LesserEqualNode(BinaryNode):
    pass
class EqualNode(BinaryNode):
    pass
class NotNode(AtomicNode):
    pass