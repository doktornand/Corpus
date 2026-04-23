#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaleoMemes – Version Alchimique (v7.1)
Auteur : (révision générée)
Date : 2025
Description : Générateur mystique de "Paléo Mèmes" avec oracle, transmutation,
géométries sacrées, animations et exports (.pmem7, .json, .png).
VERSION STABILISÉE : Correction erreurs X11 + ajout scrollbars
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataclasses import dataclass, asdict
import random, math, json, os, sys, time
from typing import List, Tuple, Dict, Any

# ---- CONFIGURATION ----
@dataclass
class Config:
    BG = "#0f1720"
    FG = "#f8f3e6"
    ACCENT = "#e6b800"
    MUTED = "#94a3b8"
    WARN = "#d97706"
    ERROR = "#e11d48"

    FONT_TITLE = ("Georgia", 16, "bold")  # Réduit de 18 à 16
    FONT_LABEL = ("Helvetica", 10)
    FONT_SYMBOL = ("Segoe UI Symbol", 28, "bold")  # Réduit de 36 à 28
    FONT_SMALL = ("Courier New", 9)
    CANVAS_W, CANVAS_H = 900, 520

# ---- SYMBOLS DATA ----
SYMBOL_DATA: List[Tuple[str,str,str,str,str,str]] = [
    ("✋","Main","Présence, témoin du réel","Corps","Air","Gardien"),
    ("🌀","Spirale","Flux du temps, souffle","Âme","Water","Voyageur"),
    ("◆","Losange","Fécondité du cœur","Âme","Earth","Nexus"),
    ("⚡","Zigzag","Percée, étincelle","Esprit","Fire","Éveilleur"),
    ("☉","Soleil","Clarté, conscience","Esprit","Fire","Clairvoyant"),
    ("☽","Lune","Rythme, réceptivité","Âme","Water","Veilleuse"),
    ("☿","Mercure","Mutation, passage","Âme","Air","Messager"),
    ("♄","Saturne","Limite, mémoire","Corps","Earth","Sculpteur"),
    ("✚","Croix","Rencontre, équilibre","Esprit","Air","Pont"),
    ("⭕","Cercle","Totalité, œuf cosmique","Corps","Earth","Matrice"),
    ("🪶","Plume","Esprit messager","Esprit","Air","Souffle"),
    ("•","Point","Graine, étoile","Corps","Fire","Germe"),
    ("▲","Triangle","Montée, feu sacré","Esprit","Fire","Ascension"),
    ("∞","Méandre","Continuité, mémoire","Âme","Water","Tisseur"),
    ("▦","Grille","Territoire, structure","Corps","Earth","Fondation"),
]

TEMPORALITES = [
    ("Primaire", {"bg":"#2a2f36","accent":"#b38b00"}),
    ("Mythique", {"bg":"#111827","accent":"#7c3aed"}),
    ("Antique", {"bg":"#1f2937","accent":"#d97706"}),
    ("Contemporaine", {"bg":"#0f1724","accent":"#06b6d4"}),
    ("Futur", {"bg":"#001219","accent":"#00ffa3"}),
    ("Post-Humain", {"bg":"#060606","accent":"#ff4d6d"}),
    ("Éonique", {"bg":"#071e3d","accent":"#ffd166"}),
]

SUPPORTS = ["Pierre","Peau","Feuille","Cuivre"]
TRANSMUTE_ORDER = ["Fire","Air","Water","Earth"]

# ---- DATA CLASSES ----
@dataclass
class PaleoMeme:
    intention: str
    intensite: int
    temporalite: str
    support: str
    symbols: List[Tuple[str,str,str,str,str,str]]
    created_at: float

    def to_text(self) -> str:
        lines = [
            f"// PALEO MEME ALCHIMIQUE – {self.intention} [{self.intensite}]",
            f"// Temporalité: {self.temporalite} – Support: {self.support}",
            f"// Généré le: {time.ctime(self.created_at)}",
            "-"*60,
            "COMPOSITION :",
            " ".join([s[0] for s in self.symbols]),
            "",
            "SYMBOLS:",
        ]
        for ch,name,desc,plan,element,arch in self.symbols:
            lines.append(f"{ch} {name} ({plan} / {element} / {arch}) : {desc}")
        lines.append("-"*60)
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps({
            "intention": self.intention,
            "intensite": self.intensite,
            "temporalite": self.temporalite,
            "support": self.support,
            "created_at": self.created_at,
            "symbols": [
                {"char":s[0],"name":s[1],"desc":s[2],"plan":s[3],"element":s[4],"arch":s[5]}
                for s in self.symbols
            ]
        }, ensure_ascii=False, indent=2)

# ---- UTILITAIRES POLICE ----
def get_font_pil(size:int, bold:bool=False):
    try:
        from PIL import ImageFont
        # Limiter la taille pour éviter les problèmes
        size = min(size, 48)
        candidates = [
            "DejaVuSans.ttf",
            "NotoSansSymbols2-Regular.ttf",
            "Arial.ttf",
            "LiberationSans-Regular.ttf"
        ]
        for c in candidates:
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
        return ImageFont.load_default()
    except Exception:
        return None

# ---- MAIN APPLICATION ----
class PaleoAlchimiqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PaleoMemes – Version Alchimique v7.1 (Stabilisée)")
        self.root.geometry("1200x820")
        self.root.configure(bg=Config.BG)
        self.root.minsize(800, 600)

        self.current: PaleoMeme | None = None
        self.history: List[PaleoMeme] = []
        self.anim_running = False
        self.pulse = 0.0

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Créer un canvas principal avec scrollbars
        main_canvas = tk.Canvas(self.root, bg=Config.BG, highlightthickness=0)
        main_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        
        h_scrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=main_canvas.xview)
        h_scrollbar.pack(side="bottom", fill="x")

        main_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Frame conteneur dans le canvas
        container = tk.Frame(main_canvas, bg=Config.BG)
        canvas_window = main_canvas.create_window((0, 0), window=container, anchor="nw")

        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            
        def on_canvas_configure(event):
            canvas_width = event.width
            main_canvas.itemconfig(canvas_window, width=canvas_width)

        container.bind("<Configure>", on_frame_configure)
        main_canvas.bind("<Configure>", on_canvas_configure)

        # Bind mousewheel
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Top header
        header = tk.Frame(container, bg=Config.BG)
        header.pack(fill="x", pady=8)
        tk.Label(header, text="PALEO MEMES – ALCHIMIQUE", font=Config.FONT_TITLE, 
                bg=Config.BG, fg=Config.ACCENT).pack(side="left", padx=12)
        tk.Label(header, text="(v7.1 Stabilisée) – Oracle & Transmutation", 
                font=Config.FONT_SMALL, bg=Config.BG, fg=Config.MUTED).pack(side="left", padx=8)

        # Main frames
        body = tk.Frame(container, bg=Config.BG)
        body.pack(fill="both", expand=True, padx=10, pady=6)

        left = tk.Frame(body, width=340, bg=Config.BG)
        left.pack(side="left", fill="y", padx=8, pady=8)
        right = tk.Frame(body, bg=Config.BG)
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # --- Left panel: controls ---
        params_frame = tk.LabelFrame(left, text="Paramètres & Rituel", bg=Config.BG, 
                                     fg=Config.FG, font=Config.FONT_LABEL, padx=8, pady=8)
        params_frame.pack(fill="x", pady=4)

        # Intention
        tk.Label(params_frame, text="Intention :", bg=Config.BG, fg=Config.FG, 
                anchor="w").grid(row=0, column=0, sticky="w")
        self.intention_var = tk.StringVar(value="Protection")
        intentions = ["Protection","Passage","Sacralisation","Lien","Chasse","Rêve",
                     "Deuil","Invocation","Transcendance"]
        ttk.Combobox(params_frame, textvariable=self.intention_var, values=intentions, 
                    state="readonly", width=20).grid(row=0,column=1, sticky="w")

        # Intensité
        tk.Label(params_frame, text="Intensité (1-7) :", bg=Config.BG, 
                fg=Config.FG).grid(row=1,column=0, sticky="w", pady=6)
        self.intens_var = tk.IntVar(value=4)
        ttk.Spinbox(params_frame, from_=1, to=7, textvariable=self.intens_var, 
                   width=6).grid(row=1,column=1, sticky="w")

        # Temporalité
        tk.Label(params_frame, text="Temporalité :", bg=Config.BG, 
                fg=Config.FG).grid(row=2, column=0, sticky="w")
        self.temporal_var = tk.StringVar(value=TEMPORALITES[3][0])
        ttk.Combobox(params_frame, textvariable=self.temporal_var, 
                    values=[t[0] for t in TEMPORALITES], state="readonly", 
                    width=20).grid(row=2,column=1, sticky="w")

        # Support
        tk.Label(params_frame, text="Support :", bg=Config.BG, 
                fg=Config.FG).grid(row=3, column=0, sticky="w", pady=6)
        self.support_var = tk.StringVar(value=SUPPORTS[0])
        ttk.Combobox(params_frame, textvariable=self.support_var, values=SUPPORTS, 
                    state="readonly", width=20).grid(row=3,column=1, sticky="w")

        # Buttons
        btn_frame = tk.Frame(left, bg=Config.BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="→ GÉNÉRER", command=self.generate, bg=Config.ACCENT, 
                 fg="black", font=("Helvetica",11,"bold")).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🎲 Aléatoire", command=self.randomize, 
                 bg="#6b7280", fg="white").pack(side="left", padx=4)
        tk.Button(btn_frame, text="🜂 Transmuter", command=self.transmute_current, 
                 bg="#f97316", fg="white").pack(side="left", padx=4)
        tk.Button(btn_frame, text="↶ Undo", command=self.undo, 
                 bg="#ef4444", fg="white").pack(side="left", padx=4)

        # Oracle preview avec scrollbar
        oracle_frame = tk.LabelFrame(left, text="Oracle", bg=Config.BG, fg=Config.FG, 
                                     padx=8, pady=8)
        oracle_frame.pack(fill="both", expand=True, pady=8)
        
        oracle_scroll = tk.Scrollbar(oracle_frame)
        oracle_scroll.pack(side="right", fill="y")
        
        self.oracle_text = tk.Text(oracle_frame, height=12, wrap="word", bg="#071028", 
                                  fg=Config.FG, font=Config.FONT_SMALL, 
                                  yscrollcommand=oracle_scroll.set)
        self.oracle_text.pack(fill="both", expand=True, padx=4, pady=4)
        oracle_scroll.config(command=self.oracle_text.yview)
        self.oracle_text.insert("1.0", "L'oracle apparaîtra ici...")

        # Exports
        export_frame = tk.LabelFrame(left, text="Export", bg=Config.BG, fg=Config.FG, 
                                     padx=8, pady=8)
        export_frame.pack(fill="x", pady=6)
        tk.Button(export_frame, text="💾 .pmem7", command=self.export_pmem).pack(side="left", padx=4)
        tk.Button(export_frame, text="📄 .json", command=self.export_json).pack(side="left", padx=4)
        tk.Button(export_frame, text="🖼️ PNG", command=self.export_png).pack(side="left", padx=4)

        # Animation toggle
        util_frame = tk.Frame(left, bg=Config.BG)
        util_frame.pack(fill="x", pady=6)
        self.anim_btn = tk.Button(util_frame, text="▶ Animation", command=self.toggle_anim, 
                                 bg="#10b981", fg="white")
        self.anim_btn.pack(side="left", padx=4)
        tk.Button(util_frame, text="Effacer", command=self.clear_canvas, 
                 bg="#6b7280", fg="white").pack(side="left", padx=4)

        # --- Right panel: visualization & description ---
        viz_frame = tk.Frame(right, bg=Config.BG)
        viz_frame.pack(fill="both", expand=True)

        # Canvas area
        self.canvas_frame = tk.LabelFrame(viz_frame, text="Visualisation", bg=Config.BG, 
                                         fg=Config.FG, padx=8, pady=8)
        self.canvas_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        canvas_container = tk.Frame(self.canvas_frame, bg=Config.BG)
        canvas_container.pack(fill="both", expand=True)
        
        canvas_vscroll = tk.Scrollbar(canvas_container, orient="vertical")
        canvas_vscroll.pack(side="right", fill="y")
        
        canvas_hscroll = tk.Scrollbar(canvas_container, orient="horizontal")
        canvas_hscroll.pack(side="bottom", fill="x")
        
        self.canvas = tk.Canvas(canvas_container, width=Config.CANVAS_W, height=Config.CANVAS_H, 
                               bg="#f8fafc", scrollregion=(0,0,Config.CANVAS_W,Config.CANVAS_H),
                               yscrollcommand=canvas_vscroll.set, 
                               xscrollcommand=canvas_hscroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        canvas_vscroll.config(command=self.canvas.yview)
        canvas_hscroll.config(command=self.canvas.xview)

        # Description text avec scrollbar
        desc_frame = tk.LabelFrame(viz_frame, text="Description / Métadonnées", 
                                  bg=Config.BG, fg=Config.FG, padx=8, pady=8)
        desc_frame.pack(fill="x", padx=6, pady=6)
        
        desc_scroll = tk.Scrollbar(desc_frame)
        desc_scroll.pack(side="right", fill="y")
        
        self.desc_text = tk.Text(desc_frame, height=8, wrap="word", bg="#071028", 
                                fg=Config.FG, font=Config.FONT_SMALL,
                                yscrollcommand=desc_scroll.set)
        self.desc_text.pack(fill="both", expand=True)
        desc_scroll.config(command=self.desc_text.yview)

        # Footer
        footer = tk.Frame(container, bg=Config.BG)
        footer.pack(fill="x", pady=6)
        tk.Label(footer, text="v7.1 Stabilisée : Tailles police réduites + Scrollbars • Ctrl+Z: Undo • Space: Animation",
                 bg=Config.BG, fg=Config.MUTED, font=Config.FONT_SMALL).pack(side="left", padx=12)

    def _bind_keys(self):
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<space>', lambda e: self.toggle_anim())

    # ---- CORE ACTIONS ----
    def randomize(self):
        self.intention_var.set(random.choice(["Protection","Passage","Sacralisation",
                                             "Lien","Rêve","Invocation"]))
        self.intens_var.set(random.randint(1,7))
        self.temporal_var.set(random.choice([t[0] for t in TEMPORALITES]))
        self.support_var.set(random.choice(SUPPORTS))
        self.generate()

    def generate(self):
        try:
            n = max(1, min(6, self.intens_var.get()))
            symbols = random.sample(SYMBOL_DATA, n)
            meme = PaleoMeme(
                intention=self.intention_var.get(),
                intensite=self.intens_var.get(),
                temporalite=self.temporal_var.get(),
                support=self.support_var.get(),
                symbols=symbols,
                created_at=time.time()
            )
            if self.current:
                self.history.append(self.current)
                if len(self.history) > 40:
                    self.history.pop(0)
            self.current = meme
            self._render(meme)
        except Exception as e:
            messagebox.showerror("Erreur génération", str(e))

    def undo(self):
        if self.history:
            self.current = self.history.pop()
            self._render(self.current)

    def transmute_current(self):
        if not self.current:
            messagebox.showwarning("Rien à transmuter", "Génère d'abord un mème.")
            return
        trans = []
        for s in self.current.symbols:
            ch,name,desc,plan,element,arch = s
            idx = TRANSMUTE_ORDER.index(element) if element in TRANSMUTE_ORDER else 0
            new_element = TRANSMUTE_ORDER[(idx+1) % len(TRANSMUTE_ORDER)]
            new_desc = desc + " (transmuté→" + new_element + ")"
            trans.append((ch,name,new_desc,plan,new_element,arch))
        newm = PaleoMeme(
            intention=self.current.intention + " • transmuté",
            intensite=max(1, min(7, self.current.intensite)),
            temporalite=self.current.temporalite,
            support=self.current.support,
            symbols=trans,
            created_at=time.time()
        )
        self.history.append(self.current)
        self.current = newm
        self._render(newm)

    # ---- RENDERING ----
    def _render(self, meme:PaleoMeme):
        self.oracle_text.delete("1.0", tk.END)
        self.oracle_text.insert("1.0", self._generate_oracle(meme))

        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", meme.to_text())

        self.canvas.delete("all")
        pal = next((t[1] for t in TEMPORALITES if t[0]==meme.temporalite), {})
        bg = pal.get("bg", "#0b1220")
        accent = pal.get("accent", Config.ACCENT)
        self.canvas.configure(bg=bg)
        
        # Protection contre les erreurs X11
        try:
            if meme.support == "Pierre":
                self._draw_mandala(meme, accent)
            elif meme.support == "Peau":
                self._draw_organic(meme, accent)
            elif meme.support == "Feuille":
                self._draw_spiral(meme, accent)
            elif meme.support == "Cuivre":
                self._draw_grid(meme, accent)
            else:
                self._draw_mandala(meme, accent)
        except Exception as e:
            # En cas d'erreur, afficher un message simple
            self.canvas.create_text(Config.CANVAS_W//2, Config.CANVAS_H//2, 
                                   text=f"Erreur de rendu: {str(e)[:50]}", 
                                   fill=Config.ERROR, font=Config.FONT_SMALL)

        names = " • ".join([f"{s[1]}" for s in meme.symbols])
        self.canvas.create_text(Config.CANVAS_W//2, Config.CANVAS_H-18, 
                               text=names, fill=Config.MUTED, font=Config.FONT_SMALL)

    def _generate_oracle(self, meme:PaleoMeme) -> str:
        tone = meme.temporalite
        lines = []
        intro = f"Oracle – {meme.intention} [{meme.intensite}] – {tone}"
        lines.append(intro)
        lines.append("—" * len(intro))
        for s in meme.symbols:
            ch,name,desc,plan,element,arch = s
            tpls = [
                f"{ch} {name} : {desc}.",
                f"→ Le {plan.lower()} recherche l'équilibre du {element.lower()}.",
                f"⚗️ Sous l'égide du {arch.lower()}, un seuil s'éclaire.",
                f"« {name} » murmure au rythme du {tone.lower()}.",
                f"Le symbole {ch} active la mémoire collective."
            ]
            lines.append(random.choice(tpls))
            if len(lines) >= 6:
                break
        lines.append("")
        lines.append("Invocation : " + " ".join([s[0] for s in meme.symbols]))
        return "\n".join(lines)

    # ---- DRAWING MODES (avec protection taille police) ----
    def _draw_mandala(self, meme:PaleoMeme, accent="#e6b800"):
        cx, cy = Config.CANVAS_W//2, Config.CANVAS_H//2 - 20
        n = len(meme.symbols)
        radius = 120 + (meme.intensite * 6)
        pulse = 8 * (1+math.sin(self.pulse)) if self.anim_running else 6
        self.canvas.create_oval(cx-radius-20-pulse, cy-radius-20-pulse, 
                               cx+radius+20+pulse, cy+radius+20+pulse, 
                               outline=accent, width=2, dash=(6,4))
        for i,(ch,name,desc,plan,element,arch) in enumerate(meme.symbols):
            a = 2*math.pi*i/n - math.pi/2
            x = cx + radius * math.cos(a)
            y = cy + radius * math.sin(a)
            self.canvas.create_oval(x-36, y-36, x+36, y+36, outline=Config.MUTED, width=2)
            # Police réduite et protégée
            self.canvas.create_text(x, y, text=ch, 
                                   font=("Segoe UI Symbol", 24, "bold"), fill=Config.FG)
        self.canvas.create_text(cx, cy, text="✦", font=("Georgia", 32, "bold"), fill=accent)

    def _draw_organic(self, meme:PaleoMeme, accent="#7dd3fc"):
        base_y = Config.CANVAS_H//2
        spacing = (Config.CANVAS_W - 200) // max(1, len(meme.symbols))
        start_x = 100
        for i,(ch,name,desc,plan,element,arch) in enumerate(meme.symbols):
            x = start_x + i * spacing
            y = base_y + 40 * math.sin(i*0.7 + self.pulse*0.5)
            self.canvas.create_text(x, y, text=ch, 
                                   font=("Segoe UI Symbol", 32), fill=Config.FG)
            self._draw_wave(x-60, y+30, x+60, y+30, amplitude=12 + 6*math.sin(self.pulse + i))
        for k in range(3):
            offset = 40*k + int(10*math.sin(self.pulse + k))
            self.canvas.create_line(40, base_y+offset, Config.CANVAS_W-40, base_y+offset, 
                                   fill=Config.MUTED, smooth=True)

    def _draw_spiral(self, meme:PaleoMeme, accent="#ffd166"):
        cx, cy = Config.CANVAS_W//2 - 50, Config.CANVAS_H//2 - 30
        a = 4 + meme.intensite
        b = 0.25 + meme.intensite*0.02
        theta = 0.0
        points = []
        for i in range(0, 400):
            r = a * math.exp(b * theta)
            x = cx + r * math.cos(theta)
            y = cy + r * math.sin(theta)
            points.append((x,y))
            theta += 0.2
            if r > min(Config.CANVAS_W, Config.CANVAS_H):
                break
        for i in range(len(points)-1):
            x1,y1 = points[i]; x2,y2 = points[i+1]
            self.canvas.create_line(x1,y1,x2,y2, fill=Config.MUTED, smooth=True, width=1)
        step = max(1, len(points)//(len(meme.symbols)+1))
        for i,s in enumerate(meme.symbols):
            idx = (i+1)*step
            if idx < len(points):
                x,y = points[idx]
                ch = s[0]
                self.canvas.create_text(x, y, text=ch, 
                                       font=("Segoe UI Symbol", 28), fill=Config.FG)

    def _draw_grid(self, meme:PaleoMeme, accent="#f472b6"):
        cols = 3
        rows = math.ceil(len(meme.symbols)/cols)
        w = 140; h = 110
        start_x = (Config.CANVAS_W - (w*cols))/2 + w/2
        start_y = 120
        for i,(ch,name,desc,plan,element,arch) in enumerate(meme.symbols):
            col = i % cols
            row = i // cols
            x = start_x + col * w
            y = start_y + row * h
            self.canvas.create_rectangle(x-60,y-50,x+60,y+50, outline=Config.MUTED, width=2)
            self.canvas.create_text(x, y-6, text=ch, 
                                   font=("Segoe UI Symbol", 28), fill=Config.FG)
            self.canvas.create_text(x, y+30, text=name, 
                                   font=Config.FONT_SMALL, fill=Config.MUTED)

    def _draw_wave(self, x1,y1,x2,y2, amplitude=10, segments=16):
        points = []
        for i in range(segments+1):
            t = i/segments
            x = x1 + (x2-x1)*t
            y = y1 + amplitude * math.sin(t*math.pi*2 + self.pulse)
            points.append((x,y))
        for i in range(len(points)-1):
            self.canvas.create_line(points[i][0], points[i][1], 
                                   points[i+1][0], points[i+1][1], 
                                   smooth=True, fill=Config.MUTED)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.oracle_text.delete("1.0", tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.oracle_text.insert("1.0", "Effacé – génère un nouveau mème.")
        self.desc_text.insert("1.0", "")

    # ---- ANIMATION ----
    def toggle_anim(self):
        self.anim_running = not self.anim_running
        self.anim_btn.config(text=("⏸ Animation" if self.anim_running else "▶ Animation"))
        if self.anim_running:
            self._animate()

    def _animate(self):
        if not self.anim_running:
            return
        self.pulse += 0.2
        if self.current:
            self._render(self.current)
        self.root.after(120, self._animate)

    # ---- EXPORTS ----
    def export_pmem(self):
        if not self.current:
            messagebox.showwarning("Rien à exporter", "Génère d'abord un mème.")
            return
        data = self.current.to_text()
        path = filedialog.asksaveasfilename(defaultextension=".pmem7", 
                                           filetypes=[("PaleoMeme text",".pmem7")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(data)
                messagebox.showinfo("Exporté", f"Fichier sauvegardé :\n{path}")
            except Exception as e:
                messagebox.showerror("Erreur écriture", str(e))

    def export_json(self):
        if not self.current:
            messagebox.showwarning("Rien à exporter", "Génère d'abord un mème.")
            return
        data = self.current.to_json()
        path = filedialog.asksaveasfilename(defaultextension=".json", 
                                           filetypes=[("JSON",".json")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(data)
                messagebox.showinfo("Exporté", f"JSON sauvegardé :\n{path}")
            except Exception as e:
                messagebox.showerror("Erreur écriture", str(e))

    def export_png(self):
        if not self.current:
            messagebox.showwarning("Rien à exporter", "Génère d'abord un mème.")
            return
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            messagebox.showerror("Pillow requis", "Installe Pillow : pip install pillow")
            return
        
        w,h = Config.CANVAS_W, Config.CANVAS_H
        pal = next((t[1] for t in TEMPORALITES if t[0]==self.current.temporalite), {})
        bg = pal.get("bg", "#071028")
        img = Image.new("RGBA", (w,h), bg)
        draw = ImageDraw.Draw(img)
        
        # Polices avec tailles réduites
        font_sym = get_font_pil(48)  # Réduit de 64 à 48
        font_small = get_font_pil(14)
        
        title = f"PALEO MEME – {self.current.intention} [{self.current.intensite}]"
        try:
            draw.text((18,12), title, fill=Config.FG, font=font_small)
        except:
            pass
        
        # Dessiner selon le support
        if self.current.support == "Pierre":
            cx,cy = w//2, h//2
            radius = 120 + (self.current.intensite*6)
            try:
                draw.text((cx-14, cy-26), "✦", font=get_font_pil(40), 
                         fill=pal.get("accent", Config.ACCENT))
            except:
                pass
            n = len(self.current.symbols)
            for i,(ch,name,desc,plan,element,arch) in enumerate(self.current.symbols):
                a = 2*math.pi*i/n - math.pi/2
                x = cx + radius*math.cos(a)
                y = cy + radius*math.sin(a)
                try:
                    draw.text((x-18,y-18), ch, font=font_sym, fill=Config.FG)
                except Exception:
                    draw.ellipse([x-20,y-20,x+20,y+20], outline=Config.FG)
                    
        elif self.current.support == "Peau":
            base_y = h//2
            spacing = (w-200)//max(1,len(self.current.symbols))
            start_x = 100
            for i,(ch,name,desc,plan,element,arch) in enumerate(self.current.symbols):
                x = start_x + i*spacing
                y = base_y + int(40*math.sin(i*0.7))
                try:
                    draw.text((x-18,y-18), ch, font=font_sym, fill=Config.FG)
                except:
                    draw.rectangle([x-20,y-20,x+20,y+20], outline=Config.FG)
                    
        elif self.current.support == "Feuille":
            cx,cy = w//2 - 50, h//2 - 30
            a = 4 + self.current.intensite
            b = 0.25 + self.current.intensite*0.02
            theta = 0.0
            points = []
            for i in range(0,300):
                r = a * math.exp(b * theta)
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)
                points.append((x,y))
                theta += 0.2
                if r > max(w,h):
                    break
            step = max(1, len(points)//(len(self.current.symbols)+1))
            for i,s in enumerate(self.current.symbols):
                idx = (i+1)*step
                if idx < len(points):
                    x,y = points[idx]
                    try:
                        draw.text((x-18,y-18), s[0], font=font_sym, fill=Config.FG)
                    except:
                        draw.rectangle([x-20,y-20,x+20,y+20], outline=Config.FG)
        else:
            # Grid
            cols = 3
            spacing_x = 160
            spacing_y = 120
            start_x = 200
            start_y = 140
            for i,(ch,name,desc,plan,element,arch) in enumerate(self.current.symbols):
                col = i % cols
                row = i // cols
                x = start_x + col*spacing_x
                y = start_y + row*spacing_y
                try:
                    draw.text((x-18,y-18), ch, font=font_sym, fill=Config.FG)
                except:
                    draw.rectangle([x-20,y-20,x+20,y+20], outline=Config.FG)
        
        # Légende en bas
        y0 = h-140
        for (ch,name,desc,plan,element,arch) in self.current.symbols:
            line = f"{ch} {name} ({plan}/{element}) – {desc}"
            if len(line) > 80:
                line = line[:77] + "..."
            try:
                draw.text((20,y0), line, fill=Config.MUTED, font=font_small)
            except:
                pass
            y0 += 20
            if y0 > h - 20:
                break

        path = filedialog.asksaveasfilename(defaultextension=".png", 
                                           filetypes=[("PNG Image",".png")])
        if path:
            try:
                img.save(path)
                messagebox.showinfo("Export PNG", f"Image sauvegardée :\n{path}")
            except Exception as e:
                messagebox.showerror("Erreur export", str(e))

# ---- RUN ----
def main():
    root = tk.Tk()
    app = PaleoAlchimiqueApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
