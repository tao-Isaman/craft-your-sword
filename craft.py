import json
import random
import sys

def load_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def get_pr_content(username):
    pr_filepath = f"craft_recipes/{username}.json"
    return load_data(pr_filepath)

def calculate_final_stats(sword_attributes, provided_materials, materials_data):
    base_stats = sword_attributes['base_stats']
    total_strength = base_stats['strength']
    total_magic = base_stats['magic']
    total_durability = base_stats['durability']
    total_soul = base_stats['soul']

    for material in provided_materials:
        if material not in materials_data:
            # If the material is not recognized, return None indicating a failed crafting
            return None
        
        random_multiplier = random.uniform(0.2, 1.0)
        total_strength += materials_data[material]['strength'] * random_multiplier
        total_magic += materials_data[material]['magic'] * random_multiplier
        total_durability += materials_data[material]['durability'] * random_multiplier
        total_soul += materials_data[material]['soul'] * random_multiplier

    return {
        "strength": total_strength,
        "magic": total_magic,
        "durability": total_durability,
        "soul": total_soul
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python blacksmith_bot.py <username>")
        exit()

    username = sys.argv[1]
    materials_data = load_data("materials.json")
    swords_data = load_data("swords.json")
    pr_content = get_pr_content(username)

    crafted_sword = None
    sword_stats = None

    for sword, attributes in swords_data.items():
        if all(material in pr_content['chosen_materials'] for material in attributes['materials']):
            sword_stats = calculate_final_stats(attributes, pr_content['chosen_materials'], materials_data)
            if sword_stats is not None:
                if random.randint(1, 100) <= attributes['success_rate']:
                    crafted_sword = sword
                    break

    if crafted_sword and sword_stats:
        print(f"\nSuccess! You've crafted the {crafted_sword}!")
        print(f"Strength: {sword_stats['strength']:.2f}")
        print(f"Magic: {sword_stats['magic']:.2f}")
        print(f"Durability: {sword_stats['durability']:.2f}")
        print(f"Soul: {sword_stats['soul']:.2f}")

        special_message = RARE_SWORD_MESSAGES.get(crafted_sword)
        if special_message:
            print(f"\n{special_message}\n")
    else:
        print("\nSorry, your attempt to craft a sword with the provided materials has failed. You received a broken sword.")

# Dictionary for special messages
RARE_SWORD_MESSAGES = {
    "eclipsed_void_reaver": "The cosmos trembles as the Eclipsed Void Reaver takes form!",
    "lunar_shadowblade": "The night bows in respect; the Lunar Shadowblade is born!",
    "oceanic_dreadfang": "The very oceans roar in recognition of the Oceanic Dreadfang's creation!",
    "draconian_heartseeker": "Dragons of old awaken to herald the forging of the Draconian Heartseeker!",
    "whispering_voidtalon": "Eerie whispers from the void celebrate the birth of the Whispering Voidtalon!",
    "ancient_abyssreaver": "Timeless energies converge, marking the arrival of the Ancient Abyssreaver!"
}

if __name__ == '__main__':
    main()
