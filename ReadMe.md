# Fichier 'worker_results.py'

## Exécution du fichier
Exécuter le fichier worker_results.py permet de récupérer toutes les informations des moteurs de recherche pour les requêtes des différents domains (dictionnaire 'Domains' dans le fichier conf.py)
Des informations sont récupérées automatiquement sur SNIDE, si celles-ci ne sont pas complètes, le moteur de recherche s'affiche dans le navigateur avec une fenêtre tkinter. Il faut remplir les informations de la page web dans la fenêtre tkinter et enregistrer ces informations.

Pour certains moteurs de recherche, les positions des liens collectés automatiquement sur SNIDE et ceux visibles lorsque nous faisons une recherche sur le navigateur peuvent être différentes. Cela peut donc nous amener à enregistrer deux fois le même lien pour un moteur de recherche.
Nous pouvons donc choisir 'only_manual= True or False' pour remplir les informations. Si on choisit True, aucune information ne sera récupérer automatiquement sur SNIDE et il faudra toutes les rentrer à la main.

## Enregistrement des informations
Lorsqu'il y a des informations manquantes pour un moteur de recherche, la page du moteur de recherche s'affiche avec la requête correspondante et il faut copier coller les liens des pages dans le tableau. 
Pour certains moteurs de recherche, les positions des liens collectés automatiquement sur SNIDE et ceux visibles lorsque nous faisons une recherche sur le navigateur peuvent être différentes. Cela peut donc nous amener à enregistrer deux fois le même lien pour un moteur de recherche.  
Il n'est pas nécessaire de remplir les titres des pages car ils ne sont pas utilisés dans le traitement des données.

## Problème de collecte des données
Lors de l'enregistrement des informations manquantes avec la fenêtre Tkinter, si celle-ci est fermée, une fenêtre s'affiche et le fichier arrête son exécution pour le domaine concerné.

Il peut aussi y avoir un problème pour récupérer les données automatiquement sur SNIDE avec le certificat SSL du serveur. 
Si besoin le certificat est dans le fichier 'snide-inria-fr-chain.pem'

## Nombre de pages
Vous pouvez choisir le nombre de pages qu'un moteur de recherche affiche en modifiant la variable 'nb_pages' du fichier conf.py
A noter que SNIDE référence au maximum 10 pages par moteur de recherche. Donc tout lien supplémentaire devra être rajouté manuellement.

## Mise à jour des classements et scores
Une fois que les informations des différentes requêtes d'un domaine sont complètes, les nouveaux scores des pages web, moteurs de recherche et classements sont mis à jour avec la méthode 'update'.

## Sauvegarde des données
Les informations sont enregistrées sous forme de dictionnaire dans un fichier json grâce à la méthode 'save_results' dans le dossier 'SNIDE Results'.  
Ils portent le nom : 'Campaign_results_domain.json'. Ils seront ensuite réutilisés pour faire les tests statistiques.

## Enregistremement de nouvelles informations
Si vous voulez enregistrer des informations pour de nouveaux domaines avec des nouvelles requêtes, il faut modifier le dictionnaire 'Domains' du fichier 'conf.py'.

# Fichier 'worker_test.py'

## Exécution du fichier
Exécuter le fichier worker_results.py permet d'effectuer des tests statistiques sur les données enregistrées grâce à 'worker_results.py'.
La classe 'TestsDomain' va faire des tests statistiques pour un domaine, alors que la classe 'TestsDomains' va faire des statistiques en comparant les résultats des différents domaines.

## Choix de alpha
Alpha correspond au niveau avec lequel les tests sont réalisés. Les valeurs de alpha doivent être prises dans la liste [.30, .20, .10, .05, .02, .01, .005] en raison des valeurs enregistrées pour le test de dixon.

## Fichiers json pour exploiter les tests statistiques
L'exécution du fichier 'main.py' va créer un fichier 'campaign_results_domain.json' pour pouvoir faire ensuite les tests statistiques avec. Si vous avez déjà les fichiers json, vous n'avez pas besoin d'exécuter le programme du fichier 'worker_results.py', vous pouvez donc commenter la ligne où l'on fait appel à la classe DomainResults.   
Pour pouvoir exécuter le code de la classe TestsDomains, il faut que tous les fichiers json associés au clé du dictionnaire Domains aient été calculés.

## Ajouter un nouveau test
Pour ajouter un nouveau test, il faut ajouter le test dans la classe TestsDomain ou TestDomains. Si le test à ajouter compare les différentes domaines entre eux, il faut l'ajouter dans la classe TestDomains. Sinon, il faut l'ajouter dans la classe TestDomain.  
Il faut enregistrer les résultats du test dans le dictionnaire 'self.results_test'.  
Il faut ensuite mettre à jour le dictionnaire 'self.execution' en rajoutant ( 'nouveau_test' : self.nouveau_test() ).  
Il faut également mettre à jour le dictionnaire 'grouped_tests_domains(s)' (du fichier 'tests_tools.py'). Si les résultats du nouveau test sont de même "nature" que certains tests déjà présents et qu'il est judicieux de faire apparaître les tests sur un même tableau, vous pouvez ajouter le nouveau test dans une liste avec d'autres tests.
Il faut ensuite modifier la méthode 'save_results()' de la classe TestDomain ou TestDomains pour faire apparaître les résultats du test dans le fichier.  
Vous pouvez ensuite afficher une documentation du test en modifiant le dictionnaire 'documentation_tests_domain(s)' du fichier 'tests_tools.py'.

## Affichage des résultats
Pour afficher les résultats il faut exécuter le fichier. Les résultats apparaissent sous forme de fichier texte au format 'tests_domain_alpha.txt' dans dossier 'Tests Results'.

## Métriques utilisées pour les tests
Pour effectuer les tests, nous avons utilisé 3 métriques : 'bias', 'Mosh', 'score'.

'bias' correspond à la métrique ou l'on attribue un poids différent aux pages suivant leur position (CTR). Le score 'bias' d'une page correspond à la formule (2) du papier 'comparison', c'est la visibilité moyenne de la page sur tous les moteurs de recherche.
Le score 'bias' d'un moteur de recherche correspond à la formule (1) du papier 'comparison'.

'Mosh' correspond à la métrique ou l'on attribue le score de 1 si le moteur de recherche montre la page et 0 sinon. De la même façon, nous pouvons définir un score pour chaque moteur de recherche avec la formule (1) du papier.

'score' correspond aux scores des moteurs de recherche obtenus avec la formule (3) avec le CTR.

## Tests réalisés

### dtest0
C'est un test de dixon qui prend en entrée un vecteur de biais pour les métriques 'bias' et 'Mosh'. Les biais ont été calculé avec t=1, soit une seule requête. Nous avons utilisé 2 métriques 'bias' qui correspond au score CTR, 'Mosh' qui correspond au score binaire.
Puis pour 'Dixon tests score' nous avons pris en entrée le vecteur des scores des moteurs de recherche avec les poids du CTR.

### dtest0bis
C'est un test de dixon qui prend en entrée un vecteur de biais. Les biais ont été calculé avec plusieurs requêtes comme le veut la formule (1). Nous avons utilisé seulement 2 métriques pour le calcul du biais: 'bias' et 'Mosh', la métrique 

### dtest1
C'est un test de dixon qui prend en entrée le vecteur des scores des différents moteurs de recherche. Il permet de détecter si un moteur de recherche a un score anormal pour une certaine requête.  
Idée 2.3.3.1 du papier 'comparison'.

### dtest2
C'est un test de dixon qui prend en entrée un vecteur dont l'élément associé à un moteur de recherche correspond au poids de la page la plus populaire pour ce moteur de recherche. La page la plus populaire est celle provenant du classement 'consensus'. Il permet de tester si un moteur de recherche donne peu de visibilité à une page populaire auprès des autres moteurs de recherche.  
Idée 2.3.3.2 du papier 'comparison'.

### dtest3
Permet de tester si la page la plus populaire pour un moteur de recherche est elle aussi bien référencée par les autres moteurs de recherche.  
Idée 2.3.3.3 du papier 'comparison'.

### dtest4
A chaque moteur de recherche, on lui associe le score de la page qu'il place en première positio. Cela permet de tester si un moteur de recherche donne beaucoup de visibilité à une page qui n'est pas jugée pertinente par les autres moteurs de recherche.  
Idée 2.3.3.4 du papier 'comparison'.

### ANOVA1test1
Test ANOVA qui teste si les requêtes pour un domaine donné ont le même biais. Ici la formule du biais utilisée est celle pour t=1 compte tenu que l'on compare les différentes requêtes pour un même domaine.  
Idée 2.1.3 (2ème point) du papier 'comparison'.

### ANOVA1test2
Test ANOVA qui teste si les moteurs de recherche ont le même biais pour un sous-domaine donné. Encore une fois, les biais utilisés sont calculés pour t=1.  
Idée 2.1.3 (2ème point) du papier 'comparison'.

### ANOVA1test3
Test ANOVA qui test si pour un moteur de recherche, celui-ci biaise ses résultats suivant le domaine des requêtes.  
Idée 2.1.3 (1er point) du papier 'comparison'.

### ANOVA2test1
Test ANOVA qui permet de tester si les scores des moteurs de recherche peuvent être expliqués de manière significative par le moteur de recherche ou le domaine.  
Idée 2.1.3 (3ème point) du papier 'comparison'.


# Fichier 'main.py'

## Exécution du fichier
L'exécution du fichier va automatiquement récolter les informations sur SNIDE, compléter celles manquantes avec le fichier 'worker_results.py' et faire les tests statistiques du fichier 'worker_tests.py'.