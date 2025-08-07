import tkinter as tk
import random
import os
import importlib.util
from ekran import yazilar
from PIL import Image, ImageTk
import os

print("Dosya var mı:", os.path.exists("scr.png"))
print("Roller içeriği:", yazilar.roller)
VERI_KLASORU = "veri"
rota_klasor = "DATAroutes"
print("Roller içeriği:", yazilar.roller)
print("Türü:", type(yazilar.roller))
print("İlk eleman:", yazilar.roller[0])
print("Tüm elemanlar ayrı mı?")
for rol in yazilar.roller:
    print("-", rol)

def veri_al(dosya_adi, klasor="veri"):
    dosya_yolu = os.path.join(klasor, f"{dosya_adi.lower()}.py")
    if not os.path.exists(dosya_yolu):
        return None
    spec = importlib.util.spec_from_file_location("modul", dosya_yolu)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return getattr(modul, "veriler", None) or getattr(modul, "rotalar", None)
print("Test (stations):", veri_al("stations"))
print("Test (trains):", veri_al("trains"))
print("Test (zone):", veri_al("zone"))

class App:
    def __init__(self, root):
        self.root = root
        root.title(yazilar.baslik)
        root.geometry("500x500")
        root.resizable(True, True)
        self.rol_frame = tk.Frame(root)
        self.rol_frame.pack(fill="both", expand=True)

        image = Image.open("scr.png")
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(self.rol_frame, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.rol_frame = tk.Frame(root, bg="#f0f0f0")

        # 1. Ekran - Rol seçimi

        self.rol_frame = tk.Frame(root)
        self.rol_frame.pack(fill="both", expand=True)

        self.rol_label = tk.Label(self.rol_frame, text="Select Role", font=("Arial", 14, "bold"))
        self.rol_label.pack(pady=10)

        self.selected_rol = tk.StringVar(value=yazilar.roller[0])

        for rol in yazilar.roller:
            rb = tk.Radiobutton(self.rol_frame, text=rol, variable=self.selected_rol, value=rol, font=("Arial", 12))
            rb.pack(anchor="w", padx=50)

        self.next_button = tk.Button(self.rol_frame, text="Next", command=self.next_ekran)
        self.next_button.pack(pady=20)

        # 2. Ekran - Rol bazlı seçim
        self.secim_frame = tk.Frame(root)

    def next_ekran(self):
        self.rol_frame.pack_forget()
        self.secim_frame.pack(fill="both", expand=True)
        self.rol_secim()

    def rol_secim(self):
        # Clear frame
        for widget in self.secim_frame.winfo_children():
            widget.destroy()

        rol = self.selected_rol.get()

        if rol == "Passenger":
            self.passenger_ekran()
        elif rol == "Dispatcher":
            self.dispatcher_ekran()
        elif rol == "Driver":
            self.driver_ekran()
        elif rol == "Guard":
            self.guard_ekran()
        elif rol == "Signaller":
            self.signaller_ekran()

    def passenger_ekran(self):
        button = tk.Button(self.secim_frame, text="Generate Route", command=self.passenger_sonuc)
        button.pack(pady=15)

        button1 = tk.Button(self.secim_frame, text="Back", command=self.baslangic)
        button1.pack(pady=15)

    def baslangic(self):
        self.secim_frame.pack_forget()
        self.rol_frame.pack(fill="both", expand=True)

    def passenger_sonuc(self):
        stations = veri_al("stations")

        if len(stations) < 2:
            tk.Label(self.secim_frame, text="Not enough stations to generate route.", fg="red").pack()
            return

        start, finish = random.sample(stations, 2)

        for widget in self.secim_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.rol_label:
                widget.destroy()

        tk.Label(self.secim_frame, text=f"Start Station: {start}", font=("Arial", 12), fg="blue").pack(pady=5)
        tk.Label(self.secim_frame, text=f"Finish Station: {finish}", font=("Arial", 12), fg="blue").pack(pady=5)

    def dispatcher_ekran(self):
        stations = veri_al("stations")
        label = tk.Label(self.secim_frame, text="Random Station:", font=("Arial", 12))
        label.pack(pady=10)

        if stations:
            station = random.choice(stations)
            result_label = tk.Label(self.secim_frame, text=station, fg="blue", font=("Arial", 12))
            result_label.pack()
        else:
            result_label = tk.Label(self.secim_frame, text="No stations found.", fg="red", font=("Arial", 12))
            result_label.pack()
        button1 = tk.Button(self.secim_frame, text="Back", command=self.baslangic)
        button1.pack(pady=15)



    def driver_ekran(self):
        label = tk.Label(self.secim_frame, text="Select Operator", font=("Arial", 12))
        label.pack(pady=10)
        self.selected_operator = tk.StringVar(value=yazilar.operatorler[0])
        button1 = tk.Button(self.secim_frame, text="Back", command=self.baslangic)
        button1.pack(pady=15)

        for op in yazilar.operatorler:
            rb = tk.Radiobutton(self.secim_frame, text=op, variable=self.selected_operator, value=op,
                                font=("Arial", 12))
            rb.pack(anchor="w", padx=50)

        button = tk.Button(self.secim_frame, text="Generate Route", command=self.driver_sonuc)
        button.pack(pady=15)

        self.result_label = tk.Label(self.secim_frame, text="", fg="blue")
        self.result_label.pack()
        self.label5 = tk.Label(self.secim_frame, text="", fg="blue")
        self.label5.pack()


    def driver_sonuc(self):
     operator = self.selected_operator.get()
     veriler = veri_al(operator)
     data = veri_al("routes", klasor="DATAroutes") 

     if not veriler:
        self.result_label.config(text="No trains found.", fg="red")
     else:
        train = random.choice(veriler)
        self.result_label.config(text=f"Train: {train}", fg="blue")

     if not data:
        self.label5.config(text="No routes found.", fg="red")
     else:
        rota = random.choice(data)
        self.label5.config(text=f"Route: {rota}", fg="blue")

    def guard_ekran(self):
        # Önce ekranı temizleyelim
        for widget in self.secim_frame.winfo_children():
            widget.destroy()

        # Rastgele tren butonu
        button = tk.Button(self.secim_frame, text="Generate Random", command=self.guard_sonuc, font=("Arial", 12))
        button.pack(pady=10)

        # Geri dön butonu
        button1 = tk.Button(self.secim_frame, text="Back", command=self.baslangic)
        button1.pack(pady=15)

        # Sonuç gösterilecek label (ilk başta boş)
        self.guard_result_label = tk.Label(self.secim_frame, text="", fg="blue", font=("Arial", 12))
        self.guard_result_label.pack(pady=10)

    def guard_sonuc(self):
        trains = veri_al("trains")

        if trains:
            train = random.choice(trains)
            self.guard_result_label.config(text=train)
        else:
            self.guard_result_label.config(text="No trains found.", fg="red")

    def signaller_ekran(self):
        for widget in self.secim_frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.secim_frame, text="Random Zone:", font=("Arial", 12))
        label.pack(pady=10)

        zones = veri_al("zone")
        if zones:
            zone = random.choice(zones)
            result_label = tk.Label(self.secim_frame, text=zone, fg="blue", font=("Arial", 12))
            result_label.pack()
        else:
            result_label = tk.Label(self.secim_frame, text="No zones found.", fg="red", font=("Arial", 12))
            result_label.pack()

        button1 = tk.Button(self.secim_frame, text="Back", command=self.baslangic)
        button1.pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()