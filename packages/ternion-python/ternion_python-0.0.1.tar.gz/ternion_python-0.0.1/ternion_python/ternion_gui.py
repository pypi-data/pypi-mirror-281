import customtkinter as ctk


class TernionGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x240")
        self.title("Ternion Commander")
        self.resizable(False, False)
        self.mainloop()


if __name__ == "__main__":
    gui = TernionGui()
