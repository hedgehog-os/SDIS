class Multiset:
    """
    @brief Класс мультимножества c поддержкой вложенных структур.
    @details Поддерживает парсинг из строки, операции объединения, пересечения, разности,
             проверку на пустоту, удаление элементов и построение булеана.
    """

    def to_multiset(self, element):
        """
        @brief Добавляет элемент в мультимножество.
        @param element Элемент (строка или другой Multiset).
        """
        ...

        if element in self.multiset:
            self.multiset[element] += 1
        else:
            self.multiset[element] = 1

    def __init__(self, s):
        """
        @brief Конструктор мультимножества из строки.
        @param s Строка вида '{a, b, {c, d}, a}'.
        @details Рекурсивно парсит вложенные множества и сохраняет кратности элементов.
        """
        ...

        self.multiset = {}

        if isinstance(s, dict):
            for elem, count in s.items():
                for _ in range(count):
                    self.to_multiset(elem)
            return

        depth = 0 
        elem = ''
        subset = ''

        for sym in s[1:-1]:

            if sym == '{':
                depth += 1
                if depth == 1:
                    subset = '' 
                else:
                    subset += sym
                continue

            if sym == '}':
                depth -= 1
                if depth == 0:
                    self.to_multiset(Multiset('{' + subset + '}'))
                    subset = ''
                else:
                    subset += sym
                continue

            if depth > 0:
                subset += sym
                continue

            if sym == ',':
                if elem.strip():
                    self.to_multiset(elem.strip())
                elem = ''
            elif sym != ' ':
                elem += sym

        if elem.strip():
            self.to_multiset(elem.strip())
    
    def __repr__(self):
        """
        @brief Возвращает строковое представление мультимножества.
        @return Строка вида 'Multiset({...})'.
        """
        ...

        return f"Multiset({self.multiset})"

    def __eq__(self, other):
        """
        @brief Проверка на равенство двух мультимножеств.
        @param other Другой объект Multiset.
        @return True, если множества равны.
        """
        ...

        if not isinstance(other, Multiset):
            return False
        return self.multiset == other.multiset

    # Хэш-значение объекта
    def __hash__(self):
        """
        @brief Хэш-функция для мультимножества.
        @return Хэш на основе frozenset.
        """
        ...

        return hash(frozenset(self.multiset.items()))

    # Проверка на наличие элементов в множестве
    def __contains__(self, elem):
        """
        @brief Проверка наличия элемента в мультимножестве.
        @param elem Элемент для проверки.
        @return True, если элемент присутствует.
        """
        ...

        return elem in self.multiset

    # Объединение двух мультимножеств
    def __and__(self, other):
        """
        @brief Объединение двух мультимножеств.
        @param other Второе мультимножество.
        @return Новое объединённое мультимножество.
        """
        ...

        result = Multiset('{}')

        for elem, count in self.multiset.items():
            for _ in range(count):
                result.to_multiset(elem)

        for elem, count in other.multiset.items():
            for _ in range(count):
                result.to_multiset(elem)

        return result
    
    def __add__(self, other):
        """
        @brief Оператор + для объединения мультимножеств.
        @param other Второе мультимножество.
        @return Новое объединённое мультимножество.
        """
        ...

        result = Multiset('{}')
        for elem, count in self.multiset.items():
            for _ in range(count):
                result.to_multiset(elem)
        for elem, count in other.multiset.items():
            for _ in range(count):
                result.to_multiset(elem)
        return result


    def __iadd__(self, other):
        """
        @brief Инкрементальное объединение с другим мультимножеством.
        @param other Второе мультимножество.
        @return Обновлённый self.
        """
        ...

        for elem, count in other.multiset.items():
            for _ in range(count):
                self.to_multiset(elem)
        return self

    # Разность двух мультимножеств
    def __sub__(self, multiset):
        """
        @brief Разность двух мультимножеств.
        @param multiset Множество, которое нужно вычесть.
        @return Новое мультимножество.
        """
        ...

        result = Multiset('{}')
        for elem, count in self.multiset.items():
            difference = count - multiset.multiset.get(elem, 0)
            if difference > 0:
                for _ in range(difference):
                    result.to_multiset(elem)
        return result

    def __isub__(self, multiset):
        """
        @brief Инкрементальное вычитание элементов.
        @param multiset Множество, которое нужно вычесть.
        @return Обновлённый self.
        """
        ...

        for elem, count in multiset.multiset.items():
            self.ndelete(elem, count)
        return self

    def __mul__(self, multiset):
        """
        @brief Пересечение двух мультимножеств.
        @param multiset Второе множество.
        @return Множество c минимальной кратностью элементов.
        """
        ...

        result = Multiset('{}')
        for elem, count in self.multiset.items():
            if elem in multiset.multiset:
                for _ in range(min(count, multiset.multiset[elem])):
                    result.to_multiset(elem)
        return result

    def __imul__(self, multiset):
        """
        @brief Инкрементальное пересечение с другим множеством.
        @param multiset Второе множество.
        @return Обновлённый self.
        """
        ...

        result = {}
        for elem in self.multiset:
            if elem in multiset.multiset:
                minimum = min(self.multiset[elem], multiset.multiset[elem])
                result[elem] = minimum
        self.multiset = result
        return self

    # Проверка на пустое мультимножество
    def is_empty(self):
        """
        @brief Проверка на пустоту мультимножества.
        @return True, если множество пусто.
        """
        ...

        for elem, count  in self.multiset.items():
            if isinstance(elem, Multiset):
                    return False
            else:
                if count > 0:
                    return False
        return True

    # Полное удаление определенного элемента из мультимножества
    def delete(self, elem):
        """
        @brief Полное удаление элемента.
        @param elem Элемент для удаления.
        """
        ...

        if elem in self.multiset:
            del self.multiset[elem]
    
    # Удаление некого количества одинаковых элементов
    def ndelete(self, elem, number):
        """
        @brief Удаление заданного количества экземпляров элемента.
        @param elem Элемент.
        @param number Количество экземпляров для удаления.
        """
        ...

        if elem in self.multiset:
            if self.multiset[elem] <= number:
                self.delete(elem)
            else :
                self.multiset[elem] -= number

    # Мощность множества
    def cardinality(self):
        """
        @brief Мощность мультимножества.
        @return Сумма всех кратностей элементов.
        """
        ...

        return sum(self.multiset.values())

    # Построение булеана мультимножества
    def bolean(self):
        """
        @brief Построение булеана мультимножества.
        @return Список всех возможных подмножеств.
        """
        ...
        
        elements = list(self.multiset.items())  
        result = [] 

        def backtrack(index, current):
            if index == len(elements):
                subset = Multiset('{}')
                for elem, count in current.items():
                    for _ in range(count):
                        subset.to_multiset(elem)
                result.append(subset)
                return
            
            elem, max_count = elements[index]
            for c in range(max_count + 1):
                current[elem] = c
                backtrack(index + 1, current)
            del current[elem]

        backtrack(0, {})
        return result