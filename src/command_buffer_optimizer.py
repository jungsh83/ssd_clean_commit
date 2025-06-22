from abc import abstractmethod, ABC

from src.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferData, MAX_SIZE_OF_COMMAND_BUFFERS, \
    ERASE_CHUNK_SIZE


class CommandBufferOptimizeStrategy(ABC):
    @abstractmethod
    def optimize(self, command_buffers):
        pass


class IgnoreCommandStrategy(CommandBufferOptimizeStrategy):

    def optimize(self, current_command_buffers: list[CommandBufferData]):
        new_command_buffers: list[CommandBufferData] = []
        new_order = 0
        for source_index, source_command in enumerate(current_command_buffers):
            unvisited = self._get_update_range(source_command)
            for overwrite_command in current_command_buffers[source_index + 1:]:
                visited = self._get_update_range(overwrite_command)
                unvisited.difference_update(visited)
            if unvisited:
                new_order = self._append_unoverwritten_command(new_command_buffers, new_order, source_command)

        self._append_empty(new_command_buffers, new_order)

        return new_command_buffers

    def _append_unoverwritten_command(self, new_command_buffers, new_order, source_command):
        new_order += 1
        new_command_buffers.append(CommandBufferData(order=new_order,
                                                command_type=source_command.command_type,
                                                lba=source_command.lba,
                                                value=source_command.value,
                                                size=source_command.size))
        return new_order

    def _append_empty(self, new_command_buffers, new_order):
        for _ in range(new_order, MAX_SIZE_OF_COMMAND_BUFFERS):
            new_order += 1
            new_command_buffers.append(CommandBufferData(order=new_order))

    def _get_update_range(self, command):
        result: set[int] = set()
        if command.command_type == WRITE:
            result.add(command.lba)
        elif command.command_type == ERASE:
            result = set([i for i in range(command.lba, command.lba + command.size)])
            result.add(command.lba)
        return result


class MergeEraseStrategy(CommandBufferOptimizeStrategy):

    def optimize(self, current_command_buffers: list[CommandBufferData]):
        new_command_buffers: list[CommandBufferData] = []
        new_order = 0
        merged_command_orders: set[int] = set()
        for source_index, source_command in enumerate(current_command_buffers):
            if source_command.command_type == WRITE:
                new_order = self._append_write(new_command_buffers, new_order, source_command)

            if self._is_skipped_target(merged_command_orders, source_command):
                continue

            new_end_lba, new_start_lba = self._calculate_new_start_and_end_lba(merged_command_orders,
                                                                               current_command_buffers,
                                                                               source_command, source_index)

            new_order = self._append_erase_chunk_with_new_start_and_end_lba(new_command_buffers, new_order,
                                                                            new_start_lba, new_end_lba)

        self._append_empty(new_command_buffers, new_order)

        if self._erase_count(current_command_buffers) <= self._erase_count(new_command_buffers):
            return current_command_buffers

        return new_command_buffers

    def _calculate_new_start_and_end_lba(self, merged_command_orders, current_command_buffers, source_command,
                                         source_index):
        new_start_lba = source_command.start_lba
        new_end_lba = source_command.end_lba
        for overwrite_command in current_command_buffers[source_index + 1:]:
            if self._is_skipped_target(merged_command_orders, overwrite_command):
                continue

            if new_start_lba <= overwrite_command.end_lba and new_end_lba >= overwrite_command.start_lba:
                new_start_lba = min(new_start_lba, overwrite_command.start_lba)
                new_end_lba = max(new_end_lba, overwrite_command.end_lba)
                merged_command_orders.add(overwrite_command.order)
        return new_end_lba, new_start_lba

    def _is_skipped_target(self, merged_command_orders, command) -> bool:
        if command.command_type == EMPTY:
            return True
        elif command.command_type == WRITE:
            return True
        elif command.order in merged_command_orders:
            return True
        return False

    def _append_write(self, new_command_buffers, new_order, source_command) -> int:
        new_order += 1
        new_command_buffers.append(
            CommandBufferData(order=new_order, command_type=WRITE, lba=source_command.lba, value=source_command.value))
        return new_order

    def _append_empty(self, new_command_buffers, new_order):
        for _ in range(new_order, MAX_SIZE_OF_COMMAND_BUFFERS):
            new_order += 1
            new_command_buffers.append(CommandBufferData(order=new_order))

    def _append_erase_chunk_with_new_start_and_end_lba(self, new_command_buffers, new_order, new_start_lba,
                                                       new_end_lba) -> int:
        while new_end_lba - new_start_lba > ERASE_CHUNK_SIZE:
            new_order += 1
            new_command_buffers.append(
                CommandBufferData(order=new_order, command_type=ERASE, lba=new_start_lba, size=ERASE_CHUNK_SIZE))
            new_start_lba += ERASE_CHUNK_SIZE
        new_order += 1
        new_command_buffers.append(
            CommandBufferData(order=new_order, command_type=ERASE, lba=new_start_lba, size=new_end_lba - new_start_lba))
        return new_order

    def _erase_count(self, command_buffers):
        result = 0
        for command in command_buffers:
            if command.command_type == ERASE:
                result += 1
        return result


class CommandBufferOptimizer:
    def __init__(self, strategy):
        self._strategy = strategy

    def optimize(self, current_command_buffers: list[CommandBufferData]):
        return self._strategy.optimize(current_command_buffers)
