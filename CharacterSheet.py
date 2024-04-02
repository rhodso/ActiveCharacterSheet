import json

class CharacterSheet:
    @staticmethod
    def read_json(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{file_path}' not found.") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from file '{file_path}': {e}") from e

    @staticmethod
    def write_json(file_path, data):
        if data is None:
            raise ValueError("No data to write.")
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error encoding JSON data: {e}") from e

    @staticmethod
    def update_json(file_path, data):
        # Load the existing data
        existing_data = CharacterSheet.read_json(file_path)
        
        # Update the existing data with the new data
        for key, value in data.items():
            # Automatically determine if the value is a number
            if isinstance(value, str):
                # Determine if the value is a number but drop the plus sign if there is one
                if value[0] == '+':
                    value = value[1:]
                if value.isnumeric():
                    value = int(value)
            
            existing_data[key] = value

        # Write the updated data to the file
        CharacterSheet.write_json(file_path, existing_data)

class Weapon:
    id_tracker = 0

    def __init__(self, name="", attributes="", ability="", damage_type="", is_proficient=False, range="", damage="", hit_bonus=0):
        self.id = Weapon.id_tracker
        self.name = name
        self.attributes = attributes
        self.ability = ability
        self.damage_type = damage_type
        self.is_proficient = is_proficient
        self.range = range
        self.damage = damage
        self.hit_bonus = hit_bonus

        Weapon.id_tracker += 1

class Spell:
    id_tracker = 0

    def __init__(self, level=0, name="", save="", cast_time="", range="", damage="", duration="", description="", ritual=False, concentration=False):
        self.id = Spell.id_tracker
        self.level = level
        self.name = name
        self.save = save
        self.cast_time = cast_time
        self.range = range
        self.damage = damage
        self.duration = duration
        self.description = description
        self.ritual = ritual
        self.concentration = concentration

        Spell.id_tracker += 1

class Tracker:
    id_tracker = 0

    def __init__(self, name="", value=0, max_value=0, refresh=""):
        self.id = Tracker.id_tracker
        self.name = name
        self.value = value
        self.max_value = max_value
        self.refresh = refresh

        Tracker.id_tracker += 1

if __name__ == "__main__":
    # Example usage:
    file_path = 'test_sheet.json'
    try:
        # Example of reading JSON from file
        read_data = CharacterSheet.read_json('test_sheet.json')
        if read_data:
            print("Read JSON data:")
            print(read_data)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
