# cqql/parser.py
# -------------------------------------------------
# Recursive-descent parser for CQQL formulas.
# Grammar (precedence):
#   expr    := or_expr
#   or_expr := and_expr ('|' and_expr)*
#   and_expr:= unary ('&' unary)*
#   unary   := '!' unary | primary
#   primary := ATOM | '(' expr ')' | WAND(...) | WOR(...)
#
# Weighted forms:
#   WAND(theta1,theta2, expr, expr)
#   WOR(theta1,theta2, expr, expr)
# -------------------------------------------------

from dataclasses import dataclass
from typing import List, Optional

from cqql.ast import Atom, Not, And, Or, WeightedAnd, WeightedOr, Formula


# ----------------------------
# Tokenizer
# ----------------------------
@dataclass
class Token:
    kind: str   # 'ATOM', 'OP', 'LPAREN', 'RPAREN', 'COMMA', 'EOF'
    value: str


def tokenize(s: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(s)

    def is_ident_char(ch: str) -> bool:
        return ch.isalnum() or ch == "_"

    while i < n:
        ch = s[i]

        if ch.isspace():
            i += 1
            continue

        if ch in ("&", "|", "!"):
            tokens.append(Token("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(Token("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(Token("RPAREN", ch))
            i += 1
            continue

        if ch == ",":
            tokens.append(Token("COMMA", ch))
            i += 1
            continue

        # identifier: ATOM / function name (WAND/WOR)
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and is_ident_char(s[j]):
                j += 1
            ident = s[i:j]
            tokens.append(Token("ATOM", ident))
            i = j
            continue

        raise ValueError(f"Unexpected character '{ch}' at position {i}")

    tokens.append(Token("EOF", ""))
    return tokens


# ----------------------------
# Parser
# ----------------------------
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, kind: str, value: Optional[str] = None) -> Token:
        tok = self.peek()
        if tok.kind != kind:
            raise ValueError(f"Expected token kind {kind}, got {tok.kind} ('{tok.value}')")
        if value is not None and tok.value != value:
            raise ValueError(f"Expected token '{value}', got '{tok.value}'")
        self.pos += 1
        return tok

    def match(self, kind: str, value: Optional[str] = None) -> bool:
        tok = self.peek()
        if tok.kind != kind:
            return False
        if value is not None and tok.value != value:
            return False
        self.pos += 1
        return True

    # expr := or_expr
    def parse(self) -> Formula:
        expr = self.parse_or()
        self.consume("EOF")
        return expr

    # or_expr := and_expr ('|' and_expr)*
    def parse_or(self) -> Formula:
        left = self.parse_and()
        while self.match("OP", "|"):
            right = self.parse_and()
            left = Or(left, right)
        return left

    # and_expr := unary ('&' unary)*
    def parse_and(self) -> Formula:
        left = self.parse_unary()
        while self.match("OP", "&"):
            right = self.parse_unary()
            left = And(left, right)
        return left

    # unary := '!' unary | primary
    def parse_unary(self) -> Formula:
        if self.match("OP", "!"):
            return Not(self.parse_unary())
        return self.parse_primary()

    # primary := ATOM | '(' expr ')' | WAND(...) | WOR(...)
    def parse_primary(self) -> Formula:
        tok = self.peek()

        # parenthesized expression
        if self.match("LPAREN"):
            e = self.parse_or()
            self.consume("RPAREN")
            return e

        # must start with ATOM token (either identifier or WAND/WOR)
        if tok.kind == "ATOM":
            ident = self.consume("ATOM").value

            # function call?
            if ident in ("WAND", "WOR") and self.match("LPAREN"):
                theta1 = self.consume("ATOM").value
                self.consume("COMMA")
                theta2 = self.consume("ATOM").value
                self.consume("COMMA")
                left = self.parse_or()
                self.consume("COMMA")
                right = self.parse_or()
                self.consume("RPAREN")

                if ident == "WAND":
                    return WeightedAnd(theta1, theta2, left, right)
                else:
                    return WeightedOr(theta1, theta2, left, right)

            # plain atom
            return Atom(ident)

        raise ValueError(f"Unexpected token {tok.kind} ('{tok.value}') at position {self.pos}")


def parse_formula(text: str) -> Formula:
    return Parser(tokenize(text)).parse()
