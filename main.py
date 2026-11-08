"""Лаба 3 - Артдуэль: поединок двух танков (tkinter)."""

import math
import random
import tkinter as tk
from tkinter import messagebox

W, H = 900, 450      # размер поля
ZEML = 400           # уровень земли
X1, X2 = 120, 780    # позиции танков
G = 0.35             # гравитация для снаряда

# цвета
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
        spravka.add_command(label="О программе", command=self.o_programme,
                            accelerator="Ctrl+H")
        menu.add_cascade(label="Справка", menu=spravka)
        root.config(menu=menu)
        root.bind_all("<Control-h>", lambda e: self.o_programme())

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
        self.hod_igroka = True   # чей сейчас ход
        self.snar = None         # летящий снаряд на канвасе
        self.narisovat()

    def narisovat(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, ZEML, W, H, fill=CVET_ZEML, outline="")
        self.tank(c, X1, CVET_T1, self.hp1, 1)
        self.tank(c, X2, CVET_T2, self.hp2, 2)

    def tank(self, c, x, cvet, hp, nomer):
        # корпус, башня и ствол
        c.create_rectangle(x - 25, ZEML - 14, x + 25, ZEML, fill=cvet, outline="#333")
        c.create_rectangle(x - 12, ZEML - 26, x + 12, ZEML - 14, fill=cvet, outline="#333")
        c.create_line(x, ZEML - 20, x + 18, ZEML - 34, width=3, fill="#333")
        c.create_text(x, ZEML - 42, text=f"Танк {nomer}", fill="#333")
        # полоска здоровья над танком
        c.create_rectangle(x - 30, ZEML - 60, x + 30, ZEML - 54, outline="#333")
        w = max(0, 60 * hp / 100)
        c.create_rectangle(x - 30, ZEML - 60, x - 30 + w, ZEML - 54,
                           fill="#cc3333", outline="")

    def vistrel(self):
        # ходит только игрок и только если нет летящего снаряда
        if not self.hod_igroka or self.snar:
            return
        try:
            ugol = float(self.ugol_ent.get().replace(",", "."))
            sila = float(self.sila_ent.get().replace(",", "."))
        except ValueError:
            self.status.config(text="Нужно ввести числа!", fg="#aa2222")
            return
        if not (1 <= ugol <= 89) or not (10 <= sila <= 100):
            self.status.config(text="Угол 1..89, сила 10..100", fg="#aa2222")
            return
        vx, vy = self.skorost(ugol, sila, vpravo=True)
        self.zapustit(X1 + 18, ZEML - 34, vx, vy, vpravo=True)

    def skorost(self, ugol, sila, vpravo):
        # переводим угол и силу в скорость по осям
        rad = ugol * math.pi / 180
        v = sila * 0.22
        naprav = 1 if vpravo else -1
        return v * math.cos(rad) * naprav, -v * math.sin(rad)

    def zapustit(self, x, y, vx, vy, vpravo):
        self.snar = self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#222")
        self.dvizh(vx, vy, vpravo)

    def dvizh(self, vx, vy, vpravo):
        c = self.canvas
        x1, y1, x2, y2 = c.coords(self.snar)
        x = (x1 + x2) / 2 + vx
        y = (y1 + y2) / 2 + vy
        vy += G
        c.coords(self.snar, x - 4, y - 4, x + 4, y + 4)
        tx = X2 if vpravo else X1
        if abs(x - tx) < 28 and y > ZEML - 30:
            self.popal(vpravo)
            return
        if y >= ZEML - 4 or x < -20 or x > W + 20:
            self.mimo(vpravo)
            return
        self.root.after(20, lambda: self.dvizh(vx, vy, vpravo))

    def popal(self, vpravo):
        uron = random.randint(15, 35)
        if vpravo:
            self.hp2 = max(0, self.hp2 - uron)
        else:
            self.hp1 = max(0, self.hp1 - uron)
        self.canvas.delete(self.snar)
        self.snar = None
        self.narisovat()
        kto = "Вы попали!" if vpravo else "Вас ранили!"
        self.status.config(text=f"{kto} Урон {uron}", fg="#aa2222")
        if self.hp2 <= 0:
            messagebox.showinfo("Победа!", "Вы уничтожили вражеский танк!")
            self.novaya_igra()
            return
        if self.hp1 <= 0:
            messagebox.showinfo("Поражение", "Ваш танк уничтожен...")
            self.novaya_igra()
            return
        self.sled_hod(vpravo)

    def mimo(self, vpravo):
        self.canvas.delete(self.snar)
        self.snar = None
        self.status.config(text="Промах!", fg="#225522")
        self.sled_hod(vpravo)

    def sled_hod(self, vpravo):
        if vpravo:
            # после выстрела игрока ходит комп
            self.hod_igroka = False
            self.status.config(text="Ходит компьютер...", fg="#225522")
            self.root.after(900, self.hod_kompa)
        else:
            self.hod_igroka = True
            self.status.config(text="Ваш ход", fg="#225522")

    def hod_kompa(self):
        # комп прицеливается с небольшой случайной ошибкой
        dx = abs(X2 - X1)
        best = None
        for _ in range(40):
            ugol = random.randint(25, 70)
            sila = random.randint(45, 85)
            vx, vy = self.skorost(ugol, sila, vpravo=False)
            # грубо симулируем полёт и смотрим куда упадёт
            x, y, cx, cy = X2, ZEML - 34, vx, vy
            while y < ZEML and 0 < x < W:
                x += cx
                y += cy
                cy += G
            if best is None or abs(x - X1) < best[0]:
                best = (abs(x - X1), ugol, sila)
        ugol, sila = best[1], best[2]
        ugol += random.randint(-4, 4)
        sila += random.randint(-6, 6)
        self.status.config(text=f"Комп: угол {ugol}, сила {sila}", fg="#225522")
        vx, vy = self.skorost(ugol, sila, vpravo=False)
        self.zapustit(X2 - 18, ZEML - 34, vx, vy, vpravo=False)

    def novaya_igra(self):
        self.hp1 = 100
        self.hp2 = 100
        self.hod_igroka = True
        if self.snar:
            self.canvas.delete(self.snar)
            self.snar = None
        self.narisovat()
        self.status.config(text="Новая игра. Ваш ход", fg="#225522")

    def o_programme(self):
        # модальное окно - пока его не закроешь, игра не работает
        okno = tk.Toplevel(self.root)
        okno.title("О программе")
        okno.geometry("330x180+300+200")
        okno.resizable(False, False)
        okno.transient(self.root)
        okno.grab_set()
        tk.Label(okno, text="Артдуэль", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(okno, text="Лабораторная работа № 3\n"
                            "Приложения с графическим интерфейсом\n"
                            "Python + tkinter", justify="center").pack()
        tk.Label(okno, text="Вариант (свой): поединок танков", fg="#666").pack(pady=4)
        tk.Button(okno, text="Закрыть", command=okno.destroy).pack(pady=8)


def main():
    root = tk.Tk()
    Artduel(root)
    root.mainloop()


if __name__ == "__main__":
    main()
