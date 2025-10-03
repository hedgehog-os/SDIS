from Commands import Command, Clear, Mark, Jump, Left, Right, Stop

class Parser:
    """
    @brief Класс для парсинга текстовых команд в объекты.
    """
    def parse(self, commands):
        """
        @brief Парсинг текстовых команд в объекты.
        @param commands Список строковых команд.
        @return Список объектов-команд.
        """
        result = []

        for command in commands:
            
            command = command.strip()
            if not command:
                continue
            
            if command[0] == 'V':
                _, j = command.split()
                result.append(Mark(int(j)))
            
            elif command[0] == 'X':
                _, j = command.split()
                result.append(Clear(int(j)))
            
            elif command[0] == '→' or command[0] == 'r':
                _, j = command.split()
                result.append(Right(int(j)))

            elif command[0] == '←' or command[0] == 'l':
                _, j = command.split()
                result.append(Left(int(j)))

            elif command[0] == '?':
                parts = command[1:].split(";")
                j1 = int(parts[0].strip())
                j2 = int(parts[1].strip())
                result.append(Jump(int(j1), int(j2)))

            elif command[0] == '!':
                result.append(Stop())

            else:
                raise ValueError(f'Неизвестная команда: {command}')
        
        return result