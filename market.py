def supply_market(game, items_data, stats):
    """Shopping interface"""
    while True:
        discount = stats['merchant_discount']
        
        print("\n" + "═"*60)
        print("🏪 SUPPLY MARKET")
        print("═"*60)
        print(f"💰 Gold: {game['resources']['gold']}")
        if discount > 0:
            print(f"✨ Merchant Discount: {int(discount*100)}%")
        
        menu = {}
        num = 1
        
        print("\nBASIC SUPPLIES:")
        for item_id, item in items_data['basic_supplies'].items():
            cost = int(item['cost'] * (1 - discount))
            print(f"{num}) {item['name']:25s} {cost:3d} gold")
            menu[str(num)] = ('basic', item_id)
            num += 1
        
        print("\nSPECIAL ITEMS:")
        for item_id, item in items_data['special_items'].items():
            cost = int(item['cost'] * (1 - discount))
            owned = "✓ OWNED" if item_id in game['special_items'] else f"{cost} gold"
            print(f"{num}) {item['name']:25s} {owned}")
            menu[str(num)] = ('special', item_id)
            num += 1
        
        print(f"\n{num}) DONE SHOPPING")
        
        choice = input("\nChoice: ").strip()
        
        if choice == str(num):
            break
        
        if choice in menu:
            item_type, item_id = menu[choice]
            
            if item_type == 'basic':
                item = items_data['basic_supplies'][item_id]
                cost = int(item['cost'] * (1 - discount))
                
                if game['resources']['gold'] >= cost:
                    game['resources']['gold'] -= cost
                    game['resources'][item['resource']] += item['amount']
                    print(f"\n✓ Purchased {item['name']} (+{item['amount']} {item['resource']})")
                else:
                    print(f"\n❌ Not enough gold! Need {cost}, have {game['resources']['gold']}")
            
            elif item_type == 'special':
                if item_id in game['special_items']:
                    print("\n❌ You already own this item!")
                else:
                    item = items_data['special_items'][item_id]
                    cost = int(item['cost'] * (1 - discount))
                    
                    if game['resources']['gold'] >= cost:
                        game['resources']['gold'] -= cost
                        game['special_items'].append(item_id)
                        print(f"\n✓ Purchased {item['name']}")
                        print(f"   {item['description']}")
                    else:
                        print(f"\n❌ Not enough gold! Need {cost}, have {game['resources']['gold']}")
        else:
            print("\n❌ Invalid choice!")