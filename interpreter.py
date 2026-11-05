# interpreter.py

from errors import TahaRuntimeError
from ast_nodes import *
from lexer import Lexer
from parser import Parser

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent


    def define(self, name : str, value : object, source_location : SourceLocation):
        if name in self.variables:
            raise TahaRuntimeError.variable_already_defined(
                name=name,
                line=source_location.line,
                column=source_location.column
            )

        self.variables[name] = value


    def get(self, name : str, source_location : SourceLocation):
        if name in self.variables:
            return self.variables[name]
        else:
            current_environment : Environment = self.parent

            while current_environment is not None:
                if name in current_environment.variables:
                    return current_environment.variables[name]
                
                current_environment = current_environment.parent

        raise TahaRuntimeError.undefined_variable(
            name=name,
            line=source_location.line,
            column=source_location.column
        )


    def exists(self, name: str) -> bool:
        current_environment = self

        while current_environment is not None:
            if name in current_environment.variables:
                return True

            current_environment = current_environment.parent

        return False


class Interpreter:

    def __init__(self, env: Environment):
        self.env = env

    def execute_expression(self, expr: Expression, env: Environment) -> object:

        if isinstance(expr, NumberLiteral) or isinstance(expr, StringLiteral) or isinstance(expr, BooleanLiteral):
            return expr.value
        
        elif isinstance(expr, Identifier):
            return env.get(expr.name, expr.location)
        
        elif isinstance(expr, BinaryExpression):
            left_value = self.execute_expression(expr.left, env=env)
            right_value = self.execute_expression(expr.right, env=env)

            match expr.operator:
                case TokenType.PLUS:
                    if self.can_compare_order(left_value, right_value):
                        return left_value + right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="PLUS can only apply to two numbers or two strings.",
                            line=expr.location.line,
                            column=expr.location.column
                        )
                
                case TokenType.MINUS:
                    if self.is_number(left_value) and self.is_number(right_value):
                        return left_value - right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="MINUS can only apply to two numbers.",
                            line=expr.location.line,
                            column=expr.location.column
                        )
                
                case TokenType.STAR:
                    if self.is_number(left_value) and self.is_number(right_value):
                        return left_value * right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="STAR can only apply to two numbers.",
                            line=expr.location.line,
                            column=expr.location.column
                        )
                
                case TokenType.SLASH:
                    if self.is_number(left_value) and self.is_number(right_value):
                        if right_value == 0:
                            raise TahaRuntimeError.division_by_zero(
                                line=expr.right.location.line,
                                column=expr.right.location.column
                            )
                        return left_value / right_value

                    else:
                        raise TahaRuntimeError.type_error(
                            message="SLASH can only apply to two numbers.",
                            line=expr.location.line,
                            column=expr.location.column
                        )

                case TokenType.PERCENT:
                    if self.is_number(left_value) and self.is_number(right_value):
                        if right_value == 0:
                            raise TahaRuntimeError.division_by_zero(
                                line=expr.right.location.line,
                                column=expr.right.location.column
                            )
                        return left_value % right_value

                    else:
                        raise TahaRuntimeError.type_error(
                            message="PERCENT can only apply to two numbers.",
                            line=expr.location.line,
                            column=expr.location.column
                        )


                case TokenType.EQUAL_EQUAL:
                    return self.are_equal(left_value, right_value)

                case TokenType.BANG_EQUAL:
                    return not self.are_equal(left_value, right_value)

                case TokenType.LESS:
                    if self.can_compare_order(left_value, right_value):
                        return left_value < right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="LESS can only apply to two numbers or two strings.",
                            line=expr.location.line,
                            column=expr.location.column
                        )

                case TokenType.GREATER:
                    if self.can_compare_order(left_value, right_value):
                        return left_value > right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="GREATER can only apply to two numbers or two strings.",
                            line=expr.location.line,
                            column=expr.location.column
                        )

                case TokenType.LESS_EQUAL:
                    if self.can_compare_order(left_value, right_value):
                        return left_value <= right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="LESS_EQUAL can only apply to two numbers or two strings.",
                            line=expr.location.line,
                            column=expr.location.column
                        )

                case TokenType.GREATER_EQUAL:
                    if self.can_compare_order(left_value, right_value):
                        return left_value >= right_value
                    else:
                        raise TahaRuntimeError.type_error(
                            message="GREATER_EQUAL can only apply to two numbers or two strings.",
                            line=expr.location.line,
                            column=expr.location.column
                        )

        elif isinstance(expr, UnaryExpression):
            operand = self.execute_expression(expr.operand, env=env)

            match expr.operator:
                case TokenType.MINUS:
                    if type(operand) not in (int, float):
                        raise TahaRuntimeError.type_error(
                            message="MINUS can only apply to INT or FLOAT.",
                            line=expr.operand.location.line,
                            column=expr.operand.location.column
                        )
                    
                    return -operand
                
                case TokenType.BANG:
                    if type(operand) is not bool:
                        raise TahaRuntimeError.type_error(
                            message="BANG can only apply to BOOLEAN.",
                            line=expr.operand.location.line,
                            column=expr.operand.location.column
                        )
                    
                    return not operand

    def execute_statement(self, statement: Statement, env: Environment):
        if isinstance(statement, LetStatement):
            self.execute_let_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, PrintStatement):
            self.execute_print_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, IfStatement):
            self.execute_if_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, BlockStatement):
            self.execute_block_statement(
                statement=statement,
                env=env
            )

    def execute_print_statement(self, statement: PrintStatement, env: Environment):
        print_value = self.execute_expression(
            statement.expression,
            env=env
        )

        print(print_value)

    def execute_let_statement(self, statement: LetStatement, env: Environment):
        env.define(
            name=statement.name,
            value=self.execute_expression(expr=statement.value, env=env),
            source_location=statement.location
        )

    def execute_block_statement(self, statement: BlockStatement, env:Environment):
        child_env = Environment(parent=env)
        inner_statements = statement.statements

        for statement in inner_statements:
            self.execute_statement(statement=statement, env=child_env)

    def execute_if_statement(self, statement: IfStatement, env: Environment):
        condition_value = self.execute_expression(expr=statement.condition, env=env)

        if type(condition_value) is not bool:
            raise TahaRuntimeError.type_error(
                message="IF condition must evaluate to BOOLEAN.",
                line=statement.condition.location.line,
                column=statement.condition.location.column
            )

        if condition_value:
            self.execute_block_statement(
                statement=statement.then_branch,
                env=env
            )
        else:
            if statement.else_branch is not None:
                self.execute_block_statement(
                    statement=statement.else_branch,
                    env=env
                )

    def is_number(self, value: object) -> bool:
        return type(value) in (int, float)

    def can_compare_order(self, left: object, right: object) -> bool:
        if (
            self.is_number(left) and self.is_number(right) or
            type(left) is str and type(right) is str
        ):
            return True

        return  False

    def are_equal(self, left: object, right: object) -> bool:
        if (
            (type(left) is bool and type(right) is not bool) or
            (type(left) is not bool and type(right) is bool)
        ):
            return False
        else:
            return left == right
