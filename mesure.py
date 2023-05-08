import pyglet
import pyglet.window.key as key
import pyglet.window.mouse as mouse
import pyglet.clock
import numpy as np

longueur = int(712*1.3)
largeur = int(484*1.3)


def calcul_hauteur_largeur(h, l, a):
    H = h / np.sin(a)
    L = l / np.cos(a)
    return H, L


class Fenetre(pyglet.window.Window):

    def __init__(self):
        super().__init__(longueur, largeur)

        self.image = pyglet.resource.image("image_test.png")
        self.image.width = longueur
        self.image.height = largeur

        self.mouse_x = 0
        self.mouse_y = 0

        self.carre_echelle = pyglet.shapes.Rectangle(
            self.image.width - 50, 50, 20, 20, color=(255, 0, 0))
        self.echelle = pyglet.shapes.Rectangle(
            0, 0, 0, 2, color=(255, 0, 0))
        self.start_selection_échelle = False
        self.first_click_echelle = True
        self.end_select_echelle = False
        self.mesure_echelle = pyglet.text.Label("Échelle",
            x=self.image.width - 120, y=55,  color=(255, 255, 255, 255))

        self.largeur_pillier = pyglet.shapes.Rectangle(
            0, 0, 0, 2, color=(0, 255, 0))
        self.carre_largeur_pillier = pyglet.shapes.Rectangle(
            self.image.width - 50, 100, 20, 20, color=(0, 255, 0))
        self.start_largeur_pillier = False
        self.first_click_largeur_pillier = True
        self.end_select_largeur_pillier = False
        self.largeur = pyglet.text.Label("Largeur du pillier",
            x=self.image.width - 185, y=105, color=(255, 255, 255, 255))

        self.hauteur_pillier = pyglet.shapes.Rectangle(
            0, 0, 2, 0, color=(255, 255, 0))
        self.carre_hauteur_pillier = pyglet.shapes.Rectangle(
            self.image.width - 50, 150, 20, 20, color=(255, 255, 0))
        self.start_hauteur_pillier = False
        self.first_click_hauteur_pillier = True
        self.end_select_hauteur_pillier = False
        self.hauteur = pyglet.text.Label("Hauteur du pillier",
            x=self.image.width - 185, y=155, color=(255, 255, 255, 255))

        self.carre_reset = pyglet.shapes.Rectangle(
            self.image.width - 50, 200, 20, 20, color=(255, 255, 255))
        self.zero = pyglet.text.Label("Remettre à zero",
            x=self.image.width - 175, y=205, color=(255, 255, 255, 255))

        self.carre_valider = pyglet.shapes.Rectangle(
            self.image.width - 50, 250, 20, 20, color=(0, 0, 255))
        self.valider = pyglet.text.Label("Valider les mesures",
            x=self.image.width - 205, y=255, color=(255, 255, 255, 255))

        pyglet.clock.schedule_interval(self.reshape_echelle, 1/60)
        pyglet.clock.schedule_interval(self.reshape_largeur_pillier, 1/60)
        pyglet.clock.schedule_interval(self.reshape_hauteur_pillier, 1/60)

    def reshape_echelle(self, dt):
        if self.start_selection_échelle:
            if self.first_click_echelle and not self.end_select_echelle:
                self.echelle.x = self.mouse_x
                self.echelle.y = self.mouse_y
                self.first_click_echelle = False
            else:
                self.echelle.width = abs(self.mouse_x - self.echelle.x)

    def reshape_largeur_pillier(self, dt):
        if self.start_largeur_pillier:
            if self.first_click_largeur_pillier and not self.end_select_largeur_pillier:
                self.largeur_pillier.x = self.mouse_x
                self.largeur_pillier.y = self.mouse_y
                self.first_click_largeur_pillier = False
            else:
                self.largeur_pillier.width = abs(
                    self.mouse_x - self.largeur_pillier.x)

    def reshape_hauteur_pillier(self, dt):
        if self.start_hauteur_pillier:
            if self.first_click_hauteur_pillier and not self.end_select_hauteur_pillier:
                self.hauteur_pillier.x = self.mouse_x
                self.hauteur_pillier.y = self.mouse_y
                self.first_click_hauteur_pillier = False
            else:
                self.hauteur_pillier.height = (
                    self.mouse_y - self.hauteur_pillier.y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            if self.start_selection_échelle:
                self.end_select_echelle = False
            if self.start_largeur_pillier:
                self.end_select_largeur_pillier = False
            if self.start_hauteur_pillier:
                self.end_select_hauteur_pillier = False
            self.mouse_x = x
            self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if (self.carre_echelle.x < x < self.carre_echelle.x
                + self.carre_echelle.width and
                self.carre_echelle.y < y < self.carre_echelle.y
                    + self.carre_echelle.height):
                if self.start_selection_échelle:
                    self.start_selection_échelle = False
                    print("end selection échelle")
                else:
                    self.start_selection_échelle = True
                    self.start_largeur_pillier = False
                    self.start_hauteur_pillier = False
                    print("start selection échelle")

            if (self.carre_largeur_pillier.x < x < self.carre_largeur_pillier.x
                + self.carre_largeur_pillier.width and
                self.carre_largeur_pillier.y < y < self.carre_largeur_pillier.y
                    + self.carre_largeur_pillier.height):
                if self.start_largeur_pillier:
                    self.start_largeur_pillier = False
                    print("end selection largeur pillier")
                else:
                    self.start_largeur_pillier = True
                    self.start_hauteur_pillier = False
                    self.start_selection_échelle = False
                    print("start selection largeur pillier")

            if (self.carre_hauteur_pillier.x < x < self.carre_hauteur_pillier.x
                + self.carre_hauteur_pillier.width and
                self.carre_hauteur_pillier.y < y < self.carre_hauteur_pillier.y
                    + self.carre_hauteur_pillier.height):
                if self.start_hauteur_pillier:
                    self.start_hauteur_pillier = False
                    print("end selection hauteur pillier")
                else:
                    self.start_hauteur_pillier = True
                    self.start_largeur_pillier = False
                    self.start_selection_échelle = False
                    print("start selection hauteur pillier")

            if (self.carre_reset.x < x < self.carre_reset.x
                + self.carre_reset.width and
                self.carre_reset.y < y < self.carre_reset.y
                    + self.carre_reset.height):
                
                self.largeur_pillier.width = 0
                self.hauteur_pillier.height = 0
                self.echelle.width = 0
                

                self.start_largeur_pillier = False
                self.start_hauteur_pillier = False
                self.start_selection_échelle = False

                print("reset mesure")

            if (self.carre_valider.x < x < self.carre_valider.x
                + self.carre_valider.width and
                self.carre_valider.y < y < self.carre_valider.y
                    + self.carre_valider.height):
                print("selection validée")
                a = float(input("Quel est l'angle d'inclinaison (en degré ): "))
                e = float(
                    input("Quelle est la longueur réelle de l'échelle ? (en micromètre) :"))
                # hauteur sans l'angle d'inclinaison
                h = (e*10**(-6)*self.hauteur_pillier.width)/self.echelle.width+1
                # largeur sans l'angle d'inclinaison
                l = (e*10**(-6)*self.largeur_pillier.width)/self.echelle.width
                x = calcul_hauteur_largeur(
                    h, l, a)
                print(f"hauteur réelle du pillier : {x[0]} micro mètre")
                print(f"largeur réelle du pillier : {x[1]} micro mètre")
                print(f"surface du pillier : {np.pi * x[1]**2} micro mètre carré")

    def on_mouse_release(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.start_selection_échelle:
                self.first_click_echelle = True
                self.end_select_echelle = True
            if self.start_largeur_pillier:
                self.first_click_largeur_pillier = True
                self.end_select_largeur_pillier = True
            if self.start_hauteur_pillier:
                self.first_click_hauteur_pillier = True
                self.end_select_hauteur_pillier = True

    def on_draw(self):
        self.clear()
        self.image.blit(0, 0)

        self.largeur_pillier.draw()
        self.hauteur_pillier.draw()
        self.echelle.draw()

        self.carre_echelle.draw()
        self.carre_largeur_pillier.draw()
        self.carre_hauteur_pillier.draw()
        self.carre_reset.draw()
        self.carre_valider.draw()

        self.mesure_echelle.draw()
        self.largeur.draw()
        self.hauteur.draw()
        self.zero.draw()
        self.valider.draw()


window = Fenetre()
pyglet.app.run()
