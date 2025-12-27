import json
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, ThreeLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

# --- WINDOW SIZE FOR PC TESTING ---
if platform not in ['android', 'ios']:
    Window.size = (360, 800)

# --- DATABASE MANAGER ---
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"accounts": {}, "cards": {}, "trades": []}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if "accounts" not in data: data["accounts"] = {}
            if "cards" not in data: data["cards"] = {}
            if "trades" not in data: data["trades"] = []
            return data
    except:
        return {"accounts": {}, "cards": {}, "trades": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- ASSET MAPPING ---
ITEM_MAP = {
    "Hack Envelope": "assets/hack.png",
    "Nobi Envelope": "assets/nobi.png",
    "Beach Envelope": "assets/beach.png",
    "Halloween Envelope": "assets/halloween.png",
    "Xmas Envelope": "assets/xmas.png",
    "Toy Envelope": "assets/toy.png",
    "Ghost Envelope": "assets/ghost.png",
    "NYPC Envelope": "assets/nypc.png",
    "Santa Envelope": "assets/santa.png",
    "10th Anniversary": "assets/10thAni.png",
    "4th Anniversary": "assets/4thAni.png",
    "Puni Envelope": "assets/puni.png",
    "Negative Envelope": "assets/neg.png",
    "Dice Envelope": "assets/dice.png",
    "Surprise Envelope": "assets/surp.png",
    "Luxury Envelope": "assets/lux.png",
    "Basic Envelope": "assets/bas.png"
}

# --- SCREENS ---

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="15dp", padding="30dp")
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        layout.adaptive_height = True

        title = MDLabel(text="ULTIMATE TOOLKIT", halign="center", font_style="H4", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        
        btns = [
            ("BLACK MARKET", (0.9, 0.3, 0.2, 1), 'market'),
            ("TIER CRAFTING", (0.2, 0.6, 0.8, 1), 'crafting'),
            ("INVENTORY", (0.3, 0.7, 0.3, 1), 'inventory_list'),
            ("TRADES", (0.8, 0.8, 0.2, 1), 'trade_list'),
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list')
        ]

        layout.add_widget(title)
        
        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="16sp", size_hint=(1, None), height="55dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)

        self.add_widget(layout)

    def go_to(self, route):
        self.manager.current = route
        screen = self.manager.get_screen(route)
        if hasattr(screen, 'refresh_list'):
            screen.refresh_list()

# --- OPTION 1: BLACK MARKET (FIXED UI & MATH) ---
class MarketScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        
        # Header
        container.add_widget(MDLabel(text="Black Market", halign="center", font_style="H4"))
        
        # Inputs Card
        input_card = MDCard(orientation='vertical', padding="15dp", spacing="15dp", size_hint_y=None, height="220dp", radius=[15])
        self.in_rub = MDTextField(hint_text="Target Net Rubles (Profit)", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Qty Luna (Resources)", mode="rectangle", input_filter="float")
        self.in_tax = MDTextField(text="35", hint_text="Tax %", mode="rectangle", input_filter="int")
        
        input_card.add_widget(self.in_rub)
        input_card.add_widget(self.in_luna)
        input_card.add_widget(self.in_tax)
        container.add_widget(input_card)
        
        # Calculate Button
        btn = MDFillRoundFlatButton(text="CALCULATE DEAL", size_hint=(1, None), height="50dp", md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        container.add_widget(btn)
        
        # Results Grid
        grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.res_list = self.create_res_box("Listing Price (Unit)", "0")
        self.res_rate = self.create_res_box("Real Exchange Rate", "0")
        grid.add_widget(self.res_list)
        grid.add_widget(self.res_rate)
        container.add_widget(grid)
        
        # Back Button
        container.add_widget(MDFillRoundFlatButton(text="BACK TO MENU", md_bg_color=(0.4, 0.4, 0.4, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        
        scroll.add_widget(container)
        self.add_widget(scroll)

    def create_res_box(self, title, value):
        card = MDCard(orientation='vertical', padding="10dp", size_hint_y=None, height="100dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        lbl_t = MDLabel(text=title, theme_text_color="Secondary", font_style="Caption")
        lbl_v = MDLabel(text=value, theme_text_color="Custom", text_color=(0,1,0,1), font_style="H5", halign="center")
        card.add_widget(lbl_t)
        card.add_widget(lbl_v)
        card.val_label = lbl_v
        return card

    def calc(self, _):
        try:
            net_target = float(self.in_rub.text)
            qty_luna = float(self.in_luna.text)
            tax_percent = float(self.in_tax.text) / 100.0
            
            if qty_luna > 0:
                # Math: Gross = Net / (1 - Tax)
                gross_total = net_target / (1.0 - tax_percent)
                
                # Unit Listing Price
                unit_price = gross_total / qty_luna
                
                # Exchange Rate (Profit per Luna)
                rate = net_target / qty_luna
                
                self.res_list.val_label.text = f"{unit_price:,.0f}"
                self.res_rate.val_label.text = f"{rate:,.0f}"
        except:
            self.res_list.val_label.text = "Error"

# --- OPTION 2: CRAFTING (FIXED LOGIC & INPUTS) ---
class CraftingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        container.add_widget(MDLabel(text="Tier Calculator", halign="center", font_style="H4"))
        
        # Target
        container.add_widget(MDLabel(text="I Want To Make:", theme_text_color="Secondary"))
        grid_target = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.in_qty = MDTextField(hint_text="Qty Cards", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4, 5, or 6)", mode="rectangle", input_filter="int")
        grid_target.add_widget(self.in_qty)
        grid_target.add_widget(self.in_tier)
        container.add_widget(grid_target)
        
        # Inventory (Restored!)
        container.add_widget(MDLabel(text="I Currently Have:", theme_text_color="Secondary"))
        grid_inv = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.inv_t3 = MDTextField(hint_text="T3 Count", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4 Count", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5 Count", mode="rectangle", input_filter="int")
        self.inv_t6 = MDTextField(hint_text="T6 Count", mode="rectangle", input_filter="int")
        
        grid_inv.add_widget(self.inv_t3)
        grid_inv.add_widget(self.inv_t4)
        grid_inv.add_widget(self.inv_t5)
        grid_inv.add_widget(self.inv_t6)
        container.add_widget(grid_inv)
        
        btn = MDFillRoundFlatButton(text="CALCULATE COST", size_hint=(1, None), height="50dp", md_bg_color=(0.2, 0.6, 0.8, 1), on_release=self.calc)
        container.add_widget(btn)
        
        self.res = MDLabel(text="Ready", halign="center", size_hint_y=None, height="100dp")
        container.add_widget(self.res)
        
        container.add_widget(MDFillRoundFlatButton(text="BACK", md_bg_color=(0.4,0.4,0.4,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        scroll.add_widget(container)
        self.add_widget(scroll)

    def calc(self, _):
        try:
            # Inputs
            q_target = int(self.in_qty.text or 0)
            t_target = int(self.in_tier.text or 4)
            
            # Inventory
            i3 = int(self.inv_t3.text or 0)
            i4 = int(self.inv_t4.text or 0)
            i5 = int(self.inv_t5.text or 0)
            i6 = int(self.inv_t6.text or 0)
            
            # Logic: Convert EVERYTHING to "T3 Units" to compare
            # Based on user: 1 T5 = 20 T3. 1 T4 = 4 T3.
            # Multipliers: T3=1, T4=4, T5=20, T6=100
            
            cost_map = {3:1, 4:4, 5:20, 6:100}
            
            if t_target not in cost_map:
                self.res.text = "Invalid Tier (Use 4, 5, or 6)"
                return
            
            total_needed_t3_units = q_target * cost_map[t_target]
            
            current_t3_units = (i3 * 1) + (i4 * 4) + (i5 * 20) + (i6 * 100)
            
            missing_t3_units = total_needed_t3_units - current_t3_units
            
            if missing_t3_units <= 0:
                self.res.text = "You have enough resources!"
                self.res.text_color = (0, 1, 0, 1)
            else:
                # Show result in T3 terms, but maybe suggest higher tiers?
                self.res.text = f"MISSING RESOURCES:\n{missing_t3_units} Tier 3 Cards\n(Or {missing_t3_units/4:.1f} T4s)"
                self.res.text_color = (1, 0, 0, 1)

        except: 
            self.res.text = "Error in calculation"

# --- HELPER SCREEN: ADD ACCOUNT (CRASH FIX) ---
# Replaces MDDialog which crashes on Android
class AddAccountScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_screen = "" # Where to go back to (inventory or cards)
        
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        
        layout.add_widget(MDLabel(text="Create New Account", halign="center", font_style="H5"))
        
        self.field = MDTextField(hint_text="Enter Account Name", mode="rectangle")
        layout.add_widget(self.field)
        
        btn_save = MDFillRoundFlatButton(text="SAVE ACCOUNT", size_hint=(1, None), md_bg_color=(0.2, 0.8, 0.2, 1), on_release=self.save)
        layout.add_widget(btn_save)
        
        btn_cancel = MDFlatButton(text="CANCEL", size_hint=(1, None), on_release=self.cancel)
        layout.add_widget(btn_cancel)
        
        # Spacer
        layout.add_widget(MDLabel())
        
        self.add_widget(layout)

    def setup(self, target):
        self.target_screen = target
        self.field.text = ""

    def save(self, _):
        name = self.field.text.strip()
        if not name: return
        
        data = load_data()
        
        if self.target_screen == 'inventory_list':
            if name not in data["accounts"]:
                data["accounts"][name] = {"items": {}}
        elif self.target_screen == 'card_list':
            if name not in data["cards"]:
                data["cards"][name] = []
        
        save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = self.target_screen
        # Refresh the list of the target screen
        screen = self.manager.get_screen(self.target_screen)
        if hasattr(screen, 'refresh_list'):
            screen.refresh_list()

# --- OPTION 3: INVENTORY ---
class InventoryListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        toolbar.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Inventory Accounts", halign="center", font_style="H6"))
        
        # FIX: Button now goes to AddAccountScreen instead of crashing Dialog
        toolbar.add_widget(MDIconButton(icon="account-plus", on_release=self.go_add))
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        for name, details in data.get("accounts", {}).items():
            item = TwoLineAvatarIconListItem(
                text=name, 
                secondary_text=f"Items: {len(details.get('items', {}))}",
                on_release=lambda x, n=name: self.open_account(n)
            )
            icon_src = "assets/bas.png" if os.path.exists("assets/bas.png") else "assets/hack.png"
            if os.path.exists(icon_src):
                item.add_widget(ImageLeftWidget(source=icon_src))
            else:
                item.add_widget(IconRightWidget(icon="account"))
            self.list_view.add_widget(item)

    def open_account(self, name):
        self.manager.get_screen('inventory_edit').load_account(name)
        self.manager.current = 'inventory_edit'

class InventoryEditScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        toolbar.add_widget(MDIconButton(icon="arrow-left", on_release=self.go_back))
        self.toolbar_lbl = MDLabel(text="Inventory", halign="center", font_style="H6")
        toolbar.add_widget(self.toolbar_lbl)
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        footer = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        footer.add_widget(MDFillRoundFlatButton(text="ADD ITEM", size_hint_x=0.7, on_release=self.show_item_selector))
        footer.add_widget(MDIconButton(icon="trash-can", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account))
        layout.add_widget(footer)
        self.add_widget(layout)
        self.qty_dialog = None
        self.selected_item_temp = None

    def load_account(self, name):
        self.account_name = name
        self.toolbar_lbl.text = name
        self.refresh_items()

    def refresh_items(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        for item_name, qty in items.items():
            img_src = ITEM_MAP.get(item_name, "assets/hack.png")
            if not os.path.exists(img_src): img_src = "assets/hack.png"
            row = TwoLineAvatarIconListItem(text=item_name, secondary_text=f"Quantity: {qty}")
            row.add_widget(ImageLeftWidget(source=img_src))
            row.add_widget(IconRightWidget(icon="delete", on_release=lambda x, i=item_name: self.delete_single_item(i)))
            self.list_view.add_widget(row)

    def show_item_selector(self, _):
        bottom_sheet = MDGridBottomSheet()
        for name, src in ITEM_MAP.items():
            if not os.path.exists(src): continue
            bottom_sheet.add_item(name, lambda x, n=name: self.ask_qty(n), icon_src=src)
        bottom_sheet.open()

    def ask_qty(self, item_name):
        self.selected_item_temp = item_name
        self.qty_field = MDTextField(hint_text="Enter Quantity", input_filter="int")
        self.qty_dialog = MDDialog(
            title=f"Add {item_name}",
            type="custom",
            content_cls=self.qty_field,
            buttons=[MDRaisedButton(text="ADD", on_release=self.add_item_confirm)]
        )
        self.qty_dialog.open()

    def add_item_confirm(self, _):
        if self.qty_field.text:
            qty = int(self.qty_field.text)
            data = load_data()
            curr = data["accounts"][self.account_name]["items"].get(self.selected_item_temp, 0)
            data["accounts"][self.account_name]["items"][self.selected_item_temp] = curr + qty
            save_data(data)
            self.refresh_items()
        self.qty_dialog.dismiss()

    def delete_single_item(self, item_name):
        data = load_data()
        if item_name in data["accounts"][self.account_name]["items"]:
            del data["accounts"][self.account_name]["items"][item_name]
            save_data(data)
            self.refresh_items()

    def delete_account(self, _):
        data = load_data()
        if self.account_name in data["accounts"]:
            del data["accounts"][self.account_name]
            save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'inventory_list'
        self.manager.get_screen('inventory_list').refresh_list()

# --- OPTION 4: TRADES ---
class TradeListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        toolbar.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Select Trader", halign="center"))
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        for name in data.get("accounts", {}):
            item = TwoLineAvatarIconListItem(text=name, secondary_text="Tap to trade", on_release=lambda x, n=name: self.open_trade(n))
            item.add_widget(IconRightWidget(icon="handshake"))
            self.list_view.add_widget(item)

    def open_trade(self, name):
        self.manager.get_screen('trade_action').load_account(name)
        self.manager.current = 'trade_action'

class TradeActionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        
        self.lbl_title = MDLabel(text="New Trade", halign="center", font_style="H5")
        layout.add_widget(self.lbl_title)

        self.btn_item = MDFillRoundFlatButton(text="SELECT ITEM FROM INVENTORY", on_release=self.open_item_sheet)
        layout.add_widget(self.btn_item)

        self.in_ign = MDTextField(hint_text="Recipient IGN")
        self.in_qty = MDTextField(hint_text="Quantity", input_filter="int")
        
        layout.add_widget(self.in_ign)
        layout.add_widget(self.in_qty)

        btn = MDFillRoundFlatButton(text="CONFIRM TRADE", md_bg_color=(0.8, 0.8, 0.2, 1), on_release=self.process_trade)
        layout.add_widget(btn)

        self.lbl_status = MDLabel(text="Ready", halign="center", theme_text_color="Secondary")
        layout.add_widget(self.lbl_status)

        layout.add_widget(MDFillRoundFlatButton(text="BACK", on_release=self.go_back))
        self.add_widget(layout)
        self.selected_item = None

    def load_account(self, name):
        self.account_name = name
        self.lbl_title.text = f"Trading from: {name}"
        self.selected_item = None
        self.btn_item.text = "SELECT ITEM FROM INVENTORY"
        self.lbl_status.text = "Ready"

    def open_item_sheet(self, _):
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        if not items:
            self.lbl_status.text = "Inventory is empty!"
            return

        bottom_sheet = MDGridBottomSheet()
        for name, qty in items.items():
            src = ITEM_MAP.get(name, "assets/hack.png")
            if not os.path.exists(src): src = "assets/hack.png"
            bottom_sheet.add_item(f"{name} ({qty})", lambda x, n=name: self.select_item(n), icon_src=src)
        bottom_sheet.open()

    def select_item(self, name):
        self.selected_item = name
        self.btn_item.text = f"Selected: {name}"

    def process_trade(self, _):
        ign = self.in_ign.text
        if not self.selected_item:
            self.lbl_status.text = "Please select an item."
            return
        try:
            qty = int(self.in_qty.text)
        except:
            self.lbl_status.text = "Invalid Quantity"
            return

        data = load_data()
        inventory = data["accounts"][self.account_name]["items"]
        
        if self.selected_item in inventory and inventory[self.selected_item] >= qty:
            inventory[self.selected_item] -= qty
            log = {"from": self.account_name, "to": ign, "item": self.selected_item, "qty": qty}
            data["trades"].append(log)
            save_data(data)
            self.lbl_status.text = f"Sent {qty} {self.selected_item} to {ign}!"
            self.lbl_status.text_color = (0, 1, 0, 1)
        else:
            self.lbl_status.text = "Not enough items in inventory."
            self.lbl_status.text_color = (1, 0, 0, 1)

    def go_back(self, _):
        self.manager.current = 'trade_list'

# --- OPTION 5: CARDS ---
class CardListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        toolbar.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Card Accounts", halign="center"))
        
        # FIX: Button now goes to AddAccountScreen
        toolbar.add_widget(MDIconButton(icon="account-plus", on_release=self.go_add))
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        for name in data.get("cards", {}):
            item = TwoLineAvatarIconListItem(text=name, secondary_text="Tap to view cards", on_release=lambda x, n=name: self.open_cards(n))
            item.add_widget(IconRightWidget(icon="cards"))
            self.list_view.add_widget(item)

    def open_cards(self, name):
        self.manager.get_screen('card_edit').load_account(name)
        self.manager.current = 'card_edit'

class CardEditScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="10dp")
        
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        toolbar.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'card_list')))
        self.title_lbl = MDLabel(text="Cards", halign="center")
        toolbar.add_widget(self.title_lbl)
        layout.add_widget(toolbar)

        form = MDBoxLayout(orientation='vertical', size_hint_y=None, height="140dp", padding="10dp", spacing="5dp")
        row1 = MDBoxLayout(spacing="10dp")
        self.in_name = MDTextField(hint_text="Card Name")
        self.in_tier = MDTextField(hint_text="Tier (1-6)", size_hint_x=0.3, input_filter="int")
        row1.add_widget(self.in_name)
        row1.add_widget(self.in_tier)
        
        row2 = MDBoxLayout(spacing="10dp")
        self.in_qty = MDTextField(hint_text="Qty", input_filter="int")
        btn = MDRaisedButton(text="ADD CARD", on_release=self.add_card)
        row2.add_widget(self.in_qty)
        row2.add_widget(btn)

        form.add_widget(row1)
        form.add_widget(row2)
        layout.add_widget(form)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        del_btn = MDFillRoundFlatButton(text="DELETE ACCOUNT", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account)
        layout.add_widget(del_btn)
        
        self.add_widget(layout)

    def load_account(self, name):
        self.account_name = name
        self.title_lbl.text = f"{name}'s Cards"
        self.refresh_list()

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        cards = data["cards"].get(self.account_name, [])
        for i, c in enumerate(cards):
            row = ThreeLineListItem(text=c['name'], secondary_text=f"Tier: {c['tier']}", tertiary_text=f"Qty: {c['qty']}")
            row.add_widget(IconRightWidget(icon="delete", on_release=lambda x, idx=i: self.delete_card(idx)))
            self.list_view.add_widget(row)

    def add_card(self, _):
        if self.in_name.text and self.in_qty.text:
            data = load_data()
            new_card = {"name": self.in_name.text, "tier": self.in_tier.text, "qty": int(self.in_qty.text)}
            data["cards"][self.account_name].append(new_card)
            save_data(data)
            self.refresh_list()
            self.in_name.text = ""
            self.in_qty.text = ""

    def delete_card(self, index):
        data = load_data()
        del data["cards"][self.account_name][index]
        save_data(data)
        self.refresh_list()

    def delete_account(self, _):
        data = load_data()
        if self.account_name in data["cards"]:
            del data["cards"][self.account_name]
            save_data(data)
        self.manager.current = 'card_list'
        self.manager.get_screen('card_list').refresh_list()

class UltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(CraftingScreen(name='crafting'))
        sm.add_widget(InventoryListScreen(name='inventory_list'))
        sm.add_widget(InventoryEditScreen(name='inventory_edit'))
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(TradeActionScreen(name='trade_action'))
        sm.add_widget(CardListScreen(name='card_list'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        
        # New helper screen for adding accounts (Crash Fix)
        sm.add_widget(AddAccountScreen(name='add_account'))
        
        return sm

if __name__ == '__main__':
    UltimateApp().run()
