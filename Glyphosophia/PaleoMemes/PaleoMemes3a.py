import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import random
#
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

class VonPetzingerSymbols:
    """
    Générateur d'images basées sur les 26 symboles géométriques
    identifiés par Genevieve von Petzinger dans l'art rupestre paléolithique
    """
    
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
    
    def create_canvas(self, bg_color='#F5E6D3'):
        """Crée un canvas avec fond style paroi de grotte"""
        fig, ax = plt.subplots(figsize=(10, 7.5))
        ax.set_xlim(0, self.img_size[0])
        ax.set_ylim(0, self.img_size[1])
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        return fig, ax
    
    # Symboles de base
    def draw_line(self, ax, x, y, scale=1.0, angle=0):
        """Ligne simple"""
        length = 50 * scale
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        ax.plot([x, x_end], [y, y_end], 'k-', linewidth=3)
    
    def draw_circle(self, ax, x, y, scale=1.0, angle=0):
        """Cercle"""
        circle = patches.Circle((x, y), 20*scale, fill=False, edgecolor='black', linewidth=2.5)
        ax.add_patch(circle)
    
    def draw_dot(self, ax, x, y, scale=1.0, angle=0):
        """Point"""
        circle = patches.Circle((x, y), 5*scale, fill=True, color='black')
        ax.add_patch(circle)
    
    def draw_open_angle(self, ax, x, y, scale=1.0, angle=0):
        """Angle ouvert (V ou chevron)"""
        size = 30 * scale
        points = np.array([[x-size, y-size], [x, y+size], [x+size, y-size]])
        angle_rad = np.radians(angle)
        rot_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                               [np.sin(angle_rad), np.cos(angle_rad)]])
        rotated = (points - [x, y]) @ rot_matrix.T + [x, y]
        ax.plot(rotated[:, 0], rotated[:, 1], 'k-', linewidth=2.5)
    
    def draw_triangle(self, ax, x, y, scale=1.0, angle=0):
        """Triangle"""
        size = 25 * scale
        triangle = patches.RegularPolygon((x, y), 3, radius=size, 
                                         orientation=np.radians(angle),
                                         fill=False, edgecolor='black', linewidth=2.5)
        ax.add_patch(triangle)
    
    def draw_quadrangle(self, ax, x, y, scale=1.0, angle=0):
        """Quadrilatère"""
        size = 25 * scale
        square = patches.Rectangle((x-size, y-size), size*2, size*2, 
                                   angle=angle, fill=False, 
                                   edgecolor='black', linewidth=2.5)
        ax.add_patch(square)
    
    def draw_spiral(self, ax, x, y, scale=1.0, angle=0):
        """Spirale"""
        theta = np.linspace(0, 4*np.pi, 100)
        r = theta * 3 * scale
        x_spiral = x + r * np.cos(theta)
        y_spiral = y + r * np.sin(theta)
        ax.plot(x_spiral, y_spiral, 'k-', linewidth=2)
    
    def draw_zigzag(self, ax, x, y, scale=1.0, angle=0):
        """Zigzag"""
        size = 15 * scale
        points_x = [x-40*scale, x-20*scale, x, x+20*scale, x+40*scale]
        points_y = [y, y+size, y, y+size, y]
        ax.plot(points_x, points_y, 'k-', linewidth=2.5)
    
    def draw_cross(self, ax, x, y, scale=1.0, angle=0):
        """Croix"""
        size = 25 * scale
        ax.plot([x-size, x+size], [y, y], 'k-', linewidth=2.5)
        ax.plot([x, x], [y-size, y+size], 'k-', linewidth=2.5)
    
    def draw_crosshatch(self, ax, x, y, scale=1.0, angle=0):
        """Grille croisée"""
        size = 30 * scale
        for i in range(4):
            offset = -size + i * size/1.5
            ax.plot([x-size, x+size], [y+offset, y+offset], 'k-', linewidth=1.5)
            ax.plot([x+offset, x+offset], [y-size, y+size], 'k-', linewidth=1.5)
    
    def draw_hand(self, ax, x, y, scale=1.0, angle=0):
        """Main stylisée"""
        size = 30 * scale
        # Paume
        circle = patches.Circle((x, y), size*0.7, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        # Doigts
        for i in range(5):
            angle_finger = -60 + i * 30
            x_end = x + size * 1.3 * np.cos(np.radians(angle_finger))
            y_end = y + size * 1.3 * np.sin(np.radians(angle_finger))
            ax.plot([x, x_end], [y, y_end], 'k-', linewidth=2)
    
    def draw_tectiform(self, ax, x, y, scale=1.0, angle=0):
        """Tectiforme (forme de toit)"""
        size = 25 * scale
        points_x = [x-size, x, x+size, x+size, x-size, x-size]
        points_y = [y-size, y+size, y-size, y-size*1.5, y-size*1.5, y-size]
        ax.plot(points_x, points_y, 'k-', linewidth=2.5)
    
    def draw_penniform(self, ax, x, y, scale=1.0, angle=0):
        """Penniforme (forme de plume)"""
        size = 30 * scale
        # Tige centrale
        ax.plot([x, x], [y-size, y+size], 'k-', linewidth=2.5)
        # Barbes
        for i in range(5):
            y_pos = y - size + i * size/2
            ax.plot([x-size*0.4, x], [y_pos, y_pos], 'k-', linewidth=1.5)
            ax.plot([x, x+size*0.4], [y_pos, y_pos], 'k-', linewidth=1.5)
    
    def draw_claviform(self, ax, x, y, scale=1.0, angle=0):
        """Claviforme (forme de massue)"""
        size = 30 * scale
        # Manche
        ax.plot([x, x], [y-size, y], 'k-', linewidth=2.5)
        # Tête
        circle = patches.Circle((x, y+size*0.3), size*0.4, fill=False, edgecolor='black', linewidth=2.5)
        ax.add_patch(circle)
    
    def draw_aviform(self, ax, x, y, scale=1.0, angle=0):
        """Aviforme (forme d'oiseau stylisé)"""
        size = 25 * scale
        # Corps
        ellipse = patches.Ellipse((x, y), size*1.5, size*0.8, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(ellipse)
        # Bec
        ax.plot([x+size*0.75, x+size*1.2], [y, y+size*0.3], 'k-', linewidth=2)
    
    def draw_scalariform(self, ax, x, y, scale=1.0, angle=0):
        """Scalariforme (forme d'échelle)"""
        size = 30 * scale
        # Montants
        ax.plot([x-size*0.5, x-size*0.5], [y-size, y+size], 'k-', linewidth=2.5)
        ax.plot([x+size*0.5, x+size*0.5], [y-size, y+size], 'k-', linewidth=2.5)
        # Barreaux
        for i in range(5):
            y_pos = y - size + i * size/2
            ax.plot([x-size*0.5, x+size*0.5], [y_pos, y_pos], 'k-', linewidth=2.5)
    
    def draw_finger_fluting(self, ax, x, y, scale=1.0, angle=0):
        """Tracé digital (lignes ondulées parallèles)"""
        size = 30 * scale
        for i in range(3):
            t = np.linspace(0, 2*np.pi, 50)
            x_wave = x + t * size/6 - size
            y_wave = y + np.sin(t*3) * size*0.15 + i*size*0.3 - size*0.3
            ax.plot(x_wave, y_wave, 'k-', linewidth=2)
    
    def draw_cupule(self, ax, x, y, scale=1.0, angle=0):
        """Cupule (dépression circulaire)"""
        circle = patches.Circle((x, y), 8*scale, fill=True, color='black', alpha=0.7)
        ax.add_patch(circle)
    
    def draw_wavy_line(self, ax, x, y, scale=1.0, angle=0):
        """Ligne ondulée"""
        t = np.linspace(0, 4*np.pi, 100)
        x_wave = x + t * 10 * scale - 60*scale
        y_wave = y + np.sin(t) * 15 * scale
        ax.plot(x_wave, y_wave, 'k-', linewidth=2.5)
    
    def draw_oval(self, ax, x, y, scale=1.0, angle=0):
        """Ovale"""
        ellipse = patches.Ellipse((x, y), 40*scale, 25*scale, angle=angle,
                                 fill=False, edgecolor='black', linewidth=2.5)
        ax.add_patch(ellipse)
    
    def draw_semi_circle(self, ax, x, y, scale=1.0, angle=0):
        """Demi-cercle"""
        theta = np.linspace(0, np.pi, 50)
        radius = 25 * scale
        x_arc = x + radius * np.cos(theta)
        y_arc = y + radius * np.sin(theta)
        ax.plot(x_arc, y_arc, 'k-', linewidth=2.5)
        ax.plot([x-radius, x+radius], [y, y], 'k-', linewidth=2.5)
    
    def draw_rectangle(self, ax, x, y, scale=1.0, angle=0):
        """Rectangle"""
        rect = patches.Rectangle((x-30*scale, y-20*scale), 60*scale, 40*scale,
                                angle=angle, fill=False, edgecolor='black', linewidth=2.5)
        ax.add_patch(rect)
    
    def draw_asterisk(self, ax, x, y, scale=1.0, angle=0):
        """Astérisque"""
        size = 20 * scale
        for angle_line in [0, 45, 90, 135]:
            x_end = x + size * np.cos(np.radians(angle_line))
            y_end = y + size * np.sin(np.radians(angle_line))
            ax.plot([x-size*np.cos(np.radians(angle_line)), x_end], 
                   [y-size*np.sin(np.radians(angle_line)), y_end], 'k-', linewidth=2.5)
    
    def draw_serpentiform(self, ax, x, y, scale=1.0, angle=0):
        """Serpentiforme"""
        t = np.linspace(0, 6*np.pi, 100)
        x_serp = x + t * 8 * scale - 80*scale
        y_serp = y + np.sin(t) * 20 * scale
        ax.plot(x_serp, y_serp, 'k-', linewidth=3)
    
    def draw_pectiform(self, ax, x, y, scale=1.0, angle=0):
        """Pectiforme (forme de peigne)"""
        size = 25 * scale
        # Base
        ax.plot([x-size, x+size], [y, y], 'k-', linewidth=2.5)
        # Dents
        for i in range(7):
            x_pos = x - size + i * size/3
            ax.plot([x_pos, x_pos], [y, y+size], 'k-', linewidth=2)
    
    def draw_dots_series(self, ax, x, y, scale=1.0, angle=0):
        """Série de points"""
        for i in range(5):
            x_dot = x - 40*scale + i * 20*scale
            circle = patches.Circle((x_dot, y), 4*scale, fill=True, color='black')
            ax.add_patch(circle)
    
    def generate_image(self, symbols_list=None, num_symbols=10, seed=None):
        """
        Génère une image avec des symboles aléatoires ou spécifiés
        
        Args:
            symbols_list: Liste de noms de symboles à dessiner (None = aléatoire)
            num_symbols: Nombre de symboles si aléatoire
            seed: Graine pour la reproductibilité
        """
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        fig, ax = self.create_canvas()
        
        if symbols_list is None:
            symbols_list = random.choices(list(self.symbols.keys()), k=num_symbols)
        
        for symbol_name in symbols_list:
            x = random.uniform(100, self.img_size[0]-100)
            y = random.uniform(100, self.img_size[1]-100)
            scale = random.uniform(0.7, 1.3)
            angle = random.uniform(0, 360)
            
            self.symbols[symbol_name](ax, x, y, scale, angle)
        
        plt.tight_layout()
        return fig
    
    def list_symbols(self):
        """Liste tous les symboles disponibles"""
        return list(self.symbols.keys())
    
    def create_narrative_composition(self, narrative_type='hunting', seed=None):
        """
        Crée une composition narrative basée sur des thèmes paléolithiques
        
        Args:
            narrative_type: Type de narration
                - 'hunting': Scène de chasse
                - 'journey': Voyage/migration
                - 'ritual': Rituel/cérémonie
                - 'territory': Marquage territorial
                - 'astronomy': Observation céleste
                - 'water': Source d'eau
                - 'shelter': Abri/habitation
                - 'danger': Avertissement de danger
        """
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        fig, ax = self.create_canvas()
        
        narratives = {
            'hunting': self._compose_hunting,
            'journey': self._compose_journey,
            'ritual': self._compose_ritual,
            'territory': self._compose_territory,
            'astronomy': self._compose_astronomy,
            'water': self._compose_water,
            'shelter': self._compose_shelter,
            'danger': self._compose_danger
        }
        
        if narrative_type in narratives:
            narratives[narrative_type](ax)
        else:
            print(f"Type narratif inconnu: {narrative_type}")
            return None
        
        plt.tight_layout()
        return fig
    
    def _compose_hunting(self, ax):
        """Composition: Scène de chasse"""
        # Groupe de chasseurs (mains)
        for i in range(3):
            self.draw_hand(ax, 150 + i*80, 200, scale=0.9)
        
        # Animaux/cibles (aviformes et lignes)
        for i in range(2):
            self.draw_aviform(ax, 500 + i*100, 300 + random.randint(-30, 30), scale=1.2)
        
        # Trajectoires (lignes et flèches)
        for i in range(4):
            self.draw_line(ax, 250 + i*50, 220, angle=random.randint(10, 30))
        
        # Traces/chemin (série de points)
        self.draw_dots_series(ax, 400, 150, scale=1.1)
        
        # Armes (claviformes)
        self.draw_claviform(ax, 200, 350, angle=-45)
        self.draw_claviform(ax, 280, 330, angle=-30)
    
    def _compose_journey(self, ax):
        """Composition: Voyage/migration"""
        # Chemin principal (ligne ondulée)
        self.draw_serpentiform(ax, 400, 300, scale=1.0)
        
        # Points de départ et arrivée (cercles)
        self.draw_circle(ax, 150, 300, scale=1.5)
        self.draw_circle(ax, 650, 300, scale=1.5)
        
        # Étapes du voyage (série de points)
        for i in range(5):
            self.draw_dot(ax, 200 + i*100, 280 + random.randint(-20, 20), scale=1.5)
        
        # Repères géographiques (triangles = montagnes)
        self.draw_triangle(ax, 250, 450, scale=1.3)
        self.draw_triangle(ax, 320, 470, scale=1.0)
        self.draw_triangle(ax, 550, 440, scale=1.2)
        
        # Groupe en déplacement (mains)
        for i in range(4):
            self.draw_hand(ax, 350 + i*40, 200 - i*10, scale=0.7)
        
        # Direction (flèches/angles)
        self.draw_open_angle(ax, 600, 350, scale=1.2, angle=90)
    
    def _compose_ritual(self, ax):
        """Composition: Rituel/cérémonie"""
        # Centre rituel (spirale centrale)
        self.draw_spiral(ax, 400, 300, scale=1.5)
        
        # Cercle de participants (mains en cercle)
        radius = 150
        for i in range(8):
            angle = i * 45
            x = 400 + radius * np.cos(np.radians(angle))
            y = 300 + radius * np.sin(np.radians(angle))
            self.draw_hand(ax, x, y, scale=0.8)
        
        # Symboles sacrés (croix et astérisques)
        self.draw_cross(ax, 400, 300, scale=1.2)
        self.draw_asterisk(ax, 300, 450, scale=1.0)
        self.draw_asterisk(ax, 500, 450, scale=1.0)
        
        # Offrandes/objets (ovales)
        for i in range(4):
            self.draw_oval(ax, 350 + i*30, 150, scale=0.7)
        
        # Délimitation sacrée (cercle)
        circle = patches.Circle((400, 300), 200, fill=False, 
                               edgecolor='black', linewidth=3, linestyle='--')
        ax.add_patch(circle)
    
    def _compose_territory(self, ax):
        """Composition: Marquage territorial"""
        # Limite de territoire (ligne en zigzag)
        self.draw_zigzag(ax, 400, 300, scale=2.0)
        
        # Marques de propriété (mains aux coins)
        self.draw_hand(ax, 150, 150, scale=1.0)
        self.draw_hand(ax, 650, 150, scale=1.0)
        self.draw_hand(ax, 150, 450, scale=1.0)
        self.draw_hand(ax, 650, 450, scale=1.0)
        
        # Ressources du territoire (symboles variés)
        self.draw_aviform(ax, 250, 250, scale=1.0)  # Gibier
        self.draw_wavy_line(ax, 500, 200, scale=0.8)  # Eau
        self.draw_tectiform(ax, 350, 400, scale=1.2)  # Abri
        
        # Frontières (séries de cupules)
        for i in range(10):
            self.draw_cupule(ax, 150 + i*55, 500, scale=1.0)
        
        # Symbole tribal (composition unique)
        self.draw_penniform(ax, 400, 400, scale=1.3)
        self.draw_circle(ax, 400, 400, scale=1.5)
    
    def _compose_astronomy(self, ax):
        """Composition: Observation céleste"""
        # Voûte céleste (demi-cercle)
        self.draw_semi_circle(ax, 400, 200, scale=3.0)
        
        # Constellations (groupes de points)
        # Grande Ourse
        constellation_points = [(250, 400), (280, 420), (310, 410), (340, 430)]
        for x, y in constellation_points:
            self.draw_dot(ax, x, y, scale=1.5)
            
        # Pléiades
        for i in range(7):
            x = 500 + random.randint(-20, 20)
            y = 450 + random.randint(-20, 20)
            self.draw_dot(ax, x, y, scale=1.2)
        
        # Soleil et lune
        self.draw_circle(ax, 300, 500, scale=1.3)  # Soleil
        self.draw_spiral(ax, 500, 500, scale=0.8)  # Lune
        
        # Phases lunaires (série de cercles/ovales)
        for i in range(5):
            self.draw_oval(ax, 200 + i*50, 250, scale=0.5 + i*0.1)
        
        # Observateurs (mains pointant vers le ciel)
        for i in range(3):
            self.draw_hand(ax, 300 + i*100, 150, scale=0.8)
        
        # Trajectoires célestes (lignes courbes)
        self.draw_wavy_line(ax, 400, 350, scale=1.0)
    
    def _compose_water(self, ax):
        """Composition: Source d'eau"""
        # Source centrale (spirale)
        self.draw_spiral(ax, 400, 300, scale=1.5)
        
        # Cours d'eau (lignes ondulées multiples)
        for i in range(3):
            self.draw_wavy_line(ax, 400, 280 + i*40, scale=1.0)
        
        # Animaux venant boire (aviformes)
        for i in range(4):
            angle = i * 90
            x = 400 + 120 * np.cos(np.radians(angle))
            y = 300 + 120 * np.sin(np.radians(angle))
            self.draw_aviform(ax, x, y, scale=0.9)
        
        # Végétation (penniformes)
        self.draw_penniform(ax, 250, 400, scale=1.0)
        self.draw_penniform(ax, 550, 380, scale=1.1)
        
        # Traces de pas (séries de points)
        self.draw_dots_series(ax, 300, 200, scale=1.0)
        self.draw_dots_series(ax, 500, 220, scale=1.0)
        
        # Cercle d'eau (ovales concentriques)
        for i in range(3):
            circle = patches.Circle((400, 300), 50 + i*30, fill=False,
                                   edgecolor='black', linewidth=1.5, linestyle=':')
            ax.add_patch(circle)
    
    def _compose_shelter(self, ax):
        """Composition: Abri/habitation"""
        # Structure principale (tectiforme large)
        self.draw_tectiform(ax, 400, 300, scale=2.0)
        
        # Supports/poteaux (lignes verticales)
        for i in range(5):
            self.draw_line(ax, 250 + i*75, 200, angle=90, scale=1.5)
        
        # Toit (ligne)
        self.draw_line(ax, 400, 380, angle=0, scale=3.0)
        
        # Occupants (mains)
        for i in range(3):
            self.draw_hand(ax, 320 + i*60, 250, scale=0.7)
        
        # Foyer central (cercle avec croix)
        self.draw_circle(ax, 400, 200, scale=0.8)
        self.draw_cross(ax, 400, 200, scale=0.6)
        
        # Provisions stockées (quadrangles)
        for i in range(3):
            self.draw_quadrangle(ax, 280 + i*40, 150, scale=0.6)
        
        # Entrée (angle ouvert)
        self.draw_open_angle(ax, 400, 180, angle=180, scale=1.5)
        
        # Protection (grille croisée)
        self.draw_crosshatch(ax, 600, 300, scale=1.0)
    
    def _compose_danger(self, ax):
        """Composition: Avertissement de danger"""
        # Zone dangereuse (croix multiples)
        for i in range(3):
            for j in range(3):
                self.draw_cross(ax, 300 + i*100, 250 + j*80, scale=1.2)
        
        # Menace (serpentiforme)
        self.draw_serpentiform(ax, 400, 400, scale=1.2)
        
        # Limite à ne pas franchir (zigzag épais)
        self.draw_zigzag(ax, 400, 200, scale=2.0)
        for i in range(3):
            self.draw_zigzag(ax, 400, 180 + i*10, scale=2.0)
        
        # Avertissement urgent (triangles pointant vers le danger)
        for i in range(4):
            self.draw_triangle(ax, 250 + i*100, 450, angle=180, scale=1.0)
        
        # Témoins/observateurs (mains levées)
        self.draw_hand(ax, 150, 300, scale=1.0)
        self.draw_hand(ax, 650, 300, scale=1.0)
        
        # Marquage de danger (cupules)
        for i in range(8):
            self.draw_cupule(ax, 350 + i*15, 150, scale=1.2)
    
    def create_symbolic_combination(self, combination_type='protection', seed=None):
        """
        Crée des combinaisons symboliques spécifiques
        
        Args:
            combination_type: Type de combinaison
                - 'protection': Symboles de protection
                - 'fertility': Symboles de fertilité
                - 'abundance': Symboles d'abondance
                - 'journey_safe': Voyage sécurisé
                - 'sacred_space': Espace sacré
                - 'clan_identity': Identité du clan
        """
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        fig, ax = self.create_canvas()
        
        combinations = {
            'protection': [
                ('circle', 400, 300, 2.0, 0),
                ('cross', 400, 300, 1.5, 0),
                ('hand', 300, 300, 1.0, 0),
                ('hand', 500, 300, 1.0, 0),
                ('hand', 400, 200, 1.0, 0),
                ('hand', 400, 400, 1.0, 0),
                ('crosshatch', 400, 300, 0.8, 0)
            ],
            'fertility': [
                ('spiral', 400, 300, 1.5, 0),
                ('oval', 400, 300, 1.3, 0),
                ('wavy_line', 400, 400, 1.0, 0),
                ('dots_series', 400, 250, 1.2, 0),
                ('penniform', 300, 350, 1.0, 0),
                ('penniform', 500, 350, 1.0, 0),
                ('semi_circle', 400, 450, 1.5, 0)
            ],
            'abundance': [
                ('aviform', 300, 400, 1.0, 0),
                ('aviform', 350, 380, 0.9, 30),
                ('aviform', 450, 390, 1.1, -20),
                ('aviform', 500, 410, 0.95, 15),
                ('circle', 400, 300, 1.8, 0),
                ('dots_series', 350, 250, 1.0, 0),
                ('dots_series', 450, 260, 1.0, 0),
                ('penniform', 400, 500, 1.3, 0)
            ],
            'journey_safe': [
                ('serpentiform', 400, 300, 1.0, 0),
                ('hand', 200, 300, 0.9, 0),
                ('circle', 650, 300, 1.2, 0),
                ('triangle', 400, 450, 1.0, 0),
                ('open_angle', 600, 300, 1.0, 90),
                ('dots_series', 300, 250, 1.0, 0),
                ('dots_series', 450, 270, 1.0, 0),
                ('cross', 400, 200, 0.8, 0)
            ],
            'sacred_space': [
                ('circle', 400, 300, 2.5, 0),
                ('spiral', 400, 300, 1.2, 0),
                ('cross', 400, 300, 1.5, 0),
                ('asterisk', 400, 300, 1.0, 0),
                ('hand', 250, 300, 0.8, 0),
                ('hand', 550, 300, 0.8, 0),
                ('hand', 400, 150, 0.8, 0),
                ('hand', 400, 450, 0.8, 0),
                ('triangle', 300, 200, 0.7, 0),
                ('triangle', 500, 200, 0.7, 0),
                ('triangle', 300, 400, 0.7, 0),
                ('triangle', 500, 400, 0.7, 0)
            ],
            'clan_identity': [
                ('tectiform', 400, 300, 1.8, 0),
                ('claviform', 350, 400, 1.2, -30),
                ('claviform', 450, 400, 1.2, 30),
                ('hand', 400, 500, 1.0, 0),
                ('penniform', 300, 300, 1.0, 0),
                ('penniform', 500, 300, 1.0, 0),
                ('circle', 400, 200, 1.0, 0),
                ('dots_series', 400, 250, 1.0, 0)
            ]
        }
        
        if combination_type in combinations:
            for symbol_name, x, y, scale, angle in combinations[combination_type]:
                self.symbols[symbol_name](ax, x, y, scale, angle)
        else:
            print(f"Type de combinaison inconnu: {combination_type}")
            return None
        
        plt.tight_layout()
        return fig


# Exemple d'utilisation
if __name__ == "__mainzero__":
    generator = VonPetzingerSymbols()
    
    print("Symboles disponibles:")
    for i, symbol in enumerate(generator.list_symbols(), 1):
        print(f"{i}. {symbol}")
    
    # Générer une image aléatoire
    print("\nGénération d'une image avec symboles aléatoires...")
    fig = generator.generate_image(num_symbols=15, seed=42)
    plt.savefig('von_petzinger_random.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Générer une image avec symboles spécifiques
    print("\nGénération d'une image avec symboles spécifiques...")
    specific_symbols = ['spiral', 'hand', 'circle', 'triangle', 'serpentiform', 
                       'tectiform', 'cross', 'dots_series']
    fig = generator.generate_image(symbols_list=specific_symbols)
    plt.savefig('von_petzinger_specific.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Générer des compositions narratives
    print("\n=== COMPOSITIONS NARRATIVES ===")
    narrative_types = ['hunting', 'journey', 'ritual', 'territory', 
                      'astronomy', 'water', 'shelter', 'danger']
    
    for narrative in narrative_types:
        print(f"\nCréation de la narration: {narrative}")
        fig = generator.create_narrative_composition(narrative, seed=42)
        plt.savefig(f'narrative_{narrative}.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    # Afficher un exemple de narration
    fig = generator.create_narrative_composition('ritual', seed=42)
    plt.show()
    
    # Générer des combinaisons symboliques
    print("\n=== COMBINAISONS SYMBOLIQUES ===")
    combination_types = ['protection', 'fertility', 'abundance', 
                        'journey_safe', 'sacred_space', 'clan_identity']
    
    for combo in combination_types:
        print(f"\nCréation de la combinaison: {combo}")
        fig = generator.create_symbolic_combination(combo, seed=42)
        plt.savefig(f'combination_{combo}.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    # Afficher un exemple de combinaison
    fig = generator.create_symbolic_combination('sacred_space', seed=42)
    plt.show()
    
    print("\n✅ Toutes les images ont été générées avec succès!")
    
# Definition de la GUi
# --- Ajout : Interface graphique avancée ---


class PaleoMemeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Paleo Mémes — Générateur Rituel (La Hague, 2075)")
        self.root.geometry("900x700")
        self.generator = VonPetzingerSymbols()

        # Variables Tkinter
        self.narrative_type = tk.StringVar(value="ritual")
        self.combination_type = tk.StringVar(value="sacred_space")
        self.layer_type = tk.StringVar(value="megalithic")
        self.corruption_level = tk.IntVar(value=0)
        self.seed = tk.StringVar(value="42")
        self.num_symbols = tk.IntVar(value=10)

        self.selected_symbols = []
        self.setup_ui()

    def setup_ui(self):
        # === Cadre gauche : contrôles ===
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Types narratifs
        ttk.Label(left_frame, text="Composition narrative :").pack(anchor="w")
        narrative_combo = ttk.Combobox(
            left_frame,
            textvariable=self.narrative_type,
            values=list(self.generator._compose_hunting.__func__.__qualname__.split('.')[0].replace('_', '') for _ in []),
            state="readonly"
        )
        # Mais mieux : lister les clés de la méthode
        narrative_combo['values'] = [
            'hunting', 'journey', 'ritual', 'territory',
            'astronomy', 'water', 'shelter', 'danger'
        ]
        narrative_combo.pack(fill="x", pady=2)

        # Combinaisons symboliques
        ttk.Label(left_frame, text="Combinaison symbolique :").pack(anchor="w")
        combo_combo = ttk.Combobox(
            left_frame,
            textvariable=self.combination_type,
            values=[
                'protection', 'fertility', 'abundance',
                'journey_safe', 'sacred_space', 'clan_identity'
            ],
            state="readonly"
        )
        combo_combo.pack(fill="x", pady=2)

        # Couche temporelle
        ttk.Label(left_frame, text="Couche temporelle :").pack(anchor="w")
        layer_combo = ttk.Combobox(
            left_frame,
            textvariable=self.layer_type,
            values=['megalithic', 'nuclear', 'fractal'],
            state="readonly"
        )
        layer_combo.pack(fill="x", pady=2)

        # Corruption
        ttk.Label(left_frame, text="Corruption par la Trame (%) :").pack(anchor="w")
        corruption_slider = ttk.Scale(
            left_frame,
            from_=0, to=100,
            variable=self.corruption_level,
            orient="horizontal"
        )
        corruption_slider.pack(fill="x", pady=2)

        # Graine & Nombre
        ttk.Label(left_frame, text="Graine aléatoire :").pack(anchor="w")
        ttk.Entry(left_frame, textvariable=self.seed).pack(fill="x", pady=2)
        ttk.Label(left_frame, text="Nb symboles (si aléatoire) :").pack(anchor="w")
        ttk.Scale(
            left_frame,
            from_=1, to=20,
            variable=self.num_symbols,
            orient="horizontal"
        ).pack(fill="x", pady=2)

        # Sélection manuelle de symboles
        ttk.Label(left_frame, text="Symboles manuels :").pack(anchor="w")
        self.symbol_listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, height=8)
        for sym in self.generator.list_symbols():
            self.symbol_listbox.insert(tk.END, sym)
        self.symbol_listbox.pack(fill="x", pady=2)

        # Boutons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Générer Composition Narrative", command=self.generate_narrative).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Générer Combinaison", command=self.generate_combination).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Générer Symboles Aléatoires", command=self.generate_random).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Générer Symboles Sélectionnés", command=self.generate_selected).pack(side="left", padx=2)

        # === Cadre droit : aperçu ===
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.preview_label = ttk.Label(right_frame, text="Aperçu du Paleo Mème\n(Clic pour agrandir)")
        self.preview_label.pack()

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _corrupt_symbols(self, symbols):
        """Applique une corruption symbolique selon le niveau de Trame"""
        if self.corruption_level.get() == 0:
            return symbols
        corrupted = symbols.copy()
        corruption_rate = self.corruption_level.get() / 100.0
        parasite_pool = ['dots_series', 'wavy_line', 'crosshatch', 'spiral']
        for i in range(len(corrupted)):
            if random.random() < corruption_rate:
                corrupted[i] = random.choice(parasite_pool)
        return corrupted

    def _render_to_image(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor())
        buf.seek(0)
        img = Image.open(buf)
        return ImageTk.PhotoImage(img)

    def _apply_layer_effects(self, fig, ax):
        """Modifie le style selon la couche temporelle"""
        layer = self.layer_type.get()
        if layer == 'nuclear':
            fig.patch.set_facecolor('#2e3b2f')  # Vert sombre
            for child in ax.get_children():
                if hasattr(child, 'set_color'):
                    child.set_color('#a0ffa0')  # Vert radioactif
        elif layer == 'fractal':
            fig.patch.set_facecolor('#000010')
            # Ajouter un effet de glitch léger (à implémenter via perturbations si besoin)

    def _show_figure(self, fig):
        self._apply_layer_effects(fig, fig.axes[0])
        photo = self._render_to_image(fig)
        self.preview_label.configure(image=photo, text="")
        self.preview_label.image = photo  # référence pour éviter le garbage collect

    def generate_narrative(self):
        try:
            seed = int(self.seed.get()) if self.seed.get().isdigit() else None
            fig = self.generator.create_narrative_composition(self.narrative_type.get(), seed=seed)
            if fig:
                self._show_figure(fig)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def generate_combination(self):
        try:
            seed = int(self.seed.get()) if self.seed.get().isdigit() else None
            fig = self.generator.create_symbolic_combination(self.combination_type.get(), seed=seed)
            if fig:
                self._show_figure(fig)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def generate_random(self):
        try:
            seed = int(self.seed.get()) if self.seed.get().isdigit() else None
            fig = self.generator.generate_image(num_symbols=self.num_symbols.get(), seed=seed)
            if fig:
                self._show_figure(fig)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def generate_selected(self):
        selected = [self.generator.list_symbols()[i] for i in self.symbol_listbox.curselection()]
        if not selected:
            messagebox.showwarning("Attention", "Aucun symbole sélectionné.")
            return
        try:
            seed = int(self.seed.get()) if self.seed.get().isdigit() else None
            corrupted = self._corrupt_symbols(selected)
            fig = self.generator.generate_image(symbols_list=corrupted, seed=seed)
            if fig:
                self._show_figure(fig)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    # Désactiver le mode backend blocant si nécessaire
    import matplotlib
    matplotlib.use('Agg')  # ou TkAgg selon environnement

    root = tk.Tk()
    app = PaleoMemeGUI(root)
    root.mainloop()
