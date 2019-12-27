import re
import queue
from math import fmod

class Calculator:
    """
    A simple calculator class
    Parses a string expression and extracts operations and operands using re.
    Since it does not use an expression tree, only simple expressions are sup-
    ported.
    
    Supports the following arithmetic operations:
        +, -, *, /, ^, mod
    
    Other supported commands:
        store, recall, clear
    """
    
    # TODO: improve regular expressions so that they deal with signed numbers
    # TODO: add more functions (e.g. log, sqrt)
    
    def __init__(self):
        self.operators = queue.SimpleQueue()
        self.operands = queue.SimpleQueue()
        self.operators_pattern = r'[%*/+^-]|mod'
        self.operands_pattern = r'\d+\.?\d*'
        self.valid_expr_pattern = r'^\s*(\d+\.?\d*)(?:\s*([-%+^*/]|mod)\s*(\d+\.?\d*)\s*)+$|store|recall|clear|help'
        self.operators_re = re.compile(self.operators_pattern)
        self.operands_re = re.compile(self.operands_pattern)
        self.valid_expr_re = re.compile(self.valid_expr_pattern, re.I)
        self.calc_result = 0.0
        self.calc_memory = 0.0

    def extract_operands(self, expr) -> None:
        for op in re.findall(self.operands_re, expr):
            self.operands.put(float(op))
    
    def extract_operators(self, expr) -> None:
        for op in re.findall(self.operators_pattern, expr):
            self.operators.put(op)
            
    def reset(self) -> None:
        while not self.operands.empty():
            self.operands.get()
        while not self.operators.empty():
            self.operators.get()
        self.calc_result = 0.0
    
    def calculate(self, expr) -> float:
        self.extract_operands(expr)
        self.extract_operators(expr)
        
        self.calc_result = self.operands.get()
        
        while not self.operators.empty():
            op = self.operators.get()
            b = self.operands.get()
            
            if op == '+':
                self.calc_result += b
            elif op == '-':
                self.calc_result -= b
            elif op == '*':
                self.calc_result *= b
            elif op == '/':
                if b != 0:
                    self.calc_result /= b
                else:
                    self.clear()
                    raise ZeroDivisionError("Division by zero")
            elif op == '^':
                self.calc_result **= b
            elif op == '%' or op == 'mod':
                if b != 0:
                    self.calc_result = fmod(self.calc_result, b);
                else:
                    self.clear()
                    raise ValueError("Modulo 0 is not defined")
                        
        return self.calc_result
    
    def is_valid_expression(self, expr) -> bool:
        return re.fullmatch(self.valid_expr_re, expr) != None
    
    def store(self) -> None:
        self.calc_memory = self.calc_result
    
    def recall(self) -> float:
        return self.calc_memory
    
    def clear(self) -> None:
        self.calc_memory = 0.0
    
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