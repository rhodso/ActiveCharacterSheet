import random

class Helpers:
    parent_stats = {
        "str": "str",
        "athletics": "str",
        "dex": "dex",
        "acrobatics": "dex",
        "sleightOfHand": "dex",
        "stealth": "dex",
        "int": "int",
        "arcana": "int",
        "history": "int",
        "investigation": "int",
        "nature": "int",
        "religion": "int",
        "wis": "wis",
        "animalHandling": "wis",
        "insight": "wis",
        "medicine": "wis",
        "perception": "wis",
        "survival": "wis",
        "cha": "cha",
        "deception": "cha",
        "intimidation": "cha",
        "performance": "cha",
        "persuasion": "cha"        
    }

    base_stats = [
        "str",
        "dex",
        "con",
        "int",
        "wis",
        "cha"
    ]

    class_proficiencies = {
        "artificer": ["con", "int"],
        "barbarian": ["str", "con"],
        "bard": ["dex", "cha"],
        "cleric": ["wis", "cha"],
        "druid": ["int", "wis"],
        "fighter": ["str", "con"],
        "monk": ["str", "dex"],
        "mystic": ["int", "wis"],
        "paladin": ["wis", "cha"],
        "ranger": ["str", "dex"],
        "rogue": ["dex", "int"],
        "sorcerer": ["con", "cha"],
        "warlock": ["wis", "cha"],
        "wizard": ["int", "wis"]
    }

    class_spellcasting_ability = {
        "artificer": "int",
        "barbarian": "",
        "bard": "cha",
        "cleric": "wis",
        "druid": "wis",
        "fighter": "",
        "monk": "",
        "mystic": "int",
        "paladin": "cha",
        "ranger": "wis",
        "rogue": "",
        "sorcerer": "cha",
        "warlock": "cha",
        "wizard": "int"
    }

    class_spellcasting_slot_refresh = {
        "artificer": "LR",
        "barbarian": "",
        "bard": "LR",
        "cleric": "LR",
        "druid": "LR",
        "fighter": "",
        "monk": "",
        "mystic": "SR",
        "paladin": "LR",
        "ranger": "LR",
        "rogue": "",
        "sorcerer": "SR",
        "warlock": "SR",
        "wizard": "LR"
    }
    
    @staticmethod
    def get_spellcasting_ability(chr_class):
        # Check if the class is a string
        if not isinstance(chr_class, str):
            raise ValueError("Invalid class")
        
        # Check if the class is in the class_spellcasting_ability dictionary
        chr_class = chr_class.strip().lower()
        if chr_class not in Helpers.class_spellcasting_ability:
            raise ValueError("Invalid class")
        
        # Return the spellcasting ability
        return Helpers.class_spellcasting_ability[chr_class]

    @staticmethod
    def calculate_modifier(stat):
        # Check if the stat is an integer
        if not isinstance(stat, int):
            try:
                stat = int(stat)
            except ValueError:
                raise ValueError("Invalid stat")

        # Calculate the modifier for a stat
        res = (stat - 10) // 2
        # If the result is negative, return the result
        if res < 0:
            return str(res)
        # Otherwise, return the result with a '+' in front
        else:
            return "+" + str(res)
    
    @staticmethod
    def calculate_save(stat, chr_class):
        # Check if the stat is an int
        if not isinstance(stat, int):
            try:
                stat = int(stat)
            except ValueError:
                raise ValueError("Invalid stat")
        
        # Check if the class is a string
        if not isinstance(chr_class, str):
            raise ValueError("Invalid class")
        
        # Check if the class is in the class_proficiencies dictionary
        chr_class = chr_class.strip().lower()
        if chr_class not in Helpers.class_proficiencies:
            raise ValueError("Invalid class")
        
        # Calculate the modifier for a stat
        res = Helpers.calculate_modifier(stat)

        # Remove the '+' from the modifier, if it exists
        if res[0] == '+':
            res = res[1:]

        try: 
            res = int(res)
        except ValueError:
            raise ValueError("Invalid stat")
        
        # If the class has proficiency in the stat, add the proficiency bonus
        if stat in Helpers.class_proficiencies[chr_class]:
            res += 2

        # If the result is negative, return the result
        if res < 0:
            return str(res)
        # Otherwise, return the result with a '+' in front
        else:
            return "+" + str(res)

    @staticmethod
    def calculate_abchk(stat, character):
        # Ensure that the stat is a string, and is in the parent_stats dictionary
        if not isinstance(stat, str):
            raise ValueError("Invalid stat")
        if stat not in Helpers.parent_stats:
            raise ValueError("Invalid stat")
        
        # If the stat is a base stat, return the modifier
        if stat in Helpers.base_stats:
            return Helpers.calculate_modifier(character[stat])

        # Calculate the abchk for a stat
        # First, look up the stat's parent
        parent = Helpers.parent_stats[stat]

        # Now, look up the parent's value, and get the modifier
        parent_value = character[parent]
        score = Helpers.calculate_modifier(parent_value)

        # Parse the score into an integer
        if score[0] == '+':
            score = score[1:]
        
        try:
            score = int(score)
        except ValueError:
            raise ValueError("Invalid stat")

        # Now look up if we have proficiency in the stat
        if stat in character["abilities"]:
            score += (character["prof"] * character["abilities"][stat])
        
        # If the score is negative, return the score
        if score < 0:
            return str(score)
        # Otherwise, return the score with a '+' in front
        else:
            return "+" + str(score)

    # Helper function for single dice rolls, takes in 2 integers, the number of sides and the modifier
    # Returns the dice roll
    @staticmethod
    def roll_single_dice(num_sides, modifier):
        return random.randint(1, num_sides) + modifier

    # Helper function for multiple dice rolls, takes in 3 integers, the number of dice, the number of sides, and the modifier
    # Returns a list of dice rolls as well as the total of the dice rolls
    @staticmethod
    def roll_multiple_dice(num_dice, num_sides, modifier):
        rolls = []
        for i in range(num_dice):
            rolls.append(random.randint(1, num_sides))
        return rolls, sum(rolls) + modifier
    
    @staticmethod
    def roll_dice_string(dice):
        # First, parse the dice string
        if(dice == ""):
            raise ValueError("Invalid dice string")
        
        if(isinstance(dice, str)):
            try:
                dice = Helpers.parse_dice_string(dice)
            except ValueError:
                raise ValueError("Invalid dice string")

        # If the dice is an integer, return the integer
        if isinstance(dice, int):
            return dice
        
        # If the dice is a list, roll the dice
        if isinstance(dice, list):
            # If there are no dice, return the modifier
            if dice[0] == 0:
                return dice[2]
            # If there are multiple dice, roll multiple dice
            elif dice[0] > 1:
                return Helpers.roll_multiple_dice(dice[0], dice[1], dice[2])
            # If there is only one die, roll a single die
            else:
                return Helpers.roll_single_dice(dice[1], dice[2])
            
        # If the dice is not an integer or a list, or a string, raise an error
        raise ValueError("Invalid dice string")

    @staticmethod
    def parse_dice_string(dice):
        # Pase a string into a dice to roll
        # Format: AdB+C or AdB-C, and C may not exist
        # A = number of dice
        # B = number of sides
        # C = modifier

        a, b, c = 0, 0, 0

        # First, detect if there is a 'd' in the string
        if 'd' not in dice:
            # If there is no 'd', then is the string an integer?
            try:
                # If it's just an integer, then return the integer as the modifier
                roll = [0, 0, int(dice)]
                return roll
            except ValueError:
                raise ValueError("Invalid dice string")
        
        # Is there a '+' or '-' in the string?
        if('+') in dice:
            # If so, split the string into 2 parts
            c = int(dice.split('+')[1])
            # Remove the modifier from the string
            dice = dice.split('+')[0]

        if('-') in dice:
            # If so, split the string into 2 parts
            c = int(dice.split('-')[1]) * -1
            # Remove the modifier from the string
            dice = dice.split('-')[0]

        # Detect that there are characters before the 'd'
        if dice.split('d')[0] != '':
            a = int(dice.split('d')[0])
        else:
            a = 1

        # Detect that there are characters after the 'd'
        if dice.split('d')[1] != '':
            b = int(dice.split('d')[1])
        else:
            raise ValueError("Invalid dice string")
        
        # Return a list that represents the dice to roll
        return [a, b, c]
    
    @staticmethod
    def dice_to_string(roll):
        # Convert a dice roll to a string
        dice_string = ""
        
        # If A is already a string, then just use it
        if isinstance(roll[0], str):
            dice_string += roll[0]
        # Does A exist?
        elif roll[0] > 0:
            dice_string += str(roll[0])
        
        # If B is already a string, then just use it
        if isinstance(roll[1], str):
            dice_string += "d" + roll[1]
        # Does B exist?
        elif roll[1] > 0:
            dice_string += "d" + str(roll[1])

        # If C is already a string, then just use it
        if isinstance(roll[2], str):
            dice_string += roll[2]
        # Does C exist?
        elif roll[2] > 0:
            # Is C positive?
            if roll[2] > 0:
                dice_string += "+"
            dice_string += str(roll[2])
        
        # Return the dice string
        return dice_string
    
    @staticmethod
    def roll_list_to_string(roll_list):
        s = ""
        for r in roll_list:
            s += str(r) + ", "
        s = s[:-2]
        return s

    @staticmethod
    def show_dice_roll_message_string(roll):
        # Show a message box with the result of a dice roll
        # First, convert the roll to a roll if it is not already
        
        # If it's a string
        if isinstance(roll, str):
            roll = Helpers.parse_dice_string(roll)

        # If it's an integer
        elif isinstance(roll, int):
            roll = [1, 1, roll]

        # If it's a list
        elif isinstance(roll, list):
            # If it's a list of integers
            if isinstance(roll[0], int) and isinstance(roll[1], int) and isinstance(roll[2], int):
                pass
            else:
                raise ValueError("Invalid dice string")
        else:
            raise ValueError("Invalid dice string")
        
        # Now, roll the dice
        msg = ""

        # If there's no dice
        if roll[0] == 0:
            msg = "No roll needed, you got a " + str(roll[2]) + "!"

        # If there's only one die
        elif roll[0] == 1:
            res = Helpers.roll_single_dice(roll[1], roll[2])
            nod = res - roll[2]

            # Detect naturals
            nat = 0
            if nod == roll[1]:
                nat = 1
            elif nod == 1:
                nat = -1
            elif res < 1:
                nat = -2

            # Add the result to the message
            if(roll[2] < 0):
                msg += str(nod) + " - " + str(roll[2] * -1) + " = " + str(res)
            else:
                msg += str(nod) + " + " + str(roll[2]) + " = " + str(res)
            if nat == 1:
                msg = "You got a natural " + str(nod) + "!\n(" + msg + ")"
            elif nat == -1:
                msg = "You got a natural 1 :(\n(" + msg + ")"
            elif nat == -2:
                msg = "You somehow rolled lower than a nat 1.\nImpressive, but still considered a nat 1 by most DMs.\n(" + msg + ")"
            else:
                msg = "You rolled a " + str(res) + "!\n(" + msg + ")"
                    
        # If there's multiple dice
        elif roll[0] > 1:
            res = Helpers.roll_multiple_dice(roll[0], roll[1], roll[2])

            # Don't bother with naturals for multiple dice, it's not worth it

            # Get the sum of the rolls
            # TODO: This is a dumb way but it's 4 mins to dnd and I need a hotfix
            roll_sum = 0
            for r in res[0]:
                roll_sum += r

            # Add the result to the message
            msg += "You rolled the following: "
            for i in range(len(res[0])):
                msg += str(res[0][i])
                if i < len(res[0]) - 1:
                    msg += ", "

            msg += "\nWhich is " + str(roll_sum) + " + " + str(roll[2]) + " = " + str(roll_sum + roll[2])

        # Return the message
        return msg

    @staticmethod
    def show_dice_roll_message_component(num_dice, num_sides, modifier):
        # Convert a dice roll to a string
        dice_string = Helpers.dice_to_string([num_dice, num_sides, modifier])

        # Now, use the other method to show the message
        return Helpers.show_dice_roll_message_string(dice_string)


if __name__ == "__main__":
    # Test calculate_modifier method
    stat = 15
    print("Testing calculate_modifier method with stat =", stat)
    print("Output:", Helpers.calculate_modifier(stat))

    # Test calculate_save method
    stat = 16
    chr_class = "barbarian"
    print("Testing calculate_save method with stat =", stat, "and chr_class =", chr_class)
    print("Output:", Helpers.calculate_save(stat, chr_class))

    # Test calculate_abchk method
    stat = "dex"
    character = {
        "acrobatcs": True, 
        "dex": 16, 
        "prof": 2
        }
    print("Testing calculate_abchk method with stat =", stat, "and character =", character)
    print("Output:", Helpers.calculate_abchk(stat, character))

    # Test roll_single_dice method
    num_sides = 6
    modifier = 2
    print("Testing roll_single_dice method with num_sides =", num_sides, "and modifier =", modifier)
    print("Output:", Helpers.roll_single_dice(num_sides, modifier))

    # Test roll_multiple_dice method
    num_dice = 3
    num_sides = 6
    modifier = 2
    print("Testing roll_multiple_dice method with num_dice =", num_dice, "num_sides =", num_sides, "and modifier =", modifier)
    print("Output:", Helpers.roll_multiple_dice(num_dice, num_sides, modifier))

    # Test roll_dice method
    dice = "2d6+3"
    print("Testing roll_dice method with dice =", dice)
    print("Output:", Helpers.roll_dice_string(dice))

    # Test parse_dice_string method
    dice = "2d6+3"
    print("Testing parse_dice_string method with dice =", dice)
    print("Output:", Helpers.parse_dice_string(dice))

    # Test dice_to_string method
    roll = [4, 5, 6]
    print("Testing dice_to_string method with roll =", roll)
    print("Output:", Helpers.dice_to_string(roll))

    print("If you're reading this, then all tests have passed!")
