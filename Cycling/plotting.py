import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Load Excel file ---
def load_file(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name= sheet_name, engine="calamine")
    return df

# --- Filtering function ---
def filtering(df, num_of_filters, filter_column_names, ranges):
    if num_of_filters == len(filter_column_names) and num_of_filters == len(ranges):
        filtered_df = df.copy()
        for num in range(num_of_filters):
            filtered_df = filtered_df[filtered_df[filter_column_names[num]].isin(ranges[num])]
        return filtered_df
    else:
        raise ValueError("num_of_filters, filter_column_names, and ranges must have the same length")

#Plotting cell potential (V) vs specific capacity (mAh/g)

def ploting(df, multiple_graphs, legends, column_filter_name, filter_sequence, column_X, column_Y, plot_title):
    
    # 1. Set a good figure size at the start
    plt.figure(figsize=(8, 6)) # <--- ADDED
    
    if multiple_graphs == True:
        for step in filter_sequence:
            subset = df[df[column_filter_name] == step]
            plt.plot(subset[column_X], subset[column_Y], 
                     label=f"{column_filter_name} {step}",
                     linewidth=4,     # The thin line
                     linestyle='--',        # The marker shape
                     marker = 'o',
                     markersize=4,      # Make markers smaller
                     markevery=200
                     )
        
        plt.xlabel(column_X) 
        plt.ylabel(column_Y)
        plt.title(plot_title)
        if legends:
         plt.legend()
        plt.grid(True)
    else:
        plt.plot(df[column_X], df[column_Y], 
                    linewidth=4,     # The thin line
                    linestyle='--',        # The marker shape
                    marker = 'o',
                    markersize=4,      # Make markers smaller
                    markevery=200)
        plt.xlabel(column_X) 
        plt.ylabel(column_Y)
        plt.title(plot_title)
        if legends:
         plt.legend()
        plt.grid(True)
        
    # 2. Add tight_layout to fix spacing
    plt.tight_layout() # <--- ADDED
        
    # Make sure the folder exists
    save_folder = "Cycling/plots/NMC_200_73"
    os.makedirs(save_folder, exist_ok=True)

    # Replace invalid filename characters
    safe_title = plot_title.replace(" ", "_").replace("/", "_")
    save_name = safe_title + ".png"
    save_path = os.path.join(save_folder, save_name)
    
    if os.path.exists(save_path):
        response = input(f"⚠️ File '{save_name}' already exists. Overwrite? (y/n): ").strip().lower()
        if response != "y":
            print("❌ Plot not saved.")
            plt.close()
            return

    # Save the plot
    plt.savefig(save_path) # <--- MODIFIED
    plt.close() # Good practice to close plot after saving
    print(f"Plot saved to {save_path}")


df = load_file("Cycling/Data/Moha_NMC_200_73_Channel_12_Wb_1.xlsx", "Channel-12_1")
cycles = sorted(df["Cycle_Index"].unique())
    
selected_cycles = sorted(set(cycles[:9] + [c for c in cycles if c % 5 == 0] + cycles[-3:-1]))
print("Selected cycles:", selected_cycles)

filtered_df = filtering(df, 3, ["Step_Index", "Voltage(V)", "Cycle_Index"], [[3,7],[2.5], selected_cycles])
ploting(filtered_df, True, True, "Cycle_Index", selected_cycles, "Cycle_Index", "Specific Capacity (mAh/g)" , "discharge retention")
filtered_df = filtering(df, 3, ["Step_Index", "Voltage(V)", "Cycle_Index"], [[2,6],[4.2], selected_cycles])
ploting(filtered_df, True, True, "Cycle_Index", selected_cycles, "Cycle_Index", "Specific Capacity (mAh/g)" , "charge retention")
filtered_df = filtering(df, 2, ["Step_Index", "Cycle_Index"], [[2,6], selected_cycles])
ploting(filtered_df, True, True, "Cycle_Index", selected_cycles, "Specific Capacity (mAh/g)", "Voltage(V)", "Charging_all plot of Voltage (V) vs Specific Capacity (mAh/g)")
filtered_df = filtering(df, 2, ["Step_Index", "Cycle_Index"], [[3,7], selected_cycles])
ploting(filtered_df, True, True, "Cycle_Index", selected_cycles, "Specific Capacity (mAh/g)", "Voltage(V)", "discharging_all Plot of Voltage (V) vs Specific Capacity (mAh/g)")


#charge and discharge on the same graph 1-3-5-10-25-last cycle add a range for cycles show every 5 cycles or 10
## state in the report that I used the theoretical capacity that the company provided to make sure that I have the right C rates