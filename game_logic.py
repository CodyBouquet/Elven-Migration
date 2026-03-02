import random


def select_elders(game, elders_data):
    """Choose 4 elders from 10"""
    
    print("\n" + "═"*60)
    print("THE COUNCIL OF DEFECTORS")
    print("═"*60)
    print("\nThe Cursed Forest is dying. The High Council refuses to leave.")
    print("But 10 elders have chosen to defy them and lead their followers")
    print("on a desperate exodus to Silverwood Vale.")
    print("\nYou must choose 4 elders to lead the migration.")
    print("═"*60)
    input("\nPress ENTER to meet the elders...")
    
    elder_list = list(elders_data['elders'].items())
    
    # Display all elders
    print("\n" + "═"*60)
    print("AVAILABLE ELDERS")
    print("═"*60)
    
    for idx, (elder_id, elder) in enumerate(elder_list, 1):
        print(f"\n{idx}) {elder['name']} - {elder['title']}")
        print(f"   Followers: {elder['followers']}")
        print(f"   Perk: {elder['perk']['name']}")
        print(f"   └─ {elder['perk']['description']}")
    
    # Choose 4
    chosen = []
    chosen_ids = []
    
    print("\n" + "═"*60)
    print("SELECT YOUR 4 ELDERS")
    print("═"*60)
    
    while len(chosen) < 4:
        print(f"\nChoosing elder {len(chosen)+1}/4")
        print("Available:", end=" ")
        for idx, (eid, e) in enumerate(elder_list, 1):
            if eid not in chosen_ids:
                print(f"{idx}) {e['name']}", end="  ")
        
        try:
            choice = int(input("\n\nSelect (1-10): "))
            if 1 <= choice <= 10:
                elder_id, elder_data = elder_list[choice-1]
                if elder_id not in chosen_ids:
                    chosen_ids.append(elder_id)
                    chosen.append({
                        'id': elder_id,
                        'name': elder_data['name'],
                        'title': elder_data['title'],
                        'followers': elder_data['followers'],
                        'perk': elder_data['perk']
                    })
                    print(f"✓ {elder_data['name']} joins!")
                else:
                    print("Already chosen!")
            else:
                print("Invalid number!")
        except:
            print("Invalid input!")
    
    # Store in game
    game['elders'] = chosen
    game['total_followers'] = sum(e['followers'] for e in chosen)
    game['max_followers'] = game['total_followers']
    
    # Apply Aldric's bonus gold
    for elder in chosen:
        if elder['id'] == 'aldric':
            game['resources']['gold'] += 200
            print(f"\n💰 {elder['name']}'s Trade Network grants +200 gold!")
    
    # Summary
    print("\n" + "═"*60)
    print("YOUR EXODUS LEADERS")
    print("═"*60)
    for elder in chosen:
        print(f"✓ {elder['name']} ({elder['followers']} followers)")
    print(f"\nTOTAL FOLLOWERS: {game['total_followers']}")
    print("═"*60)
    
    input("\nPress ENTER to continue...")


def daily_turn(game, stats, events_data):
    """Process one day of travel"""
    
    game['day'] += 1
    
    # Travel
    distance = int(stats['travel_speed'])
    game['distance_to_next_landmark'] -= distance
    game['total_distance_traveled'] += distance
    print(f"\n🚶 Traveled {distance} leagues")
    
    # Food consumption
    food_needed = game['total_followers'] // 10  # 1 food per 10 followers
    # Bug 6: food_efficiency > 1.0 means more efficient (less consumed). Division is correct.
    food_consumed = max(1, int(food_needed / stats['food_efficiency']))
    game['resources']['food'] -= food_consumed
    print(f"🍖 Consumed {food_consumed} food")

    # Starvation — Bug 5 fix: escalating percentage-based deaths instead of abs(food)*2
    if game['resources']['food'] < 0:
        game['resources']['food'] = 0
        game['days_without_food'] = game.get('days_without_food', 0) + 1
        pct = 0.01 * game['days_without_food']  # 1% per consecutive starving day
        deaths = max(1, int(game['total_followers'] * pct))
        deaths = min(deaths, game['total_followers'])
        game['total_followers'] -= deaths
        print(f"💀 {deaths} followers starved! (Day {game['days_without_food']} without food)")
    else:
        game['days_without_food'] = 0
    
    # Mana generation
    if stats['mana_generation'] > 0:
        game['resources']['mana'] += stats['mana_generation']
        print(f"✨ Generated {stats['mana_generation']} mana")
    
    # Check if all followers dead
    if game['total_followers'] <= 0:
        print("\n💀 All followers have perished. The exodus has failed.")
        game['game_over'] = True
        return
    
    # Random event
    event_chance = 0.35 + stats['luck']
    if random.random() < event_chance:
        from events import trigger_random_event
        trigger_random_event(game, events_data, stats)
    
    # Check warnings
    check_warnings(game)


def check_warnings(game):
    """Display resource warnings"""
    warnings = []
    
    if game['resources']['food'] < 30:
        warnings.append("⚠️ Food critically low!")
    
    if game['total_followers'] < game['max_followers'] * 0.3:
        warnings.append("⚠️ Most of your followers are gone!")
    
    if game['resources']['gold'] < 30:
        warnings.append("⚠️ Running out of gold!")
    
    if warnings:
        print("\n" + "\n".join(warnings))


def check_victory(game):
    """Check if reached destination"""
    if game['distance_to_next_landmark'] <= 0:
        print("\n" + "═"*60)
        print("🎉 VICTORY!")
        print("═"*60)
        print(f"After {game['day']} days of hardship, you have reached")
        print(f"{game['destination_landmark']}!")
        print(f"\n{game['total_followers']} followers survived the journey.")
        print("\nThe exodus is successful!")
        print("═"*60)
        game['game_over'] = True
        return True
    return False