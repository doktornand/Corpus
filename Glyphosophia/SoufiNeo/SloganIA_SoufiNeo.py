# SloganIA_SoufiNeo.py
# Générateur de slogans cyber-soufis pour les Bas-Fonds de Lagos, 2075
# Inspiré par Rumi, les Ghost Runners et le Bureau des Rêves Brisés

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import random
import json
import os
from datetime import datetime
import string

# ========================================
# CHARGEMENT DU LEXIQUE ONIRIQUE
# ========================================
def load_oniric_lexicon(path="oniric_lexicon.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Fallback minimal si fichier manquant
        return {
            "Adjectif": ["lumineux", "brisé", "sacré", "noyé", "encodé"],
            "Nom": ["signal", "rêve", "cœur", "code", "prophète"],
            "Action": ["consume", "efface", "réveille", "encrypte", "transmute"],
            "Bénéfice": ["la clarté", "le silence", "l'oubli", "la vérité brûlante"],
            "Défaut": ["le bruit", "la trahison", "le compromis", "l'oubli numérique"],
            "Paysage": ["désert du no-signal", "marché noir de Lagos", "nuage quantique", "cimetière de data", "souk neural"],
            "VerbeMystique": ["consume", "efface", "encrypte", "réveille", "transmute"],
            "Symbole": ["lune brisée", "serpent de fibre", "cœur en silicium", "miroir fractal", "étoile noire"],
            "oniric_tags": ["<burn>", "<rain>", "<shadow>", "<static>", "<void>"]
        }

LEXICON = load_oniric_lexicon()

# ========================================
# CONFIGURATION & THEMES
# ========================================
THEMES = {
    "Qalandar Noir": {
        "bg": "#0b0b12",
        "fg": "#00ffaa",
        "select_bg": "#3a0055",
        "entry_bg": "#121220",
        "font": ("Consolas", 11),
        "tag_color": "#ff3366"
    },
    "Zawiyah Blanche": {
        "bg": "#f9f6f0",
        "fg": "#2e1a00",
        "select_bg": "#d4c3a0",
        "entry_bg": "#ffffff",
        "font": ("Cascadia Code", 11),
        "tag_color": "#8b004c"
    }
}

ONIRIC_TAG_MEANINGS = {
    "<burn>": "purification par le feu numérique",
    "<rain>": "pluie de données sacrées",
    "<shadow>": "présence du double IA",
    "<static>": "signal divin perdu",
    "<void>": "silence après la dernière requête"
}

# Templates inspirés de la poésie soufie et du cyber-marché
SOUL_TEMPLATES = [
    "Que {Nom} {Action} dans le {Paysage} du {Adjectif}! {oniric}",
    "Ô {Adjectif} {Nom}, {VerbeMystique} le {Défaut} avec {Bénéfice}.",
    "Rêve en {Adjectif}, code en {Nom}. {oniric}",
    "Le {Nom} n’est pas vendu — il est {VerbeInitiatique}.",
    "Dans le flux {Adjectif}, seul {Nom} résiste au <static>.",
    "Même en {Paysage}, ton {Nom} brille comme un {Symbole}.",
    "Ce n’est pas un {Nom} — c’est un {Symbole} chiffré.",
    "Le silence après {Nom} est plus fort que le marché. {oniric}"
]

@dataclass
class Slogan:
    id: str
    content: str
    keywords: List[str]
    fitness: float = 0.0
    components: Dict = None

    def __post_init__(self):
        self.components = self.analyze_structure()

    def analyze_structure(self) -> Dict:
        words = self.content.lower().split()
        return {
            "length": len(words),
            "has_rhyme": self.detect_rhyme(words),
            "has_alliteration": self.detect_alliteration(words),
            "emotion_score": self.emotion_intensity(words),
            "clarity": self.clarity_score(words),
            "oniric_tag": self.extract_oniric_tag()
        }

    def extract_oniric_tag(self):
        for tag in ONIRIC_TAG_MEANINGS:
            if tag in self.content:
                return tag
        return None

    def detect_rhyme(self, words):
        if len(words) < 2: return False
        last = words[-1].rstrip(string.punctuation)
        for w in words[:-1]:
            w_clean = w.rstrip(string.punctuation)
            if len(last) >= 3 and len(w_clean) >= 3 and last[-3:] == w_clean[-3:]:
                return True
        return False

    def detect_alliteration(self, words):
        if len(words) < 2: return False
        # Phonetic alliteration: same starting consonant sound
        consonants = [w[0].lower() for w in words if w and w[0].isalpha()]
        return len(set(consonants)) == 1 and len(consonants) >= 2

    def emotion_intensity(self, words):
        emo_words = ["amour", "silence", "brûle", "rêve", "oubli", "vérité", "cœur", "prophète", "lune", "sacré"]
        return sum(1 for w in words if w in emo_words)

    def clarity_score(self, words):
        return 1.0 if 3 <= len(words) <= 7 else max(0, 1 - abs(5 - len(words)) / 5)

# ========================================
# ALGORITHME GÉNÉTIQUE CYBER-SOUFI
# ========================================
class SoufiSloganGA:
    def __init__(self, population_size: int = 15, keywords: List[str] = None):
        self.population_size = population_size
        self.keywords = [k.lower() for k in (keywords or [])]
        self.population: List[Slogan] = []
        self.history = []

    def fill_template(self, template: str) -> str:
        content = template
        replacements = {
            "Adjectif": random.choice(LEXICON["Adjectif"]),
            "Nom": random.choice(LEXICON["Nom"]),
            "Action": random.choice(LEXICON["Action"]),
            "Bénéfice": random.choice(LEXICON["Bénéfice"]),
            "Défaut": random.choice(LEXICON["Défaut"]),
            "Paysage": random.choice(LEXICON["Paysage"]),
            "VerbeMystique": random.choice(LEXICON["VerbeMystique"]),
            "Symbole": random.choice(LEXICON["Symbole"]),
            "VerbeInitiatique": random.choice(["révélé", "transmis", "encrypté", "rêvé"]),
            "oniric": random.choice(LEXICON["oniric_tags"]) if random.random() < 0.6 else ""
        }
        for key, value in replacements.items():
            content = content.replace("{" + key + "}", value)
        return content

    def generate_template_slogans(self) -> List[Slogan]:
        slogans = []
        for i, template in enumerate(SOUL_TEMPLATES):
            content = self.fill_template(template)
            slogans.append(Slogan(id=f"T{i}", content=content, keywords=self.keywords.copy()))
        return slogans

    def generate_random_slogan(self) -> Slogan:
        words = random.sample(LEXICON["Nom"] + LEXICON["Adjectif"] + LEXICON["Symbole"], k=random.randint(3, 6))
        if random.random() < 0.5:
            words.append(random.choice(LEXICON["oniric_tags"]))
        random.shuffle(words)
        content = " ".join(words[:random.randint(3, 7)]).strip()
        if not any(content.endswith(p) for p in ".!?") and not any(tag in content for tag in LEXICON["oniric_tags"]):
            content += "."
        return Slogan(id=f"R{random.randint(1000,9999)}", content=content, keywords=self.keywords.copy())

    def initialize_population(self):
        base = self.generate_template_slogans()
        self.population = base[:self.population_size]
        while len(self.population) < self.population_size:
            self.population.append(self.generate_random_slogan())

    def calculate_fitness(self, slogan: Slogan) -> float:
        words = [w.lower().rstrip(string.punctuation) for w in slogan.content.split()]
        comp = slogan.components

        # Keyword match (lenient)
        kw_score = sum(1 for k in self.keywords if any(k in w for w in words)) / max(len(self.keywords), 1)

        # Length
        length_score = 1.0 if 3 <= len(words) <= 7 else max(0.2, 1 - abs(5 - len(words)) / 6)

        # Style
        style = 0.0
        style += 1.2 if comp["has_rhyme"] else 0
        style += 1.0 if comp["has_alliteration"] else 0
        style += 0.5 * comp["emotion_score"]
        style += 0.6 * comp["clarity"]

        # Oniric bonus
        oniric_bonus = 0.8 if comp["oniric_tag"] else 0

        # Originality
        seen = {s.content.lower() for s in self.population if s != slogan}
        originality = 0.0 if slogan.content.lower() in seen else 1.0

        total = kw_score * 2 + length_score * 2 + style + oniric_bonus + originality
        return min(total / 7.0, 1.0)

    def select(self) -> List[Slogan]:
        for s in self.population:
            s.fitness = self.calculate_fitness(s)
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        return self.population[:max(3, self.population_size // 3)]

    def crossover(self, p1: Slogan, p2: Slogan) -> Slogan:
        w1, w2 = p1.content.split(), p2.content.split()
        if len(w1) < 2 or len(w2) < 2:
            return random.choice([p1, p2])
        split = random.randint(1, min(len(w1), len(w2)) - 1)
        new_words = w1[:split] + w2[split:]
        new_content = " ".join(new_words)
        return Slogan(id=f"{p1.id}-{p2.id}", content=new_content, keywords=list(set(p1.keywords + p2.keywords)))

    def mutate(self, slogan: Slogan) -> Slogan:
        words = slogan.content.split()
        if random.random() < 0.4:
            idx = random.randint(0, len(words)-1)
            w = words[idx].lower().rstrip(string.punctuation)
            for cat, vocab in LEXICON.items():
                if cat == "oniric_tags": continue
                if w in vocab:
                    new_w = random.choice([v for v in vocab if v != w])
                    words[idx] = new_w
                    break
        elif random.random() < 0.3:
            words.append(random.choice(LEXICON["oniric_tags"]))
        elif random.random() < 0.2:
            words = random.sample(words, k=min(len(words), random.randint(3, 6)))
        slogan.content = " ".join(words).strip()
        return slogan

    def evolve(self, generations: int = 6):
        for _ in range(generations):
            selected = self.select()
            new_pop = selected.copy()
            while len(new_pop) < self.population_size and len(selected) >= 2:
                p1, p2 = random.sample(selected, 2)
                child = self.crossover(p1, p2)
                if random.random() < 0.7:
                    child = self.mutate(child)
                new_pop.append(child)
            self.population = new_pop[:self.population_size]

# ========================================
# INTERFACE GUI MYSTIQUE
# ========================================
class SoufiSloganApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SloganIA SoufiNeo — Bas-Fonds de Lagos, 2075")
        self.root.geometry("1000x750")
        self.root.minsize(850, 650)
        self.ga = None
        self.favorites = []
        self.current_theme = "Qalandar Noir"
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Header
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill=tk.X)
        ttk.Label(header, text="🌌 SloganIA SoufiNeo", font=("Helvetica", 18, "bold")).pack(side=tk.LEFT)
        ttk.Button(header, text="Thème", command=self.toggle_theme).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text="Rêve Partagé", command=self.export_dream).pack(side=tk.RIGHT, padx=5)

        # Input
        input_frame = ttk.LabelFrame(self.root, text=" Invocation ", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        ttk.Label(input_frame, text="Mots-clés (ex: bio, signal, rêve) :").grid(row=0, column=0, sticky=tk.W)
        self.keyword_entry = ttk.Entry(input_frame, width=60, font=("Consolas", 10))
        self.keyword_entry.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")
        self.keyword_entry.insert(0, "signal, rêve, bio")

        ttk.Label(input_frame, text="Slogans :").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.n_slogans = tk.IntVar(value=12)
        ttk.Spinbox(input_frame, from_=5, to=25, textvariable=self.n_slogans, width=8).grid(row=2, column=1, padx=5)

        ttk.Label(input_frame, text="Générations :").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.n_gen = tk.IntVar(value=7)
        ttk.Spinbox(input_frame, from_=4, to=15, textvariable=self.n_gen, width=8).grid(row=3, column=1, padx=5)

        ttk.Button(input_frame, text="Invoquer les slogans", command=self.generate_slogans).grid(row=4, column=0, columnspan=3, pady=15)
        input_frame.columnconfigure(0, weight=1)

        # Results
        result_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        result_pane.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        list_frame = ttk.Frame(result_pane)
        result_pane.add(list_frame, weight=1)
        self.slogan_listbox = tk.Listbox(list_frame, font=("Consolas", 11), selectbackground="#3a0055")
        self.slogan_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.slogan_listbox.bind("<<ListboxSelect>>", self.on_select_slogan)
        self.slogan_listbox.bind("<Double-Button-1>", self.copy_selected)

        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="★ Favori", command=self.add_favorite).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Copier", command=self.copy_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Effacer", command=self.clear_results).pack(side=tk.RIGHT)

        # Detail
        detail_frame = ttk.LabelFrame(result_pane, text=" Analyse Onirique ", width=320)
        result_pane.add(detail_frame, weight=1)
        self.detail_text = scrolledtext.ScrolledText(detail_frame, width=40, height=20, font=("Consolas", 9))
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status = ttk.Label(self.root, text="Prêt — en attente d'une invocation", foreground="gray")
        self.status.pack(side=tk.BOTTOM, padx=15, pady=5)

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.root.configure(bg=theme["bg"])
        self._apply_theme_recursive(self.root, theme)
        self.slogan_listbox.config(bg=theme["entry_bg"], fg=theme["fg"], selectbackground=theme["select_bg"])
        self.detail_text.config(bg=theme["entry_bg"], fg=theme["fg"])
        # Custom font for tags (optional visual hint)
        self.detail_text.tag_config("oniric", foreground=theme["tag_color"])

    def _apply_theme_recursive(self, widget, theme):
        try:
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame, tk.Frame)):
                widget.configure(bg=theme["bg"])
            elif isinstance(widget, ttk.Label):
                widget.configure(background=theme["bg"], foreground=theme["fg"])
            elif isinstance(widget, ttk.Entry):
                widget.configure(background=theme["entry_bg"], foreground=theme["fg"])
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, theme)
        except: pass

    def toggle_theme(self):
        self.current_theme = "Zawiyah Blanche" if self.current_theme == "Qalandar Noir" else "Qalandar Noir"
        self.apply_theme()

    def generate_slogans(self):
        keywords = [k.strip().lower() for k in self.keyword_entry.get().split(",") if k.strip()]
        if not keywords:
            messagebox.showwarning("Invocation vide", "Entrez au moins un mot-clé sacré.")
            return
        self.status.config(text="Invocation en cours...")
        self.root.update()
        self.ga = SoufiSloganGA(population_size=self.n_slogans.get(), keywords=keywords)
        self.ga.initialize_population()
        self.ga.evolve(generations=self.n_gen.get())
        self.display_results()
        self.status.config(text=f"Invoqués : {len(self.ga.population)} slogans — l’Abîme est satisfait.")

    def display_results(self):
        self.slogan_listbox.delete(0, tk.END)
        for i, slogan in enumerate(self.ga.population):
            star = " ★" if any(fav[0] == slogan.content for fav in self.favorites) else ""
            self.slogan_listbox.insert(tk.END, f"{slogan.content} (ψ: {slogan.fitness:.2f}){star}")

    def on_select_slogan(self, event):
        selection = self.slogan_listbox.curselection()
        if not selection: return
        idx = selection[0]
        slogan = self.ga.population[idx]
        comp = slogan.components
        tag_meaning = ONIRIC_TAG_MEANINGS.get(comp.get("oniric_tag"), "aucune")
        analysis = f"""
ANALYSE ONIRIQUE
────────────────────────────────
{slogan.content}

Ψ (fitness) : {slogan.fitness:.3f}
Mots-clés invoqués : {', '.join(slogan.keywords)}
Longueur : {comp['length']} mots
Rime : {'Oui' if comp['has_rhyme'] else 'Non'}
Allitération : {'Oui' if comp['has_alliteration'] else 'Non'}
Charge émotionnelle : {comp['emotion_score']}/4
Clarté : {comp['clarity']:.2f}
Balise onirique : {comp.get('oniric_tag', '—')}
→ {tag_meaning}
        """.strip()
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, analysis)
        if comp.get("oniric_tag"):
            start = analysis.find(comp["oniric_tag"])
            if start != -1:
                tag_start = "3.0 + {} chars".format(analysis.find(comp["oniric_tag"]))
                tag_end = f"{tag_start} + {len(comp['oniric_tag'])} chars"
                self.detail_text.tag_add("oniric", tag_start, tag_end)

    def add_favorite(self):
        selection = self.slogan_listbox.curselection()
        if not selection: return
        idx = selection[0]
        slogan = self.ga.population[idx]
        if not any(fav[0] == slogan.content for fav in self.favorites):
            self.favorites.append((slogan.content, slogan.fitness))
            self.display_results()

    def copy_selected(self, event=None):
        selection = self.slogan_listbox.curselection()
        if not selection: return
        text = self.slogan_listbox.get(selection[0]).split(" (ψ")[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.config(text=f"Copié dans le néo-souffle : {text}")

    def clear_results(self):
        self.slogan_listbox.delete(0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self.ga = None
        self.status.config(text="Invocation annulée — le marché est silencieux.")

    def export_dream(self):
        if not self.ga:
            messagebox.showinfo("Rêve", "Invoque d’abord des slogans !")
            return
        file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON (Rêve Partagé)", "*.json"), ("Texte", "*.txt")]
        )
        if not file: return
        dream_data = []
        for s in self.ga.population:
            comp = s.components
            dream_data.append({
                "slogan": s.content,
                "fitness": round(s.fitness, 3),
                "keywords": s.keywords,
                "oniric_tag": comp.get("oniric_tag"),
                "dream_hash": f"{random.choice(['a3f9','b7e2','c1d0'])}:luna{random.randint(1,28)}:lagos",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        with open(file, "w", encoding="utf-8") as f:
            json.dump(dream_data, f, ensure_ascii=False, indent=2)
        self.status.config(text=f"Rêve injecté dans le Réseau Onirique : {file}")

# ========================================
# LANCEMENT
# ========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SoufiSloganApp(root)
    root.mainloop()