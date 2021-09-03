# Import pour la partie gameplay et jeu en tant que telle
import pygame
import random
import os

from database import ajout_xp

# Import pour les interfaces et menus
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from database import recuperer_infos_joueurs
from database import recuperer_pseudos_joueurs
from database import remplir_table_Profils
from database import payement
from database import ajout_objet1
from database import ajout_objet2
from database import ajout_objet3
from database import info_objet1
from database import info_objet2
from database import info_objet3
from database import supp_objet1
from database import supp_objet2
from database import supp_objet3

import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


# Fonstion qui appelle le script du jeu
def jouer():
    main(recup_profil)


# Choix du profil

# Création de la fenêtre
window_profils = Tk()

# Personnalisation de la fenêtre
window_profils.title("Connexion")
window_profils.geometry("720x600")
window_profils.minsize(480, 360)
window_profils.iconbitmap("images/logo.ico")
window_profils.config(background='#121517')

# Création de la frame
frame_profls = Frame(window_profils, bg="#121517")

# Titre
label_titre_profils = Label(window_profils, text="Choississez votre profil\n", font=("Arial", 40), bg='#121517',
                            fg='white')
label_titre_profils.pack()

# Menu déroulant
listeOptions = recuperer_pseudos_joueurs()
v = StringVar(window_profils)
v.set(listeOptions[0])
menu_deroulant = OptionMenu(window_profils, v, *listeOptions)
menu_deroulant.pack()

# Saut de ligne
label_saut = Label(frame_profls, text="\n", font=("Arial", 15), bg='#121517', fg='white')
label_saut.pack()

# Bouton validation
validation = Button(frame_profls, text="Valider", font=("Arial", 15), bg='white', fg='black',
                    command=window_profils.destroy)
validation.pack()

# Titre ajout nouveau joueur
label_nouveau = Label(frame_profls, text="\n\n______________________\n\n\n\n"
                                         " Vous êtes un nouveau joueur, ajoutez votre pseudo ici : \n",
                      font=("Arial", 15), bg='#121517', fg='white')
label_nouveau.pack()


# Entry du nouveau pseudo
def recup_nouveau_pseudo():
    recup_nouveau = entry_pseudo.get()
    # Condition pour que le nouveau pseudo soit accepté
    if recup_nouveau in recuperer_pseudos_joueurs() or recup_nouveau == "":
        messagebox.showinfo("erreur", "Le pseudo que vous avez choisi est déjà pris "
                                      "ou ne correspond pas aux normes.")
    elif " " in recup_nouveau:
        messagebox.showinfo("erreur", "Le pseudo que vous avez choisi est déjà pris "
                                      "ou ne correspond pas aux normes.")
    elif len(recup_nouveau) < 3 or len(recup_nouveau) > 10:
        messagebox.showinfo("erreur", "Le pseudo que vous avez choisi est déjà pris "
                                      "ou ne correspond pas aux normes.")
    else:
        # Fonction (de database.py) qui ajoute le pseudo dans la db
        remplir_table_Profils(recup_nouveau, 0, 0)


entry_pseudo = Entry(frame_profls, font=("Arial", 13), fg="red")
entry_pseudo.pack()

# Bouton qui déclanche l'appel de la fonction pour remplir la db avec le  nouveau pseudo
bouton_recup = Button(frame_profls, text="Enregistrer le nouveau pseudo", font=("Arial", 10),
                      command=recup_nouveau_pseudo)
bouton_recup.pack()

# Commenataire ajout nouveau profil
commentaire_profil = Label(frame_profls,
                           text="\n\n\n Une fois votre nouveau pseudo enregistré,"
                                " veillez relancer le jeu afin de pouvoir selectionner votre nouveau profil",
                           font=("Arial", 10), bg="#121517", fg='red')
commentaire_profil.pack()

# Ajout de la frame
frame_profls.pack()

# Affichage
window_profils.mainloop()

# Mise en mémoire du profils sélecionné
recup_profil = v.get()

'''
Partie Gameplay et jeu en tant que telle
'''


class Joueur:

    def __init__(self):
        """
        Class créant le joueur , permet aussi de le controler et de faire déplacer son laser
        Pré:-
        Post:-
        """
        self.x = 487
        self.y = 620
        self.vie = 60
        self.img = joueur_img
        self.laser_img = laser_joueur
        self.mask = pygame.mask.from_surface(self.img)
        self.vie_max = 60
        self.lasers = []
        self.cool_down_counter = 0

    def dessin(self, fenetre):
        """
        affichage du joueur des lasers et de la bar de vie sur l'écran
        Pré:fenetre
        Post:-
        """
        fenetre.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.dessin(fenetre)
        self.barre_vie(fenetre)

    def deplacement_laser(self, vel, objs):
        """
        deplacement des lasers plus test si il y a des collisions
        Pré: vel: int , objs : object
        """
        self.cooldown()
        for laser in self.lasers:
            laser.deplacement(vel)
            if laser.hors_ecran(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        global score
                        score += 20
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def cooldown(self):
        """
        Permet de gerer le timing du tir du joueur
        Pré: -
        Post: -
        """
        if self.cool_down_counter >= COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def tir(self):
        """
        Créer l'objet Tir
        """
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def barre_vie(self, fenetre):
        """
        affiche la barre de vie
        Pré: display
        Post: -
        """
        pygame.draw.rect(fenetre, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width()
                                                * (self.vie / self.vie_max), 10))


class Ennemi:

    def __init__(self, x, y):
        """
        Classe Ennemi sert à l'affichage, déplacement ennemi et ses lasers
        Pré: x,y :int y doiy être supérieur à height
        Post: -
        """
        if y > height:
            raise ValueError
        self.x = x
        self.y = y
        self.laser_img = laser_ennemi
        self.img = ennemi
        self.mask = pygame.mask.from_surface(self.img)
        self.lasers = []

    def deplacement(self, vel):
        """
        effectue le déplacement des Ennemis
        Pré: vel:int
        Post: -
        """
        self.y += vel

    def dessin(self, fenetre):
        """
        affiche l'ennemi
        Pré: fenetre: display
        """
        fenetre.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.dessin(fenetre)

    def deplacement_laser(self, vel, obj):
        """
        deplace les lasers tirer par l'ennemi
        Pré: vel:int, obj:objects
        """
        for laser in self.lasers:
            laser.deplacement(vel)
            if laser.hors_ecran(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.vie -= 10
                self.lasers.remove(laser)

    def tir(self):
        """
        Créer le tir
        Pré: -
        Post: -
        """
        laser = Laser(self.x + 20, self.y + 30, self.laser_img)
        self.lasers.append(laser)


class Laser:

    def __init__(self, x, y, img):
        """
        Classe mettant en place le tir effectuer soit par le joueur ou l'ennemmi
        Pré: x,y :int , img: display
        Post: -
        """
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def dessin(self, fenetre):
        """
        Affichage du laser
        Pré: fenetre: display
        Post: -
        """
        fenetre.blit(self.img, (self.x, self.y - 20))

    def deplacement(self, vel):
        """
        deplacement du laser
        Pré: vel: int
        Post: -
        """
        self.y += vel

    def hors_ecran(self, height):
        """
        teste si le laser est hors de l'écran ou pas
        Pré: height : int
        Post: boolean
        """
        return not (height >= self.y >= -30)

    def collision(self, obj):
        """
        teste si il y a une collision
        Pré: obj: object
        Post: boolean
        """
        return collision(self, obj)


width, height = 1000, 780

for k in range(len(info_objet1())):
    if info_objet1()[k] == recup_profil:
        if info_objet1()[k + 1] == 1:
            joueur_img = pygame.image.load(os.path.join("images", "ultraship.gif"))
        else:
            joueur_img = pygame.image.load(os.path.join("images", "ship.gif"))

for l in range(len(info_objet3())):
    if info_objet3()[l] == recup_profil:
        if info_objet3()[l + 1] == 1:
            ennemi = pygame.image.load(os.path.join("images", "oldschoolalien.gif"))
        else:
            ennemi = pygame.image.load(os.path.join("images", "alien.gif"))

laser_joueur = pygame.image.load(os.path.join("images", "shot.gif"))
laser_ennemi = pygame.image.load(os.path.join("images", "shot_alien.png"))

COOLDOWN = 45


def collision(obj1, obj2):
    """
    Pré: obj1, obj2 ce sont des object dans les cas qui nous concerne ça va être un tir et soit un joueur ou un ennemi
    Post: returns: Boolean  vrai si il y a collision faux si il n'y en a pas
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main(pseudo_choisi):
    """
    fonction qui va initialiser le jeu et faire exécuter les taches
    Post: pseudo du joueur
    Pré: -
    """
    pygame.init()
    pygame.font.init()
    bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "space.png")), (width, height))
    fenetre = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space invaders")
    global score
    score = 0
    fps = 60
    vel = 0
    for q in range(len(info_objet2())):
        if info_objet2()[q] == recup_profil:
            if info_objet2()[q + 1] == 1:
                vel = 9
            else:
                vel = 6
    jeu = True
    clock = pygame.time.Clock()
    vague = 0
    font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 100)
    joueur = Joueur()
    ennemis = []
    longueur_vague = 3
    vel_ennemi = 1
    perdu = False
    vel_laser = 9
    global COOLDOWN

    def reaffichage():
        """
        Fonction qui va s'occuper du réaffichage à l'écran quand il y a des modifications
        Pré: -
        Post: -
        """

        fenetre.blit(bg, (0, 0))
        vague_texte = font.render(f"Vague: {vague}", 1, (255, 255, 255))
        score_texte = font.render(f"Score: {score}", 1, (255, 255, 255))
        fenetre.blit(vague_texte, (10, 10))
        fenetre.blit(score_texte, (10, 50))
        for ennemi in ennemis:
            ennemi.dessin(fenetre)
        joueur.dessin(fenetre)
        if perdu:
            lost_label = lost_font.render("Game Over", 1, (255, 255, 255))
            fenetre.blit(lost_label, (width / 2 - lost_label.get_width() / 2, height / 2 - lost_label.get_height() / 2))
            pygame.quit()
            ajout_xp(score, vague - 1, pseudo_choisi)

        pygame.display.update()

    while jeu:

        clock.tick(fps)

        reaffichage()

        if joueur.vie <= 0:
            perdu = True

        if len(ennemis) == 0:
            longueur_vague += 3
            vague += 1
            for i in range(longueur_vague):
                ennemi = Ennemi(random.randrange(70, width - 70), random.randrange(-1000 + vague * -100, -200))
                ennemis.append(ennemi)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and joueur.x + vel + 32 < width:
            joueur.x += vel

        if keys[pygame.K_LEFT] and joueur.x - vel > 0:
            joueur.x -= vel

        if keys[pygame.K_SPACE]:
            joueur.tir()

        for ennemi in ennemis:
            ennemi.deplacement(vel_ennemi)
            ennemi.deplacement_laser(vel_laser, joueur)
            if random.randrange(0, fps * 3) == 1:
                ennemi.tir()
            if collision(ennemi, joueur):
                joueur.vie -= 20
                score += 20
                ennemis.remove(ennemi)
            elif ennemi.y > height:
                ennemis.remove(ennemi)

        joueur.deplacement_laser(-vel_laser, ennemis)


'''
Fin de la partie Gameplay et jeu
'''


# M E N U
def fenetre_menu():
    # Création de la fenêtre
    window_menu = Tk()

    # Personnalisation de la fenêtre
    window_menu.title("Space Invaders    " + "[" + recup_profil + "]")
    window_menu.geometry("1080x720")
    window_menu.minsize(480, 360)
    window_menu.iconbitmap("images/logo.ico")
    window_menu.config(background='#121517')

    # Création de la frame
    frame_menu = Frame(window_menu, bg='#121517')

    # Titre
    label_titre = Label(window_menu, text="Space Invaders", font=("Arial", 40), bg='#121517', fg='white')
    label_titre.pack()

    # Ajout des boutons
    bouton_jouer = Button(frame_menu, text="Jouer", font=("Arial", 25), bg='white', fg='#121517', bd="10",
                          relief="ridge", command=jouer)
    bouton_score = Button(frame_menu, text="Scores", font=("Arial", 25), bg='white', fg='#121517', bd="10",
                          relief="ridge", command=fenetre_score)
    bouton_boutique = Button(frame_menu, text="Boutique", font=("Arial", 25), bg='white', fg='#121517', bd="10",
                             relief="ridge", command=fenetre_boutique)
    bouton_inventaire = Button(window_menu, text="Inventaire", font=("Arial", 15), bg='#660000', fg='white',
                               command=inventaire)

    bouton_jouer.pack(pady=25, fill=X)
    bouton_score.pack(pady=25, fill=X)
    bouton_boutique.pack(pady=25, fill=X)
    bouton_inventaire.pack(pady=25, side=BOTTOM)

    # Ajout de la frame
    frame_menu.pack(expand=YES)

    # Affichage
    window_menu.mainloop()


# Affichage des SCORES (fenêtre des scores)
def fenetre_score():
    # Création de la fenêtre
    window_scores = Tk()

    # Personnalisation de la fenêtre
    window_scores.title("Scores")
    window_scores.geometry("600x360")
    window_scores.minsize(600, 360)
    window_scores.maxsize(600, 360)
    window_scores.iconbitmap("images/score.ico")
    window_scores.config(background='white')

    # Création des frames
    frame_scores = Frame(window_scores, bg='#660000')
    frame_scores_retour = Frame(window_scores, bg='white')

    # Ajout du tableau de scoring avec Treeview
    tree = ttk.Treeview(window_scores)
    tree["columns"] = ("one", "two")
    tree.column("#0", width=200, minwidth=200, stretch=FALSE)
    tree.column("one", width=200, minwidth=200, stretch=FALSE)
    tree.column("two", width=200, minwidth=200, stretch=FALSE)

    tree.heading("#0", text="Pseudo")
    tree.heading("one", text="xp")
    tree.heading("two", text="argent")

    for i in range(len(recuperer_infos_joueurs())):
        tree.insert("", 0, text=recuperer_infos_joueurs()[i][0], values=(recuperer_infos_joueurs()[i][1],
                                                                         recuperer_infos_joueurs()[i][2]))

    tree.pack()

    bouton_scores_retour = Button(frame_scores_retour, text="retour", font=("Arial", 15), bg='#660000', fg='white',
                                  command=window_scores.destroy)

    bouton_scores_retour.pack()

    # Ajout des frames
    frame_scores.pack()
    frame_scores_retour.pack(pady=25, fill=X, side=BOTTOM)

    # Affichage
    window_scores.mainloop()


# Affichage de la BOUTIQUE (fenêtre de la boutique)
def fenetre_boutique():
    # Création de la fenêtre
    window_boutique = Tk()

    # Personnalisation de la fenêtre
    def solde_joueur():
        for j in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[j][0] == recup_profil:
                return recuperer_infos_joueurs()[j][2]

    window_boutique.title("Boutique")
    window_boutique.geometry("800x600")
    window_boutique.minsize(480, 360)
    window_boutique.iconbitmap("images/boutique.ico")
    window_boutique.config(background='#660000')

    # Création des frames
    frame_boutique = Frame(window_boutique, bg='#660000')
    frame_boutique_retour = Frame(window_boutique, bg='#660000')

    # Ajout des textes et boutons
    label_boutique = Label(window_boutique, text="Boutique", font=("Arial", 35), bg='#660000', fg='white')
    label_solde = Label(window_boutique, text="Votre solde: " + str(solde_joueur()), font=("Arial", 15), bg='#660000',
                        fg='white')
    label2_boutique = Label(frame_boutique, text="", font=("Arial", 15), bg='#660000', fg='white')
    bouton_boutique_retour = Button(frame_boutique_retour, text="retour", font=("Arial", 15), bg='#660000', fg='white',
                                    command=window_boutique.destroy)
    label_boutique.pack()
    label_solde.pack()
    label2_boutique.pack()
    bouton_boutique_retour.pack()

    # Contenu de la boutique
    # Objet 1
    objet1 = LabelFrame(window_boutique, text="Objet 1", font=("Arial", 20), bg='#660000', padx=20, pady=20)
    objet1.pack(fill="both", expand="yes")
    Label(objet1, bg='#660000', font=("Arial", 15), text="Skin 'UltraShip' pour votre vaisseau (prix: 50)").pack()

    def achat1():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet1())):
                    if info_objet1()[j] == recup_profil:
                        if info_objet1()[j + 1] == 1:
                            messagebox.showinfo("erreur", "Vous possédez déjà cet objet")
                        else:
                            if recuperer_infos_joueurs()[i][2] >= 50:
                                payement(50, recup_profil)
                                ajout_objet1(1, recup_profil)
                                messagebox.showinfo("Boutique", "Achat bien effectué !")
                            else:
                                messagebox.showinfo("erreur", "Votre solde est insufisant !")

    bouton_achat1 = Button(objet1, text="Acheter", command=achat1)
    bouton_achat1.pack(side=BOTTOM)

    # Objet 2
    objet2 = LabelFrame(window_boutique, text="Objet 2", font=("Arial", 20), bg='#660000', padx=20, pady=20)
    objet2.pack(fill="both", expand="yes")
    Label(objet2, bg='#660000', font=("Arial", 15),
          text="'Speed Pack', une fois équipé vous vous déplacez 1,5X plus vite (prix: 50)").pack()

    def achat2():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet2())):
                    if info_objet2()[j] == recup_profil:
                        if info_objet2()[j + 1] == 1:
                            messagebox.showinfo("erreur", "Vous possédez déjà cet objet")
                        else:
                            if recuperer_infos_joueurs()[i][2] >= 50:
                                payement(50, recup_profil)
                                ajout_objet2(1, recup_profil)
                                messagebox.showinfo("Boutique", "Achat bien effectué !")
                            else:
                                messagebox.showinfo("erreur", "Votre solde est insufisant !")

    bouton_achat2 = Button(objet2, text="Acheter", command=achat2)
    bouton_achat2.pack(side=BOTTOM)

    # Objet 3
    objet3 = LabelFrame(window_boutique, text="Objet 3", font=("Arial", 20), bg='#660000', padx=20, pady=20)
    objet3.pack(fill="both", expand="yes")
    Label(objet3, bg='#660000', font=("Arial", 15), text="'Skin Oldschool' pour aliens (prix: 50)").pack()

    def achat3():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet3())):
                    if info_objet3()[j] == recup_profil:
                        if info_objet3()[j + 1] == 1:
                            messagebox.showinfo("erreur", "Vous possédez déjà cet objet")
                        else:
                            if recuperer_infos_joueurs()[i][2] >= 50:
                                payement(50, recup_profil)
                                ajout_objet3(1, recup_profil)
                                messagebox.showinfo("Boutique", "Achat bien effectué !")
                            else:
                                messagebox.showinfo("erreur", "Votre solde est insufisant !")

    bouton_achat3 = Button(objet3, text="Acheter", command=achat3)
    bouton_achat3.pack(side=BOTTOM)

    '''
    # Objet 4
    objet4 = LabelFrame(window_boutique, text="Objet 4", font=("Arial", 20), bg='#660000', padx=20, pady=20)
    objet4.pack(fill="both", expand="yes")
    Label(objet4, bg='#660000', font=("Arial", 15), text="Description objet 4 (prix: 1000)").pack()

    def achat4():
        

    bouton_achat4 = Button(objet4, text="Acheter", command=achat4)
    bouton_achat4.pack(side=BOTTOM)
    '''

    # Ajout des frames
    frame_boutique.pack()
    frame_boutique_retour.pack(pady=25, fill=X, side=BOTTOM)

    # Affichage
    window_boutique.mainloop()


# Affiche de l'inventaire du joueur (objets qu'il possède déjà)
def inventaire():
    ok1 = ""
    ok2 = ""
    ok3 = ""
    for j in range(len(info_objet1())):
        if info_objet1()[j] == recup_profil:
            if info_objet1()[j + 1] == 1:
                ok1 = "Skin 'UltraShip' "
            else:
                ok1 = ""
    for j in range(len(info_objet2())):
        if info_objet2()[j] == recup_profil:
            if info_objet2()[j + 1] == 1:
                ok2 = "'Speed Pack' "
            else:
                ok2 = ""
    for j in range(len(info_objet3())):
        if info_objet3()[j] == recup_profil:
            if info_objet3()[j + 1] == 1:
                ok3 = "'Skin Oldschool' pour aliens "
            else:
                ok3 = ""
    ok_final = ok1 + "\n\n\n" + ok2 + "\n\n\n" + ok3

    window_inventaire = Tk()

    window_inventaire.title("inventaire")
    window_inventaire.geometry("800x600")
    window_inventaire.minsize(480, 360)
    window_inventaire.iconbitmap("images/logo.ico")
    window_inventaire.config(background='#660000')

    # Création des frames
    frame_inventaire = Frame(window_inventaire, bg='#660000')
    frame_inventaire_retour = Frame(window_inventaire, bg='#660000')

    # Textes et bouttons
    label_inventaire = Label(window_inventaire, text="Inventaire", font=("Arial", 35), bg='#660000', fg='white')

    # Désacrivation de l'objet 1
    def supp1():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet1())):
                    if info_objet1()[j] == recup_profil:
                        if info_objet1()[j + 1] == 0:
                            messagebox.showinfo("erreur", "Vous ne possédez pas cet objet")
                        else:
                            supp_objet1(0, recup_profil)
                            messagebox.showinfo("Inventaire", "Objet bien supprimé")

    bouton_supp1 = Button(window_inventaire, text="Désactiver Objet 1", command=supp1)

    # Désactivation de l'objet 2
    def supp2():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet2())):
                    if info_objet2()[j] == recup_profil:
                        if info_objet2()[j + 1] == 0:
                            messagebox.showinfo("erreur", "Vous ne possédez pas cet objet")
                        else:
                            supp_objet2(0, recup_profil)
                            messagebox.showinfo("Inventaire", "Objet bien supprimé")

    bouton_supp2 = Button(window_inventaire, text="Désactiver Objet 2", command=supp2)

    # Désacrivation de l'objet 3
    def supp3():
        for i in range(len(recuperer_infos_joueurs())):
            if recuperer_infos_joueurs()[i][0] == recup_profil:
                for j in range(len(info_objet3())):
                    if info_objet3()[j] == recup_profil:
                        if info_objet3()[j + 1] == 0:
                            messagebox.showinfo("erreur", "Vous ne possédez pas cet objet")
                        else:
                            supp_objet3(0, recup_profil)
                            messagebox.showinfo("Inventaire", "Objet bien supprimé")

    bouton_supp3 = Button(window_inventaire, text="Désactiver Objet 3", command=supp3)

    bouton_inventaire_retour = Button(frame_inventaire_retour, text="retour", font=("Arial", 15), bg='#660000',
                                      fg='white',
                                      command=window_inventaire.destroy)

    frame_inventaire.pack()
    frame_inventaire_retour.pack(pady=25, fill=X, side=BOTTOM)

    label_inventaire.pack()
    bouton_inventaire_retour.pack()

    bouton_supp3.pack(side=BOTTOM)
    bouton_supp2.pack(side=BOTTOM)
    bouton_supp1.pack(side=BOTTOM)

    inventaire1 = LabelFrame(window_inventaire, text="Vous possédez", font=("Arial", 20), bg='#660000', padx=20,
                             pady=20)

    inventaire1.pack(fill="both", expand="yes")
    Label(inventaire1, bg='#660000', font=("Arial", 15), text=ok_final).pack()

    window_inventaire.mainloop()


fenetre_menu()
