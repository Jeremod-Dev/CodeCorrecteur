from cProfile import label
from random import randint
from tkinter import Button, Canvas, Label, Tk


FICHIER_ENTREE = "im2.txt"

IMAGE_Y = 21
IMAGE_X = 22

BLANC: int = 0
NOIR: int = 1
JAUNE: int = 2
ROUGE: int = 3
VERT: int = 4
BLEU: int = 5

def saisirEntree():
    with open(FICHIER_ENTREE, 'r') as fic:
        ListImage = []
        listList = []
        lignes = fic.readlines() 
        for ligne in lignes:
            for element in ligne.split(" "):
                listList.append(int(element))
            ListImage.append(listList)
            listList = []
            print(ligne)
    return ListImage

def sommeLigne(ligne):
    res: int = 0
    for element in ligne:
        res += element
    return res

def sommePondere(ligne):
    tailleLigne: int = len(ligne)
    res: int = 0
    for iter in range (1,tailleLigne):
        res += iter * ligne[iter]
    return res


def envoiMessage(matrice):
    tailleMatrice = len(matrice)
    verificateur = []
    for iter in range (tailleMatrice):
        verificateur.append((sommeLigne(matrice[iter]), sommePondere(matrice[iter])))
    return (matrice, verificateur)

def bruit(packet):
    matrice = packet[0]
    tailleMatrice = len(matrice)
    tailleLigne = len(matrice[0])
    print("tets")
    for ligne in range(tailleMatrice):
        element: int = randint(0, tailleLigne-1)
        matrice[ligne][element] = randint(0,5)
    return (matrice, packet[1])

def correctionUnitaire(ligne, tuple):
    somme: int = sommeLigne(ligne)
    sommePon: int = sommePondere(ligne)
    erreurSomme: int = somme - tuple[0]
    if erreurSomme!=0:
        position: int = abs((tuple[1]-sommePon)/erreurSomme)+1
        ligne[int(position)-1] -= erreurSomme
    return ligne
    

def correcteur(packet):
    taillePacket = len(packet[0])
    for iter in range(taillePacket):
        packet[0][iter] = correctionUnitaire(packet[0][iter],packet[1][iter])
    return packet

def afficheImage(fenetre, image, xfen, yfen, txt):
    zone_dessin = Canvas(fenetre,width=210,height=200,bg="white",bd=8)
    zone_dessin.place(x=xfen, y=yfen)
    lbTitre = Label(fenetre, text=txt)
    lbTitre.place(x=xfen+20, y=yfen+220)
    x: int = 10
    y: int = 10
    for i in range(IMAGE_Y):
        for j in range(IMAGE_X):
            if image[i][j] == BLANC:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="white")
            if image[i][j] == NOIR:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="black")
            if image[i][j] == JAUNE:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="yellow")
            if image[i][j] == ROUGE:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="red")
            if image[i][j] == VERT:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="green")
            if image[i][j] == BLEU:
                zone_dessin.create_rectangle(x*j,y*i,x+j*10,y+i*10, fill="blue")
    zone_dessin.update_idletasks()

def communication(fenetre):
    message = saisirEntree()
    packet = envoiMessage(message)
    print(f"Envoi du packet:{packet}")
    afficheImage(fenetre, message, 10,10, "PC A | Envoi")
    bruit(packet)
    print(f"Reception du packet:{packet}")
    afficheImage(fenetre, packet[0], 310,10, "PC B | Reception")
    packetCorrige = correcteur(packet)
    print(f"Correction du packet:{packetCorrige}")
    afficheImage(fenetre, packetCorrige[0], 610,10, "PC B | Correction")

def main():
    fenetre = creationFenetre()
    communication(fenetre)
    btnEnvoyer = Button(fenetre,text="Envoyer", command=lambda: communication(fenetre))
    btnEnvoyer.place(x=400, y=275)
    fenetre.mainloop()

def creationFenetre():
    fenetre = Tk()
    fenetre.title("Code correcteur")
    fenetre.geometry("850x420+800+175")
    fenetre.resizable(False, False)
    return fenetre

main()