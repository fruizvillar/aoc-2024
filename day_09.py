""" Solver for AoC 2024 Day 9"""

import collections
import dataclasses
from typing import Optional, override

import lib

DAY = int("9")


@dataclasses.dataclass
class DiskItem:
    size: int


@dataclasses.dataclass
class FilePart(DiskItem):
    id_no: int


@dataclasses.dataclass
class EmptySpace(DiskItem):
    pass


@dataclasses.dataclass
class DiskNode:
    disk_item: DiskItem
    order: int
    next: Optional["DiskNode"] = None
    prev: Optional["DiskNode"] = None


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/9"""

    EMPTY = "."

    @override
    def solve(self) -> None:

        compressed_disk = list(self.read().strip())

        disk_head, disk_tail = self.decompress_disk_into_dl_nodes(compressed_disk)

        self.print_disk(disk_head)

        self.fragment(disk_head, disk_tail)

        self.print_disk(disk_head)

        self.resolved(result_1=self.checksum(disk_head))

        disk_head, disk_tail = self.decompress_disk_into_dl_nodes(compressed_disk)
        self.compact(disk_head, disk_tail)

        self.resolved(result_2=self.checksum(disk_head))

    def decompress_disk_into_dl_nodes(self, compressed_disk):
        disk_id = 0
        is_space = False

        head = None
        iter_node = None
        tail = None

        order = 0

        for c in compressed_disk:
            size = int(c)

            if not size:
                is_space = not is_space
                continue

            if is_space:
                node = DiskNode(EmptySpace(size), order=order)
            else:
                node = DiskNode(FilePart(size, id_no=disk_id), order=order)
                disk_id += 1
            order += 1

            is_space = not is_space

            if head is None:
                head = node
                iter_node = node

            else:
                iter_node.next = node
                node.prev = iter_node
                iter_node = node

        tail = iter_node

        return head, tail

    def fragment(self, disk_head, disk_tail):

        while disk_head != disk_tail:
            if self.DEBUG:
                self.print_disk(disk_head)

            if isinstance(disk_head.disk_item, FilePart):
                disk_head = disk_head.next
                continue
            if isinstance(disk_tail.disk_item, EmptySpace):
                disk_tail = disk_tail.prev
                continue

            # We have a H-> FilePart and T-> EmptySpace. We can swap them

            if (empty_size := disk_head.disk_item.size) == (
                file_size := disk_tail.disk_item.size
            ):
                # Easiest case, just swap them
                disk_head.disk_item, disk_tail.disk_item = (
                    disk_tail.disk_item,
                    disk_head.disk_item,
                )
                disk_head = disk_head.next
                disk_tail = disk_tail.prev
                continue

            if empty_size < file_size:
                # We fill the empty space with the file, reduce the file size and continue
                del disk_head.disk_item
                disk_head.disk_item = FilePart(
                    size=empty_size, id_no=disk_tail.disk_item.id_no
                )
                disk_tail.disk_item.size -= empty_size
                aux = disk_head
                disk_head = disk_head.next
                continue

            # Here empty_size > file_size so we do: ...EEE...FF... -> ...FFE...EE...
            # We fill the empty space with the file, reduce the file size and continue
            # First, create a new node with the file size that goes at the leftmost part
            #   of the empty space.
            new_node_order = (
                (disk_head.order + disk_head.next.order) // 2
                if disk_head.next is not None
                else disk_head.order + 1
            )
            new_disk_node = DiskNode(
                FilePart(size=file_size, id_no=disk_tail.disk_item.id_no),
                order=new_node_order,
            )
            disk_head.prev.next = new_disk_node
            new_disk_node.prev = disk_head.prev
            new_disk_node.next = disk_head
            disk_head.prev = new_disk_node
            # Second, reduce the empty space size
            disk_head.disk_item.size -= file_size
            # Third, remove the file.
            disk_tail.prev.next = disk_tail.next
            if disk_tail.next is not None:
                disk_tail.next.prev = disk_tail.prev
            aux = disk_tail
            disk_tail = disk_tail.prev
            del aux

    def compact(self, disk_head, disk_tail):
        head_iter = disk_head
        tail_iter = disk_tail

        last_empty_space = disk_head

        while tail_iter is not None:
            if isinstance(tail_iter.disk_item, EmptySpace):
                tail_iter = tail_iter.prev
                continue

            moving_file_size = tail_iter.disk_item.size

            head_iter = last_empty_space
            spaces_skipped = False

            while head_iter is not None:
                if head_iter == tail_iter:
                    break
                if head_iter.order >= tail_iter.order:
                    break

                if self.DEBUG:
                    self.print_disk(disk_head, end="")
                    print(
                        f"Moving {tail_iter.disk_item.id_no} of size {moving_file_size} to {head_iter.disk_item.size}"
                    )

                if isinstance(head_iter.disk_item, FilePart):
                    head_iter = head_iter.next
                    continue

                if not spaces_skipped:
                    last_empty_space = head_iter

                if head_iter.disk_item.size >= moving_file_size:
                    self.move_file_into_empty_space(file=tail_iter, space=head_iter)
                    break

                head_iter = head_iter.next
                spaces_skipped = True

            if self.DEBUG:
                self.print_disk(disk_head)

            tail_iter = tail_iter.prev

    def move_file_into_empty_space(self, *, file: DiskNode, space: DiskNode):
        if space.disk_item.size < file.disk_item.size:
            raise ValueError("File is too big for the space")

        if space.disk_item.size == file.disk_item.size:
            space.disk_item, file.disk_item = file.disk_item, space.disk_item
            return

        # Space is bigger than the file.
        space.disk_item.size -= file.disk_item.size

        new_file_node = DiskNode(
            FilePart(size=file.disk_item.size, id_no=file.disk_item.id_no),
            order=(space.order + space.prev.order) // 2,
        )

        space.prev.next = new_file_node
        new_file_node.prev = space.prev
        new_file_node.next = space
        space.prev = new_file_node

        new_space_node = None
        if file.next is not None and isinstance(file.next.disk_item, EmptySpace):
            # We try to add the empty space to the next node
            file.next.disk_item.size += file.disk_item.size

        elif file.prev is not None and isinstance(file.prev.disk_item, EmptySpace):
            # We try to add the empty space to the previous node
            file.prev.disk_item.size += file.disk_item.size

        else:
            # We need to create a new node and replace the current one
            new_space_node = DiskNode(EmptySpace(file.disk_item.size), order=file.order)

        if new_space_node:
            self._replace_node(file, new_space_node)
        else:
            self._delete_node(file)

    def _replace_node(self, node, new_node):
        new_node.prev = node.prev
        new_node.next = node.next
        if node.prev:
            node.prev.next = new_node
        if node.next:
            node.next.prev = new_node
        del node

    def _delete_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        del node

    def print_disk(self, disk_head, end="\n"):

        node = disk_head
        while node is not None:
            if isinstance(node.disk_item, FilePart):
                if node.disk_item.size == 1:
                    print(node.disk_item.id_no, end="|")
                else:
                    print(
                        node.disk_item.id_no,
                        "_" * (node.disk_item.size - 1),
                        sep="",
                        end="|",
                    )

            else:
                print(self.EMPTY * node.disk_item.size, end="|")
            node = node.next

        print(end=end)

    def checksum(self, disk_head):
        acc = 0
        factor = -1

        node = disk_head

        while node is not None:
            for _ in range(node.disk_item.size):
                factor += 1

                if isinstance(node.disk_item, EmptySpace):
                    continue

                acc += node.disk_item.id_no * factor

                if self.DEBUG:
                    print(node.disk_item.id_no, factor, acc)

            node = node.next

        return acc


solver = Solver(DAY)
solver()
