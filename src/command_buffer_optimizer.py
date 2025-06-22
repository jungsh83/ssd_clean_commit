from abc import abstractmethod, ABC

from src.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferData


class CommandBufferOptimizeStrategy(ABC):
    @abstractmethod
    def optimize(self, command_buffers):
        pass


class IgnoreCommandStrategy(CommandBufferOptimizeStrategy):

    def optimize(self, command_buffers):
        result: list[CommandBufferData] = []
        new_order = 0
        for target_index, target_command in enumerate(command_buffers):
            unvisited = self._get_update_range(target_command)
            for overwrite_index in range(target_index + 1, 5):
                overwrite_command = command_buffers[overwrite_index]
                visited = self._get_update_range(overwrite_command)
                unvisited.difference_update(visited)
            if unvisited:
                new_order += 1
                target_command.order = new_order
                result.append(target_command)

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

    def optimize(self, command_buffers):
        result: list[CommandBufferData] = []
        new_order = 0
        merged_command_orders: set[int] = set()
        for target_index, target_command in enumerate(command_buffers):
            if target_command.command_type != ERASE:
                new_order += 1
                result.append(
                    CommandBufferData(order=new_order, command_type=target_command.command_type, lba=target_command.lba,
                                      value=target_command.value,
                                      size=target_command.size))
                continue
            elif target_command.order in merged_command_orders:
                continue
            new_lba = target_command.lba
            new_size = target_command.size
            for overwrite_index in range(target_index + 1, 5):
                overwrite_command = command_buffers[overwrite_index]
                if overwrite_command.command_type != ERASE:
                    continue
                if new_lba <= overwrite_command.lba + overwrite_command.size and \
                        new_lba + new_size >= overwrite_command.lba:
                    new_lba = min(new_lba, overwrite_command.lba)
                    new_size = max(new_lba + new_size,
                                   overwrite_command.lba + overwrite_command.size) \
                               - new_lba
                    merged_command_orders.add(overwrite_command.order)

            while new_size > 10:
                new_order += 1
                result.append(
                    CommandBufferData(order=new_order, command_type=target_command.command_type, lba=new_lba,
                                      value=target_command.value,
                                      size=10))
                new_lba += 10
                new_size -= 10
            new_order += 1
            result.append(
                CommandBufferData(order=new_order, command_type=target_command.command_type, lba=new_lba,
                                  value=target_command.value,
                                  size=new_size))

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

    def optimize(self, command_buffers):
        return self._strategy.optimize(command_buffers)
