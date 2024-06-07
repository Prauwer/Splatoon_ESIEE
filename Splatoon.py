import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 spawn des joueurs (ne peut être traversé après la sortie)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi,  on peut écrire TBL[x][y]
    return T


TBL = CreateArray(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)

# attention,  on utilise TBL[x][y]

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

# placements des joueurs et tiles


def PlacementsTiles():  # placements des tiles
    TILES = np.full(TBL.shape, -1, dtype=np.int32)  # Initialise avec des -1

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                TILES[x][y] = 0
    return TILES


TILES = PlacementsTiles()

# création de la carte des distance
def CreateDistanceMap():
    DISTANCE = np.zeros(TILES.shape, dtype=np.int64)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1:
                DISTANCE[x][y] = 1000
            elif TILES[x][y] == 1:
                DISTANCE[x][y] = 0
            else:
                DISTANCE[x][y] = 100
    return DISTANCE


DISTANCE = CreateDistanceMap()

score = 0

Player1Pos = [3, 5]
Player2Pos = [16, 5]


##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL2[x][y] = info


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40  # taille d'une case en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM + ZOOM // 2

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.title("ESIEE - SPLATOON")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == " ":
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family="Arial", size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background="black")


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def dessineCase(x, y, color):
    canvas.create_rectangle(
        To(x - 0.5), To(y - 0.5), To(x + 0.5), To(y + 0.5), fill=color, outline=""
    )

def drawPlayer(xx, yy, color):
    e=20

    # Dessiner le triangle du poulpe
    points_triangle_haut = [
    xx - 4*e/5 , yy-e/6 ,   # Point supérieur gauche du triangle
    xx, yy - e ,           # Point supérieur du triangle
    xx + 4*e/5 , yy-e/6     # Point supérieur droit du triangle
    ]
    canvas.create_polygon(points_triangle_haut, fill=color, outline="")

    # Dessiner le rectangle du poulpe
    points_rectangle = [
    xx - 1*e/2, yy - e/6,   # Coin supérieur gauche
    xx + 1*e/2, yy - e/6,   # Coin supérieur droit
    xx + 1*e/2, yy + e/3,   # Coin inférieur droit
    xx - 1*e/2, yy + e/3    # Coin inférieur gauche
    ]
    canvas.create_polygon(points_rectangle, fill=color, outline="")

    # Dessiner la jambe gauche
    x_start = xx - e / 4
    y_start = yy + e / 3
    canvas.create_oval(x_start - e / 6, y_start - e / 2, x_start + e / 6, y_start + e / 2, outline="", fill=color)

    # Dessiner la jambe droite
    x_start_2 = xx + e / 5
    y_start_2 = yy + e / 3
    canvas.create_oval(x_start_2 - e / 6, y_start_2 - e / 2, x_start_2 + e / 6, y_start_2 + e / 2, outline="", fill=color)


    # Dessiner les yeux
    x_eye_left = xx - e / 6
    y_eye = yy - e / 6
    eye_radius_outer = e / 5
    eye_radius_inner = e / 12 

    canvas.create_oval(x_eye_left - eye_radius_outer, y_eye - eye_radius_outer,
                    x_eye_left + eye_radius_outer, y_eye + eye_radius_outer, fill="white", outline="")

    canvas.create_oval(x_eye_left - eye_radius_inner, y_eye - eye_radius_inner,
                    x_eye_left + eye_radius_inner, y_eye + eye_radius_inner, fill="black", outline="")

    x_eye_right = xx + e / 6

    canvas.create_oval(x_eye_right - eye_radius_outer, y_eye - eye_radius_outer,
                    x_eye_right + eye_radius_outer, y_eye + eye_radius_outer, fill="white", outline="")


    canvas.create_oval(x_eye_right - eye_radius_inner, y_eye - eye_radius_inner,
                    x_eye_right + eye_radius_inner, y_eye + eye_radius_inner, fill="black", outline="")

    # Dessiner les sourcils
    y_brow = yy - e / 3
    brow_width = e / 4 
    brow_height = e / 12

    x_brow_left = xx - e / 3.5
    canvas.create_line(x_brow_left, y_brow - brow_height,
                    x_brow_left + brow_width, y_brow - brow_height, fill="black", width=2.5)

    x_brow_right = xx + e / 10
    canvas.create_line(x_brow_right, y_brow - brow_height,
                    x_brow_right + brow_width, y_brow - brow_height, fill="black", width=2.5)


    # Dessiner les bras
    x_arm_left = xx - e * 0.55
    x_arm_right = xx + e * 0.55
    y_arm = yy + e / 10
    arm_length = e / 6 
    arm_thickness = e / 8 

    canvas.create_oval(x_arm_left - arm_length, y_arm - arm_thickness / 2,
                    x_arm_left + arm_length / 2, y_arm + arm_thickness / 2,
                    fill=color, outline="")

    canvas.create_oval(x_arm_right - arm_length / 2, y_arm - arm_thickness / 2,
                    x_arm_right + arm_length, y_arm + arm_thickness / 2,
                    fill=color, outline="")

def Affiche(message):

    canvas.delete("all")

    # murs
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1:
                dessineCase(x, y, "blue")

    # tiles neutres
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TILES[x][y] == 0 or TILES[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 5
                dessineCase(x, y, "grey")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine les joueurs
    x1 = To(Player1Pos[0])
    y1 = To(Player1Pos[1])
    
    x2 = To(Player2Pos[0])
    y2 = To(Player2Pos[1])

    drawPlayer(x1, y1, "cyan")
    drawPlayer(x2, y2, "red")

    # texte

    canvas.create_text(
        screeenWidth // 2,
        screenHeight - 50,
        text="PAUSE : PRESS SPACE",
        fill="yellow",
        font=PoliceTexte,
    )
    canvas.create_text(
        screeenWidth // 2,
        screenHeight - 20,
        text=message,
        fill="yellow",
        font=PoliceTexte,
    )


AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################


def PlayerPossibleMove(x, y):
    L = []
    if TBL[x][y - 1] == 2:
        L.append((0, -1))
    if TBL[x][y + 1] == 2:
        L.append((0, 1))
    if TBL[x + 1][y] == 2:
        L.append((1, 0))
    if TBL[x - 1][y] == 2:
        L.append((-1, 0))
    return L


def IAPlayer():
    L = PlayerPossibleMove()
    choix = random.randrange(len(L))
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]
    pass


def updateDistanceMap(x: int, y: int):
    pass


#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0


def PlayOneTurn():
    global iteration

    if not PAUSE_FLAG:
        iteration += 1
        pass

    Affiche(message=f"score : {score}")


###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()
