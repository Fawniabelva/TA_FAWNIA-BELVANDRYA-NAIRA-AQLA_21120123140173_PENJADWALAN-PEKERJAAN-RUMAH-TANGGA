import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, name, day, duration):
        self.name = name
        self.day = day
        self.duration = duration
    
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration


class TaskManager:
    def __init__(self):
        self.tasks = {day: [] for day in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]}
    
    def add_task(self, task):
        self.tasks[task.get_day()].append(task)
    
    def remove_task(self, task_name, day):
        self.tasks[day] = [task for task in self.tasks[day] if task.get_name() != task_name]
    
    def get_tasks(self, day):
        return self.tasks[day]

    def get_all_tasks(self):
        return self.tasks


def add_task():
    task_name = task_name_entry.get()
    task_day = day_var.get()
    task_duration = duration_entry.get()

    if task_name == "" or task_duration == "":
        messagebox.showwarning("Input Error", "Task name and duration cannot be empty")
        return

    if not task_duration.isdigit() or int(task_duration) <= 0:
        messagebox.showwarning("Input Error", "Duration must be a positive integer")
        return

    new_task = Task(task_name, task_day, int(task_duration))
    task_manager.add_task(new_task)
    update_task_list(task_day)

def remove_task():
    task_name = task_name_entry.get()
    task_day = day_var.get()

    if task_name == "":
        messagebox.showwarning("Input Error", "Task name cannot be empty")
        return

    task_manager.remove_task(task_name, task_day)
    update_task_list(task_day)

def update_task_list(day):
    tasks = task_manager.get_tasks(day)
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, f"{task.get_name()} (Duration: {task.get_duration()} mins)")

def update_day_tasks(*args):
    update_task_list(day_var.get())

def show_schedule():
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Complete Schedule")

    for day, tasks in task_manager.get_all_tasks().items():
        tk.Label(schedule_window, text=f"{day}:", font=("Arial", 12, "bold")).pack()
        if tasks:
            for task in tasks:
                tk.Label(schedule_window, text=f"  - {task.get_name()} ({task.get_duration()} mins)").pack()
        else:
            tk.Label(schedule_window, text="  No tasks").pack()

task_manager = TaskManager()
days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

root = tk.Tk()
root.title("Household Scheduling Application")

frame = tk.Frame(root)
frame.pack(pady=10)

task_name_label = tk.Label(frame, text="Task Name:")
task_name_label.grid(row=0, column=0, padx=5, pady=5)

task_name_entry = tk.Entry(frame)
task_name_entry.grid(row=0, column=1, padx=5, pady=5)

day_label = tk.Label(frame, text="Day:")
day_label.grid(row=1, column=0, padx=5, pady=5)

day_var = tk.StringVar()
day_var.set(days[0])
day_menu = tk.OptionMenu(frame, day_var, *days)
day_menu.grid(row=1, column=1, padx=5, pady=5)
day_var.trace("w", update_day_tasks)

duration_label = tk.Label(frame, text="Duration (mins):")
duration_label.grid(row=2, column=0, padx=5, pady=5)

duration_entry = tk.Entry(frame)
duration_entry.grid(row=2, column=1, padx=5, pady=5)

def validate_duration_input():
    if not duration_entry.get().isdigit():
        messagebox.showwarning("Input Error", "Duration can only be filled with numbers")
        duration_entry.delete(0, tk.END)

duration_entry.bind('<FocusOut>', lambda event: validate_duration_input())

day_menu = tk.OptionMenu(frame, day_var, *days)
day_menu.config(bg="lightyellow")  # Menambahkan warna latar belakang untuk dropdown menu
day_menu["menu"].config(bg="lightyellow")  # Menambahkan warna latar belakang untuk menu dropdown
day_menu.grid(row=1, column=1, padx=5, pady=5)

add_task_button = tk.Button(frame, text="Add Task", command=add_task, bg="lightblue")
add_task_button.grid(row=3, column=0, padx=5, pady=5)

remove_task_button = tk.Button(frame, text="Remove Task", command=remove_task, bg="lightcoral")
remove_task_button.grid(row=3, column=1, padx=5, pady=5)

task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)

show_schedule_button = tk.Button(root, text="Show Complete Schedule", command=show_schedule, bg="lightgreen")
show_schedule_button.pack(pady=10)

root.mainloop()
