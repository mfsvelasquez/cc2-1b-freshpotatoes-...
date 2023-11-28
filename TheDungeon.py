import sys
import os
import random

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
        for row in self.map_grid:
            print(' '.join(row))

    def place_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.map_grid[y][x] = 'X'

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

        self.enemies = []
        for _ in range(num_enemies):
            enemy_x = random.randint(1, self.width - 2)
            enemy_y = random.randint(1, self.height - 2)
            self.enemies.append((enemy_x, enemy_y))
            self.map_grid[enemy_y][enemy_x] = 'E'

        for _ in range(num_obstacles):
            obstacle_x = random.randint(1, self.width - 2)
            obstacle_y = random.randint(1, self.height - 2)
            while (obstacle_x, obstacle_y) in self.enemies:  # Ensure obstacles don't overlap with enemies
                obstacle_x = random.randint(1, self.width - 2)
                obstacle_y = random.randint(1, self.height - 2)
            self.map_grid[obstacle_y][obstacle_x] = 'X'

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

main()
rpg_map = RPGMap(20, 10)
rpg_map.generate_maze(1, 1, 5, 35)
rpg_map.generate_random_map(0)
rpg_map.place_obstacles(10)


player = Player(1, 1)

while True:
    rpg_map.map_grid[player.y][player.x] = 'P'
    rpg_map.print_map()

    if (player.x, player.y) in rpg_map.enemies:
        print("You encountered an enemy!")

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

    rpg_map.map_grid[player.y][player.x] = ' '

