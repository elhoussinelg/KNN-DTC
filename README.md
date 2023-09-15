# Cloud Resource Allocation Using Machine Learning
Une application d'allocation de ressources utilisant une technique d'apprentissage automatique assistée par le cloud computing implémentée en Python

## 1. ***Introduction***
Une application que j'ai créée sur la base de l'article suivant : "A Machine Learning Framework for Resource Allocation Assisted by Cloud Computing" qui introduit un cadre pour effectuer l'allocation des ressources à l'aide de techniques d'apprentissage automatique et aider le Cloud Computing à faire le travail (pour plus de détails se référer au papier). Veuillez noter que cette application est une implémentation à petite échelle du papier de base.

L'image suivante illustre le système géographique sur le réseau.

<p align="center">
  <img style="display:block;margin-left: auto; margin-right: auto; width:50 %" width="500px" src="figure 1.png">
</p>

Chaque section de l'application documentée ci-dessous :    


## 2. ***Données***
#### 2.1 Description
Comme le système utilise l'apprentissage automatique pour allouer les ressources appropriées, nous avons besoin de données. Mais trouver des données préparées et propres pour faire une telle chose à petite échelle n'est pas très possible (sauf si vous utilisez les données fournies par AWS ou Google sur des centres de données massifs). J'ai donc créé mes propres données. Le module Data Creator (module Seeder dans /Cloud/storage) utilise un modèle prédéfini (/Cloud/storage/data/seeder_data_template.csv) pour créer des données. description des attributs, classes, valeurs et ... sont dans le fichier /Cloud/storage/data/data_description.txt.

#### 2.2 Process
Tout d'abord, le module seeder lit le fichier seeder_data_template.csv et crée une donnée basée sur celui-ci dans le fichier /Cloud/storage/data/dat.csv. Les attributs, les classes et les valeurs sont manipulables mais nécessitent également un codage.

#### 2.3 Execution
Pour exécuter le seeder et créer les données, exécutez python3 Cloud/seeder.py. remplacez le '/' par '\' si vous utilisez un système non basé sur Unix. la commande génère le fichier data.csv
## 3. ***Cloud Module***

#### 3.1 Description
Le module Cloud est responsable du stockage des données brutes, du prétraitement des données, de la gestion des entrepôts, de l'apprentissage basé sur les données et de la création d'un modèle ML basé sur celles-ci et enfin de l'envoi du modèle aux bords. Nous pouvons le considérer comme le cerveau de notre système.
#### 3.2 Process
Les données sont stockées dans son système de stockage et ici, nous effectuons tout le processus d'apprentissage dans le module cloud.py (dans Cloud/Storage/cloud.py, Not a Python Class). le code est entièrement commenté au format Docstring, il n'y a donc pas besoin de description détaillée mais d'un aperçu. le module lit les données, les divise à 70 % pour la formation et à 30 % pour les tests, forme son modèle à l'aide de la technique de classification d'arbre de décision, teste son modèle et le conserve dans le système de stockage. La technique de classification est choisie à l'aide de la technique de validation croisée qui a montré que l'arbre de décision peut classer les données avec une précision de 85 %, ce qui est un bon nombre pour l'allocation des ressources. d'autres techniques comme KNN avaient une précision d'environ 65% sur nos données

#### 3.3 Execution
Le module cloud est exécutable à l'aide python3 Cloud/cloud.pyde la commande. il sort un modèle au format joblib sur notre stockage.

## 4. ***Cloudlet***

#### 4.1 Description
Les cloudlets ne sont que des tâches, un nom choisi par le framework Cloudsim. Les tâches sont générées sur différents domaines (dans notre application, nous avons 3 positions différentes).

Les attributs, les valeurs et les classes sont listés ci-dessous. les données brutes créées sont toutes en nombres catégorisés ou continus, mais nous les prétraitons en valeurs catégorisées, par exemple une tâche avec 120 mi est considérée comme une tâche avec une instruction de haut niveau (plus de 100). les seuils sont calculés à l'aide d'un processus de test et d'essai. les valeurs de chaque tâche sont générées aléatoirement.
***Ce que nous devons faire, c'est trouver le meilleur travailleur pour chaque tâche***
<table>
  <tr>
    <th>
      Attributes
    </th>
    <th>
      Position
    </th>
    <th>
      Instructions (million instructions)
    </th>
    <th>
      Size (MB)
    </th>
    <th>
      High Priority
    </th>
    <th>
      Allocated Worker (Class)
    </th>
  </tr>
  <tr>
    <th rowspan=3>
      values
    </th>
    <th>
      area 1
    </th>
    <th>
      High (1 to 100)
    </th>
    <th>
      High (1 to 10)
    </th>
    <th>
      True
    </th>
    <th>
      Worker in Area 1
    </th>
  </tr>
  <tr>
    <th>
      area 2
    </th>
    <th>
      Low (101 to 300)
    </th>
    <th>
      Low (11 to 30)
    </th>
    <th>
      False
    </th>
    <th>
      Worker in Area 2
    </th>
  </tr>
  <tr>
    <th>
      area 3
    </th>
    <th>
    </th>
    <th>
    </th>
    <th>
    </th>
    <th>
      Worker in area 3
    </th>
  </tr>
  <tr>
    <th>
      Type
    </th>
    <th>
      Categorized
    </th>
    <th>
      Continues
    </th>
    <th>
      Continues
    </th>
    <th>
      Categorized
    </th>
    <th>
      Categorized
    </th>
  </tr>
</table>

#### 4.2 Process
Cloudlet est une classe générée dans les bords, je l'ai donc placée dans Edges/Cloudlet.py. la création d'un objet de la classe initialise ses attributs. Le code est entièrement commenté.
## 5. ***Worker Node***

#### 5.1 Description
Le travailleur est nos ressources, des machines qui font le travail. tous les travailleurs héritent de la classe Mother Worker (fichier Edges/workers/worker.py) qui possède toutes les fonctionnalités et tous les attributs. chaque travailleur peut remplacer ces propriétés par ses propres moyens. ma demande a 3 travailleurs. chaque travailleur a des attributs :

<ul>
  <li>
    Position: position du serveur worker
  </li>
  <li>
    Power: Puissance du serveur worker en millions d'instructions par seconde
  </li>
  <li>
    Bandwidth: bande passante entre le serveur Worker et les autres Workers en Mo/s
  </li>
  <li>
    Makespan (timer): le temps que le travailleur a consommé pour faire les travaux en secondes
  </li>
</ul>

#### 5.2 process
Worker est une classe, donc créer une classe avec un nom facultatif et hériter de la classe Worker créerait un serveur worker.
## 6. ***Master Node***

#### 6.1 Description
Si nous appelons le module Cloud le cerveau de notre système, le nœud maître du système en est le cœur. Il est chargé d'obtenir des informations sur chaque Cloudlet et de trouver le meilleur Worker pour celui-ci en utilisant le modèle formé dans le stockage cloud. par exemple, le Web a une tâche, les métadonnées de la tâche sont envoyées au nœud maître, il choisit le meilleur travailleur en tenant compte de tous les attributs de Cloudlet et des travailleurs, puis en attachant le cloudlet au travailleur. Le travailleur obtient ensuite le Cloudlet via le réseau et fait le travail. Dans cette application, j'ai implémenté une  ***greedy approach*** pour comparer les fonctionnalités et les performances du modèle ML avec celui-ci. l'algorithme Greedy considère la taille et les instructions de la tâche et non sa priorité.

#### 6.2 execution
Master Class se déclare et fait le job. commande suivante : python3 Edges/Master.pyferait tout et imprime les sorties.

## ***Conclusion***

J'ai choisi des valeurs pour les attributs dans les Cloudlets et les travailleurs utilisant Test et Essai. mon but était que le Worker 3 ait plus de puissance que le Worker 2 et le Worker 2 que le 3. mais la bande passante entre 1 et 3 est très faible, entre 1 et 2 est élevée et entre 2 et 3 est la plus élevée. L'exécution du processus d'allocation des ressources à l'aide de l'application a donné les résultats suivants en moyenne sur 40 heures d'exécution :

Utilisation de la technique d'apprentissage automatique :
<ul>
    <li>
      Worker 1 Makespan:  221.5 s
    </li>
    <li>
      Worker 2 Makespan:  569 s
    </li>
    <li>
      Worker 3 Makespan:  982.5 s
    </li>
</ul>
Utilisation Greedy Algorithm
<ul>
    <li>
      Worker 1 Makespan:  322.2 s
    </li>
    <li>
      Worker 2 Makespan:  248.4 s
    </li>
    <li>
      Worker 3 Makespan:  1050.5 s
    </li>
</ul>

Ce qui montre que le modèle ML fait un meilleur travail en répartissant les tâches sur les travailleurs et en réduisant l'envergure globale. Comme vous pouvez le voir, l'algorithme Greedy envoie la plupart des tâches au travailleur 3. mais ML équilibre les charges comme nous le voulions. bien que les données aient été générées mais un être humain, le résultat doit être ce que nous. Dans l'application du monde réel, le processus de formation du mode n'est pas unique et peut même être effectué à intervalles afin qu'il puisse trouver la meilleure façon d'allouer les ressources.
# KNN-DTC
