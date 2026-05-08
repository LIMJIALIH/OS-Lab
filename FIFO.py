def FIFO(pages, frame_size):
    # Initialize frames array with None values (pre-allocate memory)
    frames = [None] * frame_size
    page_faults = 0  # Counter for page faults (page not in memory)
    replace = 0  # Pointer to track which frame position to replace next (FIFO order)

    print(f"Number of Frames: {frame_size}")
    print(f"Page References: {pages}\n")

    # Create table header
    print(f"{'Step':<8} {'Page':<8} {'Status':<12} {'Frames':<30}")
    print("-" * 50)

    # Process each page reference
    for i in range(len(pages)):
        status = "Hit"
        # Check if page is already in memory
        if pages[i] not in frames:
            # Page not found - PAGE FAULT occurred
            status = "Fault"
            frames[replace] = pages[i]  # Replace page at current pointer position
            replace = (replace + 1) % frame_size  # Move pointer to next frame (circular)
            page_faults += 1  # Increment fault counter
        display_frames = [f for f in frames if f is not None] # Filter out None values to display only actual pages in memory
        # Print as table row
        print(f"{i+1:<8} {pages[i]:<8} {status:<12} {str(display_frames):<30}")

    # Print statistics
    print("=" * 50)
    print(f"Total Page Hits: {len(pages) - page_faults}")
    print(f"Total Page Faults: {page_faults}")
    print(f"Page Fault Rate: {page_faults / len(pages) * 100:.2f}%")
    print("=" * 50)

def valid_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Value must be a greater than 0. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def positive_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value must be a positive integer. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    pages = []
    print("=" * 50)
    print("FIRST IN FIRST OUT (FIFO) PAGE REPLACEMENT")
    print("=" * 50)
    # Get frame size from user
    frame_size = valid_input("Enter the number of frames: ")
    # Get number of page references from user
    no_pages = valid_input("Enter the number of pages: ")
    # Collect page references from user
    for i in range(no_pages):
        page = positive_input(f"{i+1}. Enter page number: ")
        pages.append(page)
    print("=" * 50)
    # Run FIFO simulation
    FIFO(pages, frame_size)