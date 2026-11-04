"""Лаба 3 - Артдуэль: поединок двух танков (tkinter)."""

import tkinter as tk

W, H = 900, 450
ZEML = 400
X1, X2 = 120, 780

CVET_NEBO = "#87CEEB"
CVET_ZEML = "#5d8a3c"
CVET_T1 = "#4a6fa5"
CVET_T2 = "#a54a4a"


class Artduel:
    def __init__(self, root):
        self.root = root
        root.title("Артдуэль")
        root.geometry("+60+40")
        root.resizable(False, False)

        # меню приложения
        menu = tk.Menu(root)
        igra = tk.Menu(menu, tearoff=0)
        igra.add_command(label="Новая игра", command=self.novaya_igra)
        igra.add_separator()
        igra.add_command(label="Выход", command=root.destroy)
        menu.add_cascade(label="Игра", menu=igra)
        spravka = tk.Menu(menu, tearoff=0)
        spravka.add_command(label="О программе", command=self.o_programme)
        menu.add_cascade(label="Справка", menu=spravka)
        root.config(menu=menu)

        self.canvas = tk.Canvas(root, width=W, height=H, bg=CVET_NEBO)
        self.canvas.pack()

        # панель управления внизу
        panel = tk.Frame(root)
        panel.pack(fill="x", padx=10, pady=6)
        tk.Label(panel, text="Угол:").pack(side="left")
        self.ugol_ent = tk.Entry(panel, width=5)
        self.ugol_ent.pack(side="left", padx=4)
        self.ugol_ent.insert(0, "45")
        tk.Label(panel, text="Сила:").pack(side="left")
        self.sila_ent = tk.Entry(panel, width=5)
        self.sila_ent.pack(side="left", padx=4)
        self.sila_ent.insert(0, "50")
        tk.Button(panel, text="Огонь!", command=self.vistrel).pack(side="left", padx=10)
        self.status = tk.Label(panel, text="Ваш ход", fg="#225522")
        self.status.pack(side="left", padx=10)

        self.hp1 = 100
        self.hp2 = 100
        self.narisovat()

    def narisovat(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, ZEML, W, H, fill=CVET_ZEML, outline="")
        self.tank(c, X1, CVET_T1, self.hp1, 1)
        self.tank(c, X2, CVET_T2, self.hp2, 2)

    def tank(self, c, x, cvet, hp, nomer):
        c.create_rectangle(x - 25, ZEML - 14, x + 25, ZEML, fill=cvet, outline="#333")
        c.create_rectangle(x - 12, ZEML - 26, x + 12, ZEML - 14, fill=cvet, outline="#333")
        c.create_line(x, ZEML - 20, x + 18, ZEML - 34, width=3, fill="#333")
        c.create_text(x, ZEML - 42, text=f"Танк {nomer}", fill="#333")

    def vistrel(self):
        # TODO: сделать сам выстрел
        print("debug: нажали огонь, угол =", self.ugol_ent.get(),
              "сила =", self.sila_ent.get())

    def novaya_igra(self):
        self.hp1 = 100
        self.hp2 = 100
        self.narisovat()
        self.status.config(text="Новая игра. Ваш ход", fg="#225522")

    def o_programme(self):
        pass  # потом сделаю


def main():
    root = tk.Tk()
    Artduel(root)
    root.mainloop()


if __name__ == "__main__":
    main()
