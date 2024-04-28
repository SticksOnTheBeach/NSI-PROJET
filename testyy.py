import tkinter as tk
from tkinter import Scale, Toplevel, Label
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import random
import pygame
import time
import numpy as np
from PIL import ImageFont

# Initialize pygame mixer
pygame.mixer.init()


# Initialize the main window
root = tk.Tk()
root.title("Word Puzzle Game")

#______________________#
#                      #
# Fonction pour le Jeu #
#______________________#

# Liste de mots à inclure dans le tableau
mots = ['Pommes', 'Banane', 'Mangue', 'Framboise', 'Peche', 'Abricot', 'Fraise', 'Raisin']
words = ['Pommes', 'Banane', 'Mangue', 'Framboise', 'Peche', 'Abricot', 'Fraise', 'Raisin']

cell_width = 30
cell_height = 30
text_color = "black"
font = ("Helvetica", 12)
window_width = 500  # Valeur de largeur de la fenêtre
window_height = 620  # Valeur de hauteur de la fenêtre
canvas = tk.Canvas(root, width=window_width, height=window_height)
# Générer un tableau vide de taille 10x10 (par exemple)
taille_tableau = 10
tableau = [[' ' for _ in range(taille_tableau)] for _ in range(taille_tableau)]

# Fonction pour inverser un mot
def reverse_word(word):
    return word[::-1]

# Fonction pour placer un mot dans le tableau
def placer_mot(mot):
    global tableau
    # Choisir une direction et une position de départ aléatoires
    direction = random.choice(['horizontal', 'vertical'])
    if direction == 'horizontal':
        x = random.randint(0, taille_tableau - len(mot))
        y = random.randint(0, taille_tableau - 1)
    else:
        x = random.randint(0, taille_tableau - 1)
        y = random.randint(0, taille_tableau - len(mot))
    # Placer le mot dans le tableau
    for i, lettre in enumerate(mot):
        if direction == 'horizontal':
            tableau[y][x + i] = lettre
        else:
            tableau[y + i][x] = lettre
    # Vérifier si le mot doit être placé à l'envers
    if random.choice([True, False]):
        mot_inverse = reverse_word(mot)
        if direction == 'horizontal':
            x = x + len(mot) - 1  # Décaler x à la fin du mot
        else:
            y = y + len(mot) - 1  # Décaler y à la fin du mot
        # Placer le mot inversé dans le tableau
        for i, lettre in enumerate(mot_inverse):
            if direction == 'horizontal':
                tableau[y][x - i] = lettre
            else:
                tableau[y - i][x] = lettre


taille_cellule = 20



# Placer chaque mot dans le tableau
for mot in mots:
    placer_mot(mot)

# Afficher le tableau
for ligne in tableau:
    print(' '.join(ligne))


        
# Fonction pour insérer une lettre dans une ligne du tableau
def insert_letter_in_row(tableau, row, letter, column):
    tableau[row] = tableau[row][:column] + letter + tableau[row][column:]

# Fonction pour insérer une lettre dans une colonne du tableau
def insert_letter_in_column(tableau, row, letter, column):
    for i in range(len(tableau)):
        tableau[i] = tableau[i][:column] + letter[i] + tableau[i][column:]

# Fonction pour insérer un mot dans une colonne du tableau
def insert_word_in_column(tableau, row, word, column):
    for i in range(len(word)):
        tableau[row+i] = tableau[row+i][:column] + word[i] + tableau[row+i][column+1:]

# Fonction pour vérifier si un mot est présent dans le tableau
def is_word_in_table(tableau, word):
    # Convertir le tableau en une seule chaîne de caractères pour faciliter la recherche
    flat_table = ''.join([''.join(row) for row in tableau])
    return word in flat_table

# Fonction pour supprimer un mot du tableau
def remove_word_from_table(tableau, word):
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j] == word[0]:
                # Vérifier si le mot est présent horizontalement
                if ''.join(tableau[i][j:j+len(word)]) == word:
                    for k in range(len(word)):
                        tableau[i][j+k] = ' '
                # Vérifier si le mot est présent verticalement
                elif ''.join([tableau[i+k][j] for k in range(len(word))]) == word:
                    for k in range(len(word)):
                        tableau[i+k][j] = ' '

# Fonction pour mettre à jour l'affichage du tableau
def update_table_display():
    global frame_photo
    table_image = Image.new("RGBA", (len(tableau[0]) * cell_width, len(tableau) * cell_height), background_color)
    draw = ImageDraw.Draw(table_image)
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            cell_x = j * cell_width
            cell_y = i * cell_height
            draw.rectangle([cell_x, cell_y, cell_x + cell_width, cell_y + cell_height], fill=cell_color)
            draw.text((cell_x + cell_width // 2, cell_y + cell_height // 2), tableau[i][j], fill=text_color, anchor="mm", font=font)
    frame_image.paste(table_image, (int((frame_width - len(tableau[0]) * cell_width) / 2), int((frame_height - len(tableau) * cell_height) / 2)))
    frame_photo = ImageTk.PhotoImage(frame_image)
    canvas.itemconfig("frame", image=frame_photo)


# --------------------------------------------


# Function to create a rounded frame
def create_rounded_frame(width, height, corner_radius, background_color, border_color, border_width):
    frame_image = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(frame_image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), corner_radius, outline=border_color, width=border_width)
    return frame_image

# Function to handle hovering over the settings button
def on_settings_button_hover(event):
    settings_button.config(bg="lightgray")

def on_settings_button_leave(event):
    settings_button.config(bg="SystemButtonFace")

# Function to update the volume icon
def update_volume_icon(volume):
    # Convert the volume from the scale (0-100) to Pygame volume (0.0-1.0)
    pygame_volume = float(volume) / 100.0

    # Select the appropriate volume icon based on the volume level
    if pygame_volume == 0:
        volume_icon_path = 'Assets/Icone/0.png'
    elif pygame_volume <= 0.25:
        volume_icon_path = 'Assets/Icone/25.png'
    elif pygame_volume <= 0.5:
        volume_icon_path = 'Assets/Icone/50.png'
    else:
        volume_icon_path = 'Assets/Icone/100.png'

    # Load the volume icon and update the volume label
    volume_icon = Image.open(volume_icon_path)
    volume_icon = volume_icon.resize((30, 30))  # Adjust size if needed
    volume_icon_photo = ImageTk.PhotoImage(volume_icon)
    volume_label.config(image=volume_icon_photo)
    volume_label.image = volume_icon_photo  # Keep a reference to avoid garbage collection


# Function to update the volume
def update_volume(volume):
    # Update the volume of the music
    pygame_volume = float(volume) / 100.0
    pygame.mixer.music.set_volume(pygame_volume)
    
    # Update the volume icon
    update_volume_icon(volume)


# Function to open the settings window
def open_settings_window():
    
    # Ouvrir la fenêtre de paramètres
    settings_window = Toplevel(root)
    settings_window.title("Paramètres")
    settings_window.geometry("200x200")
    settings_window.resizable(False, False)

    label = Label(settings_window, text="Ceci est la fenêtre de paramètres.")
    label.pack()

    # Adding the volume slider
    volume_scale = Scale(settings_window, from_=0, to=100, orient=tk.HORIZONTAL, label="",
                         command=update_volume)
    volume_scale.set(50)
    volume_scale.pack()

    # Creating the volume label
    global volume_label
    volume_label = tk.Label(settings_window, image=None)
    volume_label.pack()


# Function to play background music
def play_background_music():
    music_file = random.choice(music_files)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(loops=-1)

# Creating the main window
root.title("Interface avec Tkinter")
background_image = Image.open('Assets/fond2.jpg')
background_photo = ImageTk.PhotoImage(background_image)
window_width = 500
window_height = 620
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Initializing the dimensions of the frame
base_frame_width = 450
base_frame_height = 580
frame_width = base_frame_width
frame_height = base_frame_height

# Creating the rounded frame
frame_image = create_rounded_frame(frame_width, frame_height, corner_radius=20,
                                    background_color=(255, 255, 255, 128),
                                    border_color=(0, 0, 0, 128),
                                    border_width=3)
frame_photo = ImageTk.PhotoImage(frame_image)

# Initial position of the frame
frame_x = (window_width - frame_width) // 2
frame_y = (window_height - frame_height) // 2

# Adding the frame with rounded corners
canvas.create_image(frame_x + frame_width // 2, frame_y + frame_height // 2, image=frame_photo, tags="frame")



# Loading music files
music_files = ['Assets/Sounds/music5.mp3', 'Assets/Sounds/music1.mp3', 'Assets/Sounds/music2.mp3', 'Assets/Sounds/music3.mp3', 'Assets/Sounds/music4.mp3', 'Assets/Sounds/music6.mp3']
#
# Playing random music on startup
play_background_music()

def on_settings_button_hover(event):
    settings_button.config(bg="pink")

def on_settings_button_leave(event):
    settings_button.config(bg="pink")

        
# Adding the settings button
settings_icon = Image.open('Assets/menu.png')
settings_icon = settings_icon.resize((20, 20))
settings_icon_photo = ImageTk.PhotoImage(settings_icon)

# Placer l'icône du menu au-dessus du cercle
settings_button = tk.Button(root, image=settings_icon_photo, command=open_settings_window, borderwidth=0, bg="pink")
settings_button.place(x=19, y=19)

# Créer le cercle rose foncé
circle_size = 40
canvas.create_oval(10, 10, 10 + circle_size, 10 + circle_size, fill="pink")



# Binding hover events to the settings button
settings_button.bind("<Enter>", on_settings_button_hover)
settings_button.bind("<Leave>", on_settings_button_leave)


#------------------TABLEAU-POUR-LES-MOTS------------------#
# Charger une police d'écriture plus grosse et plus grasse
font_path = "Assets/Font/catfiles/Catfiles.ttf"  # Remplacez par le chemin de votre police
#font_path = "Assets/Font/sunny_spells_basic/SunnySpellsBasic.ttf"
font_size = 16
font = ImageFont.truetype(font_path, font_size)

# Configuration de l'apparence du tableau
cell_width = 30
cell_height = 30
background_color = (255, 255, 255, 0)  # Transparent
#cell_color = (255, 255, 255, 255)  # Blanc
cell_color = (255, 255, 255, 128)  # Couleur semi-transparente pour les cellules
text_color = (0, 0, 0)  # Noir
# Utiliser la police personnalisée
font = ImageFont.truetype(font_path, font_size)

# Mettre à jour l'affichage du tableau
update_table_display()

# Running the main loop
root.mainloop()
