import pygame
import random
import time
# Define window dimensions
WINDOW_WIDTH = 800


WINDOW_HEIGHT = 800

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define the list of weapons with their initial durability, attack strengths, and decay rates
weapons = [
    {"name": "Sword", "durability": 100, "attack": 12, "decay": 1.0},
    {"name": "Axe", "durability": 100, "attack": 18, "decay": 1.7},
    {"name": "Bow", "durability": 100, "attack": 8, "decay": 0.75},
    # Add more weapons here...
]

# Define armor for the warrior and the ghost
warrior_armor = 50
ghost_armor = 75

# Define initial HP for the ghost and warrior
ghost_hp = 100
warrior_hp = 100


# Generate a random value for max_successful_attacks
max_successful_attacks = random.randint(3, 6)

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game Inventory")

# Load warrior and ghost images and resize them
warrior_image = pygame.image.load("warrior.png")
warrior_image = pygame.transform.scale(warrior_image, (150, 200))
ghost_image = pygame.image.load("ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (150, 200))

# Define fonts
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 16)

# Variable to track the equipped weapon
equipped_weapon = None

# Variables for break/stagger mechanic
successful_attacks = 0
max_successful_attacks = random.randint(3, 6)

# Variable to track the warrior's staggered state
warrior_staggered = False

# Initialize message
message = ""

def draw_window():
    window.fill(WHITE)

    # Calculate the warrior elements' positions
    warrior_elements_x = 50
    warrior_elements_y = (WINDOW_HEIGHT - warrior_image.get_height()) // 2 - 120

    # Draw warrior HP label
    warrior_hp_label = small_font.render("Warrior HP:", True, BLACK)
    warrior_hp_label_pos = (warrior_elements_x + (warrior_image.get_width() - warrior_hp_label.get_width()) // 2, warrior_elements_y)
    window.blit(warrior_hp_label, warrior_hp_label_pos)

    # Draw warrior HP bar
    warrior_hp_bar_width = warrior_hp * 2
    warrior_hp_bar_pos = (warrior_elements_x + (warrior_image.get_width() - warrior_hp_bar_width) // 2, warrior_elements_y + 20)
    pygame.draw.rect(window, BLUE, (*warrior_hp_bar_pos, warrior_hp_bar_width, 10))

    # Draw warrior armor label
    warrior_armor_label = small_font.render("Warrior Armor:", True, BLACK)
    warrior_armor_label_pos = (warrior_elements_x + (warrior_image.get_width() - warrior_armor_label.get_width()) // 2, warrior_elements_y + 60)
    window.blit(warrior_armor_label, warrior_armor_label_pos)

    # Draw warrior armor bar
    warrior_armor_bar_width = warrior_armor * 2
    warrior_armor_bar_pos = (warrior_elements_x + (warrior_image.get_width() - warrior_armor_bar_width) // 2, warrior_elements_y + 80)
    pygame.draw.rect(window, BLUE, (*warrior_armor_bar_pos, warrior_armor_bar_width, 10))

    # Draw warrior image
    window.blit(warrior_image, (warrior_elements_x, warrior_elements_y + 120))

    # Calculate the boss elements' positions
    boss_elements_x = WINDOW_WIDTH - ghost_image.get_width() - 50
    boss_elements_y = (WINDOW_HEIGHT - ghost_image.get_height()) // 2 - 120

    # Draw boss HP label
    boss_hp_label = small_font.render("Boss HP:", True, BLACK)
    boss_hp_label_pos = (boss_elements_x + (ghost_image.get_width() - boss_hp_label.get_width()) // 2, boss_elements_y)
    window.blit(boss_hp_label, boss_hp_label_pos)

    # Draw boss HP bar
    boss_hp_bar_width = ghost_hp * 2
    boss_hp_bar_pos = (boss_elements_x + (ghost_image.get_width() - boss_hp_bar_width) // 2, boss_elements_y + 20)
    pygame.draw.rect(window, BLUE, (*boss_hp_bar_pos, boss_hp_bar_width, 10))

    # Draw boss durability label
    boss_durability_label = small_font.render("Boss Armor:", True, BLACK)
    boss_durability_label_pos = (boss_elements_x + (ghost_image.get_width() - boss_durability_label.get_width()) // 2, boss_elements_y + 60)
    window.blit(boss_durability_label, boss_durability_label_pos)

    # Calculate boss durability bar width
    ghost_armor_bar_width = ghost_armor * 2

    # Draw boss durability bar
    boss_durability_bar_pos = (boss_elements_x + (ghost_image.get_width() - ghost_armor_bar_width) // 2, boss_elements_y + 80)
    pygame.draw.rect(window, BLUE, (*boss_durability_bar_pos, ghost_armor_bar_width, 10))

    # Draw ghost image
    window.blit(ghost_image, (boss_elements_x, boss_elements_y + 120))

    # Calculate the warrior HP bar position
    warrior_hp_bar_pos = (warrior_elements_x + (warrior_image.get_width() - warrior_hp_bar_width) // 2, warrior_elements_y + 20)

    # Draw warrior HP bar
    pygame.draw.rect(window, BLUE, (*warrior_hp_bar_pos, warrior_hp_bar_width, 10))

    # Draw warrior image
    window.blit(warrior_image, (warrior_elements_x, warrior_elements_y + 120))

    # Draw weapon and armor information
    for i, weapon in enumerate(weapons):
        if weapon == equipped_weapon:
            weapon_text = f"{weapon['name']}: {weapon['durability']:.1f}% (Equipped)"
        else:
            weapon_text = f"{weapon['name']}: {weapon['durability']:.1f}%"
        weapon_surface = font.render(weapon_text, True, BLACK)
        window.blit(weapon_surface, (10, 10 + i * 30))

    # Draw buttons
    attack_button = font.render("Attack", True, BLACK)
    window.blit(attack_button, (10, WINDOW_HEIGHT - 80))
    defend_button = font.render("Defend", True, BLACK)
    window.blit(defend_button, (10, WINDOW_HEIGHT - 40))

    # Draw messages
    message_surface = font.render(message, True, BLACK)
    window.blit(message_surface, (10, WINDOW_HEIGHT - 120))

    pygame.display.update()



def decrease_durability():
    global message, ghost_armor, successful_attacks, ghost_hp

    if equipped_weapon:
        equipped_weapon["durability"] -= equipped_weapon["decay"]
        if equipped_weapon["durability"] <= 85:
            message = "Weapon durability is low. Consider changing your weapon."

        # Calculate damage to the ghost if it has armor
        if ghost_armor > 0:
            damage_to_armor = min(equipped_weapon["attack"], ghost_armor)
            damage_to_hp = equipped_weapon["attack"] - damage_to_armor
            ghost_armor -= damage_to_armor
            ghost_armor = max(0, ghost_armor)
            if damage_to_hp > 0:
                ghost_hp = max(0, ghost_hp - damage_to_hp)
                successful_attacks += 1
                message = f"You dealt {damage_to_hp} damage to the ghost!"
            else:
                message = "The ghost's armor absorbed the attack."
        else:
            ghost_hp = max(0, ghost_hp - equipped_weapon["attack"])
            successful_attacks += 1
            message = f"You dealt {equipped_weapon['attack']} damage to the ghost."

        # Check if ghost armor needs to be restored
        if successful_attacks >= max_successful_attacks:
            ghost_armor = 100
            successful_attacks = 0
            message = "The ghost's armor has been restored!"


def get_weapon_index(x, y):
    weapon_index = (y - 10) // 30
    if weapon_index >= 0 and weapon_index < len(weapons):
        return weapon_index
    return None

# Initialize last ghost attack time
last_ghost_attack_time = time.time()

# Game loop
running = True
last_armor_damage_time = time.time()  # Initialize the variable to track the time since warrior's armor was last damaged
last_ghost_attack_time = time.time()  # Initialize the variable to track the time of the last ghost attack
weapon_selected = False
MAX_ARMOR = 100 # Variable to track if a weapon is selected
# Variable to track the boss's defense state
boss_defending = False
attack_button_clicked = True
attack_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 80, 90, 30)



while running:
    for event in pygame.event.get():
        # Check for quit event
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pos = pygame.mouse.get_pos()
            if attack_button_rect.collidepoint(mouse_pos):
                if equipped_weapon is None:
                    message = "Please select a weapon."
                else:
                    decrease_durability()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if attack_button_rect.collidepoint(mouse_pos):
                    if warrior_armor > 0:
                        # Perform the attack action
                        warrior_attack()
                    else:
                        # Display a message or perform some other action to indicate the warrior cannot attack without armor
                        print("Cannot attack without armor!")

            # Check if a weapon is selected
            if not weapon_selected:
                weapon_index = get_weapon_index(mouse_x, mouse_y)
                if weapon_index is not None:
                    equipped_weapon = weapons[weapon_index]
                    weapon_selected = True
                    message = f"{equipped_weapon['name']} equipped."
                    continue

            # Check if the attack button is clicked
            if 10 <= mouse_x <= 100 and WINDOW_HEIGHT - 80 <= mouse_y <= WINDOW_HEIGHT - 50 and equipped_weapon:
                if warrior_armor > 0:  # Check if warrior armor is greater than 0
                    decrease_durability()
                else:
                    message = "The warrior cannot attack without armor."
                continue

            # Check if the defend button is clicked
            if 10 <= mouse_x <= 100 and WINDOW_HEIGHT - 40 <= mouse_y <= WINDOW_HEIGHT - 10:
                if warrior_armor < MAX_ARMOR:
                    warrior_armor += 10
                    message = "The warrior defended and regained armor."
                else:
                    message = "The warrior's armor is already at maximum."

    # ... (existing code omitted for brevity)


    # Check if it's time for the ghost to attack
    current_time = time.time()
    if current_time - last_ghost_attack_time >= random.randint(2, 5):
        if warrior_armor > 0 and not warrior_staggered:
            # Ghost attacks only if its armor is greater than 0
            if ghost_armor > 0:
                ghost_attack = random.randint(10, 20)  # Randomly determine the ghost's attack damage
                damage_to_armor = min(ghost_attack, warrior_armor)
                damage_to_hp = ghost_attack - damage_to_armor
                warrior_armor -= damage_to_armor
                warrior_armor = max(0, warrior_armor)
                if damage_to_hp > 0:
                    warrior_hp = max(0, warrior_hp - damage_to_hp)
                    message = f"The ghost dealt {damage_to_hp} damage to the warrior!"
                else:
                    message = "The warrior's armor absorbed the attack."
                last_armor_damage_time = current_time  # Update the time of the last armor damage
            else:
                # Ghost has no armor, unable to attack
                message = "The ghost is unable to attack without armor."

    # Update the time of the last ghost attack
        last_ghost_attack_time = current_time
        # Check if it's time for armor regeneration
        if current_time - last_armor_damage_time >= 10:  # Adjust the time interval as needed
            # Increase the warrior's armor gradually
                warrior_armor += 5  # Adjust the amount of armor regenerated as needed
                warrior_armor = min(warrior_armor, MAX_ARMOR)  # Limit the armor value to a maximum
                last_armor_damage_time = current_time  # Reset the time since last armor damage


        # Boss defending logic
        if not boss_defending:
            if warrior_armor > 0:
                ghost_attack = random.randint(10, 20)  # Randomly determine the ghost's attack damage
                if random.random() < 0.5:  # 50% chance of the boss defending
                    ghost_attack //= 2  # Reduce the attack damage when the boss is defending
                    boss_defending = True  # Set the boss defending state
                    message = "The boss is defending!"
                damage_to_armor = min(ghost_attack, warrior_armor)
                damage_to_hp = ghost_attack - damage_to_armor
                warrior_armor -= damage_to_armor
                warrior_armor = max(0, warrior_armor)
                if damage_to_hp > 0:
                    warrior_hp = max(0, warrior_hp - damage_to_hp)
                    message = f"The ghost dealt {damage_to_hp} damage to the warrior!"
                else:
                    message = "The warrior's armor absorbed the attack."
                last_armor_damage_time = current_time  # Update the time of the last armor damage
                if warrior_armor == 0:
                    warrior_staggered = True  # Set the warrior to staggered state
                    message = "The warrior is staggered and unable to attack."

        # Boss defending cooldown logic
    if boss_defending:
        if current_time - last_ghost_attack_time >= 3:  # Adjust the cooldown duration as needed
            boss_defending = False  # Reset the boss defending state
            last_ghost_attack_time = current_time

    # Check if the ghost's HP is 0
    if ghost_hp <= 0:
        message = "The ghost has been defeated! Game over."
        running = False
    # Draw buttons
    if warrior_staggered:
        # Warrior is staggered, disable the attack button
        pygame.draw.rect(window, RED, (10, WINDOW_HEIGHT - 80, 90, 30))
    else:
        attack_button = font.render("Attack", True, BLACK)
        window.blit(attack_button, (10, WINDOW_HEIGHT - 80))




    draw_window()

# End of the game
print("Game over.")
pygame.quit()
