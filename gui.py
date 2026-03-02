import random

# ═══════════════════════════════════════════════════════
# ELVEN EXODUS - GUI VERSION (PART 2 - UPDATED)
# ═══════════════════════════════════════════════════════

import tkinter as tk
from tkinter import messagebox
import json

# Import game logic from stats.py
from stats import calculate_stats


# ═══════════════════════════════════════════════════════
# LOAD GAME DATA
# ═══════════════════════════════════════════════════════

def load_json(filename):
    """Load JSON data file"""
    with open(filename, 'r') as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════
# MAIN GUI CLASS
# ═══════════════════════════════════════════════════════

class ElvenExodusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Elven Exodus")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        # Load game data
        self.elders = load_json('elders.json')
        self.items = load_json('items.json')
        self.events = load_json('events.json')
        self.landmarks = load_json('landmarks.json')  # Bug 12

        # Game state
        self.game = None
        self.stats = None

        # Initialize variables
        self.elder_vars = {}
        self.item_vars = {}

        # Create UI
        self.create_widgets()
        
        # Start game
        self.show_intro()
    
    def create_widgets(self):
        """Create main UI elements"""
        # Status bar at top
        self.status_frame = tk.Frame(self.root, bg='#2b2b2b', height=80)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="",
            font=('Consolas', 10),
            bg='#2b2b2b',
            fg='#d4d4d4',
            anchor=tk.W,
            justify=tk.LEFT
        )
        self.status_label.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Main text area (scrollable)
        text_frame = tk.Frame(self.root, bg='#1e1e1e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(
            text_frame,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)
        
        # Configure text tags for colors
        self.text_area.tag_config('default', foreground='#d4d4d4')
        self.text_area.tag_config('green', foreground='#4ec9b0')
        self.text_area.tag_config('blue', foreground='#569cd6')
        self.text_area.tag_config('yellow', foreground='#dcdcaa')
        self.text_area.tag_config('orange', foreground='#ce9178')
        self.text_area.tag_config('red', foreground='#f48771')
        self.text_area.tag_config('purple', foreground='#c586c0')
        self.text_area.tag_config('cyan', foreground='#4fc1ff')
        self.text_area.tag_config('magenta', foreground='#b267e6')
        self.text_area.tag_config('gold', foreground='#d7ba7d')
        self.text_area.tag_config('comment', foreground='#6a9955')
        self.text_area.tag_config('warning', foreground='#ff9800')
        self.text_area.tag_config('critical', foreground='#ff0000')
        
        # Button frame at bottom
        self.button_frame = tk.Frame(self.root, bg='#1e1e1e', height=80)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        self.button_frame.pack_propagate(False)
    
    def write_text(self, text, color='#d4d4d4'):
        """Write colored text to the text area"""
        self.text_area.config(state=tk.NORMAL)
        
        # Map hex colors to tag names
        color_map = {
            '#d4d4d4': 'default',
            '#4ec9b0': 'green',
            '#569cd6': 'blue',
            '#dcdcaa': 'yellow',
            '#ce9178': 'orange',
            '#f48771': 'red',
            '#c586c0': 'purple',
            '#4fc1ff': 'cyan',
            '#b267e6': 'magenta',
            '#d7ba7d': 'gold',
            '#6a9955': 'comment',
            '#ff9800': 'warning',
            '#ff0000': 'critical'
        }
        
        tag = color_map.get(color, 'default')
        self.text_area.insert(tk.END, text + '\n', tag)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
    
    def clear_text(self):
        """Clear the text area"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
    
    def clear_buttons(self):
        """Clear all buttons"""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
    
    def add_button(self, text, command, color='#0e639c'):
        """Add a button to the button frame"""
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            font=('Arial', 10, 'bold'),
            bg=color,
            fg='white',
            padx=8,
            pady=6,
            relief=tk.RAISED,
            bd=2,
            wraplength=140
        )
        btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.BOTH)
    
    def update_status(self):
        """Update the status bar"""
        if self.game:
            lm_key = self.game.get('current_landmark', '')
            lm = self.landmarks['landmarks'].get(lm_key, {})
            lm_name = lm.get('name', 'Unknown')
            r = self.game['resources']
            line1 = (
                f"Day {self.game['day']}  |  "
                f"Followers: {self.game['total_followers']}/{self.game['max_followers']}  |  "
                f"  {lm_name}  —  {self.game['distance_to_next_landmark']} leagues to next"
            )
            line2 = (
                f"Food: {r['food']}  |  "
                f"Gold: {r['gold']}  |  "
                f"Medicine: {r['medicine']}  |  "
                f"Arrows: {r['arrows']}  |  "
                f"Mana: {r['mana']}"
            )
            self.status_label.config(text=f"{line1}\n{line2}")
    
    # ═══════════════════════════════════════════════════════
    # GAME FLOW
    # ═══════════════════════════════════════════════════════
    
    def show_intro(self):
        """Show introduction screen"""
        self.clear_text()
        self.clear_buttons()
        
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("ELVEN EXODUS".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("")
        self.write_text("The ancient elven city of Aeloria has fallen to darkness.", '#dcdcaa')
        self.write_text("As one of the four remaining elders, you must lead your", '#dcdcaa')
        self.write_text("people on a perilous 1,600-league journey to the safety", '#dcdcaa')
        self.write_text("of Silverwood Vale.", '#dcdcaa')
        self.write_text("")
        self.write_text("Manage your resources, make difficult choices, and guide", '#dcdcaa')
        self.write_text("your followers through the wilderness. Every decision matters.", '#dcdcaa')
        self.write_text("")
        
        self.add_button("BEGIN", self.select_elders, '#0e639c')
        self.add_button("LOAD GAME", self.show_load_screen, '#4ec9b0')
        self.add_button("QUIT", self.root.quit, '#f48771')

    def select_elders(self):
        """Elder selection screen"""
        self.clear_text()
        self.clear_buttons()
        
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("SELECT YOUR ELDERS".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("")
        self.write_text("Choose 4 elders to lead the exodus:", '#dcdcaa')
        self.write_text("(Each elder provides unique bonuses)", '#6a9955')
        self.write_text("")
        
        # Create elder selection window
        self.elder_window = tk.Toplevel(self.root)
        self.elder_window.title("Select Elders")
        self.elder_window.geometry("600x700")
        self.elder_window.configure(bg='#2b2b2b')
    
        # Instructions
        tk.Label(
            self.elder_window,
            text="SELECT 4 ELDERS",
            font=('Arial', 16, 'bold'),
            bg='#2b2b2b',
            fg='#4ec9b0'
        ).pack(pady=10)
        
        tk.Label(
            self.elder_window,
            text="Click checkboxes to select (must choose exactly 4)",
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#6a9955'
        ).pack(pady=5)
        
        # Scrollable frame for elders
        canvas = tk.Canvas(self.elder_window, bg='#2b2b2b', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.elder_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Elder checkboxes
        self.elder_vars = {}  # Initialize here
        for elder_id, elder in self.elders['elders'].items():  # Access the 'elders' key
            var = tk.BooleanVar()
            self.elder_vars[elder_id] = var
            
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e', relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            cb = tk.Checkbutton(
                frame,
                text=elder['name'],
                variable=var,
                font=('Arial', 12, 'bold'),
                bg='#1e1e1e',
                fg='#dcdcaa',
                selectcolor='#2b2b2b',
                activebackground='#1e1e1e',
                activeforeground='#4ec9b0'
            )
            cb.pack(anchor=tk.W, padx=10, pady=5)
            
            tk.Label(
                frame,
                text=f"{elder['title']}",
                font=('Arial', 10),
                bg='#1e1e1e',
                fg='#569cd6'
            ).pack(anchor=tk.W, padx=30)

            tk.Label(
                frame,
                text=f"Followers: {elder['followers']}  |  Starting Gold: {elder['starting_gold']}",
                font=('Arial', 9, 'bold'),
                bg='#1e1e1e',
                fg='#d7ba7d'
            ).pack(anchor=tk.W, padx=30)

            tk.Label(
                frame,
                text=f"Perk: {elder['perk']['name']} — {elder['perk']['description']}",
                font=('Arial', 9),
                bg='#1e1e1e',
                fg='#6a9955'
            ).pack(anchor=tk.W, padx=30, pady=(0, 5))
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Confirm button
        tk.Button(
            self.elder_window,
            text="CONFIRM SELECTION",
            command=self.confirm_elders,
            font=('Arial', 12, 'bold'),
            bg='#0e639c',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Back button
        tk.Button(
            self.elder_window,
            text="BACK TO MAIN MENU",
            command=lambda: self.elder_window.destroy(),
            font=('Arial', 12, 'bold'),
            bg='#f48771',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=(0, 10))

    def confirm_elders(self):
        """Confirm elder selection and initialize game"""
        selected = [eid for eid, var in self.elder_vars.items() if var.get()]
        
        if len(selected) != 4:
            messagebox.showerror("Invalid Selection", "You must select exactly 4 elders!")
            return
        
        # Build elder objects with perk data from loaded JSON
        elders_list = []
        for eid in selected:
            elder_data = self.elders['elders'][eid]
            elders_list.append({
                'id': eid,
                'name': elder_data['name'],
                'title': elder_data['title'],
                'followers': elder_data['followers'],
                'perk': elder_data['perk']
            })

        total_followers = sum(e['followers'] for e in elders_list)

        # Bug 12: start at first landmark with its segment distance
        first_lm = self.landmarks['landmarks']['cursed_forest']

        # Gold = 100 base + each elder's starting_gold (replaces hardcoded 500 + Aldric special case)
        starting_gold = 100 + sum(
            self.elders['elders'][e['id']]['starting_gold'] for e in elders_list
        )

        # Initialize game state
        self.game = {
            'day': 1,
            'total_followers': total_followers,
            'max_followers': total_followers,
            'elders': elders_list,
            'current_landmark': 'cursed_forest',
            'resources': {
                'food': 0,
                'gold': starting_gold,
                'medicine': 0,
                'arrows': 0,
                'mana': 0
            },
            'special_items': [],
            'distance_to_next_landmark': first_lm['distance_to_next'],
            'total_distance_traveled': 0,
            'days_without_food': 0,
            'route_event_bonus': 0.0,
            'shop_used_at': None,
            'game_over': False,
        }
        
        self.elder_window.destroy()
        self.update_status()
        self.show_market()
    
    def show_market(self):
        """Show market preparation screen"""
        self.clear_text()
        self.clear_buttons()
        
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("MARKET SQUARE - FINAL PREPARATIONS".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("")
        self.write_text(f"You have {self.game['resources']['gold']} gold to spend on supplies.", '#d7ba7d')
        self.write_text("")
        self.write_text("Purchase wisely - you'll need food, medicine, and other", '#dcdcaa')
        self.write_text("essentials for the long journey ahead.", '#dcdcaa')
        self.write_text("")
        
        self.add_button("OPEN SHOP", self.open_landmark_shop, '#0e639c')
        self.add_button("BEGIN JOURNEY", self.start_journey, '#4ec9b0')
    
    def start_journey(self):
        """Start or resume the journey screen"""
        self.clear_text()
        self.clear_buttons()

        lm_key = self.game.get('current_landmark', 'cursed_forest')
        lm = self.landmarks['landmarks'][lm_key]

        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("ELVEN EXODUS".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("")
        self.write_text(f"Current region: {lm['name']}", '#569cd6')
        self.write_text(lm['description'], '#dcdcaa')
        self.write_text("")

        self._show_travel_buttons()

    def _show_travel_buttons(self):
        """Restore the main travel action buttons"""
        self.clear_buttons()
        self.add_button("TRAVEL", self.advance_day, '#0e639c')
        self.add_button("REST", self.rest, '#4ec9b0')
        self.add_button("HUNT", self.hunt, '#4ec9b0')
        self.add_button("FORAGE", self.forage, '#4ec9b0')
        self.add_button("CAST", self.cast_spell, '#c586c0')
        self.add_button("SAVE", self.show_save_screen, '#b267e6')

    def _consume_food(self):
        """Consume food for the day and apply starvation. (Bugs 5 & 11)"""
        stats = calculate_stats(self.game, self.items, self.elders)
        # 1 food per 7 followers
        # food_efficiency > 1.0 means more efficient (less consumed); division is correct
        food_needed = self.game['total_followers'] // 7
        food_consumed = max(1, int(food_needed / stats['food_efficiency']))
        self.game['resources']['food'] -= food_consumed
        self.write_text(f"Consumed {food_consumed} food.", '#6a9955')

        if self.game['resources']['food'] < 0:
            self.game['resources']['food'] = 0
            self.game['days_without_food'] += 1
            # Escalating 2%-per-day starvation (increases severity each consecutive day)
            pct = 0.02 * self.game['days_without_food']
            deaths = max(1, int(self.game['total_followers'] * pct))
            deaths = min(deaths, self.game['total_followers'])
            self.game['total_followers'] -= deaths
            self.write_text(
                f"No food! {deaths} followers starved. "
                f"(Day {self.game['days_without_food']} without food)", '#f48771')
        else:
            self.game['days_without_food'] = 0

    def advance_day(self):
        """Advance the game by one travel day."""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        stats = calculate_stats(self.game, self.items, self.elders)
        event_chance = 0.45 + stats['luck'] + self.game.get('route_event_bonus', 0.0)
        if random.random() < event_chance:
            self.resolve_event(on_done=lambda: self.finish_day(traveled=True))
        else:
            self.write_text("The day passes without incident.", '#d7ba7d')
            self.finish_day(traveled=True)

    def finish_day(self, traveled=False):
        """Complete the day: advance distance if traveled, check landmarks, increment day."""
        if traveled:
            stats = calculate_stats(self.game, self.items, self.elders)
            # Bug 11: use stats travel_speed (matches game_logic.py)
            distance = int(stats['travel_speed'])
            self.game['total_distance_traveled'] += distance
            self.game['distance_to_next_landmark'] -= distance

        self.game['day'] += 1

        # Mana generation (Miriel's perk)
        stats = calculate_stats(self.game, self.items, self.elders)
        if stats['mana_generation'] > 0:
            self.game['resources']['mana'] += stats['mana_generation']
            self.write_text(f"Generated {stats['mana_generation']} mana.", '#c586c0')

        # Bug 12: check landmark arrival
        if traveled and self.game['distance_to_next_landmark'] <= 0:
            self._arrive_at_landmark()
            return

        self.update_status()
        self._show_travel_buttons()

    def _arrive_at_landmark(self):
        """Handle arriving at a new landmark."""
        lm_key = self.game['current_landmark']
        lm = self.landmarks['landmarks'][lm_key]

        if lm.get('is_final'):
            self._show_victory()
            return

        next_key = lm['next_landmark']
        next_lm = self.landmarks['landmarks'][next_key]

        self.game['current_landmark'] = next_key
        self.game['route_event_bonus'] = 0.0  # reset on arrival

        self.clear_buttons()
        self.write_text("")
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text(f"ARRIVED: {next_lm['name']}".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text(next_lm['description'], '#dcdcaa')
        self.update_status()

        if next_lm.get('is_final'):
            self._show_victory()
        elif next_lm.get('routes'):
            self._show_route_choice(next_key, next_lm)
        else:
            self.game['distance_to_next_landmark'] = next_lm.get('distance_to_next', 0)
            self.add_button("OPEN MERCHANT", self.open_landmark_shop, '#d7ba7d')
            self.add_button("CONTINUE", self.start_journey, '#0e639c')

    def _show_route_choice(self, lm_key, lm):
        """Display route options for the next leg of the journey."""
        self.write_text("")
        self.write_text("CHOOSE YOUR ROUTE FORWARD", '#ff9800')
        self.write_text("─" * 60, '#ff9800')
        for route in lm['routes']:
            notes = []
            if route.get('gold_cost'):
                notes.append(f"Toll: {route['gold_cost']} gold")
            if route.get('food_bonus'):
                notes.append(f"+{route['food_bonus']} food")
            bonus = route.get('event_bonus', 0)
            if bonus > 0:
                notes.append(f"more events (+{int(bonus*100)}%)")
            elif bonus < 0:
                notes.append(f"fewer events ({int(bonus*100)}%)")
            note_str = f"  [{', '.join(notes)}]" if notes else ""
            self.write_text(
                f"{route['name']} — {route['distance']} leagues{note_str}", '#dcdcaa')
            self.write_text(f"  {route['description']}", '#6a9955')
            self.write_text("")

        self.clear_buttons()
        for route in lm['routes']:
            can_afford = self.game['resources']['gold'] >= route.get('gold_cost', 0)
            color = '#0e639c' if can_afford else '#555555'
            self.add_button(route['name'],
                            (lambda r=route: self._apply_route(r, lm_key)) if can_afford else lambda: None,
                            color)

    def _apply_route(self, route, lm_key):
        """Apply the chosen route: set distance, event bonus, one-time effects."""
        gold_cost = route.get('gold_cost', 0)
        if gold_cost > 0:
            self.game['resources']['gold'] -= gold_cost
            self.write_text(f"Paid {gold_cost} gold toll.", '#f48771')
        food_bonus = route.get('food_bonus', 0)
        if food_bonus > 0:
            self.game['resources']['food'] += food_bonus
            self.write_text(f"+{food_bonus} food from passing caravans.", '#4ec9b0')

        self.game['distance_to_next_landmark'] = route['distance']
        self.game['route_event_bonus'] = route.get('event_bonus', 0.0)
        self.write_text(f"Route chosen: {route['name']} ({route['distance']} leagues).", '#569cd6')

        self.update_status()
        self.clear_buttons()
        lm = self.landmarks['landmarks'][lm_key]
        if lm.get('shop_items'):
            self.add_button("OPEN MERCHANT", self.open_landmark_shop, '#d7ba7d')
        self.add_button("CONTINUE", self.start_journey, '#0e639c')

    def open_landmark_shop(self):
        """Open the landmark merchant shop with both buy and sell sections."""
        lm_key = self.game.get('current_landmark', 'cursed_forest')
        lm = self.landmarks['landmarks'][lm_key]

        # Filter items available at this landmark
        supply_ids = lm.get('shop_items', list(self.items['basic_supplies'].keys()))
        special_ids = lm.get('shop_specials', [])
        available_supplies = {k: v for k, v in self.items['basic_supplies'].items() if k in supply_ids}

        shop = tk.Toplevel(self.root)
        shop.title(f"Merchant — {lm['name']}")
        shop.geometry("680x600")
        shop.configure(bg='#2b2b2b')
        shop.transient(self.root)
        shop.grab_set()  # modal — blocks main window until closed

        # Each landmark merchant can only be visited once per stop
        if self.game.get('shop_used_at') == lm_key:
            tk.Label(shop, text="The merchant has already packed up and moved on.",
                     font=('Arial', 12), bg='#2b2b2b', fg='#f48771').pack(pady=30)
            tk.Button(shop, text="CLOSE", command=shop.destroy,
                      font=('Arial', 11), bg='#555555', fg='white',
                      padx=12, pady=6).pack()
            return

        tk.Label(shop, text=f"MERCHANT — {lm['name'].upper()}",
                 font=('Arial', 14, 'bold'), bg='#2b2b2b', fg='#d7ba7d').pack(pady=8)

        gold_label = tk.Label(shop, text=f"Gold: {self.game['resources']['gold']}",
                              font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#d7ba7d')
        gold_label.pack()

        # Pack buttons BEFORE canvas so expand=True doesn't crowd them out
        btn_frame = tk.Frame(shop, bg='#2b2b2b')
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=8)

        canvas = tk.Canvas(shop, bg='#2b2b2b')
        scrollbar = tk.Scrollbar(shop, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg='#2b2b2b')
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=640)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        # sell price per unit — food is not sellable (prevents hunt→sell exploit)
        SELL_RATES = {'arrows': 0.2, 'medicine': 1.5}
        SELL_LABELS = {'arrows': '0.2 gold/unit', 'medicine': '1.5 gold/unit'}
        sell_vars = {}
        buy_vars = {}
        special_item_vars = {}

        def safe_get_lm(v):
            try:
                return max(0, int(v.get()))
            except Exception:
                return 0

        def update_net(*_):
            sell_gold = sum(int(safe_get_lm(var) * SELL_RATES[res]) for res, var in sell_vars.items())
            buy_cost = sum(safe_get_lm(var) * int(self.items['basic_supplies'][iid]['cost'] * (1 - discount))
                           for iid, var in buy_vars.items())
            buy_cost += sum(int(self.items['special_items'][iid]['cost'] * (1 - discount))
                            for iid, var in special_item_vars.items() if var.get())
            net = sell_gold - buy_cost
            sign = '+' if net >= 0 else ''
            gold_label.config(
                text=f"Gold: {self.game['resources']['gold']}  (transaction: {sign}{net})"
            )

        # ── SELL SECTION ──
        tk.Label(content, text="── SELL SUPPLIES ──", font=('Arial', 11, 'bold'),
                 bg='#2b2b2b', fg='#ce9178').pack(pady=(8, 2), anchor=tk.W, padx=10)

        for res in ('arrows', 'medicine'):
            current = self.game['resources'].get(res, 0)
            row = tk.Frame(content, bg='#1e1e1e', relief=tk.RAISED, bd=1)
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row,
                     text=f"{res.capitalize()}: {current} available  ({SELL_LABELS[res]})",
                     font=('Arial', 10), bg='#1e1e1e', fg='#d4d4d4').pack(side=tk.LEFT, padx=10, pady=5)
            var = tk.IntVar(value=0)
            sell_vars[res] = var
            tk.Label(row, text="Sell qty:", font=('Arial', 9),
                     bg='#1e1e1e', fg='#6a9955').pack(side=tk.RIGHT, padx=(0, 4))
            tk.Entry(row, textvariable=var, width=6, font=('Arial', 10),
                     bg='#2b2b2b', fg='#d4d4d4').pack(side=tk.RIGHT, padx=(0, 10))
            var.trace_add('write', update_net)

        # ── BUY SECTION ──
        tk.Label(content, text="── BUY SUPPLIES ──", font=('Arial', 11, 'bold'),
                 bg='#2b2b2b', fg='#4ec9b0').pack(pady=(12, 2), anchor=tk.W, padx=10)

        stats = calculate_stats(self.game, self.items, self.elders)
        discount = stats.get('merchant_discount', 0.0)

        if not available_supplies:
            tk.Label(content, text="No supplies available here.",
                     font=('Arial', 10), bg='#2b2b2b', fg='#6a9955').pack(padx=10, pady=4)

        for item_id, item in available_supplies.items():
            var = tk.IntVar(value=0)
            buy_vars[item_id] = var
            discounted = int(item['cost'] * (1 - discount))
            price_text = (f"{discounted} gold (was {item['cost']})"
                          if discount > 0 else f"{item['cost']} gold")
            row = tk.Frame(content, bg='#1e1e1e', relief=tk.RAISED, bd=1)
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=f"{item['name']} — {price_text}",
                     font=('Arial', 10, 'bold'), bg='#1e1e1e', fg='#dcdcaa').pack(anchor=tk.W, padx=10, pady=(4, 0))
            tk.Label(row, text=item['description'],
                     font=('Arial', 9), bg='#1e1e1e', fg='#569cd6').pack(anchor=tk.W, padx=10, pady=(0, 4))
            tk.Entry(row, textvariable=var, width=5, font=('Arial', 10),
                     bg='#2b2b2b', fg='#d4d4d4').pack(side=tk.RIGHT, padx=10)
            var.trace_add('write', update_net)

        # ── SPECIAL ITEMS ──
        available_specials = {iid: item for iid, item in self.items['special_items'].items()
                              if iid not in self.game['special_items'] and iid in special_ids}
        if available_specials:
            tk.Label(content, text="── SPECIAL ITEMS (one-time) ──", font=('Arial', 11, 'bold'),
                     bg='#2b2b2b', fg='#b267e6').pack(pady=(12, 2), anchor=tk.W, padx=10)

        special_item_vars = {}
        for item_id, item in available_specials.items():
            discounted = int(item['cost'] * (1 - discount))
            price_text = (f"{discounted} gold (was {item['cost']})"
                          if discount > 0 else f"{item['cost']} gold")
            var = tk.BooleanVar(value=False)
            special_item_vars[item_id] = var
            row = tk.Frame(content, bg='#1e1e1e', relief=tk.RAISED, bd=1)
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=f"{item['name']} — {price_text}",
                     font=('Arial', 10, 'bold'), bg='#1e1e1e', fg='#b267e6').pack(anchor=tk.W, padx=10, pady=(4, 0))
            tk.Label(row, text=item['description'],
                     font=('Arial', 9), bg='#1e1e1e', fg='#569cd6').pack(anchor=tk.W, padx=10, pady=(0, 4))
            tk.Checkbutton(row, variable=var, command=update_net,
                           bg='#1e1e1e', selectcolor='#2b2b2b',
                           activebackground='#1e1e1e').pack(side=tk.RIGHT, padx=10)
            var.trace_add('write', update_net)

        def execute():
            # Validate sell quantities
            for res, var in sell_vars.items():
                qty = safe_get_lm(var)
                if qty > self.game['resources'].get(res, 0):
                    messagebox.showerror("Invalid Sale",
                        f"You only have {self.game['resources'].get(res, 0)} {res} to sell.")
                    return

            sell_gold = sum(int(safe_get_lm(var) * SELL_RATES[res]) for res, var in sell_vars.items())
            buy_cost = sum(safe_get_lm(var) * int(self.items['basic_supplies'][iid]['cost'] * (1 - discount))
                           for iid, var in buy_vars.items())
            buy_cost += sum(int(self.items['special_items'][iid]['cost'] * (1 - discount))
                            for iid, var in special_item_vars.items() if var.get())

            if self.game['resources']['gold'] + sell_gold < buy_cost:
                messagebox.showerror("Not Enough Gold",
                    f"You need {buy_cost} gold but only have "
                    f"{self.game['resources']['gold'] + sell_gold} (including sale proceeds).")
                return

            # Apply sells
            for res, var in sell_vars.items():
                qty = safe_get_lm(var)
                if qty > 0:
                    self.game['resources'][res] -= qty
                    self.game['resources']['gold'] += int(qty * SELL_RATES[res])

            # Apply basic supply buys
            for item_id, var in buy_vars.items():
                qty = safe_get_lm(var)
                if qty > 0:
                    item = self.items['basic_supplies'][item_id]
                    discounted_cost = int(item['cost'] * (1 - discount))
                    self.game['resources'][item['resource']] += item['amount'] * qty
                    self.game['resources']['gold'] -= discounted_cost * qty

            # Apply special item purchases
            for item_id, var in special_item_vars.items():
                if var.get() and item_id not in self.game['special_items']:
                    self.game['special_items'].append(item_id)
                    self.game['resources']['gold'] -= int(self.items['special_items'][item_id]['cost'] * (1 - discount))

            self.game['shop_used_at'] = lm_key
            shop.destroy()
            self.update_status()
            self.write_text("Transaction complete.", '#d7ba7d')

        tk.Button(btn_frame, text="EXECUTE TRANSACTION", command=execute,
                  font=('Arial', 11, 'bold'), bg='#0e639c', fg='white',
                  padx=12, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="CLOSE", command=shop.destroy,
                  font=('Arial', 11), bg='#555555', fg='white',
                  padx=12, pady=6).pack(side=tk.LEFT, padx=5)

    def _show_victory(self):
        """Show the victory screen."""
        lm = self.landmarks['landmarks'][self.game['current_landmark']]
        self.clear_text()
        self.clear_buttons()
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("VICTORY!".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text(f"After {self.game['day']} days you reached {lm['name']}!", '#4ec9b0')
        self.write_text(
            f"{self.game['total_followers']} of {self.game['max_followers']} followers survived.",
            '#dcdcaa')
        self.write_text("")
        self.add_button("RETURN TO MAIN MENU", self.show_intro, '#0e639c')

    def resolve_event(self, on_done):
        """Show event with outcome buttons; on_done() is called after the player chooses. (Bug 7)"""
        category = random.choice(['positive_events', 'negative_events', 'neutral_events'])
        event_key = random.choice(list(self.events[category].keys()))
        event = self.events[category][event_key]

        self.write_text("")
        self.write_text(f"EVENT: {event['title']}", '#ff9800')
        self.write_text(event['description'], '#dcdcaa')
        self.write_text("")

        self.clear_buttons()
        for outcome in event['outcomes']:
            can_use = self._check_requirements(outcome.get('requirements', {}))
            label = outcome['text']
            if can_use:
                self.add_button(label,
                                lambda o=outcome: self.apply_event_outcome(o, on_done),
                                '#0e639c')
            else:
                self.add_button(f"{label} [NO RESOURCES]", lambda: None, '#555555')

    def _check_requirements(self, req):
        """Return True if the current game state satisfies a requirements dict."""
        for res in ('food', 'medicine', 'gold', 'mana', 'arrows'):
            if res in req and self.game['resources'].get(res, 0) < req[res]:
                return False
        if 'stat' in req:
            stats = calculate_stats(self.game, self.items, self.elders)
            if stats.get(req['stat'], 0) < req.get('min_value', 0):
                return False
        return True

    def apply_event_outcome(self, outcome, on_done):
        """Apply a chosen outcome's effects and continue. (Bugs 8 & 9)"""
        self.write_text(f"> {outcome['text']}", '#4ec9b0')
        self.write_text(outcome['outcome_description'], '#dcdcaa')

        stats = calculate_stats(self.game, self.items, self.elders)
        effects = outcome.get('effects', {})
        affected_by = effects.get('affected_by')
        stat_mult = stats.get(affected_by, 1.0) if affected_by else 1.0

        # Arcane Veil: pop the flag now and halve all negative effects this event
        veil_active = self.game.pop('arcane_veil_active', False)
        veil_triggered = False

        for key, value in effects.items():
            if key in ('affected_by', 'success_chance',
                       'random_blessing', 'enemy_strength', 'morale'):
                continue

            # Combat trigger — losses reduced by combat_power (and veil)
            if key == 'trigger':
                if value == 'combat':
                    enemy_str = effects.get('enemy_strength', [20, 40])
                    raw = random.randint(min(enemy_str), max(enemy_str))
                    losses = max(1, int(raw / stats.get('combat_power', 1.0)))
                    if veil_active:
                        losses = max(1, losses // 2)
                        veil_triggered = True
                    losses = min(losses, self.game['total_followers'])
                    self.game['total_followers'] -= losses
                    self.write_text(f"  Combat! {losses} followers lost in the fight.", '#f48771')
                continue  # skip all other triggers (trade_menu etc.)

            if key == 'day':
                self.game['day'] += value
                self.write_text(f"  Lost {value} extra day(s).", '#f48771')
                continue

            # Bug 8: guard against inverted negative ranges like [-10, -20]
            # Bug 9: handle scalar values (not every effect is a [min, max] list)
            if isinstance(value, list):
                lo, hi = min(value[0], value[1]), max(value[0], value[1])
                change = random.randint(lo, hi)
            else:
                change = value

            if affected_by:
                if change < 0:
                    # Mitigation stats (disease_resistance, weather_resistance):
                    # higher stat = less damage. Base=0 means full damage.
                    change = int(change / (1 + stat_mult))
                else:
                    # Enhancement stats (hunting_efficiency, healing_power):
                    # higher stat = more gain.
                    change = int(change * stat_mult)

            # Arcane Veil halves all negative changes
            if veil_active and change < 0:
                change = -(abs(change) // 2)
                veil_triggered = True

            sign = '+' if change >= 0 else ''
            if key == 'followers':
                self.game['total_followers'] = max(0, self.game['total_followers'] + change)
                self.write_text(f"  Followers: {sign}{change}", '#dcdcaa')
            elif key in self.game['resources']:
                self.game['resources'][key] = max(0, self.game['resources'][key] + change)
                self.write_text(f"  {key.capitalize()}: {sign}{change}", '#dcdcaa')

        if veil_triggered:
            self.write_text("  (Arcane Veil absorbed half the damage!)", '#b267e6')

        self.update_status()

        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        on_done()

    def cast_spell(self):
        """Spend mana on an arcane effect (consumes a day)."""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        mana = self.game['resources']['mana']
        self.write_text("")
        self.write_text("ARCANE ARTS", '#c586c0')

        if mana <= 0:
            self.write_text("No mana available. The day passes without magic.", '#c586c0')
            self.finish_day(traveled=False)
            return

        self.write_text(f"Available mana: {mana}  — Choose a spell:", '#c586c0')
        self.write_text("  Conjure Rations (3 mana)  — produce 20 food from thin air", '#dcdcaa')
        self.write_text("  Healing Aura   (5 mana)  — restore 5% of lost followers", '#4ec9b0')
        self.write_text("  Arcane Veil    (8 mana)  — halve the next event's damage", '#b267e6')

        self.clear_buttons()
        if mana >= 3:
            self.add_button("CONJURE RATIONS", lambda: self._apply_spell(3, 'rations'), '#c586c0')
        if mana >= 5:
            self.add_button("HEALING AURA", lambda: self._apply_spell(5, 'heal'), '#4ec9b0')
        if mana >= 8:
            self.add_button("ARCANE VEIL", lambda: self._apply_spell(8, 'veil'), '#b267e6')
        self.add_button("CANCEL", lambda: self.finish_day(traveled=False), '#555555')

    def _apply_spell(self, cost, spell):
        """Apply the chosen spell effect."""
        self.game['resources']['mana'] -= cost
        stats = calculate_stats(self.game, self.items, self.elders)

        if spell == 'rations':
            # Base 20 food + 5 per point of mana_generation (Miriel adds 3 → +15 bonus)
            gained = 20 + int(stats.get('mana_generation', 0) * 5)
            self.game['resources']['food'] += gained
            self.write_text(f"Conjured rations! +{gained} food. (-{cost} mana)", '#c586c0')
        elif spell == 'heal':
            missing = self.game['max_followers'] - self.game['total_followers']
            recovered = min(missing, max(1, int(self.game['max_followers'] * 0.05
                                               * stats.get('healing_power', 1.0))))
            self.game['total_followers'] += recovered
            self.write_text(f"Healing aura! +{recovered} followers. (-{cost} mana)", '#4ec9b0')
        elif spell == 'veil':
            self.game['arcane_veil_active'] = True
            self.write_text(f"Arcane Veil raised. Next harmful event is halved. (-{cost} mana)", '#b267e6')

        self.update_status()
        self.finish_day(traveled=False)

    def rest(self):
        """Rest for a day: no travel, recover followers. (Bug 10)"""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        stats = calculate_stats(self.game, self.items, self.elders)
        # Recover 1% of max followers, scaled by healing_power, capped at missing count
        missing = self.game['max_followers'] - self.game['total_followers']
        recovered = min(missing, max(1, int(self.game['max_followers'] * 0.01 * stats['healing_power'])))
        if recovered > 0:
            self.game['total_followers'] += recovered
            self.write_text(f"Your followers rest and recover. +{recovered} followers.", '#4ec9b0')
        else:
            self.write_text("Your followers rest. No further recovery possible.", '#d7ba7d')

        self.finish_day(traveled=False)

    def hunt(self):
        """Hunt for food using arrows; bare-hands if none. (Bug 10)"""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        stats = calculate_stats(self.game, self.items, self.elders)
        if self.game['resources']['arrows'] >= 10:
            self.game['resources']['arrows'] -= 10
            gained = int(random.randint(40, 70) * stats['hunting_efficiency'])
            self.game['resources']['food'] += gained
            self.write_text(f"Hunt successful! +{gained} food (used 10 arrows).", '#4ec9b0')
        else:
            gained = int(random.randint(5, 12) * stats['hunting_efficiency'])
            self.game['resources']['food'] += gained
            self.write_text(f"Hunting without arrows yields little. +{gained} food.", '#d7ba7d')

        self.finish_day(traveled=False)

    def forage(self):
        """Forage for edible plants and herbs. (Bug 10)"""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        stats = calculate_stats(self.game, self.items, self.elders)
        medicine_gained = int(random.randint(3, 8) * stats['healing_power'])
        food_gained = random.randint(2, 6)
        self.game['resources']['medicine'] += medicine_gained
        self.game['resources']['food'] += food_gained
        self.write_text(f"Found herbs and plants. +{medicine_gained} medicine, +{food_gained} food.", '#4ec9b0')

        self.finish_day(traveled=False)

    # ═══════════════════════════════════════════════════════
    # SAVE / LOAD  (Bug 13)
    # ═══════════════════════════════════════════════════════

    def save_game(self, slot):
        """Serialize current game state to a save slot in player.json."""
        try:
            player_data = load_json('player.json')
            player_data['save_slots'][slot] = self.game
            with open('player.json', 'w') as f:
                json.dump(player_data, f, indent=2)
            messagebox.showinfo("Saved", f"Game saved to {slot.replace('_', ' ').title()}!")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))

    def load_game(self, slot):
        """Load a saved game from player.json and resume the journey."""
        try:
            player_data = load_json('player.json')
            saved = player_data['save_slots'].get(slot)
            if saved is None:
                messagebox.showerror("No Save", f"No save data in {slot.replace('_', ' ').title()}.")
                return
            self.game = saved
            self.update_status()
            self.start_journey()
        except Exception as e:
            messagebox.showerror("Load Failed", str(e))

    def show_save_screen(self):
        """Show save-slot picker dialog."""
        win = tk.Toplevel(self.root)
        win.title("Save Game")
        win.geometry("320x220")
        win.configure(bg='#2b2b2b')
        tk.Label(win, text="SAVE GAME", font=('Arial', 14, 'bold'),
                 bg='#2b2b2b', fg='#4ec9b0').pack(pady=10)
        for slot in ('slot_1', 'slot_2', 'slot_3'):
            label = slot.replace('_', ' ').title()
            tk.Button(win, text=label,
                      command=lambda s=slot: [self.save_game(s), win.destroy()],
                      font=('Arial', 12), bg='#0e639c', fg='white',
                      padx=10, pady=5).pack(pady=5, fill=tk.X, padx=20)

    def show_load_screen(self):
        """Show load-slot picker dialog."""
        win = tk.Toplevel(self.root)
        win.title("Load Game")
        win.geometry("360x240")
        win.configure(bg='#2b2b2b')
        tk.Label(win, text="LOAD GAME", font=('Arial', 14, 'bold'),
                 bg='#2b2b2b', fg='#4ec9b0').pack(pady=10)
        try:
            player_data = load_json('player.json')
        except Exception:
            messagebox.showerror("Error", "Could not load player.json")
            win.destroy()
            return
        for slot in ('slot_1', 'slot_2', 'slot_3'):
            saved = player_data['save_slots'].get(slot)
            label = slot.replace('_', ' ').title()
            if saved:
                label += f"  (Day {saved.get('day', '?')}, {saved.get('total_followers', '?')} followers)"
            else:
                label += "  [empty]"
            state = tk.NORMAL if saved else tk.DISABLED
            tk.Button(win, text=label, state=state,
                      command=lambda s=slot: [self.load_game(s), win.destroy()],
                      font=('Arial', 11), bg='#0e639c', fg='white',
                      padx=10, pady=5).pack(pady=5, fill=tk.X, padx=20)

    # ═══════════════════════════════════════════════════════
    # GAME OVER
    # ═══════════════════════════════════════════════════════

    def show_game_over(self, message):
        """Handle game over scenario"""
        self.clear_text()
        self.clear_buttons()

        self.write_text("=" * 60, '#f48771')
        self.write_text("GAME OVER".center(60), '#f48771')
        self.write_text("=" * 60, '#f48771')
        self.write_text(message, '#f48771')

        self.add_button("RETURN TO MAIN MENU", self.show_intro, '#0e639c')
        self.add_button("QUIT", self.root.quit, '#f48771')

# ═══════════════════════════════════════════════════════
# START THE GAME
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = ElvenExodusGUI(root)
    root.mainloop()