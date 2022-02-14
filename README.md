# CodeCorrecteur
## Mise en place d'un code correcteur dans le cadre d'une communication de transfère de bitmap
Ce projet simule l'envoi d'un fichier bitmap entre deux machines PC A et PC B. Seulement, la connexion est mauvaise et du bruit communicationnel viens s'ajouter à l'image envoyé. PC A et PC B se sont alors mis d'accord sur une manière de corriger le bruit du réseau.

La mise en situation ici est simple. L'image peut-etre composé de seulement 6 couleurs (Blanc, Noir, Rouge, Jaune, Bleu, Vert) qui admet un code unique. Ainsi pour avoir un pixel blanc, dans la matrice, il faut mettre un 0 et un pixel bleu, il faut écrire 5.

## Fonctionnement du code correcteur
*Pour chaque ligne seul un pixel peut-etre modifié dû au bruit sur le réseau*

Voici la composition d'un ligne de l'image: [0,0,2,0,0]
Au cas où, il y aurait une détérioration de l'image sur le trajet PCA va envoyer deux informations en plus de la ligne.
Il va faire une somme des coefficients et une somme pondéré de leur position:

```
Somme: 0 + 0 + 2 + 0 + 0 = 2
Somme pondere: 0x1 + 0x2 + 2x3 + 0x4 + 0x5 = 6
```

PCA va envoyer à PCB ([0,0,2,0,0], (2,6)]

Imaginons que du bruit altère la ligne contenant le code couleur du bitmap ainsi la ligne devient [0,1,2,0,0]

PCB recoit de PCA ([0,1,2,0,0], (2,6)]. Il va faire la meme opération que PCA:

```
Somme: 0 + 1 + 2 + 0 + 0 = 3
Somme Pondéré: 0x1 + 1x2 + 2x3 + 0x4 + 0x5 = 8
```

Hors PCB remarque que le tuple qu'il vient de calculer (3,8) est différent de celui recu de PCA (2,6). Il va donc faire deux opérations pour retrouver l'erreur et la position où elle se trouve.

Erreur: 3 - 2 = 1  (Somme calculé - Somme Recu)

Position: (8-6)/1 = 2 ((Somme Pondéré calculé - Somme Pondéré recu)/erreur)

Par conséquent, PCB sait que l'erreur est 1 et qu'elle se trouve en position 2. Il va donc soustrait l'erreur à ce qu'il a reçu de PC A.

[0,1-1,2,0,0] => [0,0,2,0,0]

# Limites et amélioration

Cette méthode admet plusieurs limites, tout d'abord il ne faut pas que les données ajoutés ne soient modifié par le bruit et l'ajout de ces données necessite l'envoi d'un fichier plus important. Finalement, la vérification n'est pas précise car elle s'effectue par ligne.

Une amélioration possible de la simulation serait de transformer chaque coefficient de la matrice du bitmap en un tuple correspondant au code couleur du pixel (R, V, B) ainsi le code pourra etre plus precis et vérifier que chaque pixel à la bonne teinte.
