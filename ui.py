def print_header(text):
    """Print a header"""
    print("\n" + "═"*60)
    print(text.center(60))
    print("═"*60)


def print_section(text):
    """Print a section divider"""
    print("\n" + "─"*60)
    print(text)
    print("─"*60)


def display_status(game, stats):
    """Show current status"""
    print_header(f"DAY {game['day']}")
    print(f"📍 Destination: {game['destination_landmark']}")
    print(f"📏 Distance: {game['distance_to_next_landmark']} leagues")
    print(f"\n👥 Followers: {game['total_followers']}/{game['max_followers']}")
    print(f"🍖 Food: {game['resources']['food']} | 💰 Gold: {game['resources']['gold']}")
    
    # Show active bonuses
    bonuses = []
    if stats['travel_speed'] > 20:
        bonuses.append(f"⚡+{int(stats['travel_speed']-20)} speed")
    if stats['luck'] > 0:
        bonuses.append(f"🍀+{int(stats['luck']*100)}% luck")
    
    if bonuses:
        print(f"\n✨ Active: {' | '.join(bonuses)}")


def display_dialogue(dialogue_data, key):
    """Display dialogue from JSON"""
    if key in dialogue_data:
        data = dialogue_data[key]
        if 'title' in data:
            print_header(data['title'])
        if 'text' in data:
            for line in data['text']:
                print(line)