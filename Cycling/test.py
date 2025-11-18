import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Label, Entry, Button, filedialog, Checkbutton, IntVar, StringVar, Listbox, MULTIPLE, messagebox, Scrollbar, END, Toplevel
from tkinter import OptionMenu, StringVar

# === Load Excel file ===
def load_file(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# === Filtering function (sequential) ===
def filtering(df, filter_column_names, ranges):
    filtered_df = df.copy()
    for col, allowed_vals in zip(filter_column_names, ranges):
        filtered_df = filtered_df[filtered_df[col].isin(allowed_vals)]
    return filtered_df

# === Plotting function ===
def ploting(df, multiple_graphs, legends, column_filter_name, filter_sequence, column_X, column_Y, plot_title):
    if multiple_graphs:
        for step in filter_sequence:
            subset = df[df[column_filter_name] == step]
            plt.plot(subset[column_X], subset[column_Y], marker='o', label=f"{column_filter_name} {step}")
    else:
        plt.plot(df[column_X], df[column_Y], linewidth=0.8, marker='o')
    
    plt.xlabel(column_X)
    plt.ylabel(column_Y)
    plt.title(plot_title)
    if legends:
        plt.legend()
    plt.grid(True)

    save_folder = "Cycling/plots"
    os.makedirs(save_folder, exist_ok=True)
    safe_title = plot_title.replace(" ", "_").replace("/", "_")
    save_name = safe_title + ".png"
    save_path = os.path.join(save_folder, save_name)

    if os.path.exists(save_path):
        overwrite = messagebox.askyesno(
            "File exists",
            f"⚠️ File '{save_name}' already exists.\nDo you want to replace it?"
        )
        if not overwrite:
            plt.close()
            return

    plt.savefig(save_path)
    plt.close()
    messagebox.showinfo("Saved", f"✅ Plot saved to:\n{save_path}")

# === GUI ===
root = Tk()
root.title("Excel Plotter")
df = None
columns = []

# --- Select file ---
def select_file():
    global df, columns
    file_path = filedialog.askopenfilename(title="Select Excel file",
                                           filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        sheet_name = sheet_entry.get() or "Sheet1"
        df = load_file(file_path, sheet_name)
        columns = list(df.columns)

        # Populate filter columns Listbox
        filter_columns_listbox.delete(0, END)
        for col in columns:
            filter_columns_listbox.insert(END, col)

        # Populate X/Y dropdowns
        column_X_menu["menu"].delete(0, "end")
        column_Y_menu["menu"].delete(0, "end")
        for col in columns:
            column_X_menu["menu"].add_command(label=col, command=lambda v=col: column_X_var.set(v))
            column_Y_menu["menu"].add_command(label=col, command=lambda v=col: column_Y_var.set(v))
        if len(columns) >= 3:
            column_X_var.set(columns[0])
            column_Y_var.set(columns[1])

# --- Sequential filter selection ---
def select_filters_sequential():
    selected_cols = [filter_columns_listbox.get(i) for i in filter_columns_listbox.curselection()]
    if not selected_cols:
        messagebox.showerror("Error", "Select at least one filter column.")
        return

    top = Toplevel(root)
    top.title("Select Filter Values Sequentially")

    # Store selected ranges
    ranges = []

    current_df = df.copy()  # start with full df
    row = 0

    for col in selected_cols:
        Label(top, text=f"{col}:").grid(row=row, column=0, sticky="w")
        lb = Listbox(top, selectmode=MULTIPLE, height=6)
        # get unique values based on previously filtered df
        unique_vals = sorted(current_df[col].unique())
        for val in unique_vals:
            lb.insert(END, val)
        lb.grid(row=row, column=1)
        scrollbar = Scrollbar(top, orient="vertical", command=lb.yview)
        scrollbar.grid(row=row, column=2, sticky="ns")
        lb.config(yscrollcommand=scrollbar.set)

        def update_current_df(lb=lb, col=col):
            selected_vals = [lb.get(i) for i in lb.curselection()]
            if selected_vals:
                nonlocal current_df
                current_df = current_df[current_df[col].isin(selected_vals)]

        lb.bind("<<ListboxSelect>>", lambda e, lb=lb, col=col: update_current_df(lb, col))
        ranges.append(lb)
        row += 1

    def save_ranges():
        global selected_filter_columns, selected_filter_ranges
        selected_filter_columns = selected_cols
        selected_filter_ranges = [[lb.get(i) for i in lb.curselection()] for lb in ranges]
        top.destroy()

    Button(top, text="Save", command=save_ranges).grid(row=row, column=0, columnspan=2)

# --- Run plot ---
def run_plot():
    if df is None:
        messagebox.showerror("Error", "No Excel file loaded!")
        return

    multiple_graphs = bool(multiple_graphs_var.get())
    legends = bool(legends_var.get())
    column_X = column_X_var.get()
    column_Y = column_Y_var.get()
    plot_title = plot_title_var.get() or "Plot"

    # Apply sequential filters
    if 'selected_filter_columns' in globals() and selected_filter_columns:
        filtered_df = filtering(df, selected_filter_columns, selected_filter_ranges)
    else:
        filtered_df = df

    # Determine filter sequence for plotting (use first selected filter column)
    if selected_filter_columns:
        column_filter_name = selected_filter_columns[0]
        filter_sequence = selected_filter_ranges[0]
    else:
        column_filter_name = column_X
        filter_sequence = filtered_df[column_filter_name].unique()

    ploting(filtered_df, multiple_graphs, legends, column_filter_name, filter_sequence, column_X, column_Y, plot_title)

# --- Widgets ---
Label(root, text="Sheet Name:").grid(row=0, column=0)
sheet_entry = Entry(root)
sheet_entry.grid(row=0, column=1)
Button(root, text="Select Excel File", command=select_file).grid(row=0, column=2)

multiple_graphs_var = IntVar()
Checkbutton(root, text="Multiple Graphs", variable=multiple_graphs_var).grid(row=1, column=0)

legends_var = IntVar()
Checkbutton(root, text="Show Legends", variable=legends_var).grid(row=1, column=1)

# Filter column selection
Label(root, text="Filter Columns:").grid(row=2, column=0)
filter_columns_listbox = Listbox(root, selectmode=MULTIPLE, height=6)
filter_columns_listbox.grid(row=2, column=1)
Button(root, text="Select Filter Values Sequentially", command=select_filters_sequential).grid(row=2, column=2)

# X and Y columns
Label(root, text="X Column:").grid(row=3, column=0)
column_X_var = StringVar()
column_X_menu = OptionMenu(root, column_X_var, "")
column_X_menu.grid(row=3, column=1)

Label(root, text="Y Column:").grid(row=4, column=0)
column_Y_var = StringVar()
column_Y_menu = OptionMenu(root, column_Y_var, "")
column_Y_menu.grid(row=4, column=1)

Label(root, text="Plot Title:").grid(row=5, column=0)
plot_title_var = StringVar()
Entry(root, textvariable=plot_title_var).grid(row=5, column=1)

Button(root, text="Run Plot", command=run_plot).grid(row=6, column=0, columnspan=3)

root.mainloop()
