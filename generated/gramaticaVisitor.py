# Generated from gramatica.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete generic visitor for a parse tree produced by gramaticaParser.

class gramaticaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gramaticaParser#program.
    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#task.
    def visitTask(self, ctx:gramaticaParser.TaskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#transition.
    def visitTransition(self, ctx:gramaticaParser.TransitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#statement.
    def visitStatement(self, ctx:gramaticaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#assignment_stmt.
    def visitAssignment_stmt(self, ctx:gramaticaParser.Assignment_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#print_stmt.
    def visitPrint_stmt(self, ctx:gramaticaParser.Print_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#condition.
    def visitCondition(self, ctx:gramaticaParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#comparator.
    def visitComparator(self, ctx:gramaticaParser.ComparatorContext):
        return self.visitChildren(ctx)



del gramaticaParser