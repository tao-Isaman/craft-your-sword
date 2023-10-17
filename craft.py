import json
import random
import sys
from datetime import datetime

def record_crafted_sword(username, sword_name=None, sword_stats=None):  
    with open("records.txt", "a") as file:
        if sword_name and sword_stats:
            crafted_details = (f"{username} crafted {sword_name} with "
                               f"Strength: {sword_stats['strength']:.2f}, "
                               f"Magic: {sword_stats['magic']:.2f}, "
                               f"Durability: {sword_stats['durability']:.2f}, "
                               f"Soul: {sword_stats['soul']:.2f}\n")
            file.write(crafted_details)
        else:
            file.write(f"{username} attempted to craft a sword but received a broken one.\n")


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
        
        record_crafted_sword(username, crafted_sword, sword_stats)
    else:
        print("\nSorry, your attempt to craft a sword with the provided materials has failed. You received a broken sword.")
        record_crafted_sword(username)


# Dictionary for special messages
RARE_SWORD_MESSAGES = {
    "eclipsed_void_reaver": {
        "message": "The cosmos trembles as the Eclipsed Void Reaver takes form!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/eclipsed_void_reaver.png"
    },
    "lunar_shadowblade": {
        "message": "The night bows in respect; the Lunar Shadowblade is born!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/lunar_shadowblade.png"
    },
    "oceanic_dreadfang": {
        "message": "The very oceans roar in recognition of the Oceanic Dreadfang's creation!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/oceanic_dreadfang.png"
    },
    "draconian_heartseeker": {
        "message": "Dragons of old awaken to herald the forging of the Draconian Heartseeker!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/draconian_heartseeker.png"
    },
    "whispering_voidtalon": {
        "message": "Eerie whispers from the void celebrate the birth of the Whispering Voidtalon!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/whispering_voidtalon.png"
    },
    "ancient_abyssreaver": {
        "message": "Timeless energies converge, marking the arrival of the Ancient Abyssreaver!",
        "image_url": "https://raw.githubusercontent.com/tao-Isaman/craft-your-sword/main/rare_sword_imgs/ancient_abyssreaver.png"
    }
}


if __name__ == '__main__':
    main()
