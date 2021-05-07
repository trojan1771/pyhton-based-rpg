import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):

        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.maxmagic = magic
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def get_action(self):
        return self.actions

    def get_name(self):
        return self.name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def choose_action(self):
        i = 1
        print("\n   " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.FAIL + bcolors.BOLD + "   ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print("   " + str(i) + ":", item)
            i += 1
        choice = input("   Choose action: ")
        if choice.isnumeric() and len(self.actions) >= int(choice) > 0:
            choice = int(choice) - 1
            return int(choice)
        else:
            return self.choose_action()

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "   MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            if spell.type == "black":
                print("   " + str(i) + ":", spell.name, "(cost:", str(spell.cost) +
                      " MP, deals:", str(spell.dmg), "DMG)")
            elif spell.type == "white":
                print("   " + str(i) + ":", spell.name, "(cost:", str(spell.cost) +
                      " MP, heals:", str(spell.dmg), "HP)")
            i += 1
        choice = input("   Choose Magic: ")
        if choice.isnumeric() and len(self.magic) >= int(choice) > 0:
            choice = int(choice) - 1
            return int(choice)
        else:
            return self.choose_magic()

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "   ITEMS" + bcolors.ENDC)
        for item in self.items:
            if item["item"].type == "attack":
                print("   " + str(i) + ":", item["item"].name, "(" + str(item["item"].description) +
                      " , deals:", str(item["item"].prop), "DMG", "x" + str(item["quantity"]) + ")")
            elif item["item"].type == "potion":
                print("   " + str(i) + ":", item["item"].name, "(" + str(item["item"].description) +
                      " , heals:", str(item["item"].prop), "HP", "x" + str(item["quantity"]) + ")")
            elif item["item"].type == "elixer":
                print("   " + str(i) + ":", item["item"].name,
                      "(" + str(item["item"].description),
                      "x" + str(item["quantity"]) + ")")
            i += 1
        choice = input("   Choose Item: ")
        if choice.isnumeric() and len(self.items) >= int(choice) > 0:
            choice = int(choice) - 1
            return int(choice)
        else:
            return self.choose_item()

    def choose_target(self, targets, target_index=0, enemy=0):
        i = 1
        if enemy == 0:
            print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
            for target in targets:
                print("   " + str(i) + ":", target.name)
                i += 1
            choice = input("   Choose enemy:")
            if choice.isnumeric() and len(targets) >= int(choice) > 0:
                choice = int(choice) - 1
                return targets[choice]
            else:
                return self.choose_target(targets)
        elif enemy == 1:
            choice = target_index
        return targets[choice]

    def get_stats(self):
        hp_bar = ""
        hp_count = (self.hp / self.maxhp) * 100 / 4

        while hp_count > 0:
            hp_bar += "█"
            hp_count -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        # HP different num count fix
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        spaces = ""

        while len(hp_string) < 9:
            spaces += " "
            hp_string = spaces + hp_string
            spaces = ""

        mp_bar = ""
        mp_count = (self.mp / self.maxmp) * 100 / 10

        while mp_count > 0:
            mp_bar += "█"
            mp_count -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        # MP different num count fix
        mp_string = str(self.mp) + "/" + str(self.maxmp)

        while len(mp_string) < 7:
            spaces += " "
            mp_string = spaces + mp_string
            spaces = ""
        # Fix with format
        # "{:>3}".format(str(self.mp)) + "/" + "{:>3}".format(str(self.maxhp))

        print("                  _________________________             __________")
        print(
            bcolors.BOLD + self.name + "   " + hp_string + "|" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + bcolors.BOLD
            + "|    " + mp_string + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC)

    def get_enemy_stats(self):
        hp_bar = ""
        hp_count = (self.hp / self.maxhp) * 100 / 2

        while hp_count > 0:
            hp_bar += "█"
            hp_count -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        # HP different num count fix
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        spaces = ""

        while len(hp_string) < 11:
            spaces += " "
            hp_string = spaces + hp_string
            spaces = ""

        print("                       __________________________________________________")
        print(
            bcolors.BOLD + self.name + "   " + hp_string + "|" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|" + bcolors.ENDC)

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_spell_dmg()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or (spell.type == "white" and int(pct) > 50):
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg