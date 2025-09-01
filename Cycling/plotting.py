import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog, messagebox

# load file
df = pd.read_excel("Cycling/Data/Moha_NMC811_Q_Channel_7_Wb_1.xlsx", sheet_name= "Channel-7_1")

charging_df = df[df["Step_Index"].isin([2,5])]
discharging_df = df[df["Step_Index"].isin([3,6])]

#checking column names
print(df.shape)

#Plotting cell potential (V) vs specific capacity (mAh/g)

def ploting(df, multiple_graphs, column_filter_name, filter_sequence, column_X, column_Y, plot_title):
    if multiple_graphs == True:
        for step in filter_sequence:
            subset = df[df[column_filter_name] == step]
            plt.plot(subset[column_X], subset[column_Y], marker='o', label=f"{column_filter_name} {step}")
        
        plt.xlabel(column_X) 
        plt.ylabel(column_Y)
        plt.title(plot_title)
        plt.legend()
        plt.grid(True)
    else:
        plt.plot(df[column_X], df[column_Y], linewidth=0.8, marker = "o")
        plt.xlabel(column_X) 
        plt.ylabel(column_Y)
        plt.title(plot_title)
        plt.legend()
        plt.grid(True)
        
    # Make sure the folder exists
    save_folder = "Cycling/plots"
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
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved to {save_path}")


ploting(charging_df, True, "Cycle_Index", [1,4,7,10,11,14, 16], "Specific Capacity (mAh/g)", "Voltage(V)", "Charging_all plot of Voltage (V) vs Specific Capacity (mAh/g)")
ploting(charging_df, True, "Cycle_Index", [4,7,10,11,14, 16], "Specific Capacity (mAh/g)", "Voltage(V)", "Charging plot of Voltage (V) vs Specific Capacity (mAh/g)")

ploting(discharging_df, True, "Cycle_Index", [1,4,7,10,11,14, 16], "Specific Capacity (mAh/g)", "Voltage(V)", "discharging_all Plot of Voltage (V) vs Specific Capacity (mAh/g)")
ploting(discharging_df, True, "Cycle_Index", [4,7,10,11,14, 16], "Specific Capacity (mAh/g)", "Voltage(V)", "discharging plot of Voltage (V) vs Specific Capacity (mAh/g)")