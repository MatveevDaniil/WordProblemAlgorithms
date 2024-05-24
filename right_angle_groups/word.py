from typing import Tuple


class ParseError(Exception):
    def __init__(self, expression, position):
        self.expression = expression
        self.position = position
        super().__init__(f"Cannot parse expression '{expression}' starting from the position {position}")


def prepare_expression(expression: str) -> str:
    allowed_special_letter = '{}^_-'
    
    _expression = []
    for letter in expression:
        if letter.isalpha() or letter.isnumeric() or \
                letter in allowed_special_letter:
            _expression.append(letter)
        elif letter in '() *':
            pass
        else:
            raise ValueError(f'not allowed letter {letter} in the expression {expression}')
    expression = ''.join(_expression)
    
    return expression


def parse_power(expression: str, i: int) -> Tuple[int, int]:
    if i + 1 >= len(expression) or expression[i + 1].isalpha():
        return 1, i + 1 
    elif expression[i + 1] == '^' and i + 2 < len(expression):
        if expression[i + 2] == '{':
            j = i + 3
            while j < len(expression) and expression[j] != '}':
                j += 1
            if j == len(expression):
                raise ParseError(expression, i)
            power = int(expression[i + 3: j])
            i = j + 1
        elif not expression[i + 2].isnumeric():
            raise ParseError(expression, i + 2)
        else:
            power = int(expression[i + 2])
            i += 3
    else:
        raise ParseError(expression, i + 1)
    return power, i


def parse_variable(expression: str, i: int) -> Tuple[str, int, int]:
    if i + 1 < len(expression) and expression[i + 1] == '_':
        if expression[i + 2] == '{':
            j = i + 3
            while j < len(expression) and expression[j] != '}':
                j += 1
            if j == len(expression):
                raise ParseError(expression, i)
            variable = expression[i: j + 1]
            i = j
        elif not expression[i + 2].isnumeric():
            raise ParseError(expression, i + 2)
        else:
            variable = expression[i:i+3]
            i += 2
    else:
        variable = expression[i]
    power, i = parse_power(expression, i)
    return variable, power, i
        

def parse_expression(expression: str) -> tuple[list[str], list[int]]:
    if expression == '1':
        return (['1'], [1])
    expression = prepare_expression(expression)
            
    variables = []
    powers = []
    i = 0
    while i < len(expression):
        if not expression[i].isalpha():
            raise ParseError(expression, i)
        else:
            variable, power, i = parse_variable(expression, i)
        variables.append(variable)
        powers.append(power)
    return (variables, powers)

"""
Word class
"""
class Word:
    def __init__(self, expression, verbose=True):
        if verbose:
            print(f'parsing {expression} ...')
        _variables, self.powers = parse_expression(expression)
        self.variables = []
        for variable in _variables:
            if '_' in variable:
                var, index = variable.split('_')
                if len(index) == 3:
                    self.variables.append(f"{var}_{index[1:-1]}")
                else:
                    self.variables.append(variable)
            else:
                self.variables.append(variable)
        self.var_power = list(zip(self.variables, self.powers))
        if verbose:
            print(f'my interpretation:', end=' ')
            print(*self.var_power)
    
    def format_word(self, var_idx: int) -> str:
        out_word = ['$']
        for idx, (var, power) in enumerate(self.var_power):
            _power = ''
            if power != 1:
                _power = str(power)
            if idx != var_idx:
                out_word.append(f'{var}^' + '{' + _power + '}')
            else:
                out_word.append(r'\boldsymbol{' + f'{var}^' + '{' + _power + '}}')
        out_word.append('$')
        return ''.join(out_word)
    

if __name__ == '__main__':
    Word('a^2b^3c^4')
    Word('x_1^2*x_2x_3^4')
    Word('x_{12}^2 (x_2x^{4})')
    Word('yz x_{1}^2*x_{10}')