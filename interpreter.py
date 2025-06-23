import re
import sys

class TokenType:
    SHOW = 'SHOW'
    DISPLAY = 'DISPLAY'
    TELL = 'TELL'
    COMBINED_WITH = 'COMBINED_WITH'
    SET = 'SET'
    TO = 'TO'
    BECOMES = 'BECOMES'
    IS_KW = 'IS_KEYWORD'
    GETS = 'GETS'
    ASK = 'ASK'
    AND_STORE_IN = 'AND_STORE_IN'
    GET_KW = 'GET_KEYWORD'
    INTO = 'INTO'
    READ = 'READ'
    LINE = 'LINE'
    FROM = 'FROM'
    KEYBOARD = 'KEYBOARD'
    ADD = 'ADD'
    INCREASE = 'INCREASE'
    DECREASE = 'DECREASE'
    BY = 'BY'
    PRODUCT_OF = 'PRODUCT_OF'
    CALCULATE = 'CALCULATE'
    AS = 'AS'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    TIMES = 'TIMES'
    DIVIDED_BY = 'DIVIDED_BY'
    AND_OP = 'AND_OPERATOR'
    IF = 'IF'
    THEN = 'THEN'
    ELSE_IF = 'ELSE_IF'
    ELSE = 'ELSE'
    END_IF = 'END_IF'
    REPEAT = 'REPEAT'
    TIMES_KW = 'TIMES_KEYWORD'
    COUNT = 'COUNT'
    FROM = 'FROM'
    TO_KW = 'TO_KEYWORD'
    WHILE = 'WHILE'
    END_WHILE = 'END_WHILE'
    END_REPEAT = 'END_REPEAT'
    END_COUNT = 'END_COUNT'
    IS_GREATER_THAN = 'IS_GREATER_THAN'
    IS_LESS_THAN = 'IS_LESS_THAN'
    IS_EQUAL_TO = 'IS_EQUAL_TO'
    IS_NOT_EQUAL_TO = 'IS_NOT_EQUAL_TO'
    IS_NOT = 'IS_NOT'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'
    COLON = 'COLON'
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'
    RIBINDULATING_FLOXYMITE = 'RIBINDULATING_FLOXYMITE'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line {self.line}, col {self.column})"

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Lexing Error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

class Lexer:
    KEYWORDS = {
        'show': TokenType.SHOW,
        'display': TokenType.DISPLAY,
        'tell': TokenType.TELL,
        'combined with': TokenType.COMBINED_WITH,
        'set': TokenType.SET,
        'to': TokenType.TO,
        'becomes': TokenType.BECOMES,
        'is': TokenType.IS_KW,
        'gets': TokenType.GETS,
        'ask': TokenType.ASK,
        'and store in': TokenType.AND_STORE_IN,
        'get': TokenType.GET_KW,
        'into': TokenType.INTO,
        'read': TokenType.READ,
        'line': TokenType.LINE,
        'from': TokenType.FROM,
        'keyboard': TokenType.KEYBOARD,
        'add': TokenType.ADD,
        'increase': TokenType.INCREASE,
        'decrease': TokenType.DECREASE,
        'by': TokenType.BY,
        'product of': TokenType.PRODUCT_OF,
        'calculate': TokenType.CALCULATE,
        'as': TokenType.AS,
        'plus': TokenType.PLUS,
        'minus': TokenType.MINUS,
        'times': TokenType.TIMES,
        'divided by': TokenType.DIVIDED_BY,
        'and': TokenType.AND_OP,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else if': TokenType.ELSE_IF,
        'else': TokenType.ELSE,
        'end if': TokenType.END_IF,
        'repeat': TokenType.REPEAT,
        'times': TokenType.TIMES_KW,
        'count': TokenType.COUNT,
        'from': TokenType.FROM,
        'to': TokenType.TO_KW,
        'while': TokenType.WHILE,
        'end while': TokenType.END_WHILE,
        'end repeat': TokenType.END_REPEAT,
        'end count': TokenType.END_COUNT,
        'is greater than': TokenType.IS_GREATER_THAN,
        'is less than': TokenType.IS_LESS_THAN,
        'is equal to': TokenType.IS_EQUAL_TO,
        'is not equal to': TokenType.IS_NOT_EQUAL_TO,
        'is not': TokenType.IS_NOT,
        'note:': None,
        'This is a description:': None,
        'ribindulating floxymite': TokenType.RIBINDULATING_FLOXYMITE,
    }

    TOKEN_PATTERNS = [
        (r'\bproduct of\b', TokenType.PRODUCT_OF),
        (r'\bcombined with\b', TokenType.COMBINED_WITH),
        (r'\band store in\b', TokenType.AND_STORE_IN),
        (r'\bdivided by\b', TokenType.DIVIDED_BY),
        (r'\belse if\b', TokenType.ELSE_IF),
        (r'\bend if\b', TokenType.END_IF),
        (r'\bend while\b', TokenType.END_WHILE),
        (r'\bend repeat\b', TokenType.END_REPEAT),
        (r'\bend count\b', TokenType.END_COUNT),
        (r'\bis greater than\b', TokenType.IS_GREATER_THAN),
        (r'\bis less than\b', TokenType.IS_LESS_THAN),
        (r'\bis equal to\b', TokenType.IS_EQUAL_TO),
        (r'\bis not equal to\b', TokenType.IS_NOT_EQUAL_TO),
        (r'\bis not\b', TokenType.IS_NOT),
        (r'\bnote:\b', 'COMMENT_START'),
        (r'\bThis is a description:\b', 'COMMENT_START'),
        (r'\bribindulating floxymite\b', TokenType.RIBINDULATING_FLOXYMITE),
        (r'\bshow\b', TokenType.SHOW),
        (r'\bdisplay\b', TokenType.DISPLAY),
        (r'\btell\b', TokenType.TELL),
        (r'\bset\b', TokenType.SET),
        (r'\bto\b', TokenType.TO),
        (r'\bbecomes\b', TokenType.BECOMES),
        (r'\bis\b', TokenType.IS_KW),
        (r'\bgets\b', TokenType.GETS),
        (r'\bask\b', TokenType.ASK),
        (r'\bget\b', TokenType.GET_KW),
        (r'\binto\b', TokenType.INTO),
        (r'\bread\b', TokenType.READ),
        (r'\bline\b', TokenType.LINE),
        (r'\bfrom\b', TokenType.FROM),
        (r'\bkeyboard\b', TokenType.KEYBOARD),
        (r'\badd\b', TokenType.ADD),
        (r'\bincrease\b', TokenType.INCREASE),
        (r'\bdecrease\b', TokenType.DECREASE),
        (r'\bby\b', TokenType.BY),
        (r'\bcalculate\b', TokenType.CALCULATE),
        (r'\bas\b', TokenType.AS),
        (r'\bplus\b', TokenType.PLUS),
        (r'\bminus\b', TokenType.MINUS),
        (r'\btimes\b', TokenType.TIMES),
        (r'\band\b', TokenType.AND_OP),
        (r'\bif\b', TokenType.IF),
        (r'\bthen\b', TokenType.THEN),
        (r'\belse\b', TokenType.ELSE),
        (r'\brepeat\b', TokenType.REPEAT),
        (r'\btimes\b', TokenType.TIMES_KW),
        (r'\bcount\b', TokenType.COUNT),
        (r'\bwhile\b', TokenType.WHILE),
        (r'(\d+\.\d*|\d+)', TokenType.NUMBER),
        (r'"([^"]*)"', TokenType.STRING),
        (r"'([^']*)'", TokenType.STRING),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
        (r':', TokenType.COLON),
        (r'\n', TokenType.NEWLINE),
        (r'\s+', None),
    ]

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = self._tokenize()

    def _tokenize(self):
        tokens = []
        text_length = len(self.text)

        while self.pos < text_length:
            match = None
            if self.text[self.pos:].startswith('note:') or self.text[self.pos:].startswith('This is a description:'):
                newline_pos = self.text.find('\n', self.pos)
                if newline_pos == -1:
                    self.pos = text_length
                else:
                    self.column += (newline_pos - self.pos)
                    self.pos = newline_pos + 1
                    self.line += 1
                    self.column = 1
                continue

            for pattern_regex, token_type in self.TOKEN_PATTERNS:
                match = re.match(pattern_regex, self.text[self.pos:], re.IGNORECASE)
                if match:
                    value = match.group(0)
                    if token_type is not None:
                        if token_type == TokenType.STRING:
                            value = value[1:-1]
                        tokens.append(Token(token_type, value, self.line, self.column))
                    
                    lines_traversed = value.count('\n')
                    if lines_traversed > 0:
                        self.line += lines_traversed
                        self.column = len(value) - value.rfind('\n')
                    else:
                        self.column += len(value)
                    self.pos += len(value)
                    break

            if not match:
                raise LexerError(f"Unexpected character: '{self.text[self.pos]}'", self.line, self.column)

        tokens.append(Token(TokenType.EOF, 'EOF', self.line, self.column))
        return tokens

    def get_tokens(self):
        return self.tokens

class ASTNode:
    def __init__(self, token):
        self.token = token

class ProgramNode(ASTNode):
    def __init__(self, statements):
        super().__init__(None)
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

class PrintNode(ASTNode):
    def __init__(self, token, expressions):
        super().__init__(token)
        self.expressions = expressions

    def __repr__(self):
        return f"PrintNode(expressions={self.expressions})"

class AssignmentNode(ASTNode):
    def __init__(self, token, identifier, value_expression):
        super().__init__(token)
        self.identifier = identifier
        self.value_expression = value_expression

    def __repr__(self):
        return f"AssignmentNode(id={self.identifier}, value={self.value_expression})"

class InputNode(ASTNode):
    def __init__(self, token, prompt_expression, identifier):
        super().__init__(token)
        self.prompt_expression = prompt_expression
        self.identifier = identifier

    def __repr__(self):
        return f"InputNode(prompt={self.prompt_expression}, id={self.identifier})"

class EasterEggNode(ASTNode):
    def __init__(self, token):
        super().__init>(token)

    def __repr__(self):
        return f"EasterEggNode()"

class BinaryOpNode(ASTNode):
    def __init__(self, token, left, op, right):
        super().__init__(token)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op.value} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, token, op, identifier, value_expression=None):
        super().__init__(token)
        self.op = op
        self.identifier = identifier
        self.value_expression = value_expression

    def __repr__(self):
        return f"UnaryOpNode({self.op.value} {self.identifier} by {self.value_expression})"

class IfNode(ASTNode):
    def __init__(self, token, condition, then_statements, else_if_branches=None, else_statements=None):
        super().__init__(token)
        self.condition = condition
        self.then_statements = then_statements
        self.else_if_branches = else_if_branches if else_if_branches is not None else []
        self.else_statements = else_statements if else_statements is not None else []

    def __repr__(self):
        return (f"IfNode(condition={self.condition}, then={self.then_statements}, "
                f"else_if={self.else_if_branches}, else={self.else_statements})")

class RepeatLoopNode(ASTNode):
    def __init__(self, token, count_expression, statements):
        super().__init__(token)
        self.count_expression = count_expression
        self.statements = statements

    def __repr__(self):
        return f"RepeatLoopNode(count={self.count_expression}, statements={self.statements})"

class CountLoopNode(ASTNode):
    def __init__(self, token, identifier, start_expression, end_expression, statements):
        super().__init__(token)
        self.identifier = identifier
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.statements = statements

    def __repr__(self):
        return (f"CountLoopNode(id={self.identifier}, start={self.start_expression}, "
                f"end={self.end_expression}, statements={self.statements})")

class WhileLoopNode(ASTNode):
    def __init__(self, token, condition, statements):
        super().__init__(token)
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"WhileLoopNode(condition={self.condition}, statements={self.statements})"

class NumberNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = float(token.value) if '.' in token.value else int(token.value)

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = str(token.value)

    def __repr__(self):
        return f"StringNode('{self.value}')"

class IdentifierNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.name = token.value

    def __repr__(self):
        return f"IdentifierNode('{self.name}')"

class ParserError(Exception):
    def __init__(self, message, token):
        super().__init__(f"Parsing Error at line {token.line}, column {token.column}: {message} (Found '{token.value}')")
        self.token = token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def _advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token(TokenType.EOF, 'EOF', self.current_token.line, self.current_token.column)

    def _eat(self, *expected_types):
        if self.current_token.type in expected_types:
            token = self.current_token
            self._advance()
            return token
        else:
            expected_str = ', '.join(t.value for t in expected_types) if expected_types else "some token"
            raise ParserError(f"Expected one of {expected_str}, but found '{self.current_token.value}'", self.current_token)

    def _peek(self, offset=1):
        if self.current_token_index + offset < len(self.tokens):
            return self.tokens[self.current_token_index + offset]
        return Token(TokenType.EOF, 'EOF', self.current_token.line, self.current_token.column)

    def _expression(self):
        if self.current_token.type == TokenType.CALCULATE:
            calc_token = self._eat(TokenType.CALCULATE)
            identifier = self._eat(TokenType.IDENTIFIER)
            self._eat(TokenType.AS)
            expr = self._parse_compound_expression()
            return AssignmentNode(calc_token, IdentifierNode(identifier), expr)

        if self.current_token.type == TokenType.PRODUCT_OF:
            op_token = self._eat(TokenType.PRODUCT_OF)
            left = self._factor()
            self._eat(TokenType.AND_OP)
            right = self._factor()
            return BinaryOpNode(op_token, left, TokenType.TIMES, right)
        
        if self.current_token.type == TokenType.IDENTIFIER or self.current_token.type == TokenType.NUMBER:
            temp_index = self.current_token_index
            temp_token = self.current_token
            left_expr = self._factor()
            if self.current_token.type == TokenType.DIVIDED_BY:
                op_token = self._eat(TokenType.DIVIDED_BY)
                right_expr = self._factor()
                return BinaryOpNode(op_token, left_expr, TokenType.DIVIDED_BY, right_expr)
            else:
                self.current_token_index = temp_index
                self.current_token = temp_token
                return self._factor()

        left = self._factor()
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES]:
            op_token = self.current_token
            if op_token.type == TokenType.PLUS:
                self._eat(TokenType.PLUS)
            elif op_token.type == TokenType.MINUS:
                self._eat(TokenType.MINUS)
            elif op_token.type == TokenType.TIMES:
                self._eat(TokenType.TIMES)
            right = self._factor()
            left = BinaryOpNode(op_token, left, op_token.type, right)
        return left

    def _factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self._eat(TokenType.NUMBER)
            return NumberNode(token)
        elif token.type == TokenType.STRING:
            self._eat(TokenType.STRING)
            return StringNode(token)
        elif token.type == TokenType.IDENTIFIER:
            self._eat(TokenType.IDENTIFIER)
            return IdentifierNode(token)
        else:
            raise ParserError(f"Expected a number, string, or identifier for expression, but found '{token.value}'", token)

    def _parse_compound_expression(self):
        left = self._factor()
        
        while self.current_token.type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDED_BY
        ]:
            op_token = self.current_token
            if op_token.type == TokenType.PLUS: self._eat(TokenType.PLUS)
            elif op_token.type == TokenType.MINUS: self._eat(TokenType.MINUS)
            elif op_token.type == TokenType.TIMES: self._eat(TokenType.TIMES)
            elif op_token.type == TokenType.DIVIDED_BY: self._eat(TokenType.DIVIDED_BY)
            
            right = self._factor()
            left = BinaryOpNode(op_token, left, op_token.type, right)
            
        return left

    def _comparison_expression(self):
        left = self._expression()

        if self.current_token.type in [
            TokenType.IS_GREATER_THAN, TokenType.IS_LESS_THAN,
            TokenType.IS_EQUAL_TO, TokenType.IS_NOT_EQUAL_TO, TokenType.IS_NOT
        ]:
            op_token = self.current_token
            op_type = op_token.type
            if op_type == TokenType.IS_GREATER_THAN: self._eat(TokenType.IS_GREATER_THAN)
            elif op_type == TokenType.IS_LESS_THAN: self._eat(TokenType.IS_LESS_THAN)
            elif op_type == TokenType.IS_EQUAL_TO: self._eat(TokenType.IS_EQUAL_TO)
            elif op_type == TokenType.IS_NOT_EQUAL_TO: self._eat(TokenType.IS_NOT_EQUAL_TO)
            elif op_type == TokenType.IS_NOT: self._eat(TokenType.IS_NOT)
            
            right = self._expression()
            return BinaryOpNode(op_token, left, op_type, right)
        else:
            return left
            
    def _parse_print_statement(self):
        initial_token_type = self.current_token.type
        print_token = self._eat(TokenType.SHOW, TokenType.DISPLAY, TokenType.TELL)
        
        expressions = []
        
        while self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.EOF:
            if expressions and self.current_token.type == TokenType.COMBINED_WITH:
                self._eat(TokenType.COMBINED_WITH)
            
            expressions.append(self._expression())

        return PrintNode(print_token, expressions)

    def _parse_assignment_statement(self):
        if self.current_token.type == TokenType.SET:
            set_token = self._eat(TokenType.SET)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            self._eat(TokenType.TO)
            value_expr = self._expression()
            return AssignmentNode(set_token, IdentifierNode(identifier_token), value_expr)
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            identifier_token = self.current_token
            peek_token = self._peek()
            if peek_token.type in [TokenType.BECOMES, TokenType.IS_KW, TokenType.GETS]:
                self._eat(TokenType.IDENTIFIER)
                op_token = self._eat(TokenType.BECOMES, TokenType.IS_KW, TokenType.GETS)
                value_expr = self._expression()
                return AssignmentNode(op_token, IdentifierNode(identifier_token), value_expr)
            else:
                pass

        raise ParserError(f"Expected an assignment statement, but found '{self.current_token.value}'", self.current_token)

    def _parse_input_statement(self):
        initial_token = self.current_token
        
        if initial_token.type == TokenType.ASK:
            self._eat(TokenType.ASK)
            prompt_expr = self._expression()
            self._eat(TokenType.AND_STORE_IN)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            return InputNode(initial_token, prompt_expr, IdentifierNode(identifier_token))
        
        elif initial_token.type == TokenType.GET_KW:
            self._eat(TokenType.GET_KW)
            if self.current_token.type == TokenType.NUMBER:
                 self._eat(TokenType.NUMBER)
            
            self._eat(TokenType.INTO)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            return InputNode(initial_token, None, IdentifierNode(identifier_token))
            
        elif initial_token.type == TokenType.READ:
            self._eat(TokenType.READ)
            self._eat(TokenType.LINE)
            self._eat(TokenType.FROM)
            self._eat(TokenType.KEYBOARD)
            self._eat(TokenType.INTO)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            return InputNode(initial_token, None, IdentifierNode(identifier_token))

        raise ParserError(f"Expected an input statement, but found '{self.current_token.value}'", self.current_token)
        
    def _parse_arithmetic_statement(self):
        initial_token = self.current_token

        if initial_token.type == TokenType.ADD:
            self._eat(TokenType.ADD)
            value_expr = self._expression()
            self._eat(TokenType.TO)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            return BinaryOpNode(initial_token, IdentifierNode(identifier_token), TokenType.ADD, value_expr)
        
        elif initial_token.type == TokenType.INCREASE:
            self._eat(TokenType.INCREASE)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            self._eat(TokenType.BY)
            value_expr = self._expression()
            return UnaryOpNode(initial_token, TokenType.INCREASE, IdentifierNode(identifier_token), value_expr)
            
        elif initial_token.type == TokenType.DECREASE:
            self._eat(TokenType.DECREASE)
            identifier_token = self._eat(TokenType.IDENTIFIER)
            self._eat(TokenType.BY)
            value_expr = self._expression()
            return UnaryOpNode(initial_token, TokenType.DECREASE, IdentifierNode(identifier_token), value_expr)
        
        raise ParserError(f"Expected an arithmetic statement, but found '{self.current_token.value}'", self.current_token)

    def _block(self, end_token_type):
        statements = []
        self._eat(TokenType.NEWLINE)
        
        while self.current_token.type != end_token_type and self.current_token.type != TokenType.EOF:
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
            while self.current_token.type == TokenType.NEWLINE:
                self._eat(TokenType.NEWLINE)
        return statements

    def _parse_easter_egg_statement(self):
        egg_token = self._eat(TokenType.RIBINDULATING_FLOXYMITE)
        return EasterEggNode(egg_token)

    def _parse_if_statement(self):
        if_token = self._eat(TokenType.IF)
        condition = self._comparison_expression()
        self._eat(TokenType.THEN)
        self._eat(TokenType.COLON)
        
        then_statements = self._block(TokenType.END_IF)
        
        else_if_branches = []
        while self.current_token.type == TokenType.ELSE_IF:
            self._eat(TokenType.ELSE_IF)
            else_if_condition = self._comparison_expression()
            self._eat(TokenType.THEN)
            self._eat(TokenType.COLON)
            else_if_statements = self._block(TokenType.END_IF)
            else_if_branches.append((else_if_condition, else_if_statements))
        
        else_statements = []
        if self.current_token.type == TokenType.ELSE:
            self._eat(TokenType.ELSE)
            self._eat(TokenType.COLON)
            else_statements = self._block(TokenType.END_IF)
            
        self._eat(TokenType.END_IF)
        
        return IfNode(if_token, condition, then_statements, else_if_branches, else_statements)

    def _parse_repeat_loop(self):
        repeat_token = self._eat(TokenType.REPEAT)
        count_expr = self._expression()
        self._eat(TokenType.TIMES_KW)
        self._eat(TokenType.COLON)
        
        statements = self._block(TokenType.END_REPEAT)
        self._eat(TokenType.END_REPEAT)
        return RepeatLoopNode(repeat_token, count_expr, statements)

    def _parse_count_loop(self):
        count_token = self._eat(TokenType.COUNT)
        self._eat(TokenType.FROM)
        start_expr = self._expression()
        self._eat(TokenType.TO_KW)
        end_expr = self._expression()
        self._eat(TokenType.AS)
        identifier_token = self._eat(TokenType.IDENTIFIER)
        self._eat(TokenType.COLON)

        statements = self._block(TokenType.END_COUNT)
        self._eat(TokenType.END_COUNT)
        return CountLoopNode(count_token, IdentifierNode(identifier_token), start_expr, end_expr, statements)

    def _parse_while_loop(self):
        while_token = self._eat(TokenType.WHILE)
        condition = self._comparison_expression()
        self._eat(TokenType.COLON)

        statements = self._block(TokenType.END_WHILE)
        self._eat(TokenType.END_WHILE)
        return WhileLoopNode(while_token, condition, statements)

    def _statement(self):
        token_type = self.current_token.type
        
        while token_type == TokenType.NEWLINE:
            self._eat(TokenType.NEWLINE)
            token_type = self.current_token.type

        if token_type == TokenType.SHOW or token_type == TokenType.DISPLAY or token_type == TokenType.TELL:
            stmt = self._parse_print_statement()
        elif token_type == TokenType.SET or \
             (token_type == TokenType.IDENTIFIER and self._peek().type in [TokenType.BECOMES, TokenType.IS_KW, TokenType.GETS]):
            stmt = self._parse_assignment_statement()
        elif token_type == TokenType.ASK or token_type == TokenType.GET_KW or token_type == TokenType.READ:
            stmt = self._parse_input_statement()
        elif token_type == TokenType.ADD or token_type == TokenType.INCREASE or token_type == TokenType.DECREASE:
            stmt = self._parse_arithmetic_statement()
        elif token_type == TokenType.IF:
            stmt = self._parse_if_statement()
        elif token_type == TokenType.REPEAT:
            stmt = self._parse_repeat_loop()
        elif token_type == TokenType.COUNT:
            stmt = self._parse_count_loop()
        elif token_type == TokenType.WHILE:
            stmt = self._parse_while_loop()
        elif token_type == TokenType.CALCULATE:
            stmt = self._expression()
            if not isinstance(stmt, AssignmentNode):
                 raise ParserError(f"Expected 'calculate ... as ...' statement, but parse resulted in {stmt}", self.current_token)
        elif token_type == TokenType.RIBINDULATING_FLOXYMITE:
            stmt = self._parse_easter_egg_statement()
        elif token_type == TokenType.EOF:
            return None
        else:
            raise ParserError(f"Unexpected token type for start of statement: '{self.current_token.type}' ('{self.current_token.value}')", self.current_token)
        
        if self.current_token.type == TokenType.NEWLINE:
            self._eat(TokenType.NEWLINE)

        return stmt

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

class InterpreterError(Exception):
    def __init__(self, message, node=None):
        line = node.token.line if node and node.token else "unknown"
        col = node.token.column if node and node.token else "unknown"
        super().__init__(f"Runtime Error at line {line}, column {col}: {message}")
        self.node = node

class Interpreter:
    def __init__(self):
        self.variables = {}

    def _get_value(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            if node.name not in self.variables:
                raise InterpreterError(f"Variable '{node.name}' is not defined.", node)
            return self.variables[node.name]
        elif isinstance(node, BinaryOpNode):
            return self.visit_BinaryOpNode(node)
        else:
            raise InterpreterError(f"Cannot get value from unsupported node type: {type(node).__name__}", node)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise InterpreterError(f"No visit_{type(node).__name__} method for node type.", node)

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_PrintNode(self, node):
        output_parts = []
        for expr in node.expressions:
            value = self._get_value(expr)
            output_parts.append(str(value))
        print("".join(output_parts))

    def visit_AssignmentNode(self, node):
        var_name = node.identifier.name
        value = self._get_value(node.value_expression)
        self.variables[var_name] = value

    def visit_EasterEggNode(self, node):
        print("Aha! You found the secret! A ribindulating floxymite is something I put here for you to find - it is like the Sampo from the Kalevala. You'd never know it was a bowl, or a ring, or a sword, or the answer to life. Keep practicing phrase_lang - it will tell you the answer to what this is!!!")

    def visit_InputNode(self, node):
        prompt = self._get_value(node.prompt_expression) if node.prompt_expression else ""
        user_input = input(str(prompt))
        var_name = node.identifier.name
        try:
            self.variables[var_name] = float(user_input) if '.' in user_input else int(user_input)
        except ValueError:
            self.variables[var_name] = user_input

    def visit_BinaryOpNode(self, node):
        left_val = self._get_value(node.left)
        right_val = self._get_value(node.right)

        if node.op == TokenType.PLUS:
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val + right_val
            elif isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            else:
                raise InterpreterError(f"Unsupported types for 'plus' operation: {type(left_val).__name__} and {type(right_val).__name__}", node)
        elif node.op == TokenType.MINUS:
            return left_val - right_val
        elif node.op == TokenType.TIMES:
            return left_val * right_val
        elif node.op == TokenType.DIVIDED_BY:
            if right_val == 0:
                raise InterpreterError("Cannot divide by zero.", node)
            return left_val / right_val
        elif node.op == TokenType.ADD:
            if not isinstance(node.left, IdentifierNode):
                raise InterpreterError(f"Expected variable for 'add ... to ...', but found {type(node.left).__name__}", node)
            var_name = node.left.name
            if var_name not in self.variables:
                raise InterpreterError(f"Variable '{var_name}' is not defined.", node.left)
            self.variables[var_name] += right_val
            return None
        
        elif node.op == TokenType.IS_GREATER_THAN:
            return left_val > right_val
        elif node.op == TokenType.IS_LESS_THAN:
            return left_val < right_val
        elif node.op == TokenType.IS_EQUAL_TO:
            return left_val == right_val
        elif node.op == TokenType.IS_NOT_EQUAL_TO:
            return left_val != right_val
        elif node.op == TokenType.IS_NOT:
            return left_val != right_val
        else:
            raise InterpreterError(f"Unknown binary operator: {node.op}", node)

    def visit_UnaryOpNode(self, node):
        if not isinstance(node.identifier, IdentifierNode):
            raise InterpreterError(f"Expected a variable for '{node.op.value}' operation, but found {type(node.identifier).__name__}", node.identifier)
        
        var_name = node.identifier.name
        if var_name not in self.variables:
            raise InterpreterError(f"Variable '{var_name}' is not defined.", node.identifier)
        
        value_to_change_by = self._get_value(node.value_expression)
        
        if node.op == TokenType.INCREASE:
            self.variables[var_name] += value_to_change_by
        elif node.op == TokenType.DECREASE:
            self.variables[var_name] -= value_to_change_by
        else:
            raise InterpreterError(f"Unknown unary operator: {node.op}", node)

    def visit_IfNode(self, node):
        if self._get_value(node.condition):
            for statement in node.then_statements:
                self.visit(statement)
        else:
            executed_else_if = False
            for cond, statements in node.else_if_branches:
                if self._get_value(cond):
                    for statement in statements:
                        self.visit(statement)
                    executed_else_if = True
                    break
            
            if not executed_else_if and node.else_statements:
                for statement in node.else_statements:
                    self.visit(statement)

    def visit_RepeatLoopNode(self, node):
        count = int(self._get_value(node.count_expression))
        for _ in range(count):
            for statement in node.statements:
                self.visit(statement)

    def visit_CountLoopNode(self, node):
        var_name = node.identifier.name
        start = int(self._get_value(node.start_expression))
        end = int(self._get_value(node.end_expression))

        for i in range(start, end + 1):
            self.variables[var_name] = i
            for statement in node.statements:
                self.visit(statement)

    def visit_WhileLoopNode(self, node):
        while self._get_value(node.condition):
            for statement in node.statements:
                self.visit(statement)

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_IdentifierNode(self, node):
        return self._get_value(node)

def interpret(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.get_tokens()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        interpreter.visit(ast)
        return interpreter.variables
    except (LexerError, ParserError, InterpreterError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}

def repl():
    print("Welcome to Phrase Lang REPL!")
    print("Type your commands. Type 'exit' to quit.")
    
    interpreter = Interpreter()

    while True:
        try:
            line = input("> ")
            if line.strip().lower() == 'exit':
                break
            if not line.strip():
                continue

            lexer = Lexer(line + '\n')
            tokens = lexer.get_tokens()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            interpreter.visit(ast)

        except (LexerError, ParserError, InterpreterError) as e:
            print(f"Error: {e}", file=sys.stderr)
        except EOFError:
            print("\nExiting Phrase Lang REPL.")
            break
