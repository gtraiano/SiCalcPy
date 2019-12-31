import re
import queue
from math import fmod

class Calculator:
    """
    A simple calculator class
    Parses a string expression and extracts operations and _operands using re.
    Since it does not use an expression tree, only simple expressions are sup-
    ported.
    
    Supports the following arithmetic operations:
        +, -, *, /, ^, mod
    
    Other supported commands:
        store, recall, clear
    """
    
    # TODO: add more functions (e.g. log, sqrt)
    
    def __init__(self):
        self._operators = queue.SimpleQueue()
        self._operands = queue.SimpleQueue()
        
        self._operators_pattern = r'(?<=\d)(?:[-+*/%]|mod)'
        self._operands_pattern = r'(?<!\d)-?\d+\.?\d*'
        self._valid_expr_pattern = r'^\s*((?<!\d)-?\d+\.?\d*)(?:\s*((?<=\d|\s)[-+*/%]|mod)\s*((?<!\d)-?\d+\.?\d*)\s*)+$|store|recall|clear|help'
        
        self._operators_re = re.compile(self._operators_pattern)
        self._operands_re = re.compile(self._operands_pattern)
        self._valid_expr_re = re.compile(self._valid_expr_pattern, re.I)
        
        self._calc_result = 0.0
        self._calc_memory = 0.0

    def _extract_operands(self, expr: str) -> None:
        for op in re.findall(self._operands_re, expr):
            self._operands.put(float(op))
    
    def _extract_operators(self, expr: str) -> None:
        for op in re.findall(self._operators_pattern, expr):
            self._operators.put(op)
            
    def _reset(self) -> None:
        while not self._operands.empty():
            self._operands.get()
        while not self._operators.empty():
            self._operators.get()
        self._calc_result = 0.0
    
    def calculate(self, expr: str) -> float:
        stripped_expr = "".join(expr.split()) # strip spaces from expr
        self._extract_operands(stripped_expr)
        self._extract_operators(stripped_expr)
        
        self._calc_result = self._operands.get()
        
        while not self._operators.empty():
            op = self._operators.get()
            b = self._operands.get()
            
            if op == '+':
                self._calc_result += b
            elif op == '-':
                self._calc_result -= b
            elif op == '*':
                self._calc_result *= b
            elif op == '/':
                if b != 0:
                    self._calc_result /= b
                else:
                    self._reset()
                    raise ZeroDivisionError("Division by zero")
            elif op == '^':
                self._calc_result **= b
            elif op == '%' or op == 'mod':
                if b != 0:
                    self._calc_result = fmod(self._calc_result, b);
                else:
                    self._reset()
                    raise ValueError("Modulo 0 is not defined")
                    
        return self._calc_result
    
    def is_valid_expression(self, expr: str) -> bool:
        return re.fullmatch(self._valid_expr_re, expr) != None
    
    def store(self) -> None:
        self._calc_memory = self._calc_result
    
    def recall(self) -> float:
        return self._calc_memory
    
    def clear(self) -> None:
        self._calc_memory = 0.0
    
    def help(self) -> None:
        print("""
            Available operations
            + : Addition
            - : Subtraction
            * : Multiplication
            / : Division
            % or mod : Modulo
            ^ : Power
            
            Available commands
            store : Store result in memory
            recall: Recall from memory
            clear : Clear memory
        """)