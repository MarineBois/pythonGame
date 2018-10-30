import pygame
import time
from random import *

#
#       VARIABLES
#

#initialisation de pygame
pygame.init()

# définir des variables de couleur utiles
blue = (113,177,227)
white = (255,255,255)
red = ( 239, 63, 43 )

# initialiser le jeu à False pour afficher le message d'accueil
game = False

#initialiser les tailles de la surface, du ballo et des nuages 
surfaceW = 800
surfaceH = 500
ballonW = 50
ballonH = 66
nuageW = 300
nuageH = 300

# création de la surface :
surface = pygame.display.set_mode((surfaceW, surfaceH))
# création du titre de la fenetre
pygame.display.set_caption("ballon volant")

#initialisation de l'horloge de pygame
horloge = pygame.time.Clock()

#on stock l'image du ballon dans une variable
img = pygame.image.load('Ballon01.png')
img_nuage01 = pygame.image.load('NuageHaut.png')
img_nuage02 = pygame.image.load('NuageBas.png')



#
#       FONCTIONS
#


# fonction d'affichage du message d'accueil
def accueilMessage():
    # arrière plan en bleu
    surface.fill(blue)
    # définir la police
    police = pygame.font.Font('BradBunR.ttf', 40)
    #créer le texte à afficher 
    texte = police.render("Appuyer sur une touche pour commencer", True, red)
    # afficher le texte
    surface.blit(texte, [70,200])
    # rafraichir l'écran
    pygame.display.update()

# fonction d'affichage du score
def score(compte) :
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("Score : " + str(compte), True, white)
    surface.blit(texte, [10,0])

#fonction d'affichage des nuages
def nuages(x_nuage, y_nuage, espace):
    surface.blit(img_nuage01, (x_nuage, y_nuage))
    surface.blit(img_nuage02, (x_nuage, y_nuage+nuageW+espace))

# fonction pour savoir si on rejoue
def rejoueOuQuitte():
    # pour chaque evenement pygame : keydown, keyup ou quit
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]) :
        # si event quit
        if event.type == pygame.QUIT :
            # on quite le jeu
            pygame.quit()
            quit()
        # si event keyup on ne fait rien on continue
        elif event.type == pygame.KEYUP :
            continue
        #sinon on renvoi l'event pour que la fonction retourne qq chose
        return event.key
    # si aucun event est détecté on ne retourne rien 
    return None

# fonction de création de l'objet texte en fonction du texte et de la police
def creaTexteObj(texte, Police) :
    texteSurface = Police.render(texte, True, red)
    return texteSurface, texteSurface.get_rect()

# fonction du message suite gameOver 
def message(texte, score):
    # définir les police des 3 lignes à afficher
    GOTexte = pygame.font.Font('BradBunR.ttf', 150)
    petitTexte = pygame.font.Font('BradBunR.ttf', 20)
    scoreTexte = pygame.font.Font('BradBunR.ttf', 50)

    # affichage du message du gameOver (Boom !!)
    GOTexteSurf, GOTexteRect = creaTexteObj(texte, GOTexte)
    GOTexteRect.center = surfaceW/2, ((surfaceH/2)-100)
    surface.blit(GOTexteSurf, GOTexteRect)

    # affichage du score 
    scoreTexteSurf, scoreTexteRect = creaTexteObj("Votre score : "+str(score)+ " !!", scoreTexte)
    scoreTexteRect.center = surfaceW/2, ((surfaceH/2))
    surface.blit(scoreTexteSurf, scoreTexteRect)

    # affichage du texte pour comment rejouer 
    petitTexteSurf, petitTexteRect = creaTexteObj("Appuyer sur une touche pour continuer", petitTexte)
    petitTexteRect.center = surfaceW/2, ((surfaceH/2)+50)
    surface.blit(petitTexteSurf, petitTexteRect)

    # on raffraichi l'écran pour tout afficher
    pygame.display.update()

    #on met un time.sleep de 2 seconde avant de pouvoir rejouer
    time.sleep(2)

    # tant que l'user n'appuie pas sur une touche on stoppe l'hologe pour "figer l'écran"
    while rejoueOuQuitte() == None :
        horloge.tick()

    # sinon on relance la fonction principale pour rejouer
    principale()

# fonction du game over 
def gameOver(score):
    message("Boom!", score)

# fonction affichage du ballon selon coordonnées :
def ballon(x,y,image):
    surface.blit(image,(x,y))

# fonction principale => génère le jeu
def principale():
    # on défini les valeurs pour le ballon 
    x = 150
    y = 200
    y_mouvement = 0

    # on défini les valeurs pour les nuages
    x_nuage = surfaceW
    y_nuage = randint(-300, 20)
    espace = ballonH*3
    nuage_vitesse = 1

    # initialisation du score à 0
    score_actuel = 0

    # initialisation du game over à False
    game_over = False

    # tant que le game_over est à False
    while not game_over :
        # pour les évenement pyagme
        for event in pygame.event.get():
            # si c'est quit => game_over = true
            if event.type == pygame.QUIT:
                game_over = True
            # si on appuie sur la fleche du HAUT => le ballon monte
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    y_mouvement = -0.8
            #si on relache la fleche du haut => le ballon descend
            if event.type == pygame.KEYUP :
                y_mouvement = 0.8
            
        # le ballon bouge en fonction du mouvement :
        y+= y_mouvement

        # arrière plan en bleu
        surface.fill(blue)

        # afficher le ballon
        ballon(x,y,img)

        # afficher les nuages
        nuages(x_nuage, y_nuage, espace)

        # afficher le score
        score(score_actuel)

        # mouvement du nuage
        x_nuage -= nuage_vitesse

        # si le Y du ballon sort du la surface =>gameover
        if y > surfaceH -40 or y < -10 :
            gameOver(score_actuel)

        # augmentation de la vitesse et diminution de l'espace selon le score
        if 3 <= score_actuel < 5 :
            nuage_vitesse = 1.2
            espace = ballonH*2.8
        if 5 <= score_actuel < 7 :
            nuage_vitesse = 1.4
            espace = ballonH*2.6
        if  7 <= score_actuel < 10 :
            nuage_vitesse = 1.6
            espace = ballonH*2.4

        # gameover si le ballon entre en collision avec le nuage du haut
        if x + ballonW > x_nuage +40 :
            if y < y_nuage + nuageH - 50 :
                if x - ballonW < x_nuage + nuageW -20 :
                    gameOver(score_actuel)

        # gameover si le ballon entre en collision avec le nuage du bas
        if x + ballonW > x_nuage+40 :
            if y + ballonH > y_nuage + nuageH + espace + 50 :
                if x - ballonW < x_nuage + nuageW - 20 :
                    gameOver(score_actuel)

        # lorque les nuages arrivent de l'autre côté de l'écran ils sont regénérés à l'oposé pour donner l'effet de défilement
        if x_nuage < (-1*nuageW):
            x_nuage = surfaceW
            y_nuage = randint(-300,20)
            score_actuel += 1


        # rafraichir l'écran
        pygame.display.update()


#
#       MAIN
#

# tant que le game est à False => affichage du message d'accueil
while not game :
    accueilMessage()

    # écoute des évenement pygame
    for event in pygame.event.get():
        # si une touche est appuyée lancement du jeu
        if event.type == pygame.KEYDOWN:
            game = True
            # lancement du jeu :
            principale()

#lorque la fenetre est fermée => le jeu est quitté
pygame.quit()
quit()