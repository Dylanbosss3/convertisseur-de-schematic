📦 Convertisseur de Schématiques Minecraft (.schematic ➔ .litematic) via IA Gemini

Un outil d'automatisation Python permettant de convertir automatiquement les anciens fichiers de construction Minecraft (.schematic) vers le format moderne Litematica (.litematic).

Ce projet s'appuie sur l'API Google Gemini avec contrainte de schéma JSON strict pour effectuer un mapping intelligent entre les anciens identifiants numériques (ID & Data values) et les BlockStates modernes de Minecraft (ex: minecraft:oak_stairs[facing=east]).

🌟 Fonctionnalités

🔍 Parsing NBT Binaire : Décodage bas niveau des fichiers NBT .schematic (extraction des blocs et décodage bit-à-bit des nibbles pour les Data Values).

🤖 Mapping Intelligent par IA : Utilisation du modèle gemini-2.5-flash pour faire correspondre de manière contextuelle les anciens IDs Minecraft avec les BlockStates modernes.

🛡️ Validation de Schéma Strict : Utilisation de GenerateContentConfig avec schéma JSON forcé pour garantir une réponse structurée et sans erreur de parsing.

🏗️ Génération Litematica : Reconstruction de la structure tridimensionnelle et exportation au format .litematic via la bibliothèque litemapy.

🛠️ Prérequis & Technologies

Python 3.10+

Bibliothèques Python :

google-genai (SDK officiel Google Gemini)

litemapy (Manipulation des fichiers Litematica)

nbtlib (Lecture/Écriture des fichiers NBT)

🚀 Installation & Configuration

1. Cloner le projet & installer les dépendances

git clone https://github.com/votre-pseudo/mineconvertion.git
cd mineconvertion
pip install google-genai litemapy nbtlib


2. Clé API Gemini

Obtenez une clé d'API sur Google AI Studio.

Créez un fichier clée.txt dans le dossier du projet (ou adaptez le chemin dans le code) et collez-y uniquement votre clé API.

💻 Utilisation

Placez votre fichier .schematic à convertir dans votre dossier de travail.

Mettez à jour le chemin du fichier dans la fonction main() du script :

fichschema = r"chemin/vers/votre_fichier.schematic"


Exécutez le script :

python main.py


Le fichier .litematic converti sera généré dans le même répertoire.

📂 Architecture du Code

| Fonction | Description |
| --- | --- |
| `main()` | Point d'entrée : charge la clé API, lit le fichier `.schematic`, orchestre l'appel IA et lance la conversion. |
| `listeblock()` | Extrait la liste unique des paires `(ID, Data)` présentes dans le fichier NBT. |
| `request()` | Envoie la liste des blocs à l'API Gemini et récupère la table de conversion au format JSON structuré. |
| `convert()` | Parcourt la grille 3D du monde et reconstruit la région au format Litematica. |
| `split_blockstate()` | Sépare le nom du bloc et ses propriétés (ex: `minecraft:chest[facing=north]`). |
| `get_data_nibble()` | Extrait le nibble (4 bits) correspondant à l'index de bloc dans le tableau NBT. |

👤 Auteur

Dylan — Développeur Software & Administrateur Système Linux

GitHub : @votre-pseudo

Services Freelance : Développement Python / Java / C# & Administration Infrastructure Linux.