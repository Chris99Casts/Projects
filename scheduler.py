import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk  # pip install pillow

SEASON_WEEKS = 14

def generate_seeded_round_robin(teams):
    names = [team[0] for team in teams]
    if len(names) % 2 != 0:
        names.append("BYE")
    n = len(names)
    base = []
    arr = names.copy()
    for _ in range(n - 1):
        base.append([f"{arr[i]} vs {arr[-1-i]}" for i in range(n//2)])
        arr = [arr[0]] + [arr[-1]] + arr[1:-1]
    schedule = []
    for w in range(SEASON_WEEKS):
        schedule.append((f"Semana {w+1}", base[w % len(base)]))
    return schedule

def on_generate():
    champ = champ_entry.get().strip()
    runner = runner_entry.get().strip()
    lines = input_text.get("1.0", tk.END).strip().splitlines()
    teams = []
    try:
        for line in lines:
            name, wins, losses = line.split(",")
            w, l = int(wins), int(losses)
            pct = w/(w+l) if (w+l)>0 else 0
            teams.append((name.strip(), pct))

        d = {n:p for n,p in teams}
        if champ not in d or runner not in d:
            raise ValueError("Campeón o subcampeón no en la lista")
        seeds = [(champ, d.pop(champ)), (runner, d.pop(runner))]
        seeds += sorted(d.items(), key=lambda x: x[1], reverse=True)

        sched = generate_seeded_round_robin(seeds)
        output_text.delete("1.0", tk.END)
        for week, games in sched:
            output_text.insert(tk.END, f"{week}:\n")
            for g in games:
                output_text.insert(tk.END, f"  - {g}\n")
            output_text.insert(tk.END, "\n")

    except Exception as e:
        messagebox.showerror(
            "Error de Entrada",
            f"{e}\nFormato: Equipo, Ganados, Perdidos"
        )

# Colores
BG     = "#75caef"
FIELD  = "#FFFFFF"
ACCENT = "#233755"
BUTTON = "#1F3A5F"

root = tk.Tk()
root.title("No Punt Intendeed Calendar Generator")
root.geometry("680x750")
root.configure(bg=BG)

# Depuración: rutas
script_dir = os.path.dirname(os.path.abspath(__file__))
cwd = os.getcwd()
print("Script directory:", script_dir)
print("Working directory:", cwd)
print("Contents of script_dir:", os.listdir(script_dir))
print("Contents of cwd:", os.listdir(cwd))

# Cargar logo con LANCZOS
logo_img = None
for base in (script_dir, cwd):
    path = os.path.join(base, "fantasy_logo.jpg")
    print(f"Checking for logo at: {path}", "Exists?", os.path.exists(path))
    if os.path.exists(path):
        try:
            img = Image.open(path)
            img = img.resize((200, 100), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            root.logo_img = logo_img
            tk.Label(root, image=logo_img, bg=BG).pack(pady=(15,5))
            print("Logo cargado desde:", path)
            break
        except Exception as e:
            print("Error al abrir logo:", e)
if logo_img is None:
    print("⚠️ No se pudo cargar fantasy_logo.jpg en ningún directorio.")

# Interfaz
tk.Label(root, text="No Punt Intendeed Calendar Generator",
         bg=BG, fg=ACCENT, font=("Arial",18,"bold")).pack(pady=(0,20))

tk.Label(root, text="Campeón anterior:", bg=BG, fg=ACCENT, font=("Arial",12))\
    .pack(anchor="w", padx=30)
champ_entry = tk.Entry(root, width=40, bg=FIELD, fg=ACCENT, font=("Arial",11))
champ_entry.pack(padx=30, pady=(0,10))

tk.Label(root, text="Subcampeón anterior:", bg=BG, fg=ACCENT, font=("Arial",12))\
    .pack(anchor="w", padx=30)
runner_entry = tk.Entry(root, width=40, bg=FIELD, fg=ACCENT, font=("Arial",11))
runner_entry.pack(padx=30, pady=(0,20))

tk.Label(root, text="Equipo, Ganados, Perdidos (una línea por equipo)",
         bg=BG, fg=ACCENT, font=("Arial",12))\
    .pack(anchor="w", padx=30)

input_text = scrolledtext.ScrolledText(root, width=60, height=8,
                                       bg=FIELD, fg=ACCENT, font=("Courier New",11))
input_text.pack(padx=30, pady=(5,25))
input_text.insert(tk.END,
    "Tigres, 9, 5\n"
    "Águilas, 8, 6\n"
    "Leones, 7, 7\n"
    "Jaguares, 6, 8\n"
    "Panteras, 5, 9\n"
    "Toros, 4, 10"
)

tk.Button(root, text="Generar Calendario", command=on_generate,
          bg=BUTTON, fg=FIELD, font=("Arial",12,"bold"),
          padx=20, pady=10).pack(pady=(0,25))

tk.Label(root, text="Calendario Generado:", bg=BG, fg=ACCENT, font=("Arial",12))\
    .pack(anchor="w", padx=30)
output_text = scrolledtext.ScrolledText(root, width=60, height=15,
                                        bg=FIELD, fg=ACCENT, font=("Courier New",11))
output_text.pack(padx=30, pady=(5,20))

root.mainloop()