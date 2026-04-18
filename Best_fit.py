from dataclasses import dataclass
from typing import List
import random


@dataclass
class MemoryBlock:
    size: int


class FirstFit:
    def __init__(self, num_memory_block: int, max_block_size: int, min_block_size: int):
        self.num_memory_block = num_memory_block
        self.max_block_size = max_block_size
        self.min_block_size = min_block_size
        self.memory_block = self.init_memory(num_memory_block, min_block_size, max_block_size)
        self.available_block = [True] * num_memory_block
        self.used_block = {}

    def init_memory(self, num_memory_block: int, min_block_size: int, max_block_size: int) -> List[MemoryBlock]:
        memory_block = []
        for _ in range(num_memory_block):
            memory_block.append(MemoryBlock(random.randint(min_block_size, max_block_size)))
        return memory_block

    def allocate_process(self):
        while True:
            try:
                process_name = input("Enter process name: ").strip()
                if not process_name:
                    print("Process name cannot be empty.")
                    continue

                search_res = self.search_process(process_name)
                if search_res[0]:
                    print("The process is already allocated. Please choose another process name.")
                    continue

                process_size = int(input(f"Enter process size (between {self.min_block_size} and {self.max_block_size}): "))
                if process_size < self.min_block_size or process_size > self.max_block_size:
                    print(f"Process size must be between {self.min_block_size} and {self.max_block_size}.")
                    continue
                break

            except ValueError:
                print("Please enter a valid number.")

        target_block = self.find_best_fit(process_size)
        if target_block == -1:
            print("Failed to allocate process.")
            return

        self.used_block[process_name] = {
            "block": target_block,
            "process_size": process_size
        }

        print(f"Process '{process_name}' allocated to block {target_block + 1}.")

    def search_process(self, process_name: str):
        info = self.used_block.get(process_name)
        if info:
            return True, info["block"], info["process_size"]
        return False, None, None

    def find_best_fit(self, process_size: int) -> int:
        best_index = -1
        best_size = float("inf")

        for i in range(len(self.memory_block)):
            if self.available_block[i] and self.memory_block[i].size >= process_size:
                if self.memory_block[i].size < best_size:
                    best_size = self.memory_block[i].size
                    best_index = i

        if best_index != -1:
            self.available_block[best_index] = False

        return best_index

    def display_memory_block(self):
        print(f"\n{'No.':<5}{'Process':<15}{'P.Size':<10}{'B.Size':<10}{'Available':<10}")
        print("-" * 55)

        for i in range(len(self.memory_block)):
            process_name = "-"
            process_size = "-"

            for name, info in self.used_block.items():
                if info["block"] == i:
                    process_name = name
                    process_size = info["process_size"]
                    break

            block_size = self.memory_block[i].size
            status = "Yes" if self.available_block[i] else "No"

            print(f"{i + 1:<5}{process_name:<15}{str(process_size):<10}{block_size:<10}{status:<10}")

        print()

    def deallocate_process(self):
        target = input("Please enter the name of the process that you wish to deallocate: ").strip()
        search_target = self.search_process(target)

        if search_target[0]:
            self.available_block[search_target[1]] = True
            del self.used_block[target]
            print(f"Process '{target}' deallocated successfully.")
        else:
            print("Process not found.")


def display_menu():
    print("1. Allocate process")
    print("2. Deallocate process")
    print("3. Display Memory Block")
    print("4. Exit\n")


def main():
    while True:
        try:
            num_memory_block = int(input("Enter number of memory blocks: "))
            min_block_size = int(input("Enter minimum block size: "))
            max_block_size = int(input("Enter maximum block size: "))

            if num_memory_block <= 0 or min_block_size <= 0 or max_block_size <= 0:
                print("All values must be positive.\n")
                continue

            if min_block_size > max_block_size:
                print("Minimum block size cannot be greater than maximum block size.\n")
                continue

            simulator = FirstFit(num_memory_block, max_block_size, min_block_size)
            break

        except ValueError:
            print("Please enter valid numbers.\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            simulator.allocate_process()
        elif choice == "2":
            simulator.deallocate_process()
        elif choice == "3":
            simulator.display_memory_block()
        elif choice == "4":
            print("\nExiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()