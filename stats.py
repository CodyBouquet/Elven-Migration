def get_base_stats():
    """Base stats before modifiers"""
    return {
        'travel_speed': 20,
        'combat_power': 1.0,
        'hunting_efficiency': 1.0,
        'healing_power': 1.0,
        'diplomacy': 0.0,
        'luck': 0.0,
        'merchant_discount': 0.0,
        'weather_resistance': 0.0,
        'disease_resistance': 0.0,
        'mana_generation': 0,
        'food_efficiency': 1.0,
        'follower_protection': 0.0,
    }


def calculate_stats(game, items_data, elders_data):
    """Calculate stats with elder perks + items"""
    stats = get_base_stats()
    
    # Apply elder perks
    for elder in game['elders']:
        perk = elder['perk']
        stat = perk['stat']
        bonus = perk['bonus']
        
        if stat in stats:
            stats[stat] += bonus
    
    # Apply item bonuses
    for item_id in game['special_items']:
        if item_id in items_data['special_items']:
            item = items_data['special_items'][item_id]
            stat = item['stat']
            bonus = item['bonus']
            
            if stat in stats:
                if item['bonus_type'] == 'additive':
                    stats[stat] += bonus
                elif item['bonus_type'] == 'multiplicative':
                    stats[stat] *= (1 + bonus)
    
    return stats