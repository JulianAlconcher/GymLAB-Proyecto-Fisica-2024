import customtkinter as ctk
from view.GUI_view import App

if __name__ == "__main__":
    app = App()
    app.after(0, lambda:app.state('zoomed'))
    app.mainloop()
