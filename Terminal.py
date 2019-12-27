from Calculator import Calculator

class Terminal:
    """
    A terminal for the Calculator class
    """
    def __init__(self):
        self.input = ""
        self.calc = Calculator()

    def main(self):
        while True:
            self.input = input("> ").lower()
            
            if self.input == "exit":
                break
            
            if not self.calc.is_valid_expression(self.input):
                print("Invalid input")
            else:
                try:
                    if self.input == "store":
                        self.calc.store()
                        print("Stored", self.calc.recall())
                    
                    elif self.input == "recall":
                        print("Recalled", self.calc.recall())
                        print("> ", self.calc.recall(), sep = "", end = "")
                        self.input = ""
                        self.input = str(self.calc.recall()) + input().lower()
                        if not self.calc.is_valid_expression(self.input):
                            print(self.input)
                            print("Invalid input")
                            continue
                        print(self.input, "=", self.calc.calculate(self.input))
                        
                    elif self.input == "clear":
                        self.calc.clear()
                        print("Cleared")
                    
                    elif self.input == "help":
                        self.calc.help()
                    
                    else:
                        print(self.input, "=", self.calc.calculate(self.input))
                
                except (ZeroDivisionError, ValueError) as e:
                    print(e)
                

if __name__ == '__main__':
    t = Terminal()
    t.main()