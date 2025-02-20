import tkinter as tk
from random import randrange

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CAR GAME')
        self.config(bg="beige")
        
        # Dimensions du canvas (zone de jeu)
        self.canvas_width = 1300
        self.canvas_height = 750
        self.can = tk.Canvas(self, bg='dimgray', width=self.canvas_width, height=self.canvas_height)
        self.can.place(x=10, y=10)
        
        # Affichage du score
        self.score_var = tk.IntVar(value=0)
        self.score_entry = tk.Entry(self, textvariable=self.score_var, fg="black", bd=5, width=15, font=("Arial", 20))
        self.score_entry.place(x=self.canvas_width + 20, y=10)
        self.score_label = tk.Label(self, text='SCORE', fg="red", font=("Arial", 20), bg="beige")
        self.score_label.place(x=self.canvas_width + 20, y=60)
        
        # Variables d'état du jeu
        self.point = 0
        self.collision = False
        self.progress_game = False  # True si le jeu est en cours
        self.obstacles = []         # Liste des obstacles
        
        # Affichage du titre et des lignes de la route
        self.title_label = tk.Label(self, text="CAR GAME", font=("Arial", 30, "bold"), fg="blue", bg="beige")
        self.title_label.place(x=self.canvas_width//2 - 100, y=0)
        self.draw_road()
        
        # Dessiner la voiture et stocker ses éléments pour la collision
        self.draw_car()
        
        # Génération des obstacles initiaux
        self.generate_obstacles(num=5)
        
        # Bindings claviers pour déplacer la voiture et contrôler le jeu
        self.bind("<Up>", lambda event: self.move_car(0, -10))
        self.bind("<Down>", lambda event: self.move_car(0, 10))
        self.bind("<Left>", lambda event: self.move_car(-10, 0))
        self.bind("<Right>", lambda event: self.move_car(10, 0))
        self.bind("<Return>", lambda event: self.start_game())
        self.bind("<Escape>", lambda event: self.quit())
        
        # Boutons de contrôle
        self.start_button = tk.Button(self, text='START', width=8, height=2, command=self.start_game)
        self.start_button.place(x=self.canvas_width + 20, y=150)
        self.stop_button = tk.Button(self, text='STOP', width=8, height=2, command=self.stop_game)
        self.stop_button.place(x=self.canvas_width + 20, y=210)
        self.pause_button = tk.Button(self, text='PAUSE', width=8, height=2, command=self.toggle_pause)
        self.pause_button.place(x=self.canvas_width + 20, y=270)
        self.restart_button = tk.Button(self, text='RESTART', width=8, height=2, command=self.restart_game, state='disabled')
        self.restart_button.place(x=self.canvas_width + 20, y=330)
        self.quit_button = tk.Button(self, text='LEAVE', width=8, height=2, command=self.quit)
        self.quit_button.place(x=self.canvas_width + 20, y=390)
    
    def draw_road(self):
        """Dessine les lignes de séparation de la route."""
        for i in range(1, 4):
            y = (self.canvas_height * i) // 4
            self.can.create_line(0, y, self.canvas_width, y, fill="white", dash=(10, 10))
    
    def draw_car(self):
        """Dessine la voiture composée d'un corps, d'un toit et de deux roues.
        Les identifiants de tous les éléments sont stockés dans self.car_items pour faciliter la détection de collision."""
        self.car_items = []
        # Corps principal
        self.c1 = self.can.create_rectangle(50, 300, 200, 360, outline='black', fill='blue')
        self.car_items.append(self.c1)
        # Toit (arc)
        self.c2 = self.can.create_arc(150, 260, 250, 360, start=0, extent=180, fill='blue')
        self.car_items.append(self.c2)
        # Avant de la voiture
        self.c3 = self.can.create_rectangle(200, 320, 250, 360, outline='black', fill='blue')
        self.car_items.append(self.c3)
        # Roues
        self.c4 = self.can.create_oval(60, 350, 90, 380, fill='grey', outline='black', width=3)
        self.car_items.append(self.c4)
        self.c5 = self.can.create_oval(210, 350, 240, 380, fill='grey', outline='black', width=3)
        self.car_items.append(self.c5)
    
    '''def generate_obstacles(self, num=6):
        """Génère 'num' obstacles placés aléatoirement sur le bord droit."""
        # Supprime les obstacles existants
        for obs in self.obstacles:
            self.can.delete(obs)
        self.obstacles.clear()
        # Crée de nouveaux obstacles
        for _ in range(num):
            x = randrange(self.canvas_width + 10, self.canvas_width + 200)
            y = randrange(0, self.canvas_height - 35)
            color = "red" if randrange(2) == 0 else "black"
            obs = self.can.create_rectangle(x, y, x + 35, y + 35, fill=color)
            self.obstacles.append(obs)'''
            
    def generate_obstacles(self, num=6):
        
    #Génère num obstacles placés aléatoirement sur le bord droit,
    #avec une répartition verticale uniforme.
    
    # Supprime les obstacles existants
        for obs in self.obstacles:
            self.can.delete(obs)
        self.obstacles.clear()
        
        obstacle_height = 35  # hauteur de l'obstacle (a adapter si besoin)
        interval = self.canvas_height // num  # intervalle vertical pour chaque obstacle
    
        for i in range(num):
            x = randrange(self.canvas_width + 10, self.canvas_width + 200)
            # Définir la plage verticale pour cet obstacle
            min_y = i * interval
            max_y = (i + 1) * interval - obstacle_height
            if max_y < min_y:
                max_y = min_y
            y = randrange(min_y, max_y + 1)
            color = "red" if randrange(2) == 0 else "black"
            obs = self.can.create_rectangle(x, y, x + 35, y + obstacle_height, fill=color)
            self.obstacles.append(obs)

    
    def start_game(self, event=None):
        """Démarre le jeu si ce n'est pas déjà le cas et que la partie n'est pas terminée."""
        if self.collision:
            return  # La partie est terminée, ne rien faire
        if not self.progress_game:
            self.progress_game = True
            self.move_obstacles()
    
    def stop_game(self, event=None):
        """Arrête (met en pause) le déplacement des obstacles."""
        self.progress_game = False
    
    def toggle_pause(self):
        """Permet de mettre en pause ou reprendre le jeu."""
        if self.progress_game:
            self.progress_game = False
            self.pause_button.config(text="RESUME")
        else:
            if not self.collision:  # Ne reprendre que si le jeu n'est pas terminé
                self.progress_game = True
                self.pause_button.config(text="PAUSE")
                self.move_obstacles()
    
    def restart_game(self):
        """Réinitialise l'état du jeu pour recommencer une partie."""
        self.can.delete("all")
        self.obstacles.clear()
        self.point = 0
        self.collision = False
        self.progress_game = False
        self.score_var.set(0)
        self.draw_road()
        self.draw_car()
        self.generate_obstacles(num=5)
        self.restart_button.config(state='disabled')
        self.pause_button.config(text='PAUSE')
    
    def move_car(self, dx, dy):
        """Déplace la voiture tout en s'assurant qu'elle ne sorte pas de la zone de jeu."""
        bbox = self.can.bbox(*self.car_items)
        if bbox:
            new_x1 = bbox[0] + dx
            new_y1 = bbox[1] + dy
            new_x2 = bbox[2] + dx
            new_y2 = bbox[3] + dy
            # Empêche de sortir des limites
            if new_x1 < 0 or new_y1 < 0 or new_x2 > self.canvas_width or new_y2 > self.canvas_height:
                return
        for item in self.car_items:
            self.can.move(item, dx, dy)
    
    def move_obstacles(self):
        """Déplace les obstacles vers la gauche, augmente leur vitesse en fonction du score,
        et repositionne ceux qui sortent de l'écran."""
        if self.progress_game:
            self.check_collision()
            # Vitesse de base augmentée en fonction du score
            speed = 7 + self.point // 10
            for obs in self.obstacles:
                self.can.move(obs, -speed, 0)
                x1, y1, x2, y2 = self.can.coords(obs)
                if x2 < 10:
                    # Repositionne l'obstacle à droite avec une position verticale aléatoire
                    new_x = randrange(self.canvas_width + 10, self.canvas_width + 200)
                    new_y = randrange(0, self.canvas_height - 35)
                    self.can.coords(obs, new_x, new_y, new_x + 35, new_y + 35)
                    self.point += 1
                    self.score_var.set(self.point)
            self.after(30, self.move_obstacles)
    
    def check_collision(self):
        """Vérifie si la voiture (toutes ses parties) entre en collision avec un obstacle."""
        car_bbox = self.can.bbox(*self.car_items)
        for obs in self.obstacles:
            obs_bbox = self.can.bbox(obs)
            if self.bbox_overlap(car_bbox, obs_bbox):
                self.game_over()
                self.collision = True
                break
    
    def bbox_overlap(self, box1, box2):
        """Retourne True si les deux boîtes (x1, y1, x2, y2) se superposent."""
        return not (box1[2] < box2[0] or box1[0] > box2[2] or box1[3] < box2[1] or box1[1] > box2[3])
    
    def game_over(self):
        """Affiche le message 'GAME OVER' et arrête le jeu."""
        self.progress_game = False
        self.can.create_text(self.canvas_width//2, self.canvas_height//2,
                               text="GAME OVER", fill="red", font=("Arial", 50))
        self.restart_button.config(state='normal')

if __name__ == '__main__':
    app = Application()
    app.geometry("1600x800")
    app.mainloop()
