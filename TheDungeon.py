import sys
import os
import random

#to edit
random_statements = [
    "Beware! Trolls are lurking in the shadows.",
    "You hear a mysterious noise echoing through the maze.",
    "The air is thick with tension as you explore The Dungeon.",
    "A distant howl sends shivers down your spine.",
    "The path ahead seems treacherous. Proceed with caution."
]

def main():
    print("#################################")
    print("##   Welcome to The Dungeon!   ##")
    print("##   What do you want to do?   ##")
    print("##        1 -> Play            ##")
    print("##        2 -> Help            ##")
    print("##       3 -> Credits          ##")
    print("##        4 -> Quit            ##")
    print("#################################")
    option = input("--> ")
    if option == "1":
        start()
    elif option == "2":
        help()
    elif option == "3":
        credits()
    elif option == "4":
        sys.exit()
    else:
        main()

def start():
    global playername
    print("# Hi there, adventurer! What do you want us to call you? #")
    option = input("--> ")
    playername = option
    if playername == (''):
        print("Invalid username. Try another one.")
        start()
    else:
        start1()

def start1():
    print(f"""Hello there, {playername}. Let this be a warning to you. 

The Dungeon is a place of mystery at the same time a place for discovery. 
It is a place that needs a lot of wits and grits. It is a place that you don’t want to be stuck in. 
As you go along, navigate and analyze the maze carefully to reach the boss and to avoid dead ends. 
Beat the trolls to gain energy. And lastly, courageously face The Boss.

Your only goal is to escape, but the question is: 
Can you overcome the challenges and escape The Dungeon? 

Good luck and may the odds be in your favor. """)
    print("Do you want to continue?")
    print("1 -> Yes")
    print("2 -> No")
    option = input("--> ")
    if option == "1":
        print_random_statement()
        RPGMap(10,10)
    elif option == "2":
        sys.exit()
    else:
        main()

def help():
    print("""I suppose you need assistance, adventurer. In order to navigate the game
    the following buttons are to be chosen:
    W -> move up
    A -> move left
    S -> move down
    D -> move right""")
    print("#################################")
    print("##   What do you want to do?   ##")
    print("##        1 -> Play            ##")
    print("##       2 -> Credits          ##")
    print("##        3 -> Quit            ##")
    print("#################################")
    option = input("--> ")
    if option == "1":
        start()
    elif option == "2":
        credits()
    elif option == "3":
        sys.exit()
    else:
        main()

def credits():
    print("""Hello there! Thank you for visiting our simple game
The Dungeon was built by five aspiring programmers: 
             Aal-anubia, Sunday
             Carbonell, Isabel
              Manangan, Angel
             Olantes, Charlene
              Velasquez, Fiona
    With the supervision and guidance of: 
             Mr. Jerry Pacalso
We hope you enjoyed The Dungeon. 'Til next time, adventurer!
             All rights reserved
                   2023""")
    print("#################################")
    print("##   What do you want to do?   ##")
    print("##        1 -> Play            ##")
    print("##        2 -> Help            ##")
    print("##        3 -> Quit            ##")
    print("#################################")
    option = input("--> ")
    if option == "1":
        start()
    elif option == "2":
        help()
    elif option == "3":
        sys.exit()
    else:
        main()

class RPGMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.enemy_x = -1
        self.enemy_y = -1

    def print_map(self):
        print("P = Player")
        print("E = Enemy")
        print("B = Boss")
        for row in self.map_grid:
            print(' '.join(row))

    def place_obstacles(self, num_obstacles, exclude_coords):
        for _ in range(num_obstacles):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Ensure obstacles do not block specific coordinates
            while (x, y) in exclude_coords:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            self.map_grid[y][x] = 'X'
            exclude_coords.append((x, y))

    def generate_random_map(self, num_rooms):
        for _ in range(num_rooms):
            room_width = random.randint(3, 8)
            room_height = random.randint(3, 6)
            x = random.randint(0, self.width - room_width)
            y = random.randint(0, self.height - room_height)

            for i in range(room_height):
                for j in range(room_width):
                    self.map_grid[y + i][x + j] = '.'

            if random.random() < 0.5:
                corridor_length = random.randint(2, 6)
                if random.random() < 0.5:
                    corridor_x = x + room_width
                    corridor_y = random.randint(y, y + room_height - 1)
                    for k in range(corridor_length):
                        self.map_grid[corridor_y][corridor_x + k] = '.'
                else:
                    corridor_x = random.randint(x, x + room_width - 1)
                    corridor_y = y + room_height
                    for k in range(corridor_length):
                        self.map_grid[corridor_y + k][corridor_x] = '.'

    def generate_maze(self, start_x, start_y, num_enemies, num_obstacles):
        stack = [(start_x, start_y)]
        visited = set()

        while stack:
            current_x, current_y = stack[-1]
            visited.add((current_x, current_y))

            neighbors = [
                (current_x + 2, current_y),
                (current_x - 2, current_y),
                (current_x, current_y + 2),
                (current_x, current_y - 2),
            ]

            unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited]

            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                wall_x = (current_x + next_x) // 2
                wall_y = (current_y + next_y) // 2

                self.map_grid[wall_y][wall_x] = '.'
                stack.append((next_x, next_y))
            else:
                stack.pop()

        for i in range(self.width):
            self.map_grid[0][i] = 'X'
            self.map_grid[self.height - 1][i] = 'X'
        for i in range(1, self.height - 1):
            self.map_grid[i][0] = 'X'
            self.map_grid[i][self.width - 1] = 'X'

        # Place obstacles inside the maze (excluding the player's starting position and path to the boss)
        exclude_coords = [(start_x, start_y)]
        for i in range(start_x, self.width - 1):
            exclude_coords.append((i, start_y))
        for j in range(start_y, self.height - 1):
            exclude_coords.append((self.width - 1, j))

        self.place_obstacles(num_obstacles, exclude_coords)

        self.enemies = []
        for _ in range(num_enemies):
            enemy_x = random.randint(1, self.width - 2)
            enemy_y = random.randint(1, self.height - 2)
            self.enemies.append((enemy_x, enemy_y))
            self.map_grid[enemy_y][enemy_x] = 'E'

        for i in range(self.width):
            # Place the boss at the lower rightmost part of the maze
            boss_x = self.width - 2
            boss_y = self.height - 2
            self.map_grid[boss_y][boss_x] = 'B'

        # You can store the boss coordinates for later reference if needed
        self.boss_coordinates = (boss_x, boss_y)

class Player:
    def __init__(self, x, y, max_health=100):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.current_health = max_health
        self.weapons = {
            'Sword': {'damage': 15},
            'Bow': {'damage': 10, 'range': 2},
        }
        self.current_weapon = 'Sword'
        self.exp = 0
        self.exp_to_next_level = 30
        self.level = 1
        self.health_regeneration_rate = 35  # Adjust as needed

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def choose_weapon(self):
        print("Available Weapons:")
        for weapon in self.weapons:
            print(f"{weapon} - Damage: {self.weapons[weapon]['damage']}")
        weapon_choice = input("Choose a weapon: ").capitalize()

        # Use case-insensitive comparison for weapon choice
        weapon_names_upper = [name.upper() for name in self.weapons.keys()]

        if weapon_choice.upper() in weapon_names_upper:
            # Convert the weapon choice to the actual case in the weapons dictionary
            actual_weapon_choice = next(name for name in self.weapons.keys() if name.upper() == weapon_choice.upper())
            self.current_weapon = actual_weapon_choice
            print(f"You selected {self.current_weapon}.")
        else:
            print("Invalid weapon. Using default weapon (Sword).")

    def battle_enemy(self, enemy_coordinates):
        enemy_health = 50
        print(f"You encountered an enemy at {enemy_coordinates}!")

        while True:
            print(f"Your Health: {self.current_health}% | Enemy Health: {enemy_health}%")
            print(f"Current Weapon: {self.current_weapon}")

            battle_action = input("Enter 'A' to attack, 'C' to change weapon, or 'R' to run: ").upper()
            if battle_action == 'A':
                # Calculate damage dealt and received
                player_damage = random.randint(self.weapons[self.current_weapon]['damage'] - 5,
                                               self.weapons[self.current_weapon]['damage'] + 5)
                enemy_damage = random.randint(5, 15)

                print(f"You attacked the enemy with {self.current_weapon} and dealt {player_damage} damage!")
                print(f"The enemy attacked you and dealt {enemy_damage} damage!")

                # Update health
                self.current_health -= enemy_damage
                enemy_health -= player_damage

                # Check for battle outcome
                if self.current_health <= 0:
                    print("You were defeated in battle. Game over.")
                    sys.exit()
                elif enemy_health <= 0:
                    print("You defeated the enemy!")

                    exp_gained = random.randint(10, 20)
                    print(f"You gained {exp_gained} EXP!")

                    self.exp += exp_gained
                    print(f"Total EXP: {self.exp} | Level: {self.level}")

                    self.check_level_up()

                    rpg_map.map_grid[player.y][player.x] = 'P'
                    rpg_map.print_map()
                    rpg_map.enemies.remove(enemy_coordinates)
                    rpg_map.map_grid[enemy_coordinates[1]][enemy_coordinates[0]] = ' '
                    break

            elif battle_action == 'C':
                self.choose_weapon()

            elif battle_action == 'R':
                print("You ran away from the enemy.")
                break

    def check_level_up(self):
        while self.exp >= self.level * 30:
            self.level += 1
            self.exp -= self.level * 30
            print(f"Level Up! You are now level {self.level}.")

        previous_health = self.current_health
        self.max_health = 100 + (self.level - 1) * 10
        self.current_health = min(self.current_health + self.health_regeneration_rate, self.max_health)

        # Calculate the amount of health regenerated
        health_regenerated = self.current_health - previous_health

        # Print a statement when the player's health is increased
        if health_regenerated > 0:
            print(f"Your health increased by {health_regenerated} to {self.current_health}!")
    
    def battle_boss(self, boss_coordinates):
        boss_health = 100
        print("You are facing the Boss!")

        # Increase weapon damage when facing the boss
        for weapon in self.weapons:
            self.weapons[weapon]['damage'] += 15  # You can adjust the damage increase as needed

        while True:
            print(f"Your Health: {self.current_health}% | Boss Health: {boss_health}%")
            print(f"Current Weapon: {self.current_weapon} - Damage: {self.weapons[self.current_weapon]['damage']}")

            battle_action = input("Enter 'A' to attack, 'C' to change weapon, or 'R' to run: ").upper()
            if battle_action == 'A':
                # Calculate damage dealt and received
                player_damage = random.randint(self.weapons[self.current_weapon]['damage'] - 5,
                                               self.weapons[self.current_weapon]['damage'] + 5)
                boss_damage = random.randint(10, 20)

                print(f"You attacked the Boss with {self.current_weapon} and dealt {player_damage} damage!")
                print(f"The Boss attacked you and dealt {boss_damage} damage!")

                # Update health
                self.current_health -= boss_damage
                boss_health -= player_damage

                # Check for battle outcome
                if self.current_health <= 0:
                    print("You were defeated by the Boss. Game over.")
                    sys.exit()
                elif boss_health <= 0:
                    print("Congratulations! You defeated the Boss and completed the game!")
                    sys.exit()

            elif battle_action == 'C':
                self.choose_weapon()

            elif battle_action == 'R':
                print("You cannot run away from the Boss! Prepare for battle.")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_random_statement():
    random_statement = random.choice(random_statements)
    print(random_statement)

main()
rpg_map = RPGMap(30, 20)
rpg_map.generate_maze(1, 1, 5, 120)
rpg_map.generate_random_map(0)

player = Player(1, 1, 100)

while True:
    rpg_map.map_grid[player.y][player.x] = 'P'
    rpg_map.print_map()

    # Set the previous player position to an empty space
    rpg_map.map_grid[player.y][player.x] = ' '

    # Update the player's position
    if (player.x, player.y) in rpg_map.enemies:
        enemy_coordinates = (player.x, player.y)
        player.battle_enemy(enemy_coordinates)

     # Check if there is only one enemy left
        if len(rpg_map.enemies) == 1:
            print("You're almost there, " + playername + "! Keep going!")

     # Check if the enemy is still present after the battle
        if enemy_coordinates in rpg_map.enemies:
            rpg_map.map_grid[enemy_coordinates[1]][enemy_coordinates[0]] = 'E'
    elif (player.x, player.y) == rpg_map.boss_coordinates:
        if player.level >= 2 and player.current_health >= 50:
            print("You encountered the Boss!")
            player.battle_boss(rpg_map.boss_coordinates)

            # Check if the boss is still present after the battle
            if rpg_map.boss_coordinates in rpg_map.enemies:
                rpg_map.map_grid[rpg_map.boss_coordinates[1]][rpg_map.boss_coordinates[0]] = 'B'
            else:
                print("Congratulations! You defeated the Boss and completed the game!") #to edit
                sys.exit()
        else:
            print("You need to be at least level 2 and have a health of at least 50 to face the Boss!")
            
    action = input("Enter direction (W/A/S/D to move, Q to quit): ").upper()

    if action == 'Q':
        break
    elif action == 'W':
        if player.y > 0 and rpg_map.map_grid[player.y - 1][player.x] != 'X':
            player.move(0, -1)
        else:
            print("You hit a wall!", flush=True)
    elif action == 'A':
        if player.x > 0 and rpg_map.map_grid[player.y][player.x - 1] != 'X':
            player.move(-1, 0)
        else:
            print("You hit a wall!", flush=True)
    elif action == 'S':
        if player.y < rpg_map.height - 1 and rpg_map.map_grid[player.y + 1][player.x] != 'X':
            player.move(0, 1)
        else:
            print("You hit a wall!", flush=True)
    elif action == 'D':
        if player.x < rpg_map.width - 1 and rpg_map.map_grid[player.y][player.x + 1] != 'X':
            player.move(1, 0)
        else:
            print("You hit a wall!", flush=True)

    # Print the updated map with the new player position
    rpg_map.map_grid[player.y][player.x] = 'P'
    rpg_map.print_map()