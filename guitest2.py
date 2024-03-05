import tkinter as tk

# Create the main application window
root = tk.Tk()

# Create a label in the main window
label_main = tk.Label(root, text="Main Window")
label_main.pack()

# Function to create a new window
def create_new_window():
    new_window = tk.Toplevel(root)  # Create a new toplevel window
    label_new = tk.Label(new_window, text="New Window")
    label_new.pack()

# Button to create a new window
button = tk.Button(root, text="Create New Window", command=create_new_window)
button.pack()

# Run the Tkinter event loop
root.mainloop()