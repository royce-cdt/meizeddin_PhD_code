import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, filedialog, Checkbutton, IntVar, StringVar, OptionMenu, Listbox, MULTIPLE, messagebox, Scrollbar, END

def ploting(df, multiple_graphs, column_filter_name, filter_sequence, column_X, column_Y, plot_title):
    plt.figure()
    
    if multiple_graphs:
        for step in filter_sequence:
            subset = df[df[column_filter_name] == step]
            plt.plot(
                subset[column_X],
                subset[column_Y],
                marker='o',
                linewidth=0.8,
                label=f"{column_filter_name} {step}"
            )
        plt.xlabel(column_X)
        plt.ylabel(column_Y)
        plt.title(plot_title)
        plt.legend()
        plt.grid(True)
    else:
        plt.plot(df[column_X], df[column_Y], marker='o', linewidth=0.8)
        plt.xlabel(column_X)
        plt.ylabel(column_Y)
        plt.title(plot_title)
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
            messagebox.showinfo("Cancelled", "Plot not saved.")
            plt.close()
            return

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    messagebox.showinfo("Saved", f"✅ Plot saved to:\n{save_path}")

# === GUI ===
root = Tk()
root.title("Excel Plotter")
df = None
columns = []

# --- Functions ---
def select_file():
    global df, columns
    file_path = filedialog.askopenfilename(
        title="Select Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if file_path:
        sheet_name = sheet_entry.get() or "Sheet1"
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        columns = list(df.columns)

        # Populate dropdowns
        filter_column_menu["menu"].delete(0, "end")
        column_X_menu["menu"].delete(0, "end")
        column_Y_menu["menu"].delete(0, "end")
        for col in columns:
            filter_column_menu["menu"].add_command(label=col, command=lambda value=col: filter_column_var.set(value))
            column_X_menu["menu"].add_command(label=col, command=lambda value=col: column_X_var.set(value))
            column_Y_menu["menu"].add_command(label=col, command=lambda value=col: column_Y_var.set(value))

        # Set defaults
        if len(columns) >= 3:
            filter_column_var.set(columns[2])
            column_X_var.set(columns[0])
            column_Y_var.set(columns[1])

        update_filter_values()

def update_filter_values(*args):
    # Populate Listbox with unique values from selected filter column
    filter_sequence_listbox.delete(0, END)
    if df is not None and filter_column_var.get() in df.columns:
        unique_values = sorted(df[filter_column_var.get()].unique())
        for val in unique_values:
            filter_sequence_listbox.insert(END, val)

def run_plot():
    if df is None:
        messagebox.showerror("Error", "No Excel file loaded!")
        return

    multiple_graphs = bool(multiple_graphs_var.get())
    column_filter_name = filter_column_var.get()
    selected_indices = filter_sequence_listbox.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No filter sequence selected!")
        return
    filter_sequence = [filter_sequence_listbox.get(i) for i in selected_indices]
    column_X = column_X_var.get()
    column_Y = column_Y_var.get()
    plot_title = plot_title_var.get() or "Plot"

    ploting(df, multiple_graphs, column_filter_name, filter_sequence, column_X, column_Y, plot_title)

# --- Widgets ---
Label(root, text="Sheet Name:").grid(row=0, column=0)
sheet_entry = Entry(root)
sheet_entry.grid(row=0, column=1)
Button(root, text="Select Excel File", command=select_file).grid(row=0, column=2)

multiple_graphs_var = IntVar()
Checkbutton(root, text="Multiple Graphs", variable=multiple_graphs_var).grid(row=1, column=0, columnspan=2)

Label(root, text="Filter Column:").grid(row=2, column=0)
filter_column_var = StringVar()
filter_column_menu = OptionMenu(root, filter_column_var, "")
filter_column_menu.grid(row=2, column=1)
filter_column_var.trace("w", update_filter_values)

Label(root, text="Filter Sequence:").grid(row=3, column=0)
filter_sequence_listbox = Listbox(root, selectmode=MULTIPLE, height=6)
filter_sequence_listbox.grid(row=3, column=1)
scrollbar = Scrollbar(root, orient="vertical", command=filter_sequence_listbox.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
filter_sequence_listbox.config(yscrollcommand=scrollbar.set)

Label(root, text="X Column:").grid(row=4, column=0)
column_X_var = StringVar()
column_X_menu = OptionMenu(root, column_X_var, "")
column_X_menu.grid(row=4, column=1)

Label(root, text="Y Column:").grid(row=5, column=0)
column_Y_var = StringVar()
column_Y_menu = OptionMenu(root, column_Y_var, "")
column_Y_menu.grid(row=5, column=1)

Label(root, text="Plot Title:").grid(row=6, column=0)
plot_title_var = StringVar()
Entry(root, textvariable=plot_title_var).grid(row=6, column=1)

Button(root, text="Run Plot", command=run_plot).grid(row=7, column=0, columnspan=2)

root.mainloop()
