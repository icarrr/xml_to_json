#!/usr/bin/env python3
import xmltodict
import json
import argparse
import sys

def convert_xml_to_json(source_path, target_path):
    try:
        # Membaca file XML
        with open(source_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()

        # Mengonversi XML menjadi dictionary
        xml_dict = xmltodict.parse(xml_content, dict_constructor=dict)

        # Mengambil elemen problem
        problem_data = xml_dict.get("problem", {})

        # Menyiapkan array untuk setiap blok soal
        problems = []

        # Memproses setiap elemen dalam problem_data
        for p, response in zip(problem_data['p'], problem_data['multiplechoiceresponse']):
            problem_block = {
                "problem": p,
                "type": response["choicegroup"]["@type"],
                "multiplechoiceresponse": {
                    "choicegroup": {
                        "choice": response["choicegroup"]["choice"]
                    }
                }
            }
            problems.append(problem_block)

        # Menyimpan JSON ke file
        with open(target_path, 'w', encoding='utf-8') as json_file:
            json.dump(problems, json_file, indent=4)

        print(f'File JSON berhasil disimpan di: {target_path}')
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert XML to JSON")
    parser.add_argument("--source", required=True, help="Path to the source XML file")
    parser.add_argument("--target", required=True, help="Path to the output JSON file")
    args = parser.parse_args()

    convert_xml_to_json(args.source, args.target)

if __name__ == "__main__":
    main()
