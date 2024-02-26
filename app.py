import tkinter as tk
from PIL import Image,ImageTk

class Aplikacja(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Steam comparison")

        # Utworzenie widżetu Canvas
        self.canvas = tk.Canvas(self, width=800, height=600, bg="#e3dbd5")
        self.canvas.pack()

        # Utwórz startową scenę jako domyślną
        self.startowa_scena = MainMenu(self, self.canvas)  # Przekazanie Canvas jako argument
        self.startowa_scena.pack()

        # Zmień rozmiar okna
        self.geometry("800x600")


class MainMenu(tk.Frame):

    def przejdz_do_nastepnej_sceny(self):
        pass
    def capsules_clicked(self):
        pass
    def events_clicked(self):
        print('you clicked an iamge')
        self.destroy()
        self.canvas.destroy()
        startowa_scena = KolejnaScena(self.master)
        startowa_scena.pack()


    def __init__(self, master, canvas, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.canvas = canvas



        self.capsule_button = tk.Button(self, text="Przejdź do następnej sceny", command=self.przejdz_do_nastepnej_sceny)
        self.capsule_button.pack(pady=10)
        self.capsules_image = tk.PhotoImage(file="icons/capsules.png")
        events = Image.open("icons/events.png")
        resized_image = events.resize((315, 315), Image.Resampling.LANCZOS)
        self.events_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(10, 50, image=self.capsules_image, anchor="nw")
        self.canvas.create_image(450, 70, image=self.events_image, anchor="nw")
        self.canvas.create_text(400, 28, text="Steam prices comparison", fill="black", font=('Helvetica 24 bold'),justify='center')
        self.canvas.create_text(180, 420, text="Capsules", fill="black", font=('Helvetica 24 bold'))
        self.canvas.create_text(610, 420, text="Events", fill="black", font=('Helvetica 24 bold'))

        img_label= tk.Label(image=self.capsules_image)

        self.button1 = tk.Button(self.canvas, image=self.capsules_image, command=self.events_clicked)
        self.canvas.pack()

class KolejnaScena(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.przycisk = tk.Button(self, text="Powrót do startowej sceny", command=self.powrot_do_startowej_sceny)
        self.przycisk.pack(pady=10)
    def powrot_do_startowej_sceny(self):
        self.destroy()
        startowa_scena = MainMenu(self.master)
        startowa_scena.pack()



if __name__ == "__main__":
    aplikacja = Aplikacja()
    aplikacja.mainloop()
