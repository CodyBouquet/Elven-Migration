import random


def trigger_random_event(game, events_data, stats):
    """Pick a random event, present choices, and apply effects"""
    category = random.choice(['positive_events', 'negative_events', 'neutral_events'])
    event_key = random.choice(list(events_data[category].keys()))
    event = events_data[category][event_key]

    print(f"\n{'═'*60}")
    print(f"⚡ EVENT: {event['title']}")
    print(f"{'═'*60}")
    print(f"\n{event['description']}")

    outcomes = event['outcomes']
    available = []

    for i, outcome in enumerate(outcomes):
        req = outcome.get('requirements', {})
        can_use = True

        for res in ('food', 'medicine', 'gold', 'mana', 'arrows'):
            if res in req and game['resources'].get(res, 0) < req[res]:
                can_use = False
                break

        if 'stat' in req and stats.get(req['stat'], 0) < req.get('min_value', 0):
            can_use = False

        label = f"{i + 1}) {outcome['text']}"
        if not can_use:
            label += " [UNAVAILABLE]"
        available.append((outcome, can_use))
        print(label)

    chosen_outcome = None
    while chosen_outcome is None:
        try:
            choice = int(input("\nYour choice: ")) - 1
            if 0 <= choice < len(available):
                outcome, can_use = available[choice]
                if can_use:
                    chosen_outcome = outcome
                else:
                    print("You don't meet the requirements for that choice!")
            else:
                print("Invalid choice!")
        except (ValueError, EOFError):
            chosen_outcome = available[0][0]

    _apply_effects(game, chosen_outcome, stats)
    print(f"\n{chosen_outcome['outcome_description']}")


def _apply_effects(game, outcome, stats):
    """Apply an outcome's effects to the game state"""
    effects = outcome.get('effects', {})
    affected_by = effects.get('affected_by')
    stat_multiplier = stats.get(affected_by, 1.0) if affected_by else 1.0

    for key, value in effects.items():
        if key in ('trigger', 'affected_by', 'success_chance', 'random_blessing',
                   'enemy_strength', 'morale'):
            continue

        if key == 'day':
            game['day'] += value
            print(f"  Lost {value} day(s).")
            continue

        # Bug 8: use min/max to handle inverted negative ranges like [-10, -20]
        change = random.randint(min(value[0], value[1]), max(value[0], value[1])) if isinstance(value, list) else value
        change = int(change * stat_multiplier) if affected_by else change

        if key == 'followers':
            game['total_followers'] = max(0, game['total_followers'] + change)
            sign = '+' if change >= 0 else ''
            print(f"  {sign}{change} followers.")
        elif key in game['resources']:
            game['resources'][key] = max(0, game['resources'][key] + change)
            sign = '+' if change >= 0 else ''
            print(f"  {sign}{change} {key}.")