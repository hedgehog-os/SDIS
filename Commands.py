class Command:
    """
    @brief Базовый класс команды машины Поста.
    @param j Номер следующей команды.
    """
    ...

    def __init__(self, j):
        self.j = j      # Переход к строке j

class Mark(Command):
    """
    @brief Команда отметки: установить 1 на текущей ячейке.
    """

    def execute(self, machine):
        """
        @brief Выполнение команды.
        @param machine Экземпляр PostMachine.
        """
        ...

        machine.tape[machine.head] = 1
        machine.index = self.j

class Clear(Command):
    """
    @brief Команда очистки: установить 0 на текущей ячейке.
    """
    ...

    def execute(self, machine):
        machine.tape[machine.head] = 0
        machine.index = self.j

class Right(Command):
    """
    @brief Команда сдвига вправо.
    """
    ...

    def execute(self, machine):
        machine.head += 1
        machine.index = self.j

class Left(Command):
    """
    @brief Команда сдвига влево.
    """
    ...

    def execute(self, machine):
        machine.head -= 1
        machine.index = self.j

class Jump:
    """
    @brief Команда условного перехода.
    @details Переход зависит от значения текущей ячейки.
    @param j1 Переход, если 0.
    @param j2 Переход, если 1.
    """
    ...

    def __init__(self, j1, j2):
        self.j1 = j1
        self.j2 = j2

    def execute(self, machine):
        if not machine.tape[machine.head]:
            machine.index = self.j1
        else:
            machine.index = self.j2

class Stop(Command):
    """
    @brief Команда остановки машины.
    """
    ...
    
    def __init__(self):
        super().__init__(None)

    def execute(self, machine):
        machine.stopped = True
