import json

def generate_md_content_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    md_content = "# Sword Recipes\n\n"

    for sword_name, sword_attributes in data.items():
        md_content += f"## {sword_name}\n"
        md_content += f"- **Materials**: {', '.join(sword_attributes['materials'])}\n"
        md_content += f"- **Success Rate**: {sword_attributes['success_rate']}%\n"
        md_content += f"- **Base Stats**:\n"
        for stat, value in sword_attributes['base_stats'].items():
            md_content += f"  - **{stat.capitalize()}**: {value}\n"
        md_content += "\n"

    return md_content

md_content = generate_md_content_from_json('swords.json')

with open('SWORD_RECIPES.md', 'w') as md_file:
    md_file.write(md_content)
