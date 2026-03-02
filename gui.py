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
        self.status_frame = tk.Frame(self.root, bg='#2b2b2b', height=60)
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
            font=('Arial', 12, 'bold'),
            bg=color,
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
    
    def update_status(self):
        """Update the status bar"""
        if self.game:
            lm_key = self.game.get('current_landmark', '')
            lm = self.landmarks['landmarks'].get(lm_key, {})
            lm_name = lm.get('name', 'Unknown')
            status = (
                f"Day {self.game['day']}  |  "
                f"Followers: {self.game['total_followers']}/{self.game['max_followers']}  |  "
                f"Food: {self.game['resources']['food']}  |  "
                f"Gold: {self.game['resources']['gold']}  |  "
                f"{lm_name}: {self.game['distance_to_next_landmark']} leagues to next"
            )
            self.status_label.config(text=status)
    
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
                text=f"Role: {elder['title']}",  # Changed to 'title' for clarity
                font=('Arial', 10),
                bg='#1e1e1e',
                fg='#569cd6'
            ).pack(anchor=tk.W, padx=30)
            
            tk.Label(
                frame,
                text=f"Specialty: {elder['specialty']}",
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

        # Initialize game state
        self.game = {
            'day': 1,
            'total_followers': total_followers,
            'max_followers': total_followers,
            'elders': elders_list,
            'current_landmark': 'cursed_forest',
            'resources': {
                'food': 0,
                'gold': 500,
                'medicine': 0,
                'arrows': 0,
                'mana': 0
            },
            'special_items': [],
            'distance_to_next_landmark': first_lm['distance_to_next'],
            'total_distance_traveled': 0,
            'days_without_food': 0,
            'game_over': False,
        }

        # Apply Aldric's Trade Network bonus (+200 gold)
        for elder in elders_list:
            if elder['id'] == 'aldric':
                self.game['resources']['gold'] += 200
        
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
        
        self.add_button("OPEN SHOP", self.open_shop, '#0e639c')
        self.add_button("BEGIN JOURNEY", self.start_journey, '#4ec9b0')
    
    def open_shop(self):
        """Open shopping window"""
        shop = tk.Toplevel(self.root)
        shop.title("Supply Shop")
        shop.geometry("600x500")  # Increased size for better visibility
        shop.configure(bg='#2b2b2b')

        tk.Label(
            shop,
            text="WELCOME TO THE SUPPLY SHOP",
            font=('Arial', 16, 'bold'),
            bg='#2b2b2b',
            fg='#4ec9b0'
        ).pack(pady=10)

        # Create a Canvas and Scrollbar
        canvas = tk.Canvas(shop, bg='#2b2b2b')
        scrollbar = tk.Scrollbar(shop, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.item_vars = {}
        self.special_item_vars = {}
        total_cost = 0  # Variable to keep track of total cost

        # Label for total cost
        total_cost_label = tk.Label(
            shop,
            text=f"Total Cost: {total_cost} gold",
            font=('Arial', 12),
            bg='#2b2b2b',
            fg='white'
        )
        total_cost_label.pack(pady=5)

        # Function to update total cost
        def update_cost():
            nonlocal total_cost
            total_cost = sum(var.get() * self.items[category][item_id]['cost'] 
                            for category in ['basic_supplies'] 
                            for item_id, var in self.item_vars.items())
            
            # Add special items cost (only one can be selected)
            special_cost = sum(var.get() * self.items['special_items'][item_id]['cost'] 
                            for item_id, var in self.special_item_vars.items())
            total_cost += special_cost
            total_cost_label.config(text=f"Total Cost: {total_cost} gold")

        # Iterate over basic supplies
        tk.Label(scrollable_frame, text="General Supplies", font=('Arial', 14, 'bold'), bg='#2b2b2b', fg='white').pack(pady=5)

        for item_id, item in self.items['basic_supplies'].items():
            var = tk.IntVar(value=0)
            self.item_vars[item_id] = var
            
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e', relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(
                frame,
                text=f"{item['name']} - {item['cost']} gold",
                font=('Arial', 12, 'bold'),
                bg='#1e1e1e',
                fg='#dcdcaa'
            ).pack(anchor=tk.W, padx=10)

            tk.Label(
                frame,
                text=item['description'],
                font=('Arial', 10),
                bg='#1e1e1e',
                fg='#569cd6'
            ).pack(anchor=tk.W, padx=10)

            entry = tk.Entry(
                frame,
                textvariable=var,
                width=5,
                font=('Arial', 12),
                bg='#2b2b2b',
                fg='#d4d4d4'
            )
            entry.pack(side=tk.RIGHT, padx=(10, 0))

            # Bind entry to update total cost
            var.trace_add('write', lambda *args: update_cost())

        # Label for special items
        tk.Label(scrollable_frame, text="Special Items", font=('Arial', 14, 'bold'), bg='#2b2b2b', fg='white').pack(pady=10)

        for item_id, item in self.items['special_items'].items():
            var = tk.IntVar(value=0)
            self.special_item_vars[item_id] = var
            
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e', relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(
                frame,
                text=f"{item['name']} - {item['cost']} gold",
                font=('Arial', 12, 'bold'),
                bg='#1e1e1e',
                fg='#dcdcaa'
            ).pack(anchor=tk.W, padx=10)

            tk.Label(
                frame,
                text=item['description'],
                font=('Arial', 10),
                bg='#1e1e1e',
                fg='#569cd6'
            ).pack(anchor=tk.W, padx=10)

            # Use Checkbutton for special items
            checkbutton = tk.Checkbutton(
                frame,
                variable=var,
                command=update_cost,
                bg='#1e1e1e'
            )
            checkbutton.pack(side=tk.RIGHT, padx=(10, 0))

        # Purchase Button
        tk.Button(
            shop,
            text="PURCHASE ITEMS",
            command=lambda: self.purchase_items(shop, self.item_vars, self.special_item_vars),
            font=('Arial', 12, 'bold'),
            bg='#0e639c',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=10)

        # Back Button
        tk.Button(
            shop,
            text="BACK",
            command=shop.destroy,  # Closes the shop window
            font=('Arial', 12, 'bold'),
            bg='#c41e3a',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=5)

    def purchase_items(self, shop, item_vars, special_item_vars):
        """Process the purchase of items"""
        total_cost = sum(var.get() * self.items['basic_supplies'][item_id]['cost']
                        for item_id, var in item_vars.items())
        special_cost = sum(var.get() * self.items['special_items'][item_id]['cost']
                          for item_id, var in special_item_vars.items())
        total_cost += special_cost

        if total_cost > self.game['resources']['gold']:
            messagebox.showerror("Not Enough Gold",
                                 f"You need {total_cost} gold but only have "
                                 f"{self.game['resources']['gold']}.")
            return

        # Deduct gold
        self.game['resources']['gold'] -= total_cost

        # Add basic supply resources
        for item_id, var in item_vars.items():
            qty = var.get()
            if qty > 0:
                item = self.items['basic_supplies'][item_id]
                self.game['resources'][item['resource']] += item['amount'] * qty

        # Add special items (checkbox = 1 means purchased)
        for item_id, var in special_item_vars.items():
            if var.get() == 1 and item_id not in self.game['special_items']:
                self.game['special_items'].append(item_id)

        shop.destroy()
        self.update_status()
        self.start_journey()
    
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
        self.add_button("SAVE", self.show_save_screen, '#b267e6')

    def _consume_food(self):
        """Consume food for the day and apply starvation. (Bugs 5 & 11)"""
        stats = calculate_stats(self.game, self.items, self.elders)
        # Bug 11: align with game_logic.py — 1 food per 10 followers
        # food_efficiency > 1.0 means more efficient (less consumed); division is correct
        food_needed = self.game['total_followers'] // 10
        food_consumed = max(1, int(food_needed / stats['food_efficiency']))
        self.game['resources']['food'] -= food_consumed
        self.write_text(f"Consumed {food_consumed} food.", '#6a9955')

        if self.game['resources']['food'] < 0:
            self.game['resources']['food'] = 0
            self.game['days_without_food'] += 1
            # Bug 5: escalating 1%-per-day percentage instead of abs(food)*2
            pct = 0.01 * self.game['days_without_food']
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

        if random.random() < 0.2:
            # Bug 7: show buttons for player choice; finish_day called after selection
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

        # Bug 12: check landmark arrival
        if traveled and self.game['distance_to_next_landmark'] <= 0:
            self._arrive_at_landmark()
            return

        self.update_status()
        self._show_travel_buttons()

    def _arrive_at_landmark(self):
        """Handle arriving at a new landmark. (Bug 12)"""
        lm_key = self.game['current_landmark']
        lm = self.landmarks['landmarks'][lm_key]

        if lm.get('is_final'):
            self._show_victory()
            return

        next_key = lm['next_landmark']
        next_lm = self.landmarks['landmarks'][next_key]

        self.game['current_landmark'] = next_key
        self.game['distance_to_next_landmark'] = next_lm['distance_to_next']

        self.clear_buttons()
        self.write_text("")
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text(f"ARRIVED: {next_lm['name']}".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text(next_lm['description'], '#dcdcaa')
        if not next_lm.get('is_final'):
            self.write_text(f"Next leg: {next_lm['distance_to_next']} leagues ahead.", '#6a9955')

        self.update_status()

        if next_lm.get('is_final'):
            self._show_victory()
        else:
            self.add_button("CONTINUE", self.start_journey, '#0e639c')

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

        for key, value in effects.items():
            if key in ('trigger', 'affected_by', 'success_chance',
                       'random_blessing', 'enemy_strength', 'morale'):
                continue

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
                change = int(change * stat_mult)

            sign = '+' if change >= 0 else ''
            if key == 'followers':
                self.game['total_followers'] = max(0, self.game['total_followers'] + change)
                self.write_text(f"  Followers: {sign}{change}", '#dcdcaa')
            elif key in self.game['resources']:
                self.game['resources'][key] = max(0, self.game['resources'][key] + change)
                self.write_text(f"  {key.capitalize()}: {sign}{change}", '#dcdcaa')

        self.update_status()

        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        on_done()

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
            gained = int(random.randint(20, 40) * stats['hunting_efficiency'])
            self.game['resources']['food'] += gained
            self.write_text(f"Hunt successful! +{gained} food (used 10 arrows).", '#4ec9b0')
        else:
            gained = int(random.randint(5, 15) * stats['hunting_efficiency'])
            self.game['resources']['food'] += gained
            self.write_text(f"Hunting without arrows yields less. +{gained} food.", '#d7ba7d')

        self.finish_day(traveled=False)

    def forage(self):
        """Forage for edible plants and herbs. (Bug 10)"""
        self._consume_food()
        if self.game['total_followers'] <= 0:
            self.show_game_over("All followers have perished.")
            return

        stats = calculate_stats(self.game, self.items, self.elders)
        gained = int(random.randint(5, 15) * stats['hunting_efficiency'])
        self.game['resources']['food'] += gained
        self.write_text(f"You find edible plants and herbs. +{gained} food.", '#4ec9b0')

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