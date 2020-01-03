import re
import queue
#from math import fmod
import math

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
    
    # TODO: include sqrt and log in complex expressions (not only stand-alone)
    
    def __init__(self):
        self._operators = queue.SimpleQueue()
        self._operands = queue.SimpleQueue()
        
        self._operators_pattern = r'(?<=\d)(?:[-+*/%^]|mod)|sqrt|log'
        self._operands_pattern = r'(?<!\d)-?\d+\.?\d*'
        self._valid_expr_pattern = r'^\s*((?<!\d)-?\d+\.?\d*)(?:\s*((?<=\d|\s)[-+*/%^]|mod)\s*((?<!\d)-?\d+\.?\d*)\s*)+$|^\s*(?:(sqrt|log)\s*((?<!\d)-?\d+\.?\d*))\s*$|store|recall|clear|help'
        
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
        # Issues to be aware of:
        # 1. Strip spaces from input before extracting operators and operands,
        #    makes operators re work properly in all cases
        #
        # 2. If dealing with sqrt or log expression, watch out for empty operands
        #    queue
        
        stripped_expr = "".join(expr.split()) # strip spaces from expr
        self._extract_operands(stripped_expr)
        self._extract_operators(stripped_expr)
        
        self._calc_result = self._operands.get()
        
        while not self._operators.empty():
            op = self._operators.get()
            try:
                b = self._operands.get(block=False)
            except queue.Empty: # for sqrt and log, operands is already empty
                pass
            
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
                    self._calc_result = math.fmod(self._calc_result, b);
                else:
                    self._reset()
                    raise ValueError("Modulo 0 is not defined")
            elif op == "sqrt":
                if self._calc_result >= 0:
                    self._calc_result = math.sqrt(self._calc_result)
                else:
                    raise ValueError('Square root of negative number is not defined')
            elif op == "log":
                if self._calc_result > 0:
                    self._calc_result = math.log10(self._calc_result)
                else:
                    raise ValueError('Logarithm of negative number is not defined')
                    
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
            sqrt : Square root
            log : Logarithm base 10
            
            Available commands
            store : Store result in memory
            recall: Recall from memory
            clear : Clear memory
        """)