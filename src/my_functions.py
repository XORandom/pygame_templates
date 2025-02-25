"""Различные функции, что могут быть полезны для проекта"""

def generate_data()-> list:
    import random
    arr: list =  [x for x in range(1000000000)]
    # arr.sort()
    return arr


def test_perfomance():
    """
    Тестирование скорости работы функций
    
    """
    from timeit import repeat

    test_func = '''

    pass
    '''
    min(repeat(test_func, repeat=5, number=10))



def my_bin_search(x:int, input_array: list) -> int:
    """
    функция бинарного поиска
    O(log n)

    :param x: что ищем
    :param input_array: список, в котором ищем
    :return: 
    """
    # Границы поиска
    left: int = 0
    "левая граница с нуля"
    right: int = len(input_array) - 1
    "правая граница последний индекс массива"
    while left < right:
        middle: int = (left+right)//2
        if input_array[middle] == x:
            return middle
        elif input_array[middle] > x:
            right = middle - 1
        elif input_array[middle] < x:
            left = middle + 1
        # print(f"l={left}, r={right}, m={middle}")
    # Интервал сократился до одного элемента
    if input_array[left] == x:
        return left
    else:
        return "не нашли"
    

def my_lin_search(x:int, input_array: list) -> int:
    """
    Линейный поиск
    O(n)


    """
    return [res for res in input_array if res == x]

if __name__ == '__main__':
    pass