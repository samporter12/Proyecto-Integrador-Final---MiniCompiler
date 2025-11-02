# Generated from gramatica.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete listener for a parse tree produced by gramaticaParser.
class gramaticaListener(ParseTreeListener):

    # Enter a parse tree produced by gramaticaParser#program.
    def enterProgram(self, ctx:gramaticaParser.ProgramContext):
        pass

    # Exit a parse tree produced by gramaticaParser#program.
    def exitProgram(self, ctx:gramaticaParser.ProgramContext):
        pass


    # Enter a parse tree produced by gramaticaParser#task.
    def enterTask(self, ctx:gramaticaParser.TaskContext):
        pass

    # Exit a parse tree produced by gramaticaParser#task.
    def exitTask(self, ctx:gramaticaParser.TaskContext):
        pass


    # Enter a parse tree produced by gramaticaParser#transition.
    def enterTransition(self, ctx:gramaticaParser.TransitionContext):
        pass

    # Exit a parse tree produced by gramaticaParser#transition.
    def exitTransition(self, ctx:gramaticaParser.TransitionContext):
        pass


    # Enter a parse tree produced by gramaticaParser#statement.
    def enterStatement(self, ctx:gramaticaParser.StatementContext):
        pass

    # Exit a parse tree produced by gramaticaParser#statement.
    def exitStatement(self, ctx:gramaticaParser.StatementContext):
        pass


    # Enter a parse tree produced by gramaticaParser#assignment_stmt.
    def enterAssignment_stmt(self, ctx:gramaticaParser.Assignment_stmtContext):
        pass

    # Exit a parse tree produced by gramaticaParser#assignment_stmt.
    def exitAssignment_stmt(self, ctx:gramaticaParser.Assignment_stmtContext):
        pass


    # Enter a parse tree produced by gramaticaParser#print_stmt.
    def enterPrint_stmt(self, ctx:gramaticaParser.Print_stmtContext):
        pass

    # Exit a parse tree produced by gramaticaParser#print_stmt.
    def exitPrint_stmt(self, ctx:gramaticaParser.Print_stmtContext):
        pass


    # Enter a parse tree produced by gramaticaParser#condition.
    def enterCondition(self, ctx:gramaticaParser.ConditionContext):
        pass

    # Exit a parse tree produced by gramaticaParser#condition.
    def exitCondition(self, ctx:gramaticaParser.ConditionContext):
        pass


    # Enter a parse tree produced by gramaticaParser#comparator.
    def enterComparator(self, ctx:gramaticaParser.ComparatorContext):
        pass

    # Exit a parse tree produced by gramaticaParser#comparator.
    def exitComparator(self, ctx:gramaticaParser.ComparatorContext):
        pass



del gramaticaParser