class Compiler:

    def __init__(self):
        print('Compiler is ready!!!')
        pass

    def load(self, command: str) -> None:
        if 'then' in command:
            self.commands = command.split('then')
        else:
            self.commands = [command]
        self._parse()
        return

    def _parse(self):
        commands = []
        for i in self.commands:
            commands.append(i.split(' '))
        self.commands = commands
        return

    def queries(self) -> list:
        return self.commands
