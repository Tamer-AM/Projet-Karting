import pygame
import socket
import asyncio 


DEVICE_ADRESS = 0x53
POWER_CTL = 0x2D
DATAX0 = 0x32

pygame.init()
pygame.font.init()

police = pygame.font.SysFont('Unispace', 40)

WIDTH = 1600
HEIGHT = 900
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Raspberry Kart')

# Configurer le socket UDP
UDP_IP = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
UDP_PORT = 5005     # Doit correspondre au port utilisé par l'émetteur

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def read_acceleration(frame_count):
    if frame_count < 150:  # Pendant le décompte (3, 2, 1, GO)
        return
    try:
        sock.settimeout(0.01)  # Définir un délai d'attente de 0.01 seconde
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        
        # Convertir et afficher les données reçues
        y, x = map(float, message.split(','))
        print(x,y)
        return y, x
    except socket.timeout:
        # Si aucune donnée n'est reçue dans le délai imparti, retourner une valeur par défaut
        return 0, 0

class Checkpoint():
    def __init__(self, x, y, longueur, largeur):
        self.x = x
        self.y = y
        self.longueur = longueur
        self.largeur = largeur
        self.rect = pygame.Rect(self.x, self.y, longueur, largeur)
        self.etat = 0
        self.indicateur = pygame.Rect(self.x, self.y+largeur -50, 50, 50)
        self.top_depart = pygame.Rect(600, 300, 400, 120)
        self.gauche = pygame.Rect(625, 310, 100, 100)
        self.milieu = pygame.Rect(750, 310, 100, 100)
        self.droite = pygame.Rect(875, 310, 100, 100)
        self.couleur = (255,0,0)
    
    
    def affichage(self,frame_count):
        if self.etat == 0:
            #○ pygame.draw.rect(SCREEN, (0,0,255), self.rect)
            pygame.draw.rect(SCREEN, (0,0,0), self.indicateur)
            if frame_count < 250:
                pygame.draw.rect(SCREEN, (0,0,0), self.top_depart)
                if frame_count > 60:
                    pygame.draw.rect(SCREEN, self.couleur, self.gauche)
                if frame_count > 90:
                    pygame.draw.rect(SCREEN, self.couleur, self.milieu)
                if frame_count > 120:
                    pygame.draw.rect(SCREEN, self.couleur, self.droite)
                if frame_count > 150:
                    self.couleur = (0,255,0)
        else:
            #pygame.draw.rect(SCREEN, (0,127,127), self.rect)
            pygame.draw.rect(SCREEN, (255,255,0), self.indicateur)


class Obstacle():
    def __init__(self, x, y, longueur, largeur):
        self.x = x
        self.y = y
        self.longueur = longueur
        self.largeur = largeur
        self.rect = pygame.Rect(self.x, self.y, longueur, largeur)
        self.vecteur_h = pygame.math.Vector2(self.x, self.x + longueur)
        self.vecteur_v = pygame.math.Vector2(self.y, self.y + largeur)
    
    def affichage(self):
        pygame.draw.rect(SCREEN, (255,0,0), self.rect)


class Hors_piste():
    def __init__(self, x, y, longueur, largeur):
        self.x = x
        self.y = y
        self.longueur = longueur
        self.largeur = largeur
        self.rect = pygame.Rect(self.x, self.y, self.longueur, self.largeur)
    
    def affichage(self):
        pygame.draw.rect(SCREEN, (0,255,0), self.rect)
        

class Kart():
    def __init__(self, joueur, x ,y):
        self.joueur = joueur
        self.x = x
        self.y = y
        self.longueur = 52                    #69 100%    52 75%
        self.largeur = 40                     #53 100%    40 75%
        if self.joueur == 1:
            self.image0 = pygame.image.load('game_files/Images/KART_1.png')
            self.image0 = pygame.transform.scale(self.image0, (self.longueur, self.largeur))
            self.image = pygame.image.load('game_files/Images/KART_1.png')
            self.image = pygame.transform.scale(self.image, (self.longueur, self.largeur))
        if self.joueur == 2:
            self.image0 = pygame.image.load('game_files/Images/KART_2.png')
            self.image0 = pygame.transform.scale(self.image0, (self.longueur, self.largeur))
            self.image = pygame.image.load('game_files/Images/KART_2.png')
            self.image = pygame.transform.scale(self.image, (self.longueur, self.largeur))
        self.rect = pygame.Rect(self.x,self.y,self.longueur,self.largeur)
        self.vecteur = pygame.math.Vector2(-1, 0)
        self.vitesse = 0
        self.vitesse_max = 7
        self.clignoter = [False,0]
        self.hp = False
        self.tour = 0
        self.tourner(1,0.1)
        self.temps = 0

    def affichage(self):
        #pygame.draw.rect(SCREEN, (255,255,255), self.rect)
        SCREEN.blit(self.image, self.rect)

    def mouvement(self):
        self.rect.center += self.vecteur*self.vitesse
    
    def accelerometre(self,frame_count):
        y, x = read_acceleration(frame_count)
        if 300 > y > 25:
            # gauche
            self.tourner(1, 0.05 * y)
        elif 1000 > y > 775:
            # droite
            self.tourner(0, -0.05 * (y - 1000))
        else:
            self.vitesse = max(0, self.vitesse)

        if 250 > x > 45:
            self.accelerer(1)
        elif 900 > x > 750:
            self.accelerer(0)
        else:
            self.vitesse = max(0, self.vitesse)

    def tourner(self,x, angle):
        if abs(angle) > 60:
            self.vitesse *= 0.6
        elif abs(angle) > 30:
            self.vitesse *= 0.8
        if x:
            #self.vecteur.rotate_ip(-(angle+(1.5*((7-abs(self.vitesse))/2))))
            self.vecteur.rotate_ip(-angle)
        else:
            #self.vecteur.rotate_ip(angle+(1.5*((7-abs(self.vitesse))/2)))
            self.vecteur.rotate_ip(angle)
        self.image = pygame.transform.rotate(self.image0, self.vecteur.angle_to(pygame.math.Vector2(1,0)))
        cord = self.rect.center
        self.rect = self.image.get_rect(center = cord)

    def accelerer(self, x):
        if self.vitesse > 3 and self.hp:
            self.vitesse = 3
        if self.vitesse < -3 and self.hp:
            self.vitesse = -3
        if self.vitesse > 3 and self.clignoter[0]:
            self.vitesse = 3
        
        if x:
            if self.vitesse < self.vitesse_max:
                self.vitesse += 0.4
        else:
            if self.vitesse > -self.vitesse_max:
                self.vitesse -= 0.6

    def freinage(self):
        if self.vitesse > 0:
            self.vitesse -= 0.2
        else:
            self.vitesse += 0.2

    def collision_obstacle(self, obs):
        for obstacle in obs:
            if self.rect.clipline((obstacle.x, obstacle.y), (obstacle.x, obstacle.y + obstacle.largeur)):
                # gauche vers droite
                self.rect.centerx = obstacle.rect.left - self.longueur + 2
                self.vecteur.rotate_ip(180)
                self.vecteur[1] = -self.vecteur[1]
                self.tourner(1, 0.1)
                self.vitesse = 2
                self.clignoter[0] = True

            elif self.rect.clipline((obstacle.x + obstacle.longueur, obstacle.y),(obstacle.x + obstacle.longueur, obstacle.y + obstacle.largeur)):
                # droite vers gauche
                self.rect.centerx = obstacle.rect.right + self.longueur - 2
                self.vecteur.rotate_ip(180)
                self.vecteur[1] = -self.vecteur[1]
                self.tourner(1, 0.1)
                self.vitesse = 2
                self.clignoter[0] = True

            if self.rect.clipline((obstacle.x, obstacle.y), (obstacle.x + obstacle.longueur, obstacle.y)):
                # haut vers bas
                self.rect.centery = obstacle.rect.top - self.largeur + 2
                self.vecteur.rotate_ip(180)
                self.vecteur[0] = -self.vecteur[0]
                self.tourner(1, 0.1)
                self.vitesse = 2
                self.clignoter[0] = True

            elif self.rect.clipline((obstacle.x, obstacle.y + obstacle.largeur), (obstacle.x + obstacle.longueur, obstacle.y + obstacle.largeur)):
                # bas vers haut
                self.rect.centery = obstacle.rect.bottom + self.largeur - 2
                self.vecteur.rotate_ip(180)
                self.vecteur[0] = -self.vecteur[0]
                self.tourner(1, 0.1)
                self.vitesse = 2
                self.clignoter[0] = True


        #if self.rect.colliderect(kart.rect):
        #    self.clignoter[0] = True
        #    kart.clignoter[0] = True


    def clignotant(self):
        if self.clignoter[0]:
            self.vitesse_max = 6
            self.vitesse_min = -6
            self.clignoter[1] += 1
            if self.clignoter[1] > 60:
                self.clignoter = [False, 0]

    def collision_hors_piste(self, hors_piste):
        self.vitesse_max = 11
        self.vitesse_min = -11
        self.hp = False
        for hs in hors_piste:
            if self.rect.colliderect(hs.rect):
                self.vitesse_max = 5
                self.hp = True

    def collision_checkpoint(self, cp):
        if self.rect.colliderect(cp[0].rect):
            cp[0].etat = 1
        if self.rect.colliderect(cp[-1].rect):
            if cp[-2].etat == 1:
                self.tour += 1
                for i in range(len(cp)):
                    cp[i].etat = 0
        for i in range(1, len(cp) - 1):
            if self.rect.colliderect(cp[i]):
                if cp[i-1].etat == 1:
                    cp[i].etat = 1
                    
            

def affichage_elements(m, hp,check, frame_count):
    SCREEN.blit(circuit, (0,0))
    #for hors_piste in hp:
    #    hors_piste.affichage()
    #for obs in m:
    #    obs.affichage()
    for checkpoint in check:
        checkpoint.affichage(frame_count)
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(180,720,2.5,120))
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(410,210,2.5,120))
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(790,720,2.5,120))
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(1200,210,2.5,120))
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(1420,720,2.5,120))
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(800,60,2.5,120))


#init_adxl345()

kart1 = Kart(1, 870, 100)
mur1 = Obstacle(313,690,190,220)
mur2 = Obstacle(325,625,160,360)
mur3 = Obstacle(335,560,140,360)
mur3 = Obstacle(345,490,120,360)
mur4 = Obstacle(370,340,70,360)

mur5 = Obstacle(1113,690,190,220)
mur6 = Obstacle(1125,625,160,360)
mur7 = Obstacle(1135,560,140,360)
mur8 = Obstacle(1145,490,120,360)
mur9 = Obstacle(1170,340,70,360)

mur10 = Obstacle(0,0,1600,5)
mur11 = Obstacle(0,0,5,900)
mur12 = Obstacle(1595,0,5,900)
mur13 = Obstacle(0,895,1600,5)

mur14 = Obstacle(600,200,400,400)
mur15 = Obstacle(190,190,1220,15)

circuit = pygame.image.load('game_files/Images/Terrain_N°1.png')
circuit = pygame.transform.scale(circuit, (1600,900))

clock = pygame.time.Clock()

murs = [mur1,mur2,mur3,mur4,mur5,mur6,mur7,mur8,mur9,mur10,mur11,mur12,mur13]
#murs = []

herbe1 = Hors_piste(0,0 , 1600, 40)
herbe2 = Hors_piste(0,0 , 40, 900)
herbe3 = Hors_piste(0,860 , 1600, 40)
herbe4 = Hors_piste(1560,0 , 40, 900)

herbe5 = Hors_piste(590,200 , 50, 300)
herbe6 = Hors_piste(625,200 , 350, 500)
herbe7 = Hors_piste(950,200 , 50, 350)
herbe12 = Hors_piste(1000,200,25,200)

herbe13 = Hors_piste(190,190,900,20)

herbe8 = Hors_piste(190,200 , 25, 400)
herbe9 = Hors_piste(190,200 , 60, 170)

herbe10 = Hors_piste(1390,200 , 25, 400)
herbe11 = Hors_piste(1350,200 , 60, 170)

hp = [herbe1,herbe2,herbe3,herbe4,herbe5,herbe6,herbe7,herbe8,herbe9,herbe10,herbe11,herbe12,herbe13]
#hp = []
frame_count = 0

cp1 = Checkpoint(180,600, 40,300)
cp2 = Checkpoint(380,200, 40,280)
cp3 = Checkpoint(770,600, 40,300)
cp4 = Checkpoint(1175,200, 40,280)
cp5 = Checkpoint(1385,600, 40,300)
cp6 = Checkpoint(770,0, 40,240)
check = [cp1, cp2, cp3,cp4, cp5, cp6]




async def main(frame_count):
    running = True
    start = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        SCREEN.fill((0,0,0))

        affichage_elements(murs, hp, check, frame_count)


        if kart1.tour == 2:
             chrono = int(frame_count/30)
             kart1.temps = chrono
             texte = police.render(str('Chrono: {} secondes.'.format(kart1.temps)), False, (0, 0, 0))
             SCREEN.blit(texte, (650,350))
             start = False
        else:
             frame_count += 1
         
        if 60 < frame_count < 90:
            SCREEN.blit((police.render('3', False, (0,0,0))), (780,450))
        if 90 < frame_count < 120:
            SCREEN.blit((police.render('2', False, (0,0,0))), (780,450))
        if 120 < frame_count < 150:
            SCREEN.blit((police.render('1', False, (0,0,0))), (780,450))
        if 150 < frame_count < 250:
            SCREEN.blit((police.render('GO', False, (0,0,0))), (780,450))
            start = True

        if not(kart1.clignoter[0] and frame_count%10 >=5):
            kart1.affichage()

        if start:
            kart1.accelerometre(frame_count)
            kart1.mouvement()
    
    
            print(kart1.hp)

            kart1.rect.centerx = min(1600,max(0,kart1.rect.centerx))
            kart1.rect.centery = min(900,max(0,kart1.rect.centery))
    
            
            #kart1.input_clavier()
            kart1.collision_hors_piste(hp)
            kart1.collision_obstacle(murs)
            kart1.collision_checkpoint(check)
            kart1.clignotant()
        
        
        
        pygame.display.update()
        clock.tick(30)
        await asyncio.sleep(0)  # Let other tasks run
asyncio.run(main(frame_count))
