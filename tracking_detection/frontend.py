from ttkbootstrap import Style
import tkinter as tk
import matplotlib
from tkinter import filedialog, font, messagebox
from tkinter import font
import os
import csv
import graphs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# The video uploading widget, simply gets the filename, get filename by getting the file_name attribute
class VideoUploader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Analyzer")
        self.pack(padx=10, pady=10)
        
        self.container = tk.Frame(self)
        self.container.pack(expand=True)

        # Button to open file dialog
        self.upload_btn = tk.Button(self, text="Upload Video", command=self.upload_video)
        self.upload_btn.pack(fill="x")

        # Label to display selected file name
        self.file_label = tk.Label(self.container, text="No file selected")
        self.file_label.pack(fill="x", pady=(5,0))
        
        self.download_btn = tk.Button(
                    self.container,
                    text="Download CSV",
                    command=self.download_csv,
                    bg="#2ecc71",
                    fg="white",
                    activebackground="#27ae60",
                    relief="flat",
                    bd=0,
                    padx=20,
                    pady=10,
                    cursor="hand2"
                )
        self.download_btn.pack(pady=(0, 20))
        self.download_btn.pack_forget()
        
        # File name storage
        self.file_name = "no file"

    def upload_video(self):
        filepath = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        if filepath:
            # filepath is already an absolute path:
            self.file_label.config(text=filepath)
            self.file_name = filepath
        else:
            self.file_label.config(text="No file selected")
            
        #Then call the main function here.
        import main
        self.download_btn.pack(pady=(0, 20))
        
        
        
        

    def download_csv(self):
        # Save directly to the Windows Downloads folder
      
        csv_path =  "Logging_Data.csv"
        try:
            # Write empty CSV with headers
            with open(csv_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Frame", "New People", "Total People", "Cumulative"])
            messagebox.showinfo("CSV Saved", f"CSV successfully saved as:\n{csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV:\n{e}")


class SeabornLinePlot(tk.Frame):
    """
    A Tkinter Frame that contains a Matplotlib FigureCanvas displaying
    a Seaborn lineplot.  You can call `plot(...)` repeatedly to update.
    """
    def __init__(self, master=None, figsize=(5, 4), dpi=100, **kwargs):
        super().__init__(master, **kwargs)
        # 1) Create a Matplotlib figure and axes
        self.fig = Figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot(111)

        # 2) Create the canvas, and put it inside this frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 3) (optional) add the Matplotlib navigation toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot(self, x=None, y=None, data=None, **seaborn_kwargs):
        """
        Re-draws the Seaborn lineplot on the existing axes.

        Args:
          x, y: column names or arrays (see seaborn.lineplot doc)
          data: a DataFrame (optional)
          seaborn_kwargs: extra kwargs passed to seaborn.lineplot
        """
        # Clear old content
        self.ax.clear()

        # Draw new plot
        sns.lineplot(x=x, y=y, data=data, ax=self.ax, **seaborn_kwargs)

        # (Re)format, e.g. grid, title, labels etc.
        self.ax.grid(True)
        self.fig.tight_layout()

        # Tell the canvas to re-draw
        self.canvas.draw()


if __name__ == "__main__":
    style = Style(theme="litera")      # choose from: 'litera','superhero','darkly',…
    app = style.master
    app.title("Bootstrap-styled Tkinter")
    app.geometry("1920x1080")
    app.option_add("*Font", "Helvetica 10")
    app.tk.call('tk', 'scaling', 5)  
    
    
   
    
    
    video_uploader = VideoUploader(master=app)
    
     #ehh order is wrong but doesn't matter
    #df = pd.read_csv("pandas_csv.csv")
    
    #total_plot = SeabornLinePlot(app, figsize=(8,4))
    #total_plot.pack(fill=tk.BOTH, expand=True)
    
    #total_df, total_agg = graphs.generate_customerspertime_graph(df, 0.1)
    
    #total_plot.plot(x="time_bin", y="new_people", data=total_agg, label="New people per time interval", color="b")
    
    
    

   

    app.mainloop()

