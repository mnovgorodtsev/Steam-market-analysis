import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()
root.title("Wykres w Tkinterze")
root.geometry("1200x800")
# Ustawienie geometrii okna
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)
root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

# Tworzenie wykresu
fig = Figure(figsize=(5, 4), dpi=100)
plot = fig.add_subplot(111)
x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 5, 7, 6]
plot.plot(x_data, y_data)

# Dodanie wykresu do interfejsu Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().place(relx=0, rely=1, anchor="sw")

root.mainloop()