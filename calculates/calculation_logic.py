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


def isfloat(value):
    """Флаг численного значения"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def split_space(expression):
    """
    Разделение пробелами
    "20+5*(2-4)" -> "20 + 5 * ( 2 - 4 )"
    """
    # Разделяем пробелами по знакам
    formatted_expression = re.sub(r'([\+\-\*/\(\)])', r' \1 ', expression)
    # Предыдущее значение (по умолчанию "0")
    prev_item = '0'
    # Флаг отрицательного числа
    add_sub = False
    # Получаем список операторов и операндов
    list_expression = formatted_expression.split()

    # Определение отрицательных чисел
    for item in range(len(list_expression)):
        # Если найден минус, а предыдущий элемент был операндом или его не было
        if list_expression[item] == '-' and prev_item in '+-*/(0':
            # Меняем флаг
            add_sub = True
        # Если флаг истина, а предыдущий элемент был минус
        if add_sub and prev_item == '-':
            # Добавляем минус к элементу
            list_expression[item] = '-' + list_expression[item]
            # Удаляем минус из предыдущего элемента
            list_expression[item - 1] = ''
            # Возвращаем флаг
            add_sub = False
        # Фиксируем предыдущее значение
        prev_item = list_expression[item]

    # Собираем в строку
    formatted_expression = ' '.join(list_expression)

    return formatted_expression


def infix_to_postfix(expression):
    """
    Перевод из инфиксной в постфиксную запись
    "20 + 5 * ( 2 - 4 )" -> "20 5 2 4 - * +"
    """
    # Операторы и их приоритеты
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    # Список для вывода постфиксной нотации
    output = []
    # Стек для операторов
    stack = Stack()

    for char in expression.split():
        # Разбиение входного инфиксного выражения на токены
        if isfloat(char):
            # Если токен - число, добавляем его в вывод
            output.append(char)
        elif char in "+-*/":
            # Если токен - оператор
            while (not stack.is_empty() and stack.items[-1] in "+-*/"
                   and precedence[char] <= precedence[stack.items[-1]]):
                # Если в стеке есть операторы с большим или
                # равным приоритетом, переносим их в вывод
                output.append(stack.pop())
            stack.push(char)
        elif char == '(':
            # Если токен - открывающая скобка, добавляем её в стек
            stack.push(char)
        elif char == ')':
            # Если токен - закрывающая скобка, переносим операторы
            # из стека в вывод до ближайшей открывающей скобки
            while not stack.is_empty() and stack.items[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Удаляем открывающую скобку

    while not stack.is_empty():
        # Переносим оставшиеся операторы из стека в вывод
        output.append(stack.pop())

    # Преобразуем список вывода в строку и возвращаем результат
    return ' '.join(output)


def calculate(post_str):
    """
    Алгоритм калькулятора с постфиксной нотацией
    "20 5 2 4 - * +" -> 10
    """
    # Преобразовываем строку в список
    item_list = post_str.split()
    # Создаем экземпляр стека
    stack = Stack()
    # Создаем словарь для операндов
    dict_operand = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    # Перебираем входные данные
    for item in item_list:
        # Делим данные на операнды и значения
        if item in '+-*/':
            # Если на входе операнд
            # Считываем последние 2 значения
            value2 = stack.pop()
            value1 = stack.pop()
            # Выполняем соответствующее действие и возврат результата в стек
            stack.push(dict_operand[item](value1, value2))
        else:
            # Если на входе значение
            # Заносим его в стек
            stack.push(float(item))
    # Возвращаем последний элемент(результат)
    return stack.pop()


def evaluate_expression(expression):
    """Вычисление выражения с использованием функций"""
    result = calculate(infix_to_postfix(split_space(expression)))
    return result