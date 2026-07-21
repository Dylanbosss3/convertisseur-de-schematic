import json
from litemapy import Schematic, Region
import litemapy
import os
import nbtlib
import matplotlib.pyplot as plt
import numpy as np
import google.genai as genai
import requests
def main():
    
    try:
        with open(r"C:\Users\desou\Desktop\mineconvertion\clée.txt", "r") as fichier:
            ma_cle = fichier.read().strip()
        try:
            client = genai.Client(api_key=ma_cle)
        except Exception as e:
            print(f"Erreur d'initialisation de l'API Gemini : {e}")
    # Gérer l'erreur (ex: quitter le programme)
            #client = None
        fichschema = r"C:\Users\desou\Desktop\mineconvertion\stadevlodrome-soccerstadium9069167.schematic"
        nbt_file = nbtlib.load(fichschema)
        root = nbt_file
        donnees_blocs = listeblock(root)
        name = os.path.basename(fichschema)
        tableconv = request(donnees_blocs, client)
        convert(tableconv, name, root)
        
    except FileNotFoundError:
       print("Fichier introuvable.")
       return
def request(data, client):
    donnees_entree = json.dumps(data, ensure_ascii=False, indent=2)
        
    # 2. Définir le PROMPT JSON strict
    prompt_json = (
        "En tant qu'expert en conversion de schématiques Minecraft, votre tâche est de convertir "
        "la liste suivante d'anciens IDs et Data Values en BlockStates modernes. "
        "Vous DEVEZ répondre UNIQUEMENT avec un tableau JSON Python (une liste de dictionnaires) "
        "et rien d'autre. Chaque objet doit avoir les clés 'id', 'data' et 'blockstate'. "
        "Utilisez 'minecraft:air' pour les IDs inconnus. \n\n"
        "LISTE DES BLOCS À CONVERTIR :\n"
        f"{donnees_entree}"
    )

    try:
        # Appel API...
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_json,
            # Config pour le JSON (peut dépendre de la version de l'API)
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json", 
                response_schema=genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        properties={
                            "id": genai.types.Schema(type=genai.types.Type.INTEGER),
                            "data": genai.types.Schema(type=genai.types.Type.INTEGER),
                            "blockstate": genai.types.Schema(type=genai.types.Type.STRING)
                        }
                    )
                )
            )
        )
        # L'API devrait renvoyer une chaîne JSON valide
        json_text = response.text  # <-- si ton SDK a un autre champ, adapte ici
# 2) convertir texte JSON -> objets Python
        table = json.loads(json_text)
        print(table)
        # resultats_json est maintenant une liste d'objets Python !
        return table
        
    except Exception as e:
        print(f"Erreur d'appel ou d'analyse JSON: {e}")
        return None
def convert(table, name, root):
    width = int(root['Width'])
    height = int(root['Height'])
    length = int(root['Length'])

    blocks = root['Blocks']
    data_bytes = root['Data']

    schem = Schematic(author="dylan")
    ma_region = Region(0, 0, 0, width, height, length)
    schem.regions['name'] = ma_region

    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = (y * length + z) * width + x

                idblock = int(blocks[index]) & 0xFF
                datablock = int(get_data_nibble(data_bytes, index))

                resol = find_item_or_block(idblock, table, datablock)

                if resol is None:
                    identifier = "minecraft:air"
                    properties = {}
                else:
                    identifier, properties = split_blockstate(str(resol["blockstate"]))

                etatblock = litemapy.BlockState(identifier)
                if properties:  # dict non vide
                    etatblock = etatblock.with_properties(**properties)

                ma_region.setblock(x, y, z, etatblock)

    sorti = name.replace(".schematic","") + ".litematic"
    schem.save(sorti)
def find_item_or_block(idblock, table, datablock):
    if table is None:
        raise ValueError("table est None (la conversion/lecture JSON a échoué avant)")
    surv = []
    for block in table:
        if block["id"] == idblock and block["data"] == datablock:
            return block
        else : 
            surv.append(block)

    print(surv)
    return None
def listeblock(root):
    blockU = set()
    ids = root['Blocks']
    data_bytes = root['Data']

    for i in range(len(ids)):
        block_id = int(ids[i]) & 0xFF
        block_data = int(get_data_nibble(data_bytes, i))
        blockU.add((block_id, block_data))

    blocs_json = [{"id": i, "data": d} for i, d in sorted(blockU)]
    return blocs_json
def split_blockstate(blockstate):
     
    if "[" not in blockstate:
        return blockstate, {}
    identifier, props = blockstate[:-1].split("[", 1)
    properties = dict(
        prop.split("=") for prop in props.split(",")
    )
    return identifier, properties
def get_data_nibble(data_bytes, i):
    b = data_bytes[i // 2]
    return (b & 0x0F) if (i % 2 == 0) else ((b >> 4) & 0x0F)


if __name__ == "__main__":
    main()
