class PostMachine:
    """
    @brief Класс машины Поста.
    @details Реализует вычислительную модель с лентой, кареткой и набором команд.
    """

    def __init__(self, string, commands):
        """
        @brief Инициализация машины.
        @param string Строка из 0 и 1 — начальное состояние ленты.
        @param commands Список команд для выполнения.
        """
        ...

        self.tape = {}              # Лента машины Поста
        self.commands = commands    # Список с выполняемыми командами
        self.head = 0               # Каретка
        self.index = 0              # Номер текущей команды
        self.stopped = False        # Остановка программы

        for i, c in enumerate(string):
            self.tape[i] = int(c)

    def run(self):
        """
        @brief Запуск машины Поста.
        @details Выполняет команды по очереди, пока не встретит Stop.
        """
        ...

        i = 1
        self.stopped = False

        while not self.stopped and self.index < len(self.commands):
            command = self.commands[self.index]
            command.execute(self)

            print(f"{i}.")
            print('')
            print(list(self.tape.values()))
            print(f"каретка: {self.head}")
            print(f"комманда: {self.index}")
            print('')
            i += 1

program = [
    "? 1; 3",   
    "V 2",      
    "→ 4",      
    "X 5",      
    "!",        
    "← 4"      
]