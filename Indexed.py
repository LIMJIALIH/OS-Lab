import random
from dataclasses import  dataclass
from typing import List, Dict
@dataclass
class File:
    name : str
    size : int
    index_block : int
    data_blocks : List[int]
    
    

class IndexedAllocationSimulator:
    
    def __init__(self, total_disk:int = 100):
        self.total_disk = total_disk
        self.files : Dict[str, File] = {}
        self.available_blocks = set(range(total_disk))
        self.used_blocks = set()
        
    def allocate_file(self):
        # check duplicated filename
        while True:
            filename = str(input("Enter the file name:"))
            if filename.strip() == "4":
                return
            if self.search_file(filename):
                print(f"File {filename} already exists , please try a new filename ")
                continue
            
            # check whether the current available blocks sufficient to fit the incoming size blocks
            while True:
                size = int(input("Enter the size of the file: "))
                # size + 1 to include the data blocks and index block
                if size + 1 > len(self.available_blocks):
                    print(f"Insufficient space! Current available space : {max(len(self.available_blocks)-1,0)}")
                    continue
                break
            break
        
        # add index block
        index_block = random.choice(list(self.available_blocks))
        self.available_blocks.remove(index_block)
        self.used_blocks.add(index_block)
        
        # add data blocks
        data_blocks = []
        for i in range(size):
            
            # randomly select data blocks from the available list
            data_block = random.choice(list(self.available_blocks))
            self.available_blocks.remove(data_block)
            self.used_blocks.add(data_block)
            data_blocks.append(data_block)
        
        self.files[filename] = File(filename, size, index_block, data_blocks)   
        print("File allocated successfully\n\n")         
                        
        return

    def delete_file(self):
        
        # check existence of file
        while True:
            filename = str(input("Enter the file name(4 to exit): "))
            if filename.strip() == "4":
                return
            if not self.search_file(filename):
                print(f"File {filename} does not exist , please try a new filename ")
                continue
            # reset the available blocks information
            self.available_blocks.update(self.files[filename].data_blocks)
            self.available_blocks.add(self.files[filename].index_block)
            
            # reset the used blocks information
            self.used_blocks.remove(self.files[filename].index_block)
            for data_block in self.files[filename].data_blocks:
                self.used_blocks.remove(data_block)
            del self.files[filename]
            break
        print("File deleted successfully")
        return
    
    
    def display_allocation(self):
        # column name
        print(f"{'No.':<5} | {'Filename':<20} | {'Index Block':<12} | {'Data Blocks':<30}")
        print("-" * 75)

        # file info
        for i, (filename, file_obj) in enumerate(self.files.items(), start=1):
            # transform list of data blocks to string
            data_blocks_str = ", ".join(map(str, file_obj.data_blocks))
            print(f"{i:<5} | {filename:<20} | {file_obj.index_block:<12} | {data_blocks_str:<30}")

        # display available and used blocks
        available_str = ", ".join(map(str, sorted(self.available_blocks)))
        used_str = ", ".join(map(str, sorted(self.used_blocks)))

        print("\nAvailable blocks:")
        print(available_str if available_str else "None")
        
        print("\nUsed blocks:")
        print(used_str if used_str else "None")
        print()
    
    def search_file(self, filename: str) -> bool:
        
        # helper function to search existence of a specific file
        return filename in self.files



def display_menu():
    print("1. allocate file")
    print("2. delete file")
    print("3. display allocation")
    print("4. exit\n")
    
def main():
    while True:
        try:
            total_disk = int(input("Enter the total number of disk blocks (default=100): "))
            if total_disk <= 0:
                print("The value of total disk must be positive")
            else:
                simulator = IndexedAllocationSimulator(total_disk)
                break     
        except ValueError:
            print("Please provide a number")
        
    while True:
        display_menu()
        choice = str(input("Enter your choices (1-4): "))
        if choice.strip() == "1":
            simulator.allocate_file()
        elif choice.strip() == "2":
            simulator.delete_file()
        elif choice.strip() == "3":
            simulator.display_allocation()
        elif choice.strip() == "4":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
            

if __name__ == "__main__":
    main()