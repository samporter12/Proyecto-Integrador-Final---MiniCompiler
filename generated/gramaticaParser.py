# Generated from gramatica.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,23,62,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,4,0,19,8,0,11,0,12,0,20,1,0,1,0,1,1,1,1,1,1,1,
        1,4,1,29,8,1,11,1,12,1,30,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,
        3,3,3,43,8,3,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,
        1,6,1,6,1,7,1,7,1,7,0,0,8,0,2,4,6,8,10,12,14,0,1,1,0,11,16,57,0,
        18,1,0,0,0,2,24,1,0,0,0,4,34,1,0,0,0,6,42,1,0,0,0,8,44,1,0,0,0,10,
        49,1,0,0,0,12,55,1,0,0,0,14,59,1,0,0,0,16,19,3,2,1,0,17,19,3,4,2,
        0,18,16,1,0,0,0,18,17,1,0,0,0,19,20,1,0,0,0,20,18,1,0,0,0,20,21,
        1,0,0,0,21,22,1,0,0,0,22,23,5,0,0,1,23,1,1,0,0,0,24,25,5,1,0,0,25,
        26,5,17,0,0,26,28,5,5,0,0,27,29,3,6,3,0,28,27,1,0,0,0,29,30,1,0,
        0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,32,1,0,0,0,32,33,5,6,0,0,33,3,
        1,0,0,0,34,35,5,2,0,0,35,36,5,17,0,0,36,37,5,3,0,0,37,38,3,12,6,
        0,38,39,5,9,0,0,39,5,1,0,0,0,40,43,3,8,4,0,41,43,3,10,5,0,42,40,
        1,0,0,0,42,41,1,0,0,0,43,7,1,0,0,0,44,45,5,17,0,0,45,46,5,10,0,0,
        46,47,5,18,0,0,47,48,5,9,0,0,48,9,1,0,0,0,49,50,5,4,0,0,50,51,5,
        7,0,0,51,52,5,18,0,0,52,53,5,8,0,0,53,54,5,9,0,0,54,11,1,0,0,0,55,
        56,5,17,0,0,56,57,3,14,7,0,57,58,5,18,0,0,58,13,1,0,0,0,59,60,7,
        0,0,0,60,15,1,0,0,0,4,18,20,30,42
    ]

class gramaticaParser ( Parser ):

    grammarFileName = "gramatica.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'tarea'", "'ir_a'", "'si'", "'print'", 
                     "'{'", "'}'", "'('", "')'", "';'", "'='", "'=='", "'!='", 
                     "'>'", "'<'", "'>='", "'<='" ]

    symbolicNames = [ "<INVALID>", "TAREA", "IR_A", "SI", "PRINT", "LBRACE", 
                      "RBRACE", "LPAREN", "RPAREN", "SEMI", "ASSIGN", "EQ", 
                      "NEQ", "GT", "LT", "GTE", "LTE", "ID", "VALUE", "NUMBER", 
                      "STRING", "BOOLEAN", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_task = 1
    RULE_transition = 2
    RULE_statement = 3
    RULE_assignment_stmt = 4
    RULE_print_stmt = 5
    RULE_condition = 6
    RULE_comparator = 7

    ruleNames =  [ "program", "task", "transition", "statement", "assignment_stmt", 
                   "print_stmt", "condition", "comparator" ]

    EOF = Token.EOF
    TAREA=1
    IR_A=2
    SI=3
    PRINT=4
    LBRACE=5
    RBRACE=6
    LPAREN=7
    RPAREN=8
    SEMI=9
    ASSIGN=10
    EQ=11
    NEQ=12
    GT=13
    LT=14
    GTE=15
    LTE=16
    ID=17
    VALUE=18
    NUMBER=19
    STRING=20
    BOOLEAN=21
    WS=22
    COMMENT=23

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(gramaticaParser.EOF, 0)

        def task(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.TaskContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.TaskContext,i)


        def transition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.TransitionContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.TransitionContext,i)


        def getRuleIndex(self):
            return gramaticaParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = gramaticaParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 18
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 16
                    self.task()
                    pass
                elif token in [2]:
                    self.state = 17
                    self.transition()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 20 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==2):
                    break

            self.state = 22
            self.match(gramaticaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TaskContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TAREA(self):
            return self.getToken(gramaticaParser.TAREA, 0)

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def LBRACE(self):
            return self.getToken(gramaticaParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(gramaticaParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.StatementContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.StatementContext,i)


        def getRuleIndex(self):
            return gramaticaParser.RULE_task

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTask" ):
                listener.enterTask(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTask" ):
                listener.exitTask(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTask" ):
                return visitor.visitTask(self)
            else:
                return visitor.visitChildren(self)




    def task(self):

        localctx = gramaticaParser.TaskContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_task)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(gramaticaParser.TAREA)
            self.state = 25
            self.match(gramaticaParser.ID)
            self.state = 26
            self.match(gramaticaParser.LBRACE)
            self.state = 28 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 27
                self.statement()
                self.state = 30 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==4 or _la==17):
                    break

            self.state = 32
            self.match(gramaticaParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IR_A(self):
            return self.getToken(gramaticaParser.IR_A, 0)

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def SI(self):
            return self.getToken(gramaticaParser.SI, 0)

        def condition(self):
            return self.getTypedRuleContext(gramaticaParser.ConditionContext,0)


        def SEMI(self):
            return self.getToken(gramaticaParser.SEMI, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_transition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransition" ):
                listener.enterTransition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransition" ):
                listener.exitTransition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransition" ):
                return visitor.visitTransition(self)
            else:
                return visitor.visitChildren(self)




    def transition(self):

        localctx = gramaticaParser.TransitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_transition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(gramaticaParser.IR_A)
            self.state = 35
            self.match(gramaticaParser.ID)
            self.state = 36
            self.match(gramaticaParser.SI)
            self.state = 37
            self.condition()
            self.state = 38
            self.match(gramaticaParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment_stmt(self):
            return self.getTypedRuleContext(gramaticaParser.Assignment_stmtContext,0)


        def print_stmt(self):
            return self.getTypedRuleContext(gramaticaParser.Print_stmtContext,0)


        def getRuleIndex(self):
            return gramaticaParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = gramaticaParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_statement)
        try:
            self.state = 42
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 40
                self.assignment_stmt()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 41
                self.print_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Assignment_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(gramaticaParser.ASSIGN, 0)

        def VALUE(self):
            return self.getToken(gramaticaParser.VALUE, 0)

        def SEMI(self):
            return self.getToken(gramaticaParser.SEMI, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_assignment_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment_stmt" ):
                listener.enterAssignment_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment_stmt" ):
                listener.exitAssignment_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment_stmt" ):
                return visitor.visitAssignment_stmt(self)
            else:
                return visitor.visitChildren(self)




    def assignment_stmt(self):

        localctx = gramaticaParser.Assignment_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_assignment_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(gramaticaParser.ID)
            self.state = 45
            self.match(gramaticaParser.ASSIGN)
            self.state = 46
            self.match(gramaticaParser.VALUE)
            self.state = 47
            self.match(gramaticaParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Print_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(gramaticaParser.PRINT, 0)

        def LPAREN(self):
            return self.getToken(gramaticaParser.LPAREN, 0)

        def VALUE(self):
            return self.getToken(gramaticaParser.VALUE, 0)

        def RPAREN(self):
            return self.getToken(gramaticaParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(gramaticaParser.SEMI, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_print_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrint_stmt" ):
                listener.enterPrint_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrint_stmt" ):
                listener.exitPrint_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_stmt" ):
                return visitor.visitPrint_stmt(self)
            else:
                return visitor.visitChildren(self)




    def print_stmt(self):

        localctx = gramaticaParser.Print_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_print_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(gramaticaParser.PRINT)
            self.state = 50
            self.match(gramaticaParser.LPAREN)
            self.state = 51
            self.match(gramaticaParser.VALUE)
            self.state = 52
            self.match(gramaticaParser.RPAREN)
            self.state = 53
            self.match(gramaticaParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def comparator(self):
            return self.getTypedRuleContext(gramaticaParser.ComparatorContext,0)


        def VALUE(self):
            return self.getToken(gramaticaParser.VALUE, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = gramaticaParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(gramaticaParser.ID)
            self.state = 56
            self.comparator()
            self.state = 57
            self.match(gramaticaParser.VALUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(gramaticaParser.EQ, 0)

        def NEQ(self):
            return self.getToken(gramaticaParser.NEQ, 0)

        def GT(self):
            return self.getToken(gramaticaParser.GT, 0)

        def LT(self):
            return self.getToken(gramaticaParser.LT, 0)

        def GTE(self):
            return self.getToken(gramaticaParser.GTE, 0)

        def LTE(self):
            return self.getToken(gramaticaParser.LTE, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_comparator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparator" ):
                listener.enterComparator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparator" ):
                listener.exitComparator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparator" ):
                return visitor.visitComparator(self)
            else:
                return visitor.visitChildren(self)




    def comparator(self):

        localctx = gramaticaParser.ComparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_comparator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 129024) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





