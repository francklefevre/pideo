Voici des consignes que tu dois appliquer systématiquement pour ce projet :
  - Fais en sorte que tout programme envoie toutes ses erreurs dans un fichier dont le nom est le nom du programme suffixé de ".err.txt". Vide ce fichier au démarrage du programme.
  - A chaque fois que je te demande une modification du script, lis ce fichier afin d'analyser les erreurs et de les corriger sans que j'aie à te le demander.
  - Décris toutes les modifications que tu réalises dans un fichier  dont le nom est le nom du programme suffixé de ".history.txt". Mets les modifications les plus récentes en haut, en faisant précéder chaque ligne de la date et de l’heure à laquelle la modification a été réalisée.
  - mets toujours à jour le fichier README.md de façon à ce qu’il contienne l’ensemble de la documentation pour un nouvel utilisateur. Cela doit inclure les procédures d’installation, d’initialisation et d’utilisation, les paramètres utilisés et leurs valeurs par défauts, les formats de fichiers utilisés...
  – mets toutes les littérales et les constantes utiles dans deux fichiers utilisant un format JSON: 
     – param.json : qui contient les paramètres qui ne sont pas confidentiels.
     – secret.json : qui contient les paramètres qui ne sont pas confidentiels.
Chacun de ces fichiers doit avoir une version example dont le nom est préfixé de « .example ».

Tu documentes en anglais le code que tu produis de façon très précise, y compris les fichiers de ressources.

Quand une action du code généré ne rend pas les résultats espérés, instrumente ton code afin d’analyser les raisons de ce dysfonctionnement et de les corriger.  

Quand tu as besoin de valider une hypothèse, lance toute application qui permettra de la valider ou de mieux comprendre. Par exemple un navigateur selenium ou des commandes CURL.
Si tu as besoin qu’un humain effectue une vérification ou te donne une information utile que tu n’a pas trouvée, demande le moi.
Consulte et mets toujours à jour un fichier « AGENTS_METHODS.md » dans lequel tu consignes tout ce qui a pu t’être utile pour réaliser l’application courante. Par exemple, tu vas  y mettre ce que tu as pu apprendre en lisant un site Web ou en accédant à un projet GITHUB. Ce fichier va aussi te servir de contexte de façon à pouvoir travailler directement sur un projet au démarrage de codex sans avoir à faire explicitement référence aux échanges précédents.

Mets en entête de tout fichier source une notice précisant que ce logiciel est un logiciel libre dont l'utilisateur peut faire ce qu'il veut, et qu'il a été développé par Franck LEFEVRE pour la société K1 ( https://k1info.com ), aidé de son équipe de gentils robots.

Tu mets à jour le fichier .gitignore avec les noms de fichiers qui ne doivent pas être remontés dans le repository git.
