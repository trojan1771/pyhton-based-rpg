from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create black Magic
fire = Spell(name="Fire", cost=25, dmg=600, type="black")
thunder = Spell(name="Thunder", cost=25, dmg=500, type="black")
blizzard = Spell(name="Blizzard", cost=25, dmg=550, type="black")
meteor = Spell(name="Meteor", cost=40, dmg=1200, type="black")
quake = Spell(name="Quake", cost=35, dmg=900, type="black")

# Create white magic
heal = Spell(name="Heal", cost=25, dmg=600, type="white")
cure = Spell(name="Cure", cost=35, dmg=1500, type="white")

# create Item
potion = Item(name="Potion", type="potion", description="Heals 50 HP", prop=50)
hipotion = Item(name="Hi-Potion", type="potion", description="Heals 100 HP", prop=100)
superpotion = Item(name="Super Potion", type="potion", description="Heals 500 HP", prop=500)
elixer = Item(name="Elixer", type="elixer", description="Fully restores MP/HP of one party member", prop=9999)
hielixer = Item(name="MegaElixer", type="elixer", description="Fully restores party's MP/HP", prop=9999)
grenade = Item(name="Granade", type="attack", description="Deals 500 damage", prop=500)

# Instantiate players
player_spells = [fire, thunder, blizzard, meteor, quake, heal, cure]
enemy_spells = [fire, thunder, blizzard, meteor, heal]
player_items = [{"item": potion, "quantity": 10}
    , {"item": hipotion, "quantity": 5}
    , {"item": superpotion, "quantity": 1}
    , {"item": elixer, "quantity": 1}
    , {"item": grenade, "quantity": 4}]
healer_items = [{"item": potion, "quantity": 15}
    , {"item": hipotion, "quantity": 5}
    , {"item": superpotion, "quantity": 2}
    , {"item": elixer, "quantity": 3}
    , {"item": hielixer, "quantity": 1}]

player1 = Person(name="Yoshi", hp=5234, mp=150, atk=400, df=34, magic=player_spells, items=player_items)
player2 = Person(name="Imoen", hp=3440, mp=350, atk=333, df=34, magic=player_spells, items=healer_items)
player3 = Person(name="Minsc", hp=6460, mp=100, atk=555, df=34, magic=player_spells, items=player_items)

enemy1 = Person(name="Ghost   ", hp=1300, mp=300, atk=530, df=325, magic=enemy_spells, items=[])
enemy2 = Person(name="Beholder", hp=15200, mp=250, atk=650, df=25, magic=enemy_spells, items=[])
enemy3 = Person(name="Imp     ", hp=1200, mp=300, atk=430, df=325, magic=enemy_spells, items=[])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

while running:

    print("============================================================")

    print("\n\n")

    print(bcolors.BOLD + "NAME               HP                                    MP" + bcolors.ENDC)
    alive_players = []
    alive_enemies = []

    for player in players:
        player.get_stats()
        if player.hp > 0:  # Check which player is alive and append to alive players
            alive_players.append(player)

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
        if enemy.hp > 0:  # Check which enemy is alive and append to alive enemies
            alive_enemies.append(enemy)

    # Check Game Status

    if len(alive_enemies) == 0:
        print(bcolors.FAIL + "You won!" + bcolors.ENDC)
        break

    for player in alive_players:  # Start the Game Party turn

        index = player.choose_action()

        if index == 0:
            attack_dmg = player.generate_damage()
            enemy = player.choose_target(alive_enemies)
            enemy.take_damage(dmg=attack_dmg)
            print(bcolors.FAIL + player.name.strip(), "attacked " + enemy.name.strip() + " for", attack_dmg,
                  "points of damage." + bcolors.ENDC)
        elif index == 1:
            magic_choice = player.choose_magic()

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_dmg()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n", player.name.strip(), " don't have enough MagicPoints!" + bcolors.ENDC)
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " restores " + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(alive_enemies)
                enemy.take_damage(dmg=magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemy.name.strip() + bcolors.ENDC)
            player.reduce_mp(spell.cost)
        elif index == 2:
            item_choice = player.choose_item()

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n", player.name.strip(), " have no more " + item.name + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " restores " + str(item.prop) + " HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for m_player in alive_players:
                        m_player.hp = m_player.maxhp
                        m_player.mp = m_player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores party HP/MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores player HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(alive_enemies)
                enemy.take_damage(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " deals " + str(
                    item.prop) + " points of damage to " + enemy.name.strip() + bcolors.ENDC)
        alive_enemies = []
        for enemy in enemies:
            enemy.get_enemy_stats()
            if enemy.get_hp() > 0:
                alive_enemies.append(enemy)

    # Enemies stuff

    if len(alive_players) == 0:
        print(bcolors.OKGREEN + "Enemes have defeated you!" + bcolors.ENDC)
        break

    print("============================================================")
    print(bcolors.FAIL + bcolors.BOLD + "Enemies attacked!" + bcolors.ENDC + bcolors.ENDC)

    for enemy in alive_enemies:  # Start the Game Enemies turn

        enemy_choice = random.randrange(0, 2)
        # enemy.choose_action = random.randrange(0,2)
        player_number = len(alive_players)
        target = random.randrange(0, player_number)
        target_player = enemy.choose_target(targets=alive_players, target_index=target, enemy=1)

        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            target_player.take_damage(dmg=enemy_dmg)
            print(bcolors.FAIL + enemy.name.strip(), "attacked", target_player.name.strip(), "for",
                  str(enemy_dmg),
                  "points of damage." + bcolors.ENDC)
        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "black":
                target_player.take_damage(dmg=magic_dmg)
                print(bcolors.OKBLUE + enemy.name.strip(), "cast", spell.name, "to", target_player.name.strip(), "for",
                      str(magic_dmg), "points of damage." + bcolors.ENDC)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKGREEN + enemy.name.strip(), "cast", spell.name, " and heals for", str(magic_dmg),
                      "HP." + bcolors.ENDC)

        alive_players = []
        for player in players:
            if player.get_hp() > 0:
                alive_players.append(player)