import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import askyesno, showwarning, showerror

from generator import generate_code

import sqlite3 as sql


class App(tk.Frame):
    def __init__(self, master):
        # Database Initialization
        connection = sql.connect("__database__")
        self.dbc = connection.cursor()
        self.dbc.execute("CREATE TABLE discount_data(id, code, use_count)")
        res =  self.dbc.execute("SELECT * FROM discount_data")
        print(res.fetchone())

        super().__init__(master)
        self.pack()
        self.winfo_toplevel().title("Umbra Memoire Discount Code Generator")

        tk.Label(self, text="Data :").grid(row=2, column=0, sticky="nes")

        self.entry_data_entry = tk.Entry(self, width=40)
        self.entry_data_entry.grid(row=2, column=1)

        self.button_data_entry = tk.Button(self, text="Add Data", command=self.add_data)
        self.button_data_entry.grid(row=2, column=2, padx=(10, 10), pady=(5, 5), sticky="ew")
        
        tk.Label(self, text="Entries :").grid(row=3, column=0, sticky="ne")

        self.list_data_entries = tk.Listbox(self, width=40)
        self.list_data_entries.grid(row=3, column=1)

        self.button_data_delete = tk.Button(self, text="Remove Data", command=self.delete_data)
        self.button_data_delete.grid(row=3, column=2, padx=(10, 10), sticky="new")

        self.button_generate_code = tk.Button(self, text="Generate Code", command=self.generate_code)
        self.button_generate_code.grid(row=4, column=0, padx=10, pady=(10, 3), columnspan=3, sticky="ew")

        self.generated_identifier = ""
        self.generated_code = ""
        self.stringvar_generated_code = tk.StringVar(self)
        self.entry_generated_code = tk.Entry(self, textvariable=self.stringvar_generated_code, disabledbackground="white", disabledforeground="black")
        self.entry_generated_code.grid(row=5, column=0, columnspan=2, padx=(10, 0), pady=(2, 5), sticky="sew")

        self.button_save_generated_code = tk.Button(self, text="Save Code", command=self.save_generated_code)
        self.button_save_generated_code.grid(row=5, column=2, padx=10, sticky="new")

        ttk.Separator(self, orient="horizontal").grid(row=6, column=0, padx=10, pady=5, columnspan=3, sticky="new")

        self.list_database_entries = tk.Listbox(self)
        self.list_database_entries.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="new")
        self.after(0, self.loop)
    
    def loop(self):
        if self.entry_data_entry.get() == "":
            self.button_data_entry.configure(state="disabled")
        else:
            self.button_data_entry.configure(state="normal")
        
        if self.list_data_entries.size() <= 0:
            self.button_data_delete.configure(state="disabled")
            self.button_generate_code.configure(state="disabled")
        else:
            self.button_data_delete.configure(state="normal")
            self.button_generate_code.configure(state="normal")

        if self.generated_code == "" or self.generated_code == None:
            self.entry_generated_code.configure(state="disabled")
        else:
            self.entry_generated_code.configure(state="normal")
        self.stringvar_generated_code.set(self.generated_code)

        self.after(50, self.loop)

    def add_data(self):
        data = self.entry_data_entry.get()
        if data == "": return
        
        self.list_data_entries.insert(self.list_data_entries.size(), data)
        self.entry_data_entry.delete(0, tk.END)

    def delete_data(self):
        index = self.list_data_entries.curselection()[0]
        self.list_data_entries.delete(index)

    def generate_code(self):
        datas = [self.list_data_entries.get(i) for i in range(self.list_data_entries.size())]
        self.list_data_entries.delete(0, tk.END)

        code = generate_code(*datas)
        self.generated_code = " ".join(code[0])
        self.generated_identifier = code[1]

    def save_generated_code(self):
        if self.saved_to == None or self.saved_to == "":
            showwarning("Code is not generated yet!", "Please generate the code first before saving")
            return

        file_data = []
        with open(self.saved_to, "r") as f:
            file_data = f.readlines()

        parsed_data = [i.replace("\n", "").split(", ") for i in file_data]
        if len(parsed_data) > 0:
            parsed_data.pop(0)
        print(parsed_data)

        if self.generated_code in [i[1] for i in parsed_data]:
            showerror("Collision Detected", "same unique code detected! try add or subtract any data")
            return

        with open(self.saved_to, "a") as f:
            if len(file_data) <= 0:
                f.writelines("Index, Unique Identifier, Voucher / Discount Code\n")
            try:
                if "\n" not in file_data[-1]:
                    f.write("\n")
            except: pass
            f.writelines(", ".join([str(len(file_data)), self.generated_identifier, self.generated_code]) + "\n")
        
        self.generated_code = ""
        self.generated_identifier = ""
        self.stringvar_generated_code.set("")
        print("Successfully Generated Code")

root = tk.Tk()
root.resizable(False, False)
myapp = App(root)
myapp.mainloop()