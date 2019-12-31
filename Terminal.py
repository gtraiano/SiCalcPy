from Calculator import Calculator

class Terminal:
    """
    A terminal for the Calculator class
    """
    def __init__(self):
        self._input = ""
        self._calc = Calculator()

    def main(self):
        while True:
            self._input = input("> ").lower()
            
            if self._input == "exit":
                break
            
            if not self._calc.is_valid_expression(self._input):
                print("Invalid _input")
            
            else:
                try:
                    if self._input == "store":
                        self._calc.store()
                        print("Stored", self._calc.recall())
                    
                    elif self._input == "recall":
                        print("Recalled", self._calc.recall())
                        print("> ", self._calc.recall(), sep = "", end = "")
                        self._input = "" # empty _input
                        self._input = str(self._calc.recall()) + input().lower() # attach recall value, then user input
                        
                        if not self._calc.is_valid_expression(self._input):
                            print("Invalid _input")
                            continue
                        
                        print(self._input, "=", self._calc.calculate(self._input))
                        
                    elif self._input == "clear":
                        self._calc.clear()
                        print("Cleared")
                    
                    elif self._input == "help":
                        self._calc.help()
                    
                    else:
                        print(self._input, "=", self._calc.calculate(self._input))
                
                except (ZeroDivisionError, ValueError) as e:
                    print(e)
                

if __name__ == '__main__':
    t = Terminal()
    t.main()