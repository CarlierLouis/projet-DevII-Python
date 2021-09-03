import unittest
import pygame
import os

from main import collision, Joueur, Ennemi, Laser
from database import recuperer_infos_joueurs
from database import recuperer_pseudos_joueurs
from database import info_objet1
from database import info_objet2
from database import info_objet3


class TestUnitaires(unittest.TestCase):
    # main
    # Gameplay
    def test_collision(self):
        """vérification qu'il y a une collision ou pas"""
        joueur = Joueur()
        alien = Ennemi(50, 50)
        alien.tir()
        joueur.tir()
        joueur.lasers[0].y = 50
        joueur.lasers[0].x = 50
        self.assertEqual(collision(joueur.lasers[0], alien), True)
        joueur.lasers[0].y = 20
        self.assertEqual(collision(joueur.lasers[0], alien), False)
        alien.lasers[0].y = 620
        alien.lasers[0].x = 487
        self.assertEqual(collision(alien.lasers[0], joueur), True)
        alien.lasers[0].y = 20
        self.assertEqual(collision(joueur.lasers[0], alien), False)
        self.assertEqual(collision(alien, joueur), False)
        alien.x = 487
        alien.y = 620
        self.assertEqual(collision(alien, joueur), True)

    def test_joueurInstance(self):
        j = Joueur()
        self.assertIsInstance(j, Joueur)

    def test_ennemiInstance(self):
        alien = Ennemi(50, 50)
        self.assertIsInstance(alien, Ennemi)
        alien = Ennemi(-50, -50)
        self.assertIsInstance(alien, Ennemi)

    def test_LaserInstance(self):
        j = Joueur()
        j.tir()
        self.assertIsInstance(j.lasers[0], Laser)
        alien = Ennemi(50, 50)
        alien.tir()
        self.assertIsInstance(alien.lasers[0], Laser)
        alien = Ennemi(-50, -50)
        alien.tir()
        self.assertIsInstance(alien.lasers[0], Laser)

    def test_LaserHors_ecran(self):
        img = pygame.image.load(os.path.join("images", "shot_alien.png"))
        tir = Laser(50, 50, img)
        self.assertEqual(tir.hors_ecran(780), False)
        tir = Laser(-50, -50, img)
        self.assertEqual(tir.hors_ecran(780), True)
    # Menus

    # database
    def test_recup_infos(self):
        self.assertIsInstance(recuperer_infos_joueurs(), list)

    def test_recup_pseudos(self):
        self.assertIsInstance(recuperer_pseudos_joueurs(), list)

    def test_info_jouets(self):
        self.assertIsInstance(info_objet1(), list)
        self.assertIsInstance(info_objet2(), list)
        self.assertIsInstance(info_objet3(), list)


if __name__ == '__main__':
    unittest.main()
