import random
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class File:
    name: str
    size: int
    index_block: int
    data_blocks: List[int]


class IndexedAllocationSimulator:

    def __init__(self, total_disk: int = 100):
        self.total_disk = total_disk
        self.files: Dict[str, File] = {}
        self.available_blocks = set(range(total_disk))
        self.used_blocks = set()

    def allocate_file(self):
        # check whether there is still space available
        if len(self.available_blocks)< 2 :
            print("The disk has no available space.\n")
            return
        while True:
            filename = input("Enter the file name: ").strip()

            # check duplicated filename
            if self.search_file(filename) :
                print(f"File '{filename}' already exists. Try another.\n")
                continue


            # input file size
            while True:
                try:
                    size = int(input("Enter the size of the file: "))

                    if size <= 0:
                        print("File size must be positive.\n")
                        continue

                    if size + 1 > len(self.available_blocks):
                        print(f"Insufficient space! Available blocks: {len(self.available_blocks) - 1}\n")
                        continue

                    break
                except ValueError:
                    print("Please enter a valid number.\n")

            break
        
        # choose a random element from available blocks as the index block
        index_block = random.choice(list(self.available_blocks))
        
        # remove the selected index block from available blocks
        self.available_blocks.remove(index_block)
        
        # add the selected index block to used blocks
        self.used_blocks.add(index_block)

        # allocate data blocks , random.sample choose (size)th elements from available blocks
        data_blocks = random.sample(list(self.available_blocks), size)
        
        # remove the selected data blocks from available blocks
        self.available_blocks.difference_update(data_blocks)
        
        # add the selected data blocks to used blocks
        self.used_blocks.update(data_blocks)

        # store file
        self.files[filename] = File(filename, size, index_block, data_blocks)

        print("\nFile allocated successfully.\n")

    def delete_file(self):
        if not self.files:
            print("No files to delete.\n")
            return

        while True:
            filename = input("Enter the file name to delete: ").strip()

            if not self.search_file(filename):
                print(f"File '{filename}' does not exist. Try again.\n")
                continue

            file_obj = self.files[filename]

            # return blocks to available
            self.available_blocks.update(file_obj.data_blocks)
            self.available_blocks.add(file_obj.index_block)

            # remove from used
            self.used_blocks.remove(file_obj.index_block)
            self.used_blocks.difference_update(file_obj.data_blocks)

            # remove from files

            del self.files[filename]
            break

        print("\nFile deleted successfully.\n")

    def display_allocation(self):
        print("\nCurrent File Allocation:\n")

        print(f"{'No.':<5} | {'Filename':<20} | {'Index -> Data Blocks':<35}")
        print("-" * 70)

        for i, (filename, file_obj) in enumerate(self.files.items(), start=1):
            data_blocks_str = ", ".join(map(str, file_obj.data_blocks))
            mapping = f"{file_obj.index_block} -> [{data_blocks_str}]"
            print(f"{i:<5} | {filename:<20} | {mapping:<35}")

        # display disk status
        available_str = ", ".join(map(str, sorted(self.available_blocks)))
        used_str = ", ".join(map(str, sorted(self.used_blocks)))

        print("\nAvailable blocks:")
        print(available_str if available_str else "None")

        print("\nUsed blocks:")
        print(used_str if used_str else "None")
        print()


    def search_file(self, filename: str) -> bool:
        return filename in self.files


def display_menu():
    print("1. Allocate file")
    print("2. Delete file")
    print("3. Display allocation")
    print("4. Exit\n")


def main():
    while True:
        try:
            total_disk = int(input("Enter total number of disk blocks (default=100): "))

            if total_disk <= 0:
                print("Value must be positive.\n")
            else:
                simulator = IndexedAllocationSimulator(total_disk)
                break

        except ValueError:
            print("Please enter a valid number.\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            simulator.allocate_file()
        elif choice == "2":
            simulator.delete_file()
        elif choice == "3":
            simulator.display_allocation()
        elif choice == "4":
            print("\nExiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()