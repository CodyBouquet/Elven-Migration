import json
from stats import calculate_stats
from ui import display_status, display_dialogue, print_header
from market import supply_market
from game_logic import select_elders, daily_turn, check_victory


# ═══════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {filename} not found!")
        exit()


ITEMS = load_json('items.json')
ELDERS = load_json('elders.json')
EVENTS = load_json('events.json')
DIALOGUE = load_json('dialogue.json')


# ═══════════════════════════════════════════════════════
# GAME INITIALIZATION
# ═══════════════════════════════════════════════════════

def new_game():
    """Create new game state"""
    return {
        'day': 1,
        'current_location': 'cursed_forest',
        'destination_landmark': 'Silverwood Vale',
        'distance_to_next_landmark': 1600,
        'total_distance_traveled': 0,
        
        'elders': [],
        'total_followers': 0,
        'max_followers': 0,
        
        'resources': {
            'food': 0,
            'mana': 0,
            'gold': 500,
            'medicine': 0,
            'arrows': 0,
        },
        
        'special_items': [],
        'days_without_food': 0,
        'game_over': False,
    }


# ═══════════════════════════════════════════════════════
# MAIN GAME LOOP
# ═══════════════════════════════════════════════════════

def main():
    """Main game"""
    
    # Show intro
    display_dialogue(DIALOGUE, 'intro')
    input("\nPress ENTER to begin...")
    
    # Create new game
    game = new_game()
    
    # Select elders
    select_elders(game, ELDERS)
    
    # Shopping phase
    print("\n" + "═"*60)
    print("PREPARATION PHASE")
    print("═"*60)
    print(f"\nYou have {game['resources']['gold']} gold to purchase supplies.")
    print("The journey is 1600 leagues. Choose wisely.")
    input("\nPress ENTER to visit the market...")
    
    stats = calculate_stats(game, ITEMS, ELDERS)
    supply_market(game, ITEMS, stats)
    
    # Show final loadout
    print("\n" + "═"*60)
    print("FINAL LOADOUT")
    print("═"*60)
    print(f"💰 Gold: {game['resources']['gold']}")
    print(f"🍖 Food: {game['resources']['food']}")
    print(f"⚕️ Medicine: {game['resources']['medicine']}")
    print(f"🏹 Arrows: {game['resources']['arrows']}")
    print(f"✨ Mana: {game['resources']['mana']}")
    print("═"*60)
    
    input("\nPress ENTER to begin the exodus...")
    
    # Main game loop
    while not game['game_over']:
        stats = calculate_stats(game, ITEMS, ELDERS)
        display_status(game, stats)
        
        # Check if reached destination
        if check_victory(game):
            break
        
        # Daily turn
        daily_turn(game, stats, EVENTS)
        
        input("\n[Press ENTER for next day]")
    
    # Game over
    print("\n" + "═"*60)
    print("GAME OVER")
    print("═"*60)
    print(f"Days survived: {game['day']}")
    print(f"Distance traveled: {game['total_distance_traveled']} leagues")
    print(f"Followers remaining: {game['total_followers']}/{game['max_followers']}")
    print("═"*60)


if __name__ == "__main__":
    main()