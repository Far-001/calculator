import re


class Stack:
    """Структура стека для вычисления"""

    def __init__(self):
        self.items = []

    def push(self, item):
        # Добавление элемента в стек
        self.items.append(item)

    def pop(self):
        # Удаление и возврат элемента из стека
        if not self.items:
            raise ValueError("Stack is empty")
        return self.items.pop()

    def is_empty(self):
        # Проверка, пуст ли стек
        return len(self.items) == 0


class BaseToken:
    pass


class Operator(BaseToken):
    """Базовый класс для операндов"""
    operand_count = NotImplemented

    def __call__(self, *args):
        self._validate(*args)
        return self._apply(*args)

    def _validate(self, *args):
        if len(args) != self.operand_count:
            raise ValueError(
                f'Expected {self.operand_count} operands, but got {len(args)}')

    def _apply(self, *args):
        raise NotImplementedError


class Add(Operator):
    """Операнд сложения"""
    operand_count = 2

    def _apply(self, *args):
        return args[0] + args[1]


class Subtract(Operator):
    """Операнд вычетания"""
    operand_count = 2

    def _apply(self, *args):
        return args[0] - args[1]


class Multiply(Operator):
    """Операнд умножения"""
    operand_count = 2

    def _apply(self, *args):
        return args[0] * args[1]


class Divide(Operator):
    """Операнд деления"""
    operand_count = 2

    def _apply(self, *args):
        return args[0] / args[1]


class Exponentiation(Operator):
    """Операнд возведения в степень"""
    operand_count = 2

    def _apply(self, *args):
        return args[0] ** args[1]


class Negative(Operator):
    """Операнд унарного минуса"""
    operand_count = 1

    def _apply(self, *args):
        return 0 - args[0]


class NumberChecker:
    """Проверка, является ли строка числом"""
    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


class Parser:
    """Парсер введенного выражения"""

    def __init__(self, expression):
        # Объявляем строку выражения в классе
        self.expression = expression

    def _str2infix(self):
        """
        Обработка входного выражения в список инфиксной формы
        "5*(2-4)" -> ['5', '*', '(', '2', '-', '4', ')']
        """
        # # Предыдущее значение (по умолчанию "0")
        prev_item = '0'
        expression = self.expression

        # Разделяем пробелами по операндам
        formatted_expression = re.sub(
            r'([\^\+\-\*/\(\)])',
            r' \1 ',
            expression
        )
        # Получаем список операторов и операндов
        infix_form_list = formatted_expression.split()

        # Определение унарных минусов
        for item in range(len(infix_form_list)):
            # Если найден минус, а предыдущий элемент был операндом или его нет
            if infix_form_list[item] == '-' and prev_item in '^+-*/(0':
                # то это унарный минус, меняем знак на "~"
                infix_form_list[item] = '~'
            # Фиксируем предыдущее значение
            prev_item = infix_form_list[item]

        # Возвращаем инфиксный список
        return infix_form_list

    def infix2postfix(self):
        """
        Перевод из инфиксного списка в список постфиксной записи
        "5*(2-4)" -> ['5', '2', '4', '-', '*']
        """
        # Операторы и их приоритеты
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '~': 4}
        # Список для вывода постфиксной нотации
        postfix_form_list = []
        # Стек для операторов
        stack = Stack()
        expression = self._str2infix()

        for char in expression:
            # Разбиение входного инфиксного выражения на токены
            if NumberChecker.is_float(char):
                # Если токен - число, добавляем его в вывод
                postfix_form_list.append(char)
            elif char in "^+-*/~":
                # Если токен - оператор
                while (
                    not stack.is_empty()
                    and stack.items[-1] in "^+-*/~"
                    and priority[char] <= priority[stack.items[-1]]
                ):
                    # Если в стеке есть операторы с большим или
                    # равным приоритетом, переносим их в вывод
                    postfix_form_list.append(stack.pop())
                stack.push(char)
            elif char == '(':
                # Если токен - открывающая скобка, добавляем её в стек
                stack.push(char)
            elif char == ')':
                # Если токен - закрывающая скобка, переносим операторы
                # из стека в вывод до ближайшей открывающей скобки
                while not stack.is_empty() and stack.items[-1] != '(':
                    postfix_form_list.append(stack.pop())
                stack.pop()  # Удаляем открывающую скобку

        while not stack.is_empty():
            # Переносим оставшиеся операторы из стека в вывод
            postfix_form_list.append(stack.pop())

        # Преобразуем список вывода в строку и возвращаем результат
        return postfix_form_list


class PostfixCalc:
    """Калькулятор для постфиксного списка"""
    def __init__(self, postfix_form_list):
        self.postfix_form_list = postfix_form_list

    # Словарь операндов
    def calculate(self):
        stack = Stack()
        operands = {
            "+": Add(),
            "-": Subtract(),
            "*": Multiply(),
            "/": Divide(),
            "^": Exponentiation(),
            "~": Negative(),
        }

        # Последовательное выполнение операций
        for token in self.postfix_form_list:
            if token in operands:
                if token == "~":
                    operand = stack.pop()
                    result = operands[token]._apply(operand)
                else:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operands[token]._apply(operand1, operand2)
                stack.push(result)
            else:
                stack.push(float(token))

        return stack.pop()


class ExpressionCalculation:
    """Получение результата вычислений"""
    def __init__(self, expression):
        self.expression = expression

    # Парсинг и вычисление результата
    def get_result(self):
        parser = Parser(self.expression)
        postfix_form_list = parser.infix2postfix()

        calculator = PostfixCalc(postfix_form_list)
        result = calculator.calculate()

        return result


expression = '-(-((3^(-2)+8/9)/(2^2)))'
calculation = ExpressionCalculation(expression)
print(calculation.get_result())
