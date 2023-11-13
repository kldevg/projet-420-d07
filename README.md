
# Lisez-moi

Ceci est une application AWS CDK (Cloud Development Kit) avec Python

## Environnement virtuel

Ce projet est configuré comme un projet Python standard. Le processus d'initialisation crée également un environnement virtuel au sein du projet, stocké dans le répertoire `.venv`. Pour cérer l'nvironnement virtuel, cela suppose qu'il y a un exécutable `python3` (ou `python` pour Windows) dans votre path avec un accès à la librairie `venv`. Si pour une raison quelconque la création automatique du virtualenv échoue,
vous pouvez créer le virtualenv manuellement.

Pour créer manuellement un virtualenv sur MacOS et Linux :

```
$ python3 -m venv .venv
```

Une fois le processus d'initialisation terminé et le virtualenv créé, vous pouvez utiliser ce qui suit pour activer votre virtualenv.

```
$ source .venv/bin/activate
```

Sur Windows, l'activation du virtualenv se fait comme ceci :

```
% .venv\Scripts\activate.bat
```

Une fois le virtualenv activé, vous pouvez installer les dépendances requises (et éventuellement les dépendances de développement).

```
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

Pour ajouter des dépendances supplémentaires, par exemple d'autres bibliothèques CDK, ajoutez les simplement dans `requirements.txt` et reexécuter la commande `pip install -r requirements.txt`.

## Authentification dans AWS

Avant de lancer les commandes `cdk`, il faudra générer une clé d'accès pour avoir des identifiants de sécurité que l'application utilisera. Vous pouvez utiliser AWS Management Console pour gérer les clés d'accès d'un utilisateur IAM (voir https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
Une fois obtenue, stocker ensuite le ID et le Secret de cette clé d'accès dans un fichier `~/.aws/credentials` (ou `C:\Users\username\.aws\credentials` pour Windows) comme suit :

```
[default]
aws_access_key_id = {ID de la clé, ex. AKIAIOSFODNN7EXAMPLE}
aws_secret_access_key = {secret de la clé, ex. wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY}
```

## Configuration du compte

Une configuration du compte ainsi que de la région AWS par défaut doit être faite en modifiant les variables d'environnement dédiées, se trouvant dans le fichier `.env`, comme suit :

```
CDK_DEFAULT_ACCOUNT = {ID du compte, ex. 123456789012}
CDK_DEFAULT_REGION = {code de région, ex. us-east-1}
```

## Exécution

Le fichier `cdk.json` indique au CDK Toolkit comment exécuter l'application.

À ce stade, vous pouvez désormais synthétiser le template CloudFormation pour ce code, puis lancer le bootstrap et le déploiement vers AWS :

```
$ cdk synth
$ cdk bootstrap
$ cdk deploy
```

## Commandes utiles

 * `cdk ls`          liste toutes les stacks (piles) dans l'application
 * `cdk synth`       émet le template (modèle) CloudFormation synthétisé
 * `cdk deploy`      déploie cette stack sur le compte/région AWS par défaut
 * `cdk diff`        compare la stack déployée avec l'état actuel
 * `cdk docs`        ouvre la documentation du CDK

Pour accéder à la documentation mise à jour de AWS CDK, voici le lien : https://docs.aws.amazon.com/cdk/v2/guide/home.html
