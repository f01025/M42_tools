import json
import os
import math
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconLeftWidget, IconRightWidget, OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform

# --- VERSION 6.0 (ROBUST LISTS) ---

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

DATA_FILE = "data.json"

# --- HELPER FUNCTIONS ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"accounts": {}, "cards": {}, "active_trades": {}}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if "accounts" not in data: data["accounts"] = {}
            if "cards" not in data: data["cards"] = {}
            if "active_trades" not in data: data["active_trades"] = {}
            return data
    except:
        return {"accounts": {}, "cards": {}, "active_trades": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_asset_path(name):
    # Map item names to filenames
    mapping = {
        "Hack Envelope": "hack.png", "Nobi Envelope": "nobi.png",
        "Beach Envelope": "beach.png", "Halloween Envelope": "halloween.png",
        "Xmas Envelope": "xmas.png", "Toy Envelope": "toy.png",
        "Ghost Envelope": "ghost.png", "NYPC Envelope": "nypc.png",
        "Santa Envelope": "santa.png", "10th Anniversary": "10thAni.png",
        "4th Anniversary": "4thAni.png", "Puni Envelope": "puni.png",
        "Negative Envelope": "neg.png", "Dice Envelope": "dice.png",
        "Surprise Envelope": "surp.png", "Luxury Envelope": "lux.png",
        "Basic Envelope": "bas.png"
    }
    filename = mapping.get(name, "hack.png") # Default fallback
    return os.path.join(os.path.dirname(__file__), 'assets', filename)

# --- BASE SCREEN ---
class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.1, 0.1, 0.1, 1)

# --- MENU SCREEN ---
class MenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="15dp", padding="30dp")
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        layout.adaptive_height = True

        title = MDLabel(text="ULTIMATE TOOLKIT", halign="center", font_style="H4", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        btns = [
            ("BLACK MARKET", (0.9, 0.3, 0.2, 1), 'market'),
            ("TIER CRAFTING", (0.2, 0.6, 0.8, 1), 'crafting'),
            ("MY INVENTORY", (0.3, 0.7, 0.3, 1), 'inventory_list'),
            ("TRADES", (0.8, 0.8, 0.2, 1), 'trade_list'),
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list')
        ]

        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="16sp", size_hint=(1, None), height="55dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)
        
        self.add_widget(layout)
        
        ver = MDLabel(text="v6.0", halign="right", theme_text_color="Secondary", font_style="Caption")
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

# --- 1. BLACK MARKET ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp")
        
        # Header
        header = MDBoxLayout(size_hint_y=None, height="50dp")
        header.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        container.add_widget(header)
        
        # Inputs
        input_card = MDCard(orientation='vertical', padding="15dp", spacing="15dp", size_hint_y=None, height="160dp", radius=[15])
        self.in_rub = MDTextField(hint_text="Rubles", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Luna", mode="rectangle", input_filter="float")
        input_card.add_widget(self.in_rub)
        input_card.add_widget(self.in_luna)
        container.add_widget(input_card)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        container.add_widget(btn)
        
        # Results
        grid = MDGridLayout(cols=2, spacing="10dp", size_hint_y=None, height="100dp")
        self.res_list = self.create_res_box("Listing Price", "0")
        self.res_rate = self.create_res_box("Exchange Rate", "0")
        grid.add_widget(self.res_list)
        grid.add_widget(self.res_rate)
        container.add_widget(grid)
        
        container.add_widget(MDLabel()) # Spacer
        self.add_widget(container)

    def create_res_box(self, title, value):
        card = MDCard(orientation='vertical', padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        card.add_widget(MDLabel(text=title, theme_text_color="Secondary", font_style="Caption"))
        lbl_v = MDLabel(text=value, theme_text_color="Custom", text_color=(0,1,0,1), font_style="H5", halign="center")
        card.add_widget(lbl_v)
        card.val_label = lbl_v
        return card

    def calc(self, _):
        try:
            rubles = float(self.in_rub.text)
            luna = float(self.in_luna.text)
            list_price = luna * 1.35
            rate = 0
            if rubles > 0: rate = (luna / rubles) * 1000000.0
            self.res_list.val_label.text = f"{math.ceil(list_price):,.0f}"
            self.res_rate.val_label.text = f"{int(rate):,.0f}"
        except:
            self.res_list.val_label.text = "Error"

# --- 2. CRAFTING ---
class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Simplified layout to prevent sizing issues
        main = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp")
        
        # Header
        head = MDBoxLayout(size_hint_y=None, height="50dp")
        head.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        head.add_widget(MDLabel(text="Tier Calculator", halign="center", font_style="H5"))
        main.add_widget(head)

        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing="15dp", adaptive_height=True)
        
        # Target
        content.add_widget(MDLabel(text="Target Item", theme_text_color="Secondary"))
        grid1 = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.in_qty = MDTextField(hint_text="Qty", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4/5/6)", mode="rectangle", input_filter="int")
        grid1.add_widget(self.in_qty)
        grid1.add_widget(self.in_tier)
        content.add_widget(grid1)
        
        # Inventory
        content.add_widget(MDLabel(text="Current Inventory", theme_text_color="Secondary"))
        grid2 = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.inv_t3 = MDTextField(hint_text="T3", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5", mode="rectangle", input_filter="int")
        self.inv_t6 = MDTextField(hint_text="T6", mode="rectangle", input_filter="int")
        grid2.add_widget(self.inv_t3)
        grid2.add_widget(self.inv_t4)
        grid2.add_widget(self.inv_t5)
        grid2.add_widget(self.inv_t6)
        content.add_widget(grid2)
        
        content.add_widget(MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), on_release=self.calc))
        
        self.res_lbl = MDLabel(text="Ready", halign="center", theme_text_color="Primary", size_hint_y=None, height="100dp")
        content.add_widget(self.res_lbl)
        
        scroll.add_widget(content)
        main.add_widget(scroll)
        self.add_widget(main)

    def calc(self, _):
        try:
            q = int(self.in_qty.text or 0)
            t = int(self.in_tier.text or 4)
            i3 = int(self.inv_t3.text or 0)
            i4 = int(self.inv_t4.text or 0)
            i5 = int(self.inv_t5.text or 0)
            i6 = int(self.inv_t6.text or 0)
            
            cost = {3:1, 4:4, 5:20, 6:120}
            if t not in cost: return
            
            needed = q * cost[t]
            owned = i3 + (i4*4) + (i5*20) + (i6*120)
            missing = needed - owned
            
            if missing <= 0:
                self.res_lbl.text = "Enough Resources!"
            else:
                t4_need = missing // 4
                t3_rem = missing % 4
                self.res_lbl.text = f"Need: {missing} T3\nOR\n{t4_need} T4 + {t3_rem} T3"
        except: pass

# --- 3. ADD ACCOUNT SCREEN ---
class AddAccountScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_screen = "" 
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="New Account", halign="center", font_style="H5"))
        self.field = MDTextField(hint_text="Account Name", mode="rectangle")
        layout.add_widget(self.field)
        layout.add_widget(MDFillRoundFlatButton(text="SAVE", on_release=self.save))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, target):
        self.target_screen = target
        self.field.text = ""

    def save(self, _):
        name = self.field.text.strip()
        if name:
            data = load_data()
            if self.target_screen == 'inventory_list':
                if name not in data["accounts"]: data["accounts"][name] = {"items": {}}
            elif self.target_screen == 'card_list':
                if name not in data["cards"]: data["cards"][name] = []
            save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = self.target_screen
        if hasattr(self.manager.get_screen(self.target_screen), 'refresh_list'):
            self.manager.get_screen(self.target_screen).refresh_list()

# --- 4. INVENTORY ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Header
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        h.add_widget(MDLabel(text="My Inventory", halign="center", font_style="H6"))
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)
        self.add_widget(layout)

    def on_enter(self):
        self.refresh_list()

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        accounts = data.get("accounts", {})
        if not accounts:
            self.list_view.add_widget(OneLineListItem(text="No Accounts Found"))
        for name in accounts:
            # Using basic list item to ensure stability
            item = TwoLineAvatarIconListItem(text=name, secondary_text="Tap to Open", on_release=lambda x, n=name: self.open_account(n))
            item.add_widget(IconLeftWidget(icon="account"))
            self.list_view.add_widget(item)

    def open_account(self, name):
        self.manager.get_screen('inventory_edit').load_account(name)
        self.manager.current = 'inventory_edit'

class InventoryEditScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical')
        
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=self.go_back))
        self.title_lbl = MDLabel(text="Items", halign="center", font_style="H6")
        h.add_widget(self.title_lbl)
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        f = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        f.add_widget(MDFillRoundFlatButton(text="ADD ITEM", on_release=self.show_selector))
        f.add_widget(MDIconButton(icon="trash-can", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_acc))
        layout.add_widget(f)
        self.add_widget(layout)

    def load_account(self, name):
        self.account_name = name
        self.title_lbl.text = name
        self.refresh_items()

    def refresh_items(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        
        for name, qty in items.items():
            # Check image existence safely
            path = get_asset_path(name)
            item = TwoLineAvatarIconListItem(text=name, secondary_text=f"Qty: {qty}", on_release=lambda x, n=name, q=qty: self.edit_item(n, q))
            
            if os.path.exists(path):
                item.add_widget(ImageLeftWidget(source=path))
            else:
                item.add_widget(IconLeftWidget(icon="cube"))
            
            self.list_view.add_widget(item)

    def show_selector(self, _):
        bs = MDGridBottomSheet()
        items = ["Hack Envelope", "Nobi Envelope", "Beach Envelope", "Halloween Envelope", 
                 "Xmas Envelope", "Toy Envelope", "Ghost Envelope", "NYPC Envelope", 
                 "Santa Envelope", "10th Anniversary", "4th Anniversary", "Puni Envelope", 
                 "Negative Envelope", "Dice Envelope", "Surprise Envelope", "Luxury Envelope", "Basic Envelope"]
        for i in items:
            path = get_asset_path(i)
            # Only add if icon exists to prevent bottom sheet crash
            if os.path.exists(path):
                bs.add_item(i, lambda x, n=i: self.ask_qty(n, bs), icon_src=path)
            else:
                # Fallback
                bs.add_item(i, lambda x, n=i: self.ask_qty(n, bs), icon_src="android")
        bs.open()

    def ask_qty(self, name, bs):
        bs.dismiss()
        self.manager.get_screen('edit_qty').setup(self.account_name, name, 0, 'inventory')
        self.manager.current = 'edit_qty'

    def edit_item(self, name, qty):
        self.manager.get_screen('edit_qty').setup(self.account_name, name, qty, 'inventory')
        self.manager.current = 'edit_qty'

    def delete_acc(self, _):
        data = load_data()
        if self.account_name in data["accounts"]:
            del data["accounts"][self.account_name]
            save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'inventory_list'
        self.manager.get_screen('inventory_list').refresh_list()

# --- GENERIC EDIT QUANTITY SCREEN ---
class EditQtyScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc = ""
        self.item = ""
        self.source = "" # 'inventory' or 'card'
        
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        self.lbl = MDLabel(text="Edit", halign="center", font_style="H5")
        layout.add_widget(self.lbl)
        
        self.field = MDTextField(hint_text="Quantity", input_filter="int", mode="rectangle")
        layout.add_widget(self.field)
        
        layout.add_widget(MDFillRoundFlatButton(text="SAVE", on_release=self.save))
        layout.add_widget(MDFillRoundFlatButton(text="DELETE ITEM", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_item))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, acc, item, qty, source):
        self.acc = acc
        self.item = item
        self.source = source
        self.lbl.text = f"{item}"
        self.field.text = str(qty)

    def save(self, _):
        if not self.field.text: return
        qty = int(self.field.text)
        data = load_data()
        if self.source == 'inventory':
            data["accounts"][self.acc]["items"][self.item] = qty
        save_data(data)
        self.go_back()

    def delete_item(self, _):
        data = load_data()
        if self.source == 'inventory':
            if self.item in data["accounts"][self.acc]["items"]:
                del data["accounts"][self.acc]["items"][self.item]
        save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        if self.source == 'inventory':
            self.manager.current = 'inventory_edit'
            self.manager.get_screen('inventory_edit').refresh_items()

# --- 5. TRADES ---
class TradeListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        h.add_widget(MDLabel(text="Select Account", halign="center"))
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def on_enter(self):
        self.list_view.clear_widgets()
        data = load_data()
        for name in data.get("accounts", {}):
            item = OneLineListItem(text=name, on_release=lambda x, n=name: self.open_recipients(n))
            self.list_view.add_widget(item)

    def open_recipients(self, name):
        self.manager.get_screen('trade_recipients').load_account(name)
        self.manager.current = 'trade_recipients'

class TradeRecipientsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        layout = MDBoxLayout(orientation='vertical')
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'trade_list')))
        self.lbl = MDLabel(text="Recipients", halign="center")
        h.add_widget(self.lbl)
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.8, 0.8, 0.2, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.add_rep)
        self.add_widget(fab)
        self.add_widget(layout)

    def load_account(self, name):
        self.acc_name = name
        self.lbl.text = f"Trades: {name}"
        self.refresh()

    def refresh(self):
        self.list_view.clear_widgets()
        data = load_data()
        reps = data["active_trades"].get(self.acc_name, {})
        for r in reps:
            count = len(reps[r])
            item = OneLineListItem(text=f"{r} ({count} items)", on_release=lambda x, n=r: self.open_details(n))
            self.list_view.add_widget(item)

    def add_rep(self, _):
        self.manager.get_screen('add_recipient').setup(self.acc_name)
        self.manager.current = 'add_recipient'

    def open_details(self, recipient):
        self.manager.get_screen('trade_details').load(self.acc_name, recipient)
        self.manager.current = 'trade_details'

class AddRecipientScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="Recipient Name", halign="center"))
        self.field = MDTextField(mode="rectangle")
        layout.add_widget(self.field)
        layout.add_widget(MDFillRoundFlatButton(text="OK", on_release=self.save))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, acc):
        self.acc = acc
        self.field.text = ""

    def save(self, _):
        if self.field.text:
            data = load_data()
            if self.acc not in data["active_trades"]: data["active_trades"][self.acc] = {}
            if self.field.text not in data["active_trades"][self.acc]: data["active_trades"][self.acc][self.field.text] = []
            save_data(data)
        self.cancel(None)

    def cancel(self, _):
        self.manager.current = 'trade_recipients'
        self.manager.get_screen('trade_recipients').load_account(self.acc)

class TradeDetailsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc = ""
        self.rep = ""
        layout = MDBoxLayout(orientation='vertical')
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=self.go_back))
        self.lbl = MDLabel(text="Trade", halign="center")
        h.add_widget(self.lbl)
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        btns = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        btns.add_widget(MDFillRoundFlatButton(text="ADD ITEM", on_release=self.show_sheet))
        btns.add_widget(MDFillRoundFlatButton(text="COMPLETE", md_bg_color=(0.2,0.8,0.2,1), on_release=self.complete))
        layout.add_widget(btns)
        self.add_widget(layout)

    def load(self, acc, rep):
        self.acc = acc
        self.rep = rep
        self.lbl.text = f"Trade: {rep}"
        self.refresh()

    def refresh(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["active_trades"].get(self.acc, {}).get(self.rep, [])
        for idx, item in enumerate(items):
            row = TwoLineAvatarIconListItem(text=item['name'], secondary_text=item['date'])
            # Cancel/Delete
            row.add_widget(IconRightWidget(icon="close-circle", on_release=lambda x, i=idx: self.cancel_item(i)))
            # Image
            path = get_asset_path(item['name'])
            if os.path.exists(path): row.add_widget(ImageLeftWidget(source=path))
            else: row.add_widget(IconLeftWidget(icon="cube"))
            self.list_view.add_widget(row)

    def show_sheet(self, _):
        bs = MDGridBottomSheet()
        items = ["Hack Envelope", "Nobi Envelope", "Beach Envelope", "Halloween Envelope", 
                 "Xmas Envelope", "Toy Envelope", "Ghost Envelope", "NYPC Envelope", 
                 "Santa Envelope", "10th Anniversary", "4th Anniversary", "Puni Envelope", 
                 "Negative Envelope", "Dice Envelope", "Surprise Envelope", "Luxury Envelope", "Basic Envelope"]
        for i in items:
            path = get_asset_path(i)
            if os.path.exists(path): bs.add_item(i, lambda x, n=i: self.add(n, bs), icon_src=path)
            else: bs.add_item(i, lambda x, n=i: self.add(n, bs), icon_src="android")
        bs.open()

    def add(self, name, bs):
        bs.dismiss()
        data = load_data()
        curr = data["accounts"].get(self.acc, {}).get("items", {}).get(name, 0)
        if curr > 0:
            data["accounts"][self.acc]["items"][name] = curr - 1
            date = datetime.now().strftime("%Y-%m-%d")
            data["active_trades"][self.acc][self.rep].append({"name": name, "date": date})
            save_data(data)
            self.refresh()

    def cancel_item(self, idx):
        data = load_data()
        item = data["active_trades"][self.acc][self.rep].pop(idx)
        # Refund
        curr = data["accounts"][self.acc]["items"].get(item['name'], 0)
        data["accounts"][self.acc]["items"][item['name']] = curr + 1
        save_data(data)
        self.refresh()

    def complete(self, _):
        data = load_data()
        del data["active_trades"][self.acc][self.rep]
        save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'trade_recipients'
        self.manager.get_screen('trade_recipients').load_account(self.acc)

# --- 6. CARDS ---
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        h.add_widget(MDLabel(text="Card Accounts", halign="center"))
        layout.add_widget(h)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.6, 0.3, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)
        self.add_widget(layout)

    def on_enter(self):
        self.list_view.clear_widgets()
        data = load_data()
        for name in data.get("cards", {}):
            item = TwoLineAvatarIconListItem(text=name, secondary_text="Open", on_release=lambda x, n=name: self.open(n))
            item.add_widget(IconLeftWidget(icon="cards"))
            self.list_view.add_widget(item)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def open(self, name):
        self.manager.get_screen('card_edit').load(name)
        self.manager.current = 'card_edit'

class CardEditScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc = ""
        layout = MDBoxLayout(orientation='vertical')
        h = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        h.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'card_list')))
        self.lbl = MDLabel(text="Cards", halign="center")
        h.add_widget(self.lbl)
        layout.add_widget(h)

        # Form
        form = MDBoxLayout(orientation='vertical', size_hint_y=None, height="120dp", padding="10dp")
        r1 = MDBoxLayout(spacing="10dp")
        self.name = MDTextField(hint_text="Name")
        self.tier = MDTextField(hint_text="Tier")
        r1.add_widget(self.name)
        r1.add_widget(self.tier)
        
        r2 = MDBoxLayout(spacing="10dp")
        self.qty = MDTextField(hint_text="Qty")
        btn = MDRaisedButton(text="ADD", on_release=self.add)
        r2.add_widget(self.qty)
        r2.add_widget(btn)
        
        form.add_widget(r1)
        form.add_widget(r2)
        layout.add_widget(form)

        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)
        
        del_btn = MDFillRoundFlatButton(text="DELETE ACCOUNT", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete)
        layout.add_widget(del_btn)
        self.add_widget(layout)

    def load(self, name):
        self.acc = name
        self.lbl.text = name
        self.refresh()

    def refresh(self):
        self.list_view.clear_widgets()
        data = load_data()
        cards = data["cards"].get(self.acc, [])
        for i, c in enumerate(cards):
            row = TwoLineAvatarIconListItem(text=c['name'], secondary_text=f"T{c['tier']} - Qty: {c['qty']}")
            row.add_widget(IconLeftWidget(icon="card-account-details"))
            row.add_widget(IconRightWidget(icon="delete", on_release=lambda x, idx=i: self.del_card(idx)))
            self.list_view.add_widget(row)

    def add(self, _):
        if self.name.text and self.qty.text:
            data = load_data()
            new = {"name": self.name.text, "tier": self.tier.text, "qty": int(self.qty.text)}
            data["cards"][self.acc].append(new)
            save_data(data)
            self.refresh()

    def del_card(self, idx):
        data = load_data()
        del data["cards"][self.acc][idx]
        save_data(data)
        self.refresh()

    def delete(self, _):
        data = load_data()
        del data["cards"][self.acc]
        save_data(data)
        self.manager.current = 'card_list'

# --- APP ---
class UltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(CraftingScreen(name='crafting'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(InventoryListScreen(name='inventory_list'))
        sm.add_widget(InventoryEditScreen(name='inventory_edit'))
        sm.add_widget(EditQtyScreen(name='edit_qty'))
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(TradeRecipientsScreen(name='trade_recipients'))
        sm.add_widget(AddRecipientScreen(name='add_recipient'))
        sm.add_widget(TradeDetailsScreen(name='trade_details'))
        sm.add_widget(CardListScreen(name='card_list'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        return sm

if __name__ == '__main__':
    UltimateApp().run()
