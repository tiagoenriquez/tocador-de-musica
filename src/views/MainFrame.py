import tkinter as tk


class MainFrame:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.update_idletasks()

        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        x = (self.width - 800) // 2
        y = (self.height - 600) // 2
        self.window.geometry(f"800x600+{x}+{y}")
        self.window.title("Tocador de Música")

    def clean(self) -> None:
        for widget in self.window.winfo_children():
            if (str(type(widget)) != "<class 'tkinter.Menu'>"):
                widget.destroy()
    
    def keep_open(self) -> None:
        self.window.mainloop()