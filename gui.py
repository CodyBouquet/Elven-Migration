import random

# ═══════════════════════════════════════════════════════
# ELVEN EXODUS - GUI VERSION (PART 2 - UPDATED)
# ═══════════════════════════════════════════════════════

import tkinter as tk
from tkinter import messagebox
import json

# Import game logic from game.py
from game import calculate_stats


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
            status = (
                f"Day {self.game['day']}  |  "
                f"Followers: {self.game['total_followers']}/{self.game['max_followers']}  |  "
                f"Food: {self.game['resources']['food']}  |  "
                f"Gold: {self.game['resources']['gold']}  |  "
                f"Distance: {self.game['distance_to_next_landmark']} leagues"
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
        
        # Initialize game state
        self.game = {
            'day': 1,
            'total_followers': 500,
            'max_followers': 500,
            'selected_elders': selected,
            'resources': {
                'food': 0,
                'gold': 2500,
                'medicine': 0,
                'arrows': 0,
                'mana': 0
            },
            'special_items': [],
            'distance_to_next_landmark': 1600,
            'total_distance_traveled': 0,
            'events_encountered': []
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

        shop.destroy()

        self.start_journey()
    
    def start_journey(self):
        """Start the journey"""
        self.clear_text()
        self.clear_buttons()
        
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("BEGINNING YOUR JOURNEY".center(60), '#4ec9b0')
        self.write_text("=" * 60, '#4ec9b0')
        self.write_text("")
        self.write_text("Your journey has begun! Each day you will travel and", '#dcdcaa')
        self.write_text("face challenges along the way.", '#dcdcaa')
        
        self.add_button("TRAVEL", self.advance_day, '#0e639c')
        self.add_button("REST", self.rest, '#4ec9b0')
        self.add_button("HUNT", self.hunt, '#4ec9b0')
        self.add_button("FORAGE", self.forage, '#4ec9b0')

    def advance_day(self):
        """Advance the game by one day"""
        
        # **Food Consumption Logic**
        food_consumed = self.game['total_followers'] * 2  # Example: each follower consumes 2 units of food
        self.game['resources']['food'] -= food_consumed

        if self.game['resources']['food'] < 0:
            self.game['days_without_food'] += 1  # Increment days without food
            food_shortage = abs(self.game['resources']['food'])  # Calculate how much food is missing
            
            # Calculate deaths based on days without food
            if self.game['days_without_food'] == 2:
                deaths = min(random.randint(1, 50), self.game['total_followers'])
                self.game['total_followers'] -= deaths
                self.write_text(f"💀 {deaths} followers died from starvation!", '#f48771')
            elif self.game['days_without_food'] > 2:
                deaths = min(random.randint(50, 100), self.game['total_followers'])  # Increase risk of death over time
                self.game['total_followers'] -= deaths
                self.write_text(f"💀 {deaths} followers died from starvation!", '#f48771')
            
            self.game['resources']['food'] = 0  # Set food to 0

        else:
            self.game['days_without_food'] = 0  # Reset if food is available

        # **Check for Events**
        self.check_events()

        # **Increment Distance Traveled**
        distance_per_day = 10  # Example: distance traveled each day
        self.game['total_distance_traveled'] += distance_per_day
        self.game['distance_to_next_landmark'] -= distance_per_day

        if self.game['distance_to_next_landmark'] < 0:
            self.game['distance_to_next_landmark'] = 0  # Prevent negative distance

        # **Increment Day Count**
        self.game['day'] += 1
        self.update_status()
    
    def check_events(self):
        """Randomly encounter events during travel"""
        if random.random() < 0.2:  # 20% chance of an event
            self.resolve_event()
        else:
            self.write_text("The day passes without incident.", '#d7ba7d')
    
    def resolve_event(self):
        """Handle event resolution"""
        category = random.choice(['positive_events', 'negative_events', 'neutral_events'])
        event_key = random.choice(list(self.events[category].keys()))
        event = self.events[category][event_key]

        self.write_text(f"EVENT: {event['description']}", '#ff9800')

        # Choose an outcome (for now, we'll just take the first one)
        outcome = event['outcomes'][0]
        self.write_text(f"You chose: {outcome['text']}", '#dcdcaa')

        # Apply effects
        effects = outcome.get('effects', {})
        
        # Apply follower changes
        if 'followers' in effects:
            follower_change = effects['followers']
            change_value = random.randint(follower_change[0], follower_change[1])
            self.game['total_followers'] += change_value
            self.write_text(f"Followers changed by: {change_value}", '#dcdcaa')

        # Apply food changes
        if 'food' in effects:
            food_change = effects['food']
            change_value = random.randint(food_change[0], food_change[1])
            self.game['resources']['food'] += change_value
            self.write_text(f"Food changed by: {change_value}", '#dcdcaa')

        # Apply other effects similarly...

    def rest(self):
        """Placeholder for the rest function"""
        self.write_text("You take a moment to rest and recover.", '#dcdcaa')

    def hunt(self):
        """Placeholder for the hunt function"""
        self.write_text("You go hunting for food.", '#dcdcaa')

    def forage(self):
        """Placeholder for the forage function"""
        self.write_text("You search for edible plants and herbs.", '#dcdcaa')

    def game_over(self, message):
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