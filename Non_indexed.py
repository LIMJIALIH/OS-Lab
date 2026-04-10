from dataclasses import dataclass

@dataclass
class File:
    filename : str
    starting_block : int
    number_of_blocks : int
    

class NonIndexedAllocation:
    def __init__(self, disk_size=100):
        self.files : list[File] = []
        self.disk_size : int = disk_size
        self.available_blocks : set[int] = set(range(disk_size))
        self.used_blocks : set[int] = set()
    
    def allocate_file(self)-> bool:
        if len(self.available_blocks)<1:
            return False
        while True:
            filename = str(input("\nEnter your filename: "))

            if self.search_file(filename):
                print("\nThe filename already existed. Please try another name.")
                continue
            else:
                break
        while True:
            try:
                size = int(input(f"\nPlease enter the file size (Remaining = {len(self.available_blocks)})"))
                if size > len(self.available_blocks):
                    print("\nInsufficient")
                    continue
                elif size <=0 :
                    print("\nPlease enter a positive number")
                    continue
                else:
                    break
            except ValueError:
                print("\nPlease enter an integer")
                
        # find whether there is enough space
        start_block = self.find_consecutive_blocks(size)
        if start_block is not None:
            self.files.append(File(filename=filename, starting_block=start_block, number_of_blocks=size))
            # update available and used blocks
            self.available_blocks.difference_update(range(start_block, start_block + size))
            self.used_blocks.update(range(start_block, start_block + size))
            return True
        else:
            return False
            
    # helper function to search whether there is duplicated filename
    def search_file(self,filename):
        for file in self.files:
            if file.filename == filename:
                return True
        return False       

    
    def delete_file(self)->bool:
        if not self.files:
            print("\nNo files to delete.")
            return False
        
        filename = input("\nEnter filename to delete: ").strip()
        
        file_to_delete = None
        for file in self.files:
            if file.filename == filename:
                file_to_delete = file
                break
        
        if file_to_delete is None:
            print(f"\nFile '{filename}' not found.")
            return False
        
        blocks_to_free = range(file_to_delete.starting_block, file_to_delete.starting_block + file_to_delete.number_of_blocks)
        
        # Update available and used blocks
        self.available_blocks.update(blocks_to_free)
        self.used_blocks.difference_update(blocks_to_free)
        
        # Remove from files list
        self.files.remove(file_to_delete)
        
        return True
        
    def display_allocation(self):
        print("\nCurrent File Allocation:\n")

        print(f"{'No.':<5} | {'Filename':<20} | {'Data Blocks':<35}")
        print("-" * 65)

        for i, file in enumerate(self.files, start=1):
            data_blocks_str = ",".join(map(str, range(file.starting_block, file.starting_block + file.number_of_blocks)))
            print(f"{i:<5} | {file.filename:<20} | {data_blocks_str:<35}")

        # display disk status
        available_str = ", ".join(map(str, sorted(self.available_blocks)))
        used_str = ", ".join(map(str, sorted(self.used_blocks)))

        print("\nAvailable blocks:")
        print(available_str if available_str else "None")

        print("\nUsed blocks:")
        print(used_str if used_str else "None")
        print()
    
    # helper function to find if there is available starting block
    def find_consecutive_blocks(self,size)-> int | None:
        if size == 1:
            for block in self.available_blocks:
                return block
        elif len(self.available_blocks) < size:
            return None
        else:
            available_blocks_list=  sorted(list(self.available_blocks))
            start_block = None               
            
            # use kinda sliding window to check only the required elements , eg if size = 3, check only from 0-3, 1-4, 2-5 etc...
            for i in range(len(available_blocks_list)-size+1):
                arr = available_blocks_list[i:i+size]
                is_consecutive = True
                
                for j in range(len(arr)-1):
                    if arr[j+1]-arr[j] != 1:
                        is_consecutive = False
                        break
                
                if is_consecutive:
                    start_block = arr[0]
                    break
            return start_block
                        
                        

def display_menu():
    print("1. Allocate file")
    print("2. Delete file")
    print("3. Display allocation")
    print("4. Exit\n")
    

def main():
    try:
        disk_size = int(input("Please enter the disk size (default=100): "))
        simulator = NonIndexedAllocation(disk_size=disk_size)
        
    except ValueError:
        disk_size = 100
        simulator = NonIndexedAllocation(disk_size=disk_size)

    
    while True:
        try:
            display_menu()
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                if simulator.allocate_file():
                    print("\nFile allocated successfully")
                    continue
                else:
                    print("\nFile allocation failed")
                    continue
            elif choice == 2:
                if simulator.delete_file():
                    print("\nFile deleted successfully")
                    continue
                else:
                    print("\nFile deletion failed")
                    continue
            elif choice == 3:
                simulator.display_allocation()
                continue
            elif choice == 4:
                break
            else:
                print("\nInvalid choice . Please try again")         
                
            
        except ValueError:
            print("please enter a choice between 1 to 4")
        
        

if __name__ == "__main__":
    main()