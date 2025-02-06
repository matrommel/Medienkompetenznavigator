import json
import os
from collections import defaultdict

def transform_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prüfen, ob die suggestions_data Liste leer ist
    if not data['suggestions_data']['collection']['items']:
        return None

    # Sortieren der suggestions_data Liste nach dem thema
    sorted_suggestions = sorted(data['suggestions_data']['collection']['items'], key=lambda x: x['data'][3]['value'])

    focalpoint_dict = defaultdict(list)

    for suggestion in sorted_suggestions:
        lernziele = []
        lerninhalt = []
        materialien = {"mebis_kurs": "Keine Unterrichtsmaterialien vorhanden"}
        kompetenzen = []
        lernaktivitaeten = []
        focalpoint_name = ""

        for d in suggestion['data']:
            if d['name'] == 'suggestion_learninggoals':
                lernziele.append(d['value'])
            elif d['name'] == 'suggestion_topics':
                lerninhalt = d['value'].split('\n')
            elif d['name'] == 'materials_array' and d['value']:
                materialien['mebis_kurs'] = d['value'][0]['link']
            elif d['name'] == 'competences_array':
                for comp in d['value']:
                    kompetenzen.append(f"{comp['competence_number']}.{comp['sectioncompetence_number']} {comp['sectioncompetence_title']}")
            elif d['name'] == 'lessonactivities_array':
                for act in d['value']:
                    lernaktivitaeten.append(act['title'])
            elif d['name'] == 'focalpoints_array' and d['value']:
                focalpoint_name = d['value'][0]['focalpoint_name']

        lern_situation = {
            "id": suggestion['data'][0]['value'],
            "thema": suggestion['data'][3]['value'],
            "lernziele": lernziele,
            "vorschlagslink": suggestion['href'],
            "lerninhalt": lerninhalt,
            "materialien": materialien,
            "fach": "Fachübergreifend (FÜ)",
            "schuljahr": 11,
            "kompetenzen": kompetenzen,
            "lernaktivitaeten": lernaktivitaeten
        }

        focalpoint_dict[focalpoint_name].append(lern_situation)

    return {
        "Fächer": [{"Bezeichnung": k, "lernsituation": v} for k, v in focalpoint_dict.items()]
    }

def process_all_files(input_folder):
    all_data = defaultdict(lambda: defaultdict(list))

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.json'):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(input_file, input_folder)
                folder_name = os.path.dirname(relative_path)
                file_name = os.path.basename(relative_path)

                transformed_data = transform_data(input_file)
                if transformed_data:
                    all_data[folder_name][file_name].append(transformed_data)

    structured_data = []
    for folder_name, files in all_data.items():
        folder_data = {
            "Beruf": folder_name,
            "Jahrgang": []
        }
        for file_name, data in sorted(files.items()):
            sorted_faecher = sorted(data[0]["Fächer"], key=lambda x: x["Bezeichnung"])
            folder_data["Jahrgang"].append({
                "Abschnitt": file_name,
                "Fächer": sorted_faecher
            })
        structured_data.append(folder_data)

    # Sortieren der strukturierten Daten nach Beruf
    structured_data.sort(key=lambda x: x["Beruf"])

    return structured_data

if __name__ == "__main__":
    input_folder = 'export'
    output_folder = 'transform'
    os.makedirs(output_folder, exist_ok=True)

    all_transformed_data = process_all_files(input_folder)

    output_file = os.path.join(output_folder, 'all_transformed_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_transformed_data, f, ensure_ascii=False, indent=4)

    print(f"Transformation abgeschlossen und Datei gespeichert unter: {output_file}")