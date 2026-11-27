# interpreter.py

from errors import TahaRuntimeError
from ast_nodes import *
from taha_builtins import BuiltinRegistry

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

    def assign(self, name: str, value: object, location: SourceLocation):
        current_env = self

        while current_env is not None:
            if name in current_env.variables:
                current_env.variables[name] = value
                return

            current_env = current_env.parent

        raise TahaRuntimeError.undefined_variable_assignment(
            line=location.line,
            column=location.column,
            name=name
        )
        


class Interpreter:

    def __init__(self, env: Environment, builtins: BuiltinRegistry):
        self.env = env
        self.builtins = builtins

    def execute_program(self, program: Program, env: Environment):
        for statement in program.statements:
            self.execute_statement(statement, env=env)

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

        elif isinstance(expr, ListExpression):
            list_elements = []

            for element in expr.elements:
                value = self.execute_expression(expr=element, env=env)

                if isinstance(value, list):
                    raise TahaRuntimeError.nested_list(
                        line=element.location.line,
                        column=element.location.column
                    )

                list_elements.append(value)

            return list_elements

        elif isinstance(expr, IndexExpression):
            expr_object = self.execute_expression(expr.object, env)

            if type(expr_object) not in (list, str):
                raise TahaRuntimeError.invalid_object_for_index_expression(
                    line=expr.object.location.line,
                    column=expr.object.location.column,
                    got=type(expr_object).__name__
                )


            expr_index = self.execute_expression(expr.index, env)

            if type(expr_index) != int:
                raise TahaRuntimeError.invalid_type_index(
                    got=expr_index,
                    line=expr.index.location.line,
                    column=expr.index.location.column
                )

            if expr_index < 0:
                raise TahaRuntimeError.negative_index(
                    got=expr_index,
                    line=expr.index.location.line,
                    column=expr.index.location.column
                )

            if expr_index >= len(expr_object):
                max_index = len(expr_object)-1

                if max_index == -1:
                    raise TahaRuntimeError.zero_index(
                        line=expr.index.location.line,
                        column=expr.index.location.column
                    )

                raise TahaRuntimeError.invalid_index(
                    max_index=max_index,
                    got_index=expr_index,
                    line=expr.index.location.line,
                    column=expr.index.location.column
                )
            
            return expr_object[expr_index]

        elif isinstance(expr, CallExpression):
            return self.execute_call_expression(expr, env)

    def execute_statement(self, statement: Statement, env: Environment):
        if isinstance(statement, LetStatement):
            self.execute_let_statement(
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

        elif isinstance(statement, CallStatement):
            self.execute_call_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, AssignmentStatement):
            self.execute_assignment_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, CompoundAssignmentStatement):
            self.execute_compound_assignment_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, WhileStatement):
            self.execute_while_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, ForStatement):
            self.execute_for_statement(
                statement=statement,
                env=env
            )

        elif isinstance(statement, RepeatStatement):
            self.execute_repeat_statement(
                statement=statement,
                env=env
            )

    def execute_call_statement(self, statement: CallStatement, env: Environment):
        self.execute_call_expression(
            expr=statement.call,
            env=env
        )

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

    def execute_call_expression(self, expr: CallExpression, env:Environment):
        expr_callee = expr.callee

        if not isinstance(expr_callee, Identifier):
            raise TahaRuntimeError.invalid_function_callee(
                line=expr_callee.location.line,
                column=expr_callee.location.column,
                got=type(expr_callee).__name__
            )

        function_name = expr_callee.name
        func, expected_count = self.builtins.get(expr_callee.name, expr_callee.location)

        if len(expr.arguments) != expected_count:
            raise TahaRuntimeError.invalid_function_argument_counts(
                line=expr.location.line,
                column=expr.location.column,
                got_arguments=len(expr.arguments),
                expected_arguments=expected_count,
                function_name=function_name
            )
        
        args = []

        for argument in expr.arguments:
            value = self.execute_expression(argument, env)
            args.append((value, argument.location))
        
        return func(*args[0])

    def execute_assignment_statement(
        self,
        statement: AssignmentStatement,
        env: Environment
    ):

        if not env.exists(statement.name):
            raise TahaRuntimeError.undefined_variable_assignment(
                line=statement.location.line,
                column=statement.location.column,
                name=statement.name
            )   

        value = self.execute_expression(statement.value, env)
        variable = env.get(statement.name, statement.location)

        if not self.is_compatible_type(value, variable):
            raise TahaRuntimeError.invalid_assignment_value_type(
                line=statement.value.location.line,
                column=statement.value.location.column,
                got=type(value).__name__,
                expected=type(variable).__name__
            )

        env.assign(
            name=statement.name,
            value=value,
            location=statement.location
        )

    def execute_compound_assignment_statement(
        self,
        statement: CompoundAssignmentStatement,
        env: Environment
    ):
        if not env.exists(statement.name):
            raise TahaRuntimeError.undefined_variable_assignment(
                line=statement.location.line,
                column=statement.location.column,
                name=statement.name
            )   

        value = self.execute_expression(statement.value, env)
        variable = env.get(statement.name, statement.location)

        operator = statement.operator

        result = self.get_compound_assignment_value(
                variable=variable,
                value=value,
                operator=operator,
                location=statement.location
        )

        if not self.is_compatible_type(result, variable):
            raise TahaRuntimeError.invalid_assignment_value_type(
                line=statement.value.location.line,
                column=statement.value.location.column,
                got=type(result).__name__,
                expected=type(variable).__name__
            )

        env.assign(
            name=statement.name,
            value=result,
            location=statement.location
        )

    def get_compound_assignment_value(
            self, 
            variable: object, 
            value: object, 
            operator: TokenType,
            location: SourceLocation
        ) -> object:

        match operator:
            case TokenType.PLUS_EQUAL:
                if not self.can_compare_order(value, variable):
                    raise TahaRuntimeError.type_error(
                        message="PLUS can only apply to two numbers or two strings.",
                        line=location.line,
                        column=location.column
                    )
                
                return variable + value

            case TokenType.MINUS_EQUAL:
                if not (self.is_number(value) and self.is_number(variable)):
                    raise TahaRuntimeError.type_error(
                        message="MINUS can only apply to two numbers.",
                        line=location.line,
                        column=location.column
                    )
                
                return variable - value

            case TokenType.STAR_EQUAL:
                if not (self.is_number(value) and self.is_number(variable)):
                  raise TahaRuntimeError.type_error(
                        message="STAR can only apply to two numbers.",
                        line=location.line,
                        column=location.column
                    )
                return variable * value

            case TokenType.SLASH_EQUAL:
                if not (self.is_number(value) and self.is_number(variable)):
                    raise TahaRuntimeError.type_error(
                        message="SLASH can only apply to two numbers.",
                        line=location.line,
                        column=location.column
                    )
                
                if value == 0:
                    raise TahaRuntimeError.division_by_zero(
                        line=location.line,
                        column=location.column
                    )
                
                return variable / value

            case TokenType.PERCENT_EQUAL:
                if not (self.is_number(value) and self.is_number(variable)):
                    raise TahaRuntimeError.type_error(
                        message="PERCENT can only apply to two numbers.",
                        line=location.line,
                        column=location.column
                    )
                
                if value == 0:
                    raise TahaRuntimeError.division_by_zero(
                        line=location.line,
                        column=location.column
                    )

                return variable % value

            case _:
                raise TahaRuntimeError.type_error(
                    message="Invalid operator for assignment",
                    line=location.line,
                    column=location.column
                )

    def execute_while_statement(self, statement: WhileStatement, env: Environment):

        while condition_value := self.execute_expression(expr=statement.condition, env=env):

            if type(condition_value) != bool:
                raise TahaRuntimeError.unexpected_while_condition_type(
                    line=statement.condition.location.line,
                    column=statement.condition.location.column,
                    condition_type=type(condition_value).__name__
                )

            for statement_ in statement.body.statements:
                self.execute_statement(statement=statement_, env=env)

    def execute_for_statement(self, statement: ForStatement, env: Environment):
        loop_env = Environment(parent=env)

        self.execute_let_statement(statement=statement.init, env=loop_env)

        if not (
            isinstance(statement.update, AssignmentStatement) or 
            isinstance(statement.update, CompoundAssignmentStatement)
        ):
            raise TahaRuntimeError.unexpected_for_update_statement_type(
                line=statement.update.location.line,
                column=statement.update.location.column,
                update_type=type(statement.update).__name__
            )

        while True:

            condition = self.execute_expression(statement.condition, loop_env)

            if type(condition) != bool:
                raise TahaRuntimeError.unexpected_for_condition_type(
                    line=statement.condition.location.line,
                    column=statement.condition.location.column,
                    condition_type=type(condition).__name__
                )

            if condition:

                self.execute_block_statement(statement.body, loop_env)
                self.execute_statement(statement=statement.update, env=loop_env)

            else:
                return

    def execute_repeat_statement(self, statement: RepeatStatement, env: Environment):
        times_value = self.execute_expression(statement.times, env=env)

        if type(times_value) != int:
            raise TahaRuntimeError.unexpected_repeat_times_expression_type(
                line=statement.times.location.line,
                column=statement.times.location.column,
                times_type=type(times_value).__name__
            )

        if times_value < 0:
            raise TahaRuntimeError.unexpected_repeat_times_expression_range(
                line=statement.times.location.line,
                column=statement.times.location.column,
                times_value=times_value
            )

        for _ in range(times_value):
            self.execute_block_statement(statement=statement.body, env=env)

    def is_number(self, value: object) -> bool:
        return type(value) in (int, float)

    def can_compare_order(self, left: object, right: object) -> bool:
        if (
            self.is_number(left) and self.is_number(right) or
            type(left) is str and type(right) is str
        ):
            return True

        return  False

    def is_compatible_type(self, old_value, new_value):
        if self.is_number(old_value) and self.is_number(new_value):
            return True

        return type(old_value) == type(new_value)

    def are_equal(self, left: object, right: object) -> bool:
        if (
            (type(left) is bool and type(right) is not bool) or
            (type(left) is not bool and type(right) is bool)
        ):
            return False
        else:
            return left == right

