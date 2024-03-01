import re

class PredictiveParser:
    def __init__(self):
        self.stack = []
        self.input = []
        self.table = {
            ('S', 'LLAVE'): ['I', 'M', 'A', 'F'],
            ('A', 'PUNCOM'): ['PUNCOM', 'M', 'A'],
            ('A', 'CLLAVE'): ['epsilon'],
            ('M', 'PLAY'): ['D', 'PAAP', 'C', 'PACI'],
            ('D', 'PLAY'): ['PLAY'],
            ('C', 'COMI'): ['COMI', 'T', 'COMI'],
            ('I', 'LLAVE'): ['LLAVE'], 
            ('F', 'CLLAVE'): ['CLLAVE'],
            ('T', 'PLETRA'): ['L', 'R'],
            ('L', 'PLETRA'):['PLETRA'],
            ('R', 'L'): ['L', 'R'],
            ('R', 'COMI'): ['epsilon'],
            }
        
        
        
    def parse(self, tokens):
        self.tokens = tokens
        self.stack = ['$', 'S']  # Asume que 'FUNCION' es el símbolo inicial
        self.cursor = 0
        output = []
        
        
        while self.stack:
            # print(f"Pila: {self.stack}, Token actual: {self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'}")
            print(f"Pila: {self.stack}")
            output.append("Pila: " + str(self.stack[:]))
            top = self.stack[-1]  # Mira el elemento superior de la pila sin desapilarlo
            current_token = self.tokens[self.cursor][0] if self.cursor < len(self.tokens) else '$'
            
            if top == current_token:  # Coincidencia con un terminal
                self.stack.pop()  # Desapila solo si hay una coincidencia
                self.cursor += 1
            elif (top, current_token) in self.table:
                self.stack.pop()  # Desapila cuando reemplaza el no terminal
                symbols = self.table[(top, current_token)]
                if symbols != ['epsilon']:  # Manejo de producción vacía
                    for symbol in reversed(symbols):
                        self.stack.append(symbol)
            else:
                print(f"No se encontró entrada en la tabla para: {top}, {current_token}")
                raise Exception("Error de sintaxis")
        
        if self.cursor == len(self.tokens):
            raise Exception("Error de sintaxis - La entrada no ha sido consumida completamente")
        print("Análisis completado con éxito")
        # return self.stack
        return "\n".join(output)
    
def lexer(input_string):
    tokens = []
    token_specs = [
        ('LLAVE', r'\{'),  # Palabras reservadas antes
        ('CLLAVE', r'\}'),
        ('PLAY', r'\bdisplayData\b'),
        ('COMI', r'\"'),
        ('PLETRA', r'[a-z]+'),  
        ('PAAP', r'\('),
        ('PACI', r'\)'),
        ('PUNCOM', r'\;'),
        ('IGNORE', r'[ \t\n]+'),
        
    ]
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    for match in re.finditer(token_regex, input_string):
        type = match.lastgroup
        if type == 'IGNORE':
            continue
        elif type == 'MISMATCH':
            raise RuntimeError(f'Illegal character: {match.group(0)}')
        else:
            tokens.append((type, match.group(0)))
    return tokens

# input_string = "function nombre(var variable: boolean; otro: boolean;)"
# tokens = lexer(input_string)
# parser = PredictiveParser()
# parser.parse(tokens)

def analizar_entrada(input_string):
    try:
        tokens = lexer(input_string)
        parser = PredictiveParser()
        estado_pila = parser.parse(tokens)  # Asegúrate de que parse retorne algo útil, como el estado final de la pila.
        return f"Análisis completado con éxito.\nEstado final de la pila: {estado_pila}"
        # return estado_pila
    except Exception as e:
        return str(e)
