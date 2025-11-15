import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class Event:
    def __init__(self, date, details):
        self.date = date
        self.details = details
        self.completed = False

    def format_event(self):
        return f"{self.details} - {self.date.strftime('%Y/%m/%d')}"

class Eventlist:
    def __init__(self, parent):
        self.parent = parent
        self.events = []
        self.setup_ui()

    def setup_ui(self):      
        self.window = tk.Toplevel(self.parent)
        self.window.title("Event List")
        self.window.configure(bg="light blue")
        
        # Calculate the center position of the screen
        window_width = 500
        window_height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add border and padding
        self.list_frame = tk.Frame(self.window, bg="light grey", bd=2, relief=tk.SOLID)
        self.list_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.window, bg="light blue")
        self.button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Event Text widget with custom font and smaller width
        self.event_text = tk.Text(self.list_frame, width=20, height=15, font=("Arial", 10))
        self.event_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Add padding and spacing for buttons
        select_date_label = tk.Label(self.button_frame, text="Select Date", bg="light blue")
        select_date_label.grid(row=0, column=0, padx=5, pady=5)

        self.date_combobox = DateEntry(self.button_frame, width=12, font=("Arial", 10))
        self.date_combobox.grid(row=0, column=1, padx=5, pady=5)

        event_label = tk.Label(self.button_frame, text="Event Name", bg="light blue")
        event_label.grid(row=1, column=0, padx=5, pady=5)

        self.event_name_entry = tk.Entry(self.button_frame, width=12, font=("Arial", 10))
        self.event_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Using sticky to expand the entry width

        self.add_event_button = tk.Button(self.button_frame, text="Add Event", command=self.add_event, width=16, font=("Garamond", 15), bg="light grey")
        self.add_event_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.import_exit_button = tk.Button(self.button_frame, text="Export and Exit", command=self.import_and_exit, width=16, font=("Garamond", 15), bg="light grey")
        self.import_exit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def toggle_completion(self, event, var, index):
        event = self.events[index]
        event.completed = not event.completed  # Toggle completion status
        self.update_event_list()  # Update event list to reflect changes

    def update_event_list(self):
        self.event_text.delete("1.0", tk.END)

        # Separate completed and uncompleted events
        completed_events = []
        uncompleted_events = []

        for index, event in enumerate(self.events):
            event_str = event.format_event()
            if event.completed:
                completed_events.append((index, event_str))
            else:
                uncompleted_events.append((index, event_str))

        # Sort both lists by date
        completed_events.sort(key=lambda x: datetime.strptime(x[1].split(' - ')[1], '%Y/%m/%d'))
        uncompleted_events.sort(key=lambda x: datetime.strptime(x[1].split(' - ')[1], '%Y/%m/%d'))

        # Insert uncompleted events
        for index, event_str in uncompleted_events:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.event_text, variable=var, command=lambda event=self.events[index], var=var, index=index: self.toggle_completion(event, var, index))
            self.event_text.window_create(tk.END, window=cb)
            self.event_text.insert(tk.END, event_str + "\n")

        # Insert completed events
        for index, event_str in completed_events:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.event_text, variable=var, command=lambda event=self.events[index], var=var, index=index: self.toggle_completion(event, var, index))
            self.event_text.window_create(tk.END, window=cb)
            self.event_text.insert(tk.END, event_str + " (Completed)\n")

    def add_event(self):
        # Get event name and selected date
        event_name = self.event_name_entry.get().strip()
        selected_date = self.date_combobox.get_date() 
        if event_name and selected_date:
            # Create new Event object
            event = Event(selected_date, event_name)
            self.events.append(event)
            # Update event list
            self.update_event_list()
            # Clear event name entry
            self.event_name_entry.delete(0, tk.END)
            # Show success message
            messagebox.showinfo("Success", f"Event '{event_name}' on {selected_date.strftime('%Y-%m-%d')} has been saved successfully!")
        elif not selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date.")
        else:
            messagebox.showwarning("No Event Name", "Please enter an event name.")       
        
    def import_and_exit(self):
        # Ask for filename to save the data
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            # Open the file and write uncompleted events
            with open(filename, 'w') as file:
                for event in self.events:
                    if not event.completed:
                        file.write(f"{event.date.strftime('%Y-%m-%d')}, {event.details}\n")
            # Show success message and close the window
            messagebox.showinfo("Success", "Your events have been saved successfully!")
            self.window.destroy()

            
class FileImportWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        # Create a new window
        self.window = tk.Toplevel(self.parent)
        self.window.title("File Import")
        self.window.configure(bg="light blue")
        
        # Calculate the center position of the screen
        window_width = 500
        window_height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Label for file import
        label = tk.Label(self.window, text="Import data from file:", bg="light blue", font=("Garamond", 30))
        label.pack(padx=70, pady=70)

        # Button to import data
        button_import = tk.Button(self.window, text="Import Data", command=self.import_data, font=("Garamond", 15), bg="light grey")
        button_import.pack(padx=20, pady=20)

    def import_data(self):
        # Ask for filename to import data
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r') as file:
                for line in file:
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) == 2:  # Assuming date and event name
                        # Parse date and create Event object
                        date_str, event_name = parts
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        event = Event(date, event_name)
                        # Call callback function to add event
                        self.callback(event)
                    else:
                        messagebox.showerror("Error", "Invalid data format in the file.")
        self.window.destroy()


class App:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        # Set up main window
        self.root.title("TODO O'clock")
        self.root.configure(bg="light blue")

        # Create welcome label
        self.welcome_label = tk.Label(self.root, text="Welcome to TODO O'clock!", bg="light blue", font=("Garamond", 30))
        self.welcome_label.pack(padx=70, pady=70)

        # Create explore button
        self.explore_button = tk.Button(self.root, text="Explore!", command=self.show_file_import_window, font=("Garamond", 15), bg="light grey")
        self.explore_button.pack(padx=20, pady=20)

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

    def show_file_import_window(self):
        # Hide main window and show file import window
        self.root.withdraw()
        FileImportWindow(self.root, self.import_data)

    def import_data(self, event):
        # Check if event list window is already created, if not, create one
        if not hasattr(self, 'eventlist_window'):
            self.eventlist_window = Eventlist(self.root)
        # Add imported event to event list
        self.eventlist_window.events.append(event)
        self.eventlist_window.update_event_list()
        
        if hasattr(self, 'file_import_window'):
            self.file_import_window.window.destroy()

if __name__ == "__main__":
    # Create main Tkinter window
    root = tk.Tk()
    root.title("TODO O'clock")

    # Initialize the application
    app = App(root)

    # Start the main event loop
    root.mainloop()
