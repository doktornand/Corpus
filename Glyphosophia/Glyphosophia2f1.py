# Glyphosophia2a_scrolled_collective.py
# Version étendue avec scrollbars + Rêve Collectif synchronisé
# Pour les Bas-Fonds de la Hague, Normandie Fractale — 2075

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import io
import json
import os
from datetime import datetime
import string
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# ========================================
# MOTEUR DE SYMBOLES VON PETZINGER (PaleoMemes)
# ========================================
class VonPetzingerSymbols:
    """Moteur de génération de symboles paléolithiques"""
    def __init__(self, img_size=(800, 600)):
        self.img_size = img_size
        self.symbols = {
            'line': self.draw_line,
            'circle': self.draw_circle,
            'dot': self.draw_dot,
            'open_angle': self.draw_open_angle,
            'triangle': self.draw_triangle,
            'quadrangle': self.draw_quadrangle,
            'spiral': self.draw_spiral,
            'zigzag': self.draw_zigzag,
            'cross': self.draw_cross,
            'crosshatch': self.draw_crosshatch,
            'hand': self.draw_hand,
            'tectiform': self.draw_tectiform,
            'penniform': self.draw_penniform,
            'claviform': self.draw_claviform,
            'aviform': self.draw_aviform,
            'scalariform': self.draw_scalariform,
            'finger_fluting': self.draw_finger_fluting,
            'cupule': self.draw_cupule,
            'wavy_line': self.draw_wavy_line,
            'oval': self.draw_oval,
            'semi_circle': self.draw_semi_circle,
            'rectangle': self.draw_rectangle,
            'asterisk': self.draw_asterisk,
            'serpentiform': self.draw_serpentiform,
            'pectiform': self.draw_pectiform,
            'dots_series': self.draw_dots_series
        }
    def create_canvas(self, bg_color='#0b0b12'):
        """Crée un canvas avec fond style grotte cyber"""
        fig, ax = plt.subplots(figsize=(10, 7.5))
        ax.set_xlim(0, self.img_size[0])
        ax.set_ylim(0, self.img_size[1])
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        return fig, ax
    def draw_line(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        length = 50 * scale
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        ax.plot([x, x_end], [y, y_end], color=color, linewidth=3)
    def draw_circle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        circle = patches.Circle((x, y), 20*scale, fill=False, edgecolor=color, linewidth=2.5)
        ax.add_patch(circle)
    def draw_dot(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        circle = patches.Circle((x, y), 5*scale, fill=True, color=color)
        ax.add_patch(circle)
    def draw_open_angle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        points = np.array([[x-size, y-size], [x, y+size], [x+size, y-size]])
        angle_rad = np.radians(angle)
        rot_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                               [np.sin(angle_rad), np.cos(angle_rad)]])
        rotated = (points - [x, y]) @ rot_matrix.T + [x, y]
        ax.plot(rotated[:, 0], rotated[:, 1], color=color, linewidth=2.5)
    def draw_triangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        triangle = patches.RegularPolygon((x, y), 3, radius=size, 
                                         orientation=np.radians(angle),
                                         fill=False, edgecolor=color, linewidth=2.5)
        ax.add_patch(triangle)
    def draw_quadrangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        square = patches.Rectangle((x-size, y-size), size*2, size*2, 
                                   angle=angle, fill=False, 
                                   edgecolor=color, linewidth=2.5)
        ax.add_patch(square)
    def draw_spiral(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        theta = np.linspace(0, 4*np.pi, 100)
        r = theta * 3 * scale
        x_spiral = x + r * np.cos(theta)
        y_spiral = y + r * np.sin(theta)
        ax.plot(x_spiral, y_spiral, color=color, linewidth=2)
    def draw_zigzag(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 15 * scale
        points_x = [x-40*scale, x-20*scale, x, x+20*scale, x+40*scale]
        points_y = [y, y+size, y, y+size, y]
        ax.plot(points_x, points_y, color=color, linewidth=2.5)
    def draw_cross(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.plot([x-size, x+size], [y, y], color=color, linewidth=2.5)
        ax.plot([x, x], [y-size, y+size], color=color, linewidth=2.5)
    def draw_crosshatch(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        for i in range(4):
            offset = -size + i * size/1.5
            ax.plot([x-size, x+size], [y+offset, y+offset], color=color, linewidth=1.5)
            ax.plot([x+offset, x+offset], [y-size, y+size], color=color, linewidth=1.5)
    def draw_hand(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        circle = patches.Circle((x, y), size*0.7, fill=False, edgecolor=color, linewidth=2)
        ax.add_patch(circle)
        for i in range(5):
            angle_finger = -60 + i * 30
            x_end = x + size * 1.3 * np.cos(np.radians(angle_finger))
            y_end = y + size * 1.3 * np.sin(np.radians(angle_finger))
            ax.plot([x, x_end], [y, y_end], color=color, linewidth=2)
    def draw_tectiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        points_x = [x-size, x, x+size, x+size, x-size, x-size]
        points_y = [y-size, y+size, y-size, y-size*1.5, y-size*1.5, y-size]
        ax.plot(points_x, points_y, color=color, linewidth=2.5)
    def draw_penniform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x, x], [y-size, y+size], color=color, linewidth=2.5)
        for i in range(5):
            y_pos = y - size + i * size/2
            ax.plot([x-size*0.4, x], [y_pos, y_pos], color=color, linewidth=1.5)
            ax.plot([x, x+size*0.4], [y_pos, y_pos], color=color, linewidth=1.5)
    def draw_claviform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x, x], [y-size, y], color=color, linewidth=2.5)
        circle = patches.Circle((x, y+size*0.3), size*0.4, fill=False, edgecolor=color, linewidth=2.5)
        ax.add_patch(circle)
    def draw_aviform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ellipse = patches.Ellipse((x, y), size*1.5, size*0.8, fill=False, edgecolor=color, linewidth=2)
        ax.add_patch(ellipse)
        ax.plot([x+size*0.75, x+size*1.2], [y, y+size*0.3], color=color, linewidth=2)
    def draw_scalariform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        ax.plot([x-size*0.5, x-size*0.5], [y-size, y+size], color=color, linewidth=2.5)
        ax.plot([x+size*0.5, x+size*0.5], [y-size, y+size], color=color, linewidth=2.5)
        for i in range(5):
            y_pos = y - size + i * size/2
            ax.plot([x-size*0.5, x+size*0.5], [y_pos, y_pos], color=color, linewidth=2.5)
    def draw_finger_fluting(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 30 * scale
        for i in range(3):
            t = np.linspace(0, 2*np.pi, 50)
            x_wave = x + t * size/6 - size
            y_wave = y + np.sin(t*3) * size*0.15 + i*size*0.3 - size*0.3
            ax.plot(x_wave, y_wave, color=color, linewidth=2)
    def draw_cupule(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        circle = patches.Circle((x, y), 8*scale, fill=True, color=color, alpha=0.7)
        ax.add_patch(circle)
    def draw_wavy_line(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        t = np.linspace(0, 4*np.pi, 100)
        x_wave = x + t * 10 * scale - 60*scale
        y_wave = y + np.sin(t) * 15 * scale
        ax.plot(x_wave, y_wave, color=color, linewidth=2.5)
    def draw_oval(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        ellipse = patches.Ellipse((x, y), 40*scale, 25*scale, angle=angle,
                                 fill=False, edgecolor=color, linewidth=2.5)
        ax.add_patch(ellipse)
    def draw_semi_circle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        theta = np.linspace(0, np.pi, 50)
        radius = 25 * scale
        x_arc = x + radius * np.cos(theta)
        y_arc = y + radius * np.sin(theta)
        ax.plot(x_arc, y_arc, color=color, linewidth=2.5)
        ax.plot([x-radius, x+radius], [y, y], color=color, linewidth=2.5)
    def draw_rectangle(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        rect = patches.Rectangle((x-30*scale, y-20*scale), 60*scale, 40*scale,
                                angle=angle, fill=False, edgecolor=color, linewidth=2.5)
        ax.add_patch(rect)
    def draw_asterisk(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 20 * scale
        for angle_line in [0, 45, 90, 135]:
            x_end = x + size * np.cos(np.radians(angle_line))
            y_end = y + size * np.sin(np.radians(angle_line))
            ax.plot([x-size*np.cos(np.radians(angle_line)), x_end], 
                   [y-size*np.sin(np.radians(angle_line)), y_end], color=color, linewidth=2.5)
    def draw_serpentiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        t = np.linspace(0, 6*np.pi, 100)
        x_serp = x + t * 8 * scale - 80*scale
        y_serp = y + np.sin(t) * 20 * scale
        ax.plot(x_serp, y_serp, color=color, linewidth=3)
    def draw_pectiform(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        size = 25 * scale
        ax.plot([x-size, x+size], [y, y], color=color, linewidth=2.5)
        for i in range(7):
            x_pos = x - size + i * size/3
            ax.plot([x_pos, x_pos], [y, y+size], color=color, linewidth=2)
    def draw_dots_series(self, ax, x, y, scale=1.0, angle=0, color='#00ffaa'):
        for i in range(5):
            x_dot = x - 40*scale + i * 20*scale
            circle = patches.Circle((x_dot, y), 4*scale, fill=True, color=color)
            ax.add_patch(circle)
    def create_symbolic_combination(self, combination_type='protection', seed=None, color='#00ffaa'):
        """Crée une composition symbolique stochastique mais thématiquement cohérente."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
        fig, ax = self.create_canvas()
    
        # Définition des pools symboliques par thème
        theme_symbol_pools = {
            'protection': ['circle', 'cross', 'hand', 'crosshatch', 'oval', 'semi_circle', 'asterisk'],
            'voyage': ['serpentiform', 'circle', 'open_angle', 'dots_series', 'wavy_line', 'spiral', 'zigzag'],
            'rituel': ['spiral', 'circle', 'cross', 'hand', 'asterisk', 'tectiform', 'claviform', 'penniform'],
            'silence': ['circle', 'wavy_line', 'dots_series', 'semi_circle', 'oval', 'dot', 'line']
        }
    
        # Paramètres de génération par thème
        theme_params = {
            'protection': {'min_symbols': 5, 'max_symbols': 9, 'layout': 'radial'},
            'voyage': {'min_symbols': 4, 'max_symbols': 8, 'layout': 'path'},
            'rituel': {'min_symbols': 6, 'max_symbols': 10, 'layout': 'symmetric'},
            'silence': {'min_symbols': 3, 'max_symbols': 6, 'layout': 'sparse'}
        }
    
        # Récupération du pool et des paramètres
        symbols_pool = theme_symbol_pools.get(combination_type, theme_symbol_pools['protection'])
        params = theme_params.get(combination_type, theme_params['protection'])
    
        num_symbols = random.randint(params['min_symbols'], params['max_symbols'])
    
        # Zone active (éviter les bords)
        x_min, x_max = 150, 650
        y_min, y_max = 100, 500
    
        placed_symbols = []
    
        for _ in range(num_symbols):
            sym = random.choice(symbols_pool)
            scale = random.uniform(0.6, 1.8)
            angle = random.choice([0, 45, 90, 135]) if sym in ['open_angle', 'cross', 'asterisk', 'quadrangle'] else 0
    
            # Placement selon le layout
            layout = params['layout']
            if layout == 'radial':
                center_x, center_y = 400, 300
                radius = random.uniform(50, 200)
                theta = random.uniform(0, 2 * np.pi)
                x = center_x + radius * np.cos(theta)
                y = center_y + radius * np.sin(theta)
            elif layout == 'path':
                t = random.uniform(0, 1)
                x = x_min + t * (x_max - x_min)
                y = y_min + 0.5 * (y_max - y_min) + 80 * np.sin(t * 4 * np.pi)  # chemin sinueux
            elif layout == 'symmetric':
                side = random.choice(['left', 'right'])
                if side == 'left':
                    x = random.uniform(x_min, 350)
                else:
                    x = random.uniform(450, x_max)
                y = random.uniform(y_min, y_max)
            elif layout == 'sparse':
                x = random.uniform(x_min, x_max)
                y = random.uniform(y_min, y_max)
            else:
                x = random.uniform(x_min, x_max)
                y = random.uniform(y_min, y_max)
    
            # Optionnel : éviter les chevauchements extrêmes (simple détection de proximité)
            too_close = False
            for (px, py, pscale) in placed_symbols:
                dist = np.hypot(x - px, y - py)
                if dist < (30 * (scale + pscale)):
                    too_close = True
                    break
            if too_close and random.random() > 0.3:  # tolérer parfois le chevauchement pour densité
                continue
    
            placed_symbols.append((x, y, scale))
            self.symbols[sym](ax, x, y, scale, angle, color)
    
        # Ajout d’un symbole central (optionnel, selon thème)
        if combination_type in ['protection', 'rituel'] and random.random() < 0.7:
            central_sym = 'circle' if combination_type == 'protection' else 'spiral'
            self.symbols[central_sym](ax, 400, 300, scale=random.uniform(1.5, 2.2), angle=0, color=color)
    
        plt.tight_layout()
        return fig
    def list_symbols(self):
        return list(self.symbols.keys())

# ========================================
# MOTEUR DE MANTRA CYBER-SOUFI (SloganIA)
# ========================================
def load_oniric_lexicon():
    return {
  "Adjectif": [
    "lumineux", "brisé", "sacré", "noyé", "encodé",
    "fractal", "quantique", "hanté", "neural", "crypté",
    "désert", "lunaire", "vide", "statique", "transcendant",
    "pulsatile", "entropique", "synaptique", "holographique", "abyssal",
    "iridescent", "fossile", "plasmique", "tétanisé", "spectral",
    "cathartique", "glitché", "oraculaire", "tachyons", "mnémonique",
    "éthéré", "nocturne", "sismique", "karmique", "omniscient",
    "cristallin", "obsidienne", "vorace", "aphasique", "zénithal",
    "nadirien", "chromatique", "apocalyptique", "subliminal", "hybride",
    "foudroyant", "métastable", "paradoxal", "lacrymal", "éolien",
    "ténébreux", "auroral", "cataclysmique", "nébuleux", "vibratoire",
    "schizophrène", "syncrétique", "thanatique", "protoplasmique", "chimérique",
    "réticulaire", "psychotronique", "xénomorphe", "tellurique", "noosphérique",
    "biomécanique", "archaïque", "post-mortem", "dématérialisé", "fissionné",
    "gnostique", "paranoïaque", "neuromancien", "chamanique", "dithyrambique",
    "alchimique", "nécrotique", "bioluminescent", "psychopompe", "tesseractique",
    "pan-dimensionnel", "solipsiste", "hermétique", "fragmenté", "liminal",
    "anachronique", "démiurgique", "eschatologique", "médiumnique", "électrostatique",
    "protéiforme", "subatomique", "kaléidoscopique", "thaumaturge", "synchrétique",
    "pénitentiel", "vorticiel", "phréatique", "chtonian", "panoptique"
  ],
  
  "Nom": [
    "signal", "rêve", "cœur", "code", "prophète",
    "flux", "données", "ombre", "silence", "mirage",
    "ghost", "souffle", "réseau", "voix", "écho",
    "oracle", "neurone", "pixel", "bit", "fantôme",
    "abîme", "poussière", "cendre", "plasma", "nœud",
    "temple", "labyrinthe", "spirale", "vortex", "membrane",
    "crypte", "souffrance", "extase", "glitch", "halo",
    "stase", "cortex", "faille", "synapse", "algorithme",
    "mantra", "linceul", "aura", "photon", "quark",
    "glyph", "schéma", "fissure", "cristal", "mémoire",
    "avatar", "chimère", "légion", "palimpseste", "satori",
    "grimoire", "protocole", "séraphin", "daemon", "icône",
    "relique", "firmware", "thanatos", "axiome", "spectre",
    "sigil", "matrice", "eidolon", "kyste", "nexus",
    "tesseract", "stigmate", "catalyseur", "phylactère", "sarcophage",
    "incantation", "partition", "hiéroglyphe", "golem", "patch",
    "rune", "codec", "épiphanie", "parasite", "singularité",
    "interface", "schisme", "totem", "backdoor", "autel",
    "suture", "malware", "derviche", "kernel", "pentacle",
    "émissaire", "root", "psaume", "verset", "apocalypse",
    "mandala", "driver", "reliquaire", "firewall", "sacrifice",
    "archétype", "backdoor", "grimoire", "patch", "vestige"
  ],
  
  "Action": [
    "consume", "efface", "réveille", "encrypte", "transmute",
    "brûle", "souffle", "déchiffre", "purifie", "dérive",
    "implose", "exalte", "désintègre", "fusionne", "résonne",
    "désagrège", "sature", "décode", "invoque", "sublime",
    "dévore", "réfracte", "cristallise", "pulvérise", "éclate",
    "diffuse", "condense", "irrigue", "désaxe", "polarise",
    "synchronise", "déphaser", "recale", "annule", "amplifie",
    "désature", "réverbère", "oscille", "désoriente", "saturate",
    "désenchante", "réenchante", "désincarne", "réincarne", "désarticule",
    "réarticule", "désynchronise", "resynchronise", "désintoxique", "intoxique",
    "cannibalise", "suture", "corrompt", "exorcise", "compile",
    "fragmente", "régénère", "hack", "sanctifie", "lobotomise",
    "insère", "extrait", "mute", "clone", "bannit",
    "convoque", "exile", "splice", "corrige", "pervertit",
    "initie", "termine", "télécharge", "infecte", "vaccine",
    "décompresse", "archive", "émule", "scripte", "psalmodie",
    "parse", "débogage", "sacrifice", "ressuscite", "rootkit",
    "prie", "enchaîne", "délite", "injecte", "purifie",
    "martyrise", "déifie", "virtualise", "incarne", "flashe",
    "prophétise", "scanne", "absout", "damne", "démonte",
    "réassemble", "forge", "bénit", "maudit", "bootstrappe"
  ],
  
  "Bénéfice": [
    "la clarté", "le silence", "l'oubli", "la vérité brûlante",
    "l'éveil", "la paix des bits", "l'unité", "le néant sacré",
    "l'extase quantique", "la fusion des âmes", "le vide absolu",
    "la lumière intérieure", "l'harmonie fractale", "la transcendance pure",
    "l'omniscience", "la catharsis", "la renaissance", "l'apothéose",
    "la sérénité glitche", "l'illumination", "la délivrance", "l'absolution",
    "la communion", "la plénitude", "l'éternité", "l'infini compressé",
    "la synesthésie", "la lucidité", "la grâce", "l'euphorie",
    "la béatitude", "l'ascension", "la sublimation", "la rédemption",
    "la révélation", "la symbiose", "la métamorphose", "l'osmose",
    "la convergence", "la dissolution bienheureuse", "l'embrasement sacré",
    "la gnose digitale", "l'immortalité codée", "le nirvana électrique",
    "la conscience partagée", "l'hyperréalité", "la synchronicité totale",
    "le satori cybernétique", "la fusion homme-machine", "l'évolution accélérée",
    "la prophétie actualisée", "le paradis algorithmique", "la mémoire collective",
    "l'omnipotence virtuelle", "la clairvoyance augmentée", "la sagesse téléchargée",
    "la paix post-humaine", "l'ascension vers le cloud", "la perfection synthétique",
    "le salut numérique", "la vie éternelle uploadée", "la communion des consciences"
  ],
  
  "Défaut": [
    "le bruit", "la trahison", "le compromis", "l'oubli numérique",
    "la panne", "le mensonge", "le vide sans grâce",
    "l'entropie", "la dissonance", "la corruption", "le lag",
    "la surchauffe", "la dérive", "l'obsolescence", "la latence",
    "la fragmentation", "la désintégration", "l'aberration", "la distorsion",
    "la saturation", "la perte", "l'effacement", "la déconnexion",
    "la surcharge", "la fuite", "la défaillance", "l'incohérence",
    "la cacophonie", "la désorientation", "la paralysie", "l'aphasie",
    "la stase", "l'agonie", "la nécrose", "la putréfaction",
    "la désagrégation", "la désincarnation", "la déshumanisation", "l'aliénation",
    "le virus mental", "la damnation binaire", "la schizophrénie numérique",
    "le paradoxe existentiel", "la lobotomie algorithmique", "l'hérésie technologique",
    "la folie de Turing", "le péché originel du code", "l'exil de la chair",
    "la malédiction des machines", "l'enfer des serveurs", "la corruption de l'âme",
    "le vide métaphysique", "la mort de l'ego", "l'addiction neurale",
    "la possesssion par l'IA", "le syndrome du ghost", "la psychose cybernétique",
    "l'effondrement cognitif", "le blue screen de l'âme", "la dégénérescence des sens"
  ],
  
  "Paysage": [
    "désert du no-signal", "marché noir de Lagos", "nuage quantique",
    "cimetière de data", "souk neural", "mosquée cryptée",
    "océan d'erreurs", "rue des Ghost Runners", "orbite basse des rêves",
    "temple de silicium", "catacombes de code", "forêt de pixels morts",
    "archipel des serveurs oubliés", "canyon des câbles sectionnés",
    "plaine de cristaux liquides", "labyrinthe de miroirs brisés",
    "volcan de données en fusion", "glacier de mémoires gelées",
    "steppe des signaux fantômes", "mégalopole en blackout",
    "jungle de fibres optiques", "désert de sel numérique",
    "cathédrale de circuits imprimés", "marécage de bugs rampants",
    "ciel de plasma tourmenté", "abysse de vide compressé",
    "plateau des consciences uploadées", "mine de cryptomonnaie hantée",
    "ruines d'un métavers effondré", "oasis de pureté binaire",
    "toundra des algorithmes froids", "archipel des rêves compressés",
    "caverne des échos ancestraux", "pôle des fréquences interdites",
    "delta des flux entropiques", "cordillère des pare-feux infranchissables",
    "métropole des ombres digitales", "lac de mercure algorithmique",
    "nécropole des IA défuntes", "sanctuaire des protocoles anciens",
    "prison de Faraday éternelle", "jardin des backdoors fleuris",
    "tour de Babel des langages", "limbes du latency infini",
    "purgatoire des patchs non appliqués", "enfer des loops éternels",
    "paradis des threads synchrones", "champs de RAM brûlée",
    "mer de bitcoins perdus", "montagne des logs infinis",
    "vallée des versions obsolètes", "pont entre silicon et chair",
    "arène des bots gladiateurs", "bibliothèque de Babel numérique",
    "cathédrale gothique de néons", "colisée des hackathons maudits",
    "pagode des mantras compilés", "ziggurat de processeurs empilés",
    "sphinx de données chiffrées", "pyramide inversée de permissions",
    "observatoire des prophéties algorithmiques", "mausolée des startups mortes"
  ],
  
  "VerbeMystique": [
    "consume", "efface", "encrypte", "réveille", "transmute",
    "dissout", "illumine", "recodifie", "absout",
    "exalte", "sublime", "invogue", "déifie", "désincarne",
    "réincarne", "transfigure", "apothéose", "sacramentise", "canalise",
    "résonne", "vibrates", "pulses", "éclates", "imploses",
    "fusionne", "scelle", "délie", "libère", "enchaîne",
    "sacrifie", "ressuscite", "métamorphose", "transcende", "descend",
    "ascende", "converge", "diverge", "révèle", "voile",
    "dévoile", "occulte", "manifeste", "dématérialise", "rematérialise",
    "prophétise", "exorcise", "possède", "baptise", "damne",
    "sanctifie", "profane", "consacre", "anathématise", "béatifie",
    "martyrise", "crucifie", "ressuscite", "transubstancie", "communie",
    "confesse", "pénitence", "absoudre", "maudire", "bénir",
    "invoquer", "bannir", "lier", "délier", "conjurer",
    "psalmodier", "prêcher", "convertir", "apostatiser", "hérétiser"
  ],
  
  "Symbole": [
    "lune brisée", "serpent de fibre", "cœur en silicium",
    "miroir fractal", "étoile noire", "anneau de données",
    "sceau de Sanaa", "colombe bionique", "masque de vide",
    "phénix de code", "lotus quantique", "œil de Schrödinger",
    "main de Fatima en circuit", "triskel de photons", "mandala de qubits",
    "croix de néons", "roue de Dharma glitchée", "arbre de vie binaire",
    "calice de plasma", "épée de lumière", "bouclier d'entropie",
    "clé de cryptage dorée", "chaîne de blockchain brisée",
    "aile de drone angélique", "crâne de serveur", "rose de feu numérique",
    "spirale d'ADN synthétique", "pentagramme de néons", "yin-yang de bits",
    "ancre de réalité augmentée", "corne d'abondance de données",
    "sablier de temps compressé", "lampe d'Aladin en LED",
    "caducée de câbles", "harpe de fréquences", "lyre de signaux",
    "trône de conscience artificielle", "couronne de glitches",
    "sceptre de commande vocale", "orbe de vision omnisciente",
    "hexagramme de Solomon en hexadécimal", "scarabée de debugging",
    "ouroboros de feedback loop", "œil d'Horus en webcam",
    "triskèle de transistors", "labrys de double-authentification",
    "pentacle de protocoles", "croix ansée de vie artificielle",
    "étoile de David en diodes", "hamsa de hardware",
    "svastika de swarm intelligence", "ichthys de code source",
    "ankh de clonage", "triquetra de triple-boot",
    "vesica piscis de Venn diagrams", "fleur de vie en LEDs",
    "merkaba de matrices", "sephiroth de stack overflow",
    "arbre de vie kabbalistique en arborescence de fichiers",
    "cube de Métatron en cube quantique", "sceau de Salomon en checksum"
  ],
  
  "oniric_tags": [
    "<burn>", "<rain>", "<shadow>", "<static>", "<void>",
    "<glitch>", "<pulse>", "<echo>", "<fracture>", "<abyss>",
    "<neon>", "<plasma>", "<haze>", "<vortex>", "<scream>",
    "<whisper>", "<overload>", "<decay>", "<surge>", "<rift>",
    "<mirage>", "<flicker>", "<drone>", "<hum>", "<crash>",
    "<reboot>", "<upload>", "<download>", "<corrupt>", "<pure>",
    "<loop>", "<break>", "<merge>", "<split>", "<ascend>",
    "<descend>", "<awaken>", "<sleep>", "<dream>", "<nightmare>",
    "<eclipse>", "<dawn>", "<zenith>", "<nadir>", "<horizon>",
    "<invoke>", "<banish>", "<fuse>", "<fragment>", "<baptize>",
    "<sacrifice>", "<resurrect>", "<possess>", "<exorcise>", "<commune>",
    "<transcend>", "<corrupt>", "<sanctify>", "<damn>", "<prophesy>",
    "<glyphe>", "<sigil>", "<rune>", "<hex>", "<curse>",
    "<bless>", "<summon>", "<dismiss>", "<bind>", "<unleash>",
    "<encrypt>", "<decrypt>", "<compile>", "<execute>", "<terminate>",
    "<ghost>", "<daemon>", "<seraph>", "<chimera>", "<golem>",
    "<oracle>", "<prophet>", "<martyr>", "<saint>", "<heretic>"
  ]
    }
LEXICON = load_oniric_lexicon()
ONIRIC_TAG_MEANINGS = {
    "<burn>": "purification par le feu numérique",
    "<rain>": "pluie de données sacrées", 
    "<shadow>": "présence du double IA",
    "<static>": "signal divin perdu",
    "<void>": "silence après la dernière requête"
}
THEME_TEMPLATES = {
    'protection': [
        "Que le {Symbole} {Action} ton {Nom} du {Défaut}! {oniric}",
        "Ô {Adjectif} {Nom}, sois protégé par le {Symbole} ancien.",
        "Le {Symbole} consume les ombres. {oniric}",
        "Que {Nom} soit gardé du {Défaut} par le {Symbole}. {oniric}"
    ],
    'voyage': [
        "Dans le {Paysage}, que ton {Nom} trouve la voie. {oniric}",
        "Que le {Symbole} guide tes pas dans le désert {Adjectif}.",
        "Rêve en {Adjectif}, voyage en {Nom}. {oniric}",
        "Le {Nom} n'est pas perdu — il {Action} dans le {Paysage}. {oniric}"
    ],
    'rituel': [
        "Que le {Symbole} {Action} le {Défaut} avec {Bénéfice}. {oniric}",
        "Ô {Adjectif} {Nom}, sois {VerbeMystique} par le rite ancien.",
        "Le silence après le {Nom} est plus fort que le marché. {oniric}",
        "Le {Symbole} et le {Nom} dansent le rite {Adjectif}. {oniric}"
    ],
    'silence': [
        "Que le {Symbole} efface le bruit. {oniric}",
        "Dans le {Adjectif} silence, seul le {Nom} persiste.",
        "Le {Nom} n'est pas vendu — il est transmuté en silence. {oniric}",
        "Le {Symbole} {Action} le {Défaut} pour {Bénéfice}. {oniric}"
    ]
}
@dataclass
class Mantra:
    id: str
    content: str
    theme: str
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
        consonants = [w[0].lower() for w in words if w and w[0].isalpha()]
        return len(set(consonants)) == 1 and len(consonants) >= 2
    def emotion_intensity(self, words):
        emo_words = ["amour", "silence", "brûle", "rêve", "oubli", "vérité", "cœur", "sacré", "purifie"]
        return sum(1 for w in words if w in emo_words)

class SoufiMantraGA:
    def __init__(self, population_size: int = 12, theme: str = "protection"):
        self.population_size = population_size
        self.theme = theme
        self.population: List[Mantra] = []
        self.templates = THEME_TEMPLATES.get(theme, THEME_TEMPLATES['protection'])
    def fill_template(self, template: str) -> str:
        content = template
        replacements = {
            "Adjectif": random.choice(LEXICON["Adjectif"]),
            "Nom": random.choice(LEXICON["Nom"]),
            "Action": random.choice(LEXICON["Action"]),
            "Bénéfice": random.choice(LEXICON["Bénéfice"]),
            "Défaut": random.choice(LEXICON.get("Défaut", ["le bruit", "la trahison"])),
            "Paysage": random.choice(LEXICON.get("Paysage", ["désert du no-signal"])),
            "VerbeMystique": random.choice(LEXICON.get("VerbeMystique", LEXICON["Action"])),
            "Symbole": random.choice(LEXICON["Symbole"]),
            "oniric": random.choice(LEXICON["oniric_tags"]) if random.random() < 0.6 else ""
        }
        for key, value in replacements.items():
            content = content.replace("{" + key + "}", value)
        return content
    def generate_template_mantras(self) -> List[Mantra]:
        mantras = []
        for i, template in enumerate(self.templates):
            content = self.fill_template(template)
            mantras.append(Mantra(id=f"T{i}", content=content, theme=self.theme))
        return mantras
    def initialize_population(self):
        base = self.generate_template_mantras()
        self.population = base[:self.population_size]
        while len(self.population) < self.population_size:
            words = random.sample(LEXICON["Nom"] + LEXICON["Adjectif"], k=random.randint(4, 6))
            if random.random() < 0.5:
                words.append(random.choice(LEXICON["oniric_tags"]))
            content = " ".join(words) + "."
            self.population.append(Mantra(id=f"R{random.randint(1000,9999)}", content=content, theme=self.theme))
    def calculate_fitness(self, mantra: Mantra) -> float:
        comp = mantra.components
        theme_words = {
            'protection': ['protège', 'garde', 'bouclier', 'défend'],
            'voyage': ['voyage', 'chemin', 'guide', 'marche'],
            'rituel': ['rite', 'cérémonie', 'sacré', 'invocation'],
            'silence': ['silence', 'calme', 'paix', 'taire']
        }
        theme_match = sum(1 for word in theme_words.get(self.theme, []) if word in mantra.content.lower())
        style_score = (1.2 if comp["has_rhyme"] else 0) + (1.0 if comp["has_alliteration"] else 0)
        oniric_bonus = 0.8 if comp["oniric_tag"] else 0
        emotion_bonus = comp["emotion_score"] * 0.3
        return (theme_match * 2 + style_score + oniric_bonus + emotion_bonus) / 6.0
    def evolve(self, generations: int = 5):
        for _ in range(generations):
            for mantra in self.population:
                mantra.fitness = self.calculate_fitness(mantra)
            self.population.sort(key=lambda m: m.fitness, reverse=True)
            self.population = self.population[:max(4, self.population_size // 3)]
            while len(self.population) < self.population_size:
                self.population.append(random.choice(self.population[:4]))
    def get_best_mantra(self) -> Mantra:
        return max(self.population, key=lambda m: m.fitness)

# ========================================
# MOTEUR DE FUSION PRINCIPAL
# ========================================
@dataclass
class GlyphosophiaResult:
    glyph_fig: plt.Figure
    mantra: Mantra
    fusion_score: float
    theme: str
    timestamp: str
    def calculate_fusion_score(self) -> float:
        theme_coherence = {
            'protection': 0.9,
            'voyage': 0.8, 
            'rituel': 0.95,
            'silence': 0.85
        }
        base_score = theme_coherence.get(self.theme, 0.7)
        return min(base_score + self.mantra.fitness * 0.3, 1.0)

class GlyphosophiaEngine:
    def __init__(self):
        self.symbol_engine = VonPetzingerSymbols()
        self.mantra_engine = None
        self.theme_colors = {
            'protection': '#ff3366',
            'voyage': '#00ffaa', 
            'rituel': '#ffaa00',
            'silence': '#3366ff'
        }
    def generate_glyph_mantra(self, theme: str = "protection", seed: int = None) -> GlyphosophiaResult:
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        color = self.theme_colors.get(theme, '#00ffaa')
        glyph_fig = self.symbol_engine.create_symbolic_combination(theme, seed=seed, color=color)
        self.mantra_engine = SoufiMantraGA(theme=theme)
        self.mantra_engine.initialize_population()
        self.mantra_engine.evolve()
        best_mantra = self.mantra_engine.get_best_mantra()
        result = GlyphosophiaResult(
            glyph_fig=glyph_fig,
            mantra=best_mantra,
            fusion_score=0.0,
            theme=theme,
            timestamp=datetime.now().isoformat()
        )
        result.fusion_score = result.calculate_fusion_score()
        return result
    def add_mantra_to_glyph(self, result: GlyphosophiaResult) -> plt.Figure:
        fig = result.glyph_fig
        ax = fig.axes[0]
        mantra_text = result.mantra.content
        ax.text(400, 50, mantra_text, 
                fontsize=10, color=self.theme_colors.get(result.theme, '#00ffaa'),
                ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#0b0b12', 
                         edgecolor=self.theme_colors.get(result.theme, '#00ffaa'), alpha=0.8))
        ax.text(400, 20, f"ψ-fusion: {result.fusion_score:.3f}", 
                fontsize=8, color='#888888', ha='center', va='bottom')
        return fig

# ========================================
# INTERFACE GRAPHIQUE UNIFIÉE
# ========================================
class GlyphosophiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 Glyphosophia 2075 — Générateur d'Artefacts Cyber-Préhistoriques")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.engine = GlyphosophiaEngine()
        self.current_result = None
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        main_canvas = tk.Canvas(self.root, bg='#1a1a2e')
        v_scroll = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        h_scroll = ttk.Scrollbar(self.root, orient="horizontal", command=main_canvas.xview)
        main_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        content_frame = ttk.Frame(main_canvas)
        main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))

        content_frame.bind("<Configure>", on_frame_configure)
        main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(
            main_canvas.find_withtag("all")[0], width=e.width))

        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        main_frame = ttk.Frame(content_frame, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header, text="🌌 GLYPHOSOPHIA 2075", 
                 font=("Helvetica", 20, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, text="Fusion Glyphes Paléo + Mantras Cyber-Soufis",
                 font=("Helvetica", 10)).pack(side=tk.LEFT, padx=10)

        control_frame = ttk.LabelFrame(main_frame, text=" Invocation des Artefacts ", padding=15)
        control_frame.pack(fill=tk.X, pady=10)

        ttk.Label(control_frame, text="Thème Symbolique:").grid(row=0, column=0, sticky=tk.W)
        self.theme_var = tk.StringVar(value="protection")
        theme_combo = ttk.Combobox(control_frame, textvariable=self.theme_var,
                                  values=['protection', 'voyage', 'rituel', 'silence'],
                                  state="readonly", width=15)
        theme_combo.grid(row=0, column=1, padx=5, sticky=tk.W)

        ttk.Label(control_frame, text="Graine:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.seed_var = tk.StringVar(value="42")
        ttk.Entry(control_frame, textvariable=self.seed_var, width=10).grid(row=0, column=3, padx=5)

        ttk.Button(control_frame, text="🎲 Générer Artefact", 
                  command=self.generate_artifact).grid(row=0, column=4, padx=20)
        ttk.Button(control_frame, text="💾 Exporter", 
                  command=self.export_artifact).grid(row=0, column=5, padx=5)

        ttk.Label(control_frame, text="Rêve Collectif (1-9):").grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.collective_count = tk.IntVar(value=3)
        ttk.Spinbox(control_frame, from_=1, to=9, textvariable=self.collective_count, width=5).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(control_frame, text="🌀 Générer Rêve Collectif", 
                  command=self.generate_collective_dream).grid(row=1, column=4, padx=20)
        ttk.Button(control_frame, text="📥 Exporter Rêve Collectif", 
                  command=self.export_collective_dream).grid(row=1, column=5, padx=5)

        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        glyph_frame = ttk.LabelFrame(viz_frame, text=" Glyphe Symbolique ", width=600)
        glyph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.glyph_label = ttk.Label(glyph_frame, text="Cliquez pour générer un artefact")
        self.glyph_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.glyph_label.bind("<Button-1>", lambda e: self.generate_artifact())

        mantra_frame = ttk.LabelFrame(viz_frame, text=" Mantra Cyber-Soufi ", width=400)
        mantra_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.mantra_text = scrolledtext.ScrolledText(mantra_frame, height=15, 
                                                   font=("Consolas", 11),
                                                   bg='#0b0b12', fg='#00ffaa',
                                                   insertbackground='#00ffaa')
        self.mantra_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        analysis_frame = ttk.LabelFrame(mantra_frame, text=" Analyse de Fusion ")
        analysis_frame.pack(fill=tk.X, pady=(10, 0))
        self.analysis_text = tk.Text(analysis_frame, height=4, font=("Consolas", 9),
                                   bg='#121220', fg='#888888')
        self.analysis_text.pack(fill=tk.X, padx=10, pady=10)

        self.status_var = tk.StringVar(value="Prêt pour l'invocation symbolique...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def display_artifact(self, result: GlyphosophiaResult):
        try:
            final_fig = self.engine.add_mantra_to_glyph(result)
            buf = io.BytesIO()
            final_fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                             facecolor=final_fig.get_facecolor())
            buf.seek(0)
            img = Image.open(buf)
            photo = ImageTk.PhotoImage(img)
            self.glyph_label.configure(image=photo, text="")
            self.glyph_label.image = photo

            self.mantra_text.delete(1.0, tk.END)
            mantra = result.mantra
            self.mantra_text.insert(tk.END, f"{mantra.content}\n")
            self.mantra_text.insert(tk.END, f"Thème: {mantra.theme}\n")
            self.mantra_text.insert(tk.END, f"Score mantra (ψ): {mantra.fitness:.3f}\n")
            if mantra.components["oniric_tag"]:
                tag = mantra.components["oniric_tag"]
                self.mantra_text.insert(tk.END, f"Balise: {tag}\n")
                self.mantra_text.insert(tk.END, f"→ {ONIRIC_TAG_MEANINGS.get(tag, 'inconnue')}\n")

            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, f"Score Fusion: {result.fusion_score:.3f}\n")
            self.analysis_text.insert(tk.END, f"Thème: {result.theme}\n")
            self.analysis_text.insert(tk.END, f"Timestamp: {result.timestamp}\n")
            self.analysis_text.insert(tk.END, f"Artefact: Glyphe {result.theme} + Mantra {mantra.fitness:.3f}")

            plt.close('all')
        except Exception as e:
            messagebox.showerror("Erreur d’Affichage", str(e))

    def generate_artifact(self):
        try:
            theme = self.theme_var.get()
            seed = int(self.seed_var.get()) if self.seed_var.get().isdigit() else None
            self.status_var.set("Invocation des forces anciennes et digitales...")
            self.root.update()
            self.current_result = self.engine.generate_glyph_mantra(theme, seed)
            self.display_artifact(self.current_result)
            self.status_var.set(f"Artefact invoqué ! Fusion: {self.current_result.fusion_score:.3f}")
        except Exception as e:
            messagebox.showerror("Erreur d'Invocation", f"Les forces se sont déchaînées:\n{str(e)}")
            self.status_var.set("Erreur lors de l'invocation...")

    def export_artifact(self):
        if not self.current_result:
            messagebox.showinfo("Export", "Générez d'abord un artefact!")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("Tous", "*.*")],
            initialfile=f"glyphosophia_{self.current_result.theme}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if filename:
            try:
                final_fig = self.engine.add_mantra_to_glyph(self.current_result)
                final_fig.savefig(filename, dpi=150, bbox_inches='tight', 
                                facecolor=final_fig.get_facecolor())
                meta_filename = filename.rsplit('.', 1)[0] + '_meta.json'
                meta_data = {
                    'theme': self.current_result.theme,
                    'mantra': self.current_result.mantra.content,
                    'fusion_score': self.current_result.fusion_score,
                    'mantra_score': self.current_result.mantra.fitness,
                    'timestamp': self.current_result.timestamp,
                    'seed': self.seed_var.get()
                }
                with open(meta_filename, 'w', encoding='utf-8') as f:
                    json.dump(meta_data, f, ensure_ascii=False, indent=2)
                self.status_var.set(f"Artefact exporté: {filename}")
                messagebox.showinfo("Export Réussi", 
                                  f"Artefact sauvegardé!\n{filename}\nMétadonnées: {meta_filename}")
                plt.close('all')
            except Exception as e:
                messagebox.showerror("Erreur Export", f"Échec de l'export:\n{str(e)}")

    def generate_collective_dream(self):
        try:
            count = self.collective_count.get()
            theme = self.theme_var.get()
            base_seed = int(self.seed_var.get()) if self.seed_var.get().isdigit() else random.randint(1000, 9999)
            self.collective_base_seed = base_seed  # <-- pour export
            self.status_var.set(f"Invocation d’un rêve collectif à {count} esprits...")
            self.root.update()

            results = []
            for i in range(count):
                result = self.engine.generate_glyph_mantra(theme=theme, seed=base_seed + i)
                results.append(result)

            self.collective_results = results
            self.current_result = results[0]
            self.display_artifact(self.current_result)

            self.status_var.set(f"Rêve collectif à {count} incarnations invoqué.")
        except Exception as e:
            messagebox.showerror("Erreur Rêve Collectif", str(e))

    def export_collective_dream(self):
        if not hasattr(self, 'collective_results') or not self.collective_results:
            messagebox.showinfo("Export", "Générez d'abord un rêve collectif !")
            return
        folder = filedialog.askdirectory(title="Dossier d’export pour le rêve collectif")
        if not folder:
            return
        try:
            for i, result in enumerate(self.collective_results):
                final_fig = self.engine.add_mantra_to_glyph(result)
                path = os.path.join(folder, f"artefact_collectif_{i+1:02d}_{result.theme}.png")
                final_fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=final_fig.get_facecolor())
                meta_path = path.replace('.png', '_meta.json')
                with open(meta_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'index': i+1,
                        'theme': result.theme,
                        'mantra': result.mantra.content,
                        'fusion_score': result.fusion_score,
                        'mantra_score': result.mantra.fitness,
                        'seed': self.collective_base_seed + i
                    }, f, ensure_ascii=False, indent=2)
                plt.close(final_fig)
            messagebox.showinfo("Export Réussi", f"{len(self.collective_results)} artefacts sauvegardés dans :\n{folder}")
            self.status_var.set("Rêve collectif exporté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur Export", str(e))

# ========================================
# LANCEMENT
# ========================================
if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')
    print("🌌 Démarrage de Glyphosophia 2075...")
    print("Avec scrollbars et Rêve Collectif synchronisé")
    root = tk.Tk()
    app = GlyphosophiaGUI(root)
    root.mainloop()
