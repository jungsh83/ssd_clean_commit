from ssd_command_action import SSDCommand

class ReadCommand(SSDCommand):
    command_name = ['read', 'r']

    def validate(self):
        if len(self._arguments) != 1 or not str(self._arguments[0]).isdigit():
            return False
        self._lba = int(self._arguments[0])
        return True

    def run(self):
        if not self.validate():
            raise InvalidArgumentException("Invalid read arguments")
        value = self._ssd_file_manager.read(self._lba)
        return f"[READ] LBA {self._lba} : {value}"