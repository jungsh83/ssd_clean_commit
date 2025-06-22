from abc import abstractmethod, ABC

from src.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferData


class CommandBufferOptimizeStrategy(ABC):
    @abstractmethod
    def optimize(self, command_buffers):
        pass


class IgnoreCommandStrategy(CommandBufferOptimizeStrategy):

    def optimize(self, command_buffers: list[CommandBufferData]):
        result: list[CommandBufferData] = []
        new_order = 0
        for source_index, source_command in enumerate(command_buffers):
            unvisited = self._get_update_range(source_command)
            for overwrite_index in range(source_index + 1, 5):
                overwrite_command = command_buffers[overwrite_index]
                visited = self._get_update_range(overwrite_command)
                unvisited.difference_update(visited)
            if unvisited:
                new_order += 1
                source_command.order = new_order
                result.append(source_command)

        for empty_order in range(new_order + 1, 6):
            result.append(CommandBufferData(order=empty_order))

        return result

    def _get_update_range(self, command):
        result: set[int] = set()
        if command.command_type == WRITE:
            result.add(command.lba)
        elif command.command_type == ERASE:
            result = set([i for i in range(command.lba, command.lba + command.size)])
            result.add(command.lba)
        return result


class MergeEraseStrategy(CommandBufferOptimizeStrategy):

    def optimize(self, command_buffers: list[CommandBufferData]):
        result: list[CommandBufferData] = []
        new_order = 0
        merged_command_orders: set[int] = set()
        for source_index, source_command in enumerate(command_buffers):
            if source_command.command_type == EMPTY:
                break
            elif source_command.command_type == WRITE:
                new_order += 1
                result.append(CommandBufferData(order=new_order, command_type=WRITE, lba=source_command.lba, value=source_command.value))
                continue
            elif source_command.order in merged_command_orders:
                continue

            new_start_lba = source_command.start_lba
            new_end_lba = source_command.end_lba
            for overwrite_index in range(source_index + 1, 5):
                overwrite_command = command_buffers[overwrite_index]
                if overwrite_command.command_type != ERASE:
                    continue

                if new_start_lba <= overwrite_command.end_lba and new_end_lba >= overwrite_command.start_lba:
                    new_start_lba = min(new_start_lba, overwrite_command.start_lba)
                    new_end_lba = max(new_end_lba, overwrite_command.end_lba)
                    merged_command_orders.add(overwrite_command.order)

            while new_end_lba - new_start_lba > 10:
                new_order += 1
                result.append(CommandBufferData(order=new_order, command_type=ERASE, lba=new_start_lba, size=10))
                new_start_lba += 10

            new_order += 1
            result.append(CommandBufferData(order=new_order, command_type=ERASE, lba=new_start_lba, size=new_end_lba  - new_start_lba))

        for i in range(new_order + 1, 6):
            result.append(CommandBufferData(order=i))

        as_is_count = 0
        for command in command_buffers:
            if command.command_type == ERASE:
                as_is_count += 1

        to_be_count = 0
        for command in result:
            if command.command_type == ERASE:
                to_be_count += 1

        if as_is_count <= to_be_count:
            return command_buffers

        return result


class CommandBufferOptimizer:
    def __init__(self, strategy):
        self._strategy = strategy

    def optimize(self, command_buffers: list[CommandBufferData]):
        return self._strategy.optimize(command_buffers)
