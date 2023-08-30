# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:37:20 2023

@author: pablo.mena
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

maxgroups = 10

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Plotter")
        self.root.geometry('1600x1000')
        self.root.state('zoomed')


        # Close button
        btn_close = ttk.Button(self.root, text='X', command=self.root.destroy)
        btn_close.place(relx=1, y=0, anchor=tk.NE)

        self.data = None

        # Create frames for controls and graph
        self.frame_controls = ttk.Frame(self.root, width=300)
        self.frame_controls.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_graph = ttk.Frame(self.root)
        self.frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_controls()
        self.spinner = tk.Label(self.root)
        self.spinner_image = tk.PhotoImage(file="path_to_spinner.gif")  # Cambia esto a la ruta de tu GIF
        self.spinner.config(image=self.spinner_image)
        
        self.cancel_btn = ttk.Button(self.frame_controls, text="Cancelar", command=self.abort_graph, state=tk.DISABLED)
        self.cancel_btn.pack(pady=20)

        
    def build_controls(self):
        self.import_btn = ttk.Button(self.frame_controls, text="Import CSV", command=self.import_csv)
        self.import_btn.pack(pady=20)
    
        ttk.Label(self.frame_controls, text="X-Axis:").pack(pady=5)
        self.combo1 = ttk.Combobox(self.frame_controls, values=[])
        self.combo1.pack(pady=5, fill=tk.X)
    
        ttk.Label(self.frame_controls, text="Y-Axis:").pack(pady=5)
        self.combo2 = ttk.Combobox(self.frame_controls, values=[])
        self.combo2.pack(pady=5, fill=tk.X)
    
        ttk.Label(self.frame_controls, text="Group:").pack(pady=5)
        self.combo3 = ttk.Combobox(self.frame_controls, values=[])
        self.combo3.pack(pady=5, fill=tk.X)
    
        ttk.Label(self.frame_controls, text="Facet:").pack(pady=5)
        self.combo4 = ttk.Combobox(self.frame_controls, values=[])
        self.combo4.pack(pady=5, fill=tk.X)
    
        self.plot_btn = ttk.Button(self.frame_controls, text="Plot Data", command=self.plot_data)
        self.plot_btn.pack(pady=20)
        
                # Para el nombre del eje X:
        self.label_xaxis = ttk.Label(self.frame_controls, text="Nombre Eje X:")
        self.label_xaxis.pack(pady=5)
        
        self.entry_xaxis = ttk.Entry(self.frame_controls)
        self.entry_xaxis.pack(pady=5)
        
        # Para el nombre del eje Y:
        self.label_yaxis = ttk.Label(self.frame_controls, text="Nombre Eje Y:")
        self.label_yaxis.pack(pady=5)
        
        self.entry_yaxis = ttk.Entry(self.frame_controls)
        self.entry_yaxis.pack(pady=5)
                
        self.label_xaxis_min = ttk.Label(self.frame_controls, text="Min X-axis:")
        self.label_xaxis_min.pack(pady=5)
        self.entry_xaxis_min = ttk.Entry(self.frame_controls)
        self.entry_xaxis_min.pack(pady=5)
        
        self.label_xaxis_max = ttk.Label(self.frame_controls, text="Max X-axis:")
        self.label_xaxis_max.pack(pady=5)
        self.entry_xaxis_max = ttk.Entry(self.frame_controls)
        self.entry_xaxis_max.pack(pady=5)
        
        self.label_yaxis_min = ttk.Label(self.frame_controls, text="Min Y-axis:")
        self.label_yaxis_min.pack(pady=5)
        self.entry_yaxis_min = ttk.Entry(self.frame_controls)
        self.entry_yaxis_min.pack(pady=5)
        
        self.label_yaxis_max = ttk.Label(self.frame_controls, text="Max Y-axis:")
        self.label_yaxis_max.pack(pady=5)
        self.entry_yaxis_max = ttk.Entry(self.frame_controls)
        self.entry_yaxis_max.pack(pady=5)

    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            self.data = pd.read_csv(file_path)
            columns = self.data.columns.tolist()
            self.combo1['values'] = columns
            self.combo2['values'] = columns
            self.combo3['values'] = columns
            self.combo4['values'] = columns
        except pd.errors.ParserError:
            # Aquí puedes mostrar un mensaje de error al usuario si lo deseas
            print("Error al leer el archivo CSV.")
            
    def save_figure(self, fig):
        file_name = filedialog.asksaveasfilename(title="Save Graph As", defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_name:
            fig.savefig(file_name)

    def plot_data(self):
        self.cancel_btn['state'] = tk.NORMAL
    
        self.show_spinner()
    
        x = self.combo1.get()
        y = self.combo2.get()
        group = self.combo3.get() if self.combo3.get() != "" else None
        facet = self.combo4.get() if self.combo4.get() != "" else None
    
        x_label = self.entry_xaxis.get() or x  # Usamos el valor ingresado o el nombre de la columna
        y_label = self.entry_yaxis.get() or y
        
        x_min = self.entry_xaxis_min.get() or None
        x_max = self.entry_xaxis_max.get() or None
        y_min = self.entry_yaxis_min.get() or None
        y_max = self.entry_yaxis_max.get() or None

        try:
            x_min = float(x_min) if x_min else None
        except ValueError:
            x_min = None
        
        try:
            x_max = float(x_max) if x_max else None
        except ValueError:
            x_max = None
        
        try:
            y_min = float(y_min) if y_min else None
        except ValueError:
            y_min = None
        
        try:
            y_max = float(y_max) if y_max else None
        except ValueError:
            y_max = None        
    
        # Validations
        cols_to_check = [col for col in [x, y, group, facet] if col is not None]
        if self.data is None or not all(col in self.data.columns for col in cols_to_check):
            self.hide_spinner()
            self.cancel_btn['state'] = tk.DISABLED
            return
    
        # When there's a facet
        if facet:
            unique_facets = self.data[facet].unique()
            n = len(unique_facets)
    
            if 1 < n <= 20:
                fig, axes = plt.subplots(n, 1, figsize=(8, 6 * n))
                if n == 1:  # Convert `axes` into a list if there's only 1 facet
                    axes = [axes]
    
                for ax, value in zip(axes, unique_facets):
                    subset = self.data[self.data[facet] == value]
                    if group:
                        for name, group_data in subset.groupby(group):
                            ax.plot(group_data[x], group_data[y], marker='o', label=name)
                        ax.legend()
                    else:
                        ax.scatter(subset[x], subset[y])
                    ax.set_title(f"{facet} = {value}")
    
                    # Establecer etiquetas para los ejes
                    ax.set_xlabel(x_label)
                    ax.set_ylabel(y_label)
                    ax.set_xlabel(x_label)
                    ax.set_ylabel(y_label)
                    if x_min is not None and x_max is not None:
                        ax.set_xlim(x_min, x_max)
                    if y_min is not None and y_max is not None:
                        ax.set_ylim(y_min, y_max)
    
            else:
                print("Número de facets no soportado.")
                self.hide_spinner()
                self.cancel_btn['state'] = tk.DISABLED
                return
    
        # When there's no facet
        else:
            plt.figure(figsize=(8, 6))
            if group:
                for name, group_data in self.data.groupby(group):
                    plt.plot(group_data[x], group_data[y], marker='o', label=name)
                plt.legend()
            else:
                plt.scatter(self.data[x], self.data[y])
    
            # Establecer etiquetas para los ejes
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            if x_min is not None and x_max is not None:
                plt.xlim(x_min, x_max)
            if y_min is not None and y_max is not None:
                plt.ylim(y_min, y_max)
    
        # Embed the graph in the Tkinter window
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
    
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    
        # Add a toolbar to manipulate the graph
        toolbar = NavigationToolbar2Tk(canvas, self.frame_graph)
        toolbar.update()
        canvas.get_tk_widget().pack()
    
        # Add a button to save the graph
        save_btn = ttk.Button(self.frame_graph, text="Save Graph", command=lambda: self.save_figure(plt.gcf()))
        save_btn.pack(pady=10)
    
        plt.close()
        self.hide_spinner()
        self.cancel_btn['state'] = tk.DISABLED

    def show_spinner(self):
        self.spinner.pack()  # O utiliza grid() dependiendo de tu diseño
        self.root.update_idletasks()
    
    def hide_spinner(self):
        self.spinner.pack_forget() 

    def abort_graph(self):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
            
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
