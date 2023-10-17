import json

def generate_materials_md_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    md_content = "# Materials Information\n\n"

    for material_name, material_attributes in data.items():
        md_content += f"## {material_name.capitalize()}\n"
        for attribute, value in material_attributes.items():
            md_content += f"- **{attribute.capitalize()}**: {value}\n"
        md_content += "\n"

    return md_content

md_content = generate_materials_md_from_json('materials.json')

with open('MATERIALS.md', 'w') as md_file:
    md_file.write(md_content)
