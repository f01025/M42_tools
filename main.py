import json
import os
import math
from datetime import datetime
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, ThreeLineIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform

# --- WINDOW SIZE FOR PC TESTING ---
if platform not in ['android', 'ios']:
    Window.size = (360, 800)

# --- DATABASE MANAGER ---
DATA_FILE = "data.json"

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

# --- MENU SCREEN ---
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
        self.manager.transition = NoTransition()
        self.manager.current = route

# --- 1. BLACK MARKET ---
class MarketScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        container.add_widget(MDLabel(text="Black Market", halign="center", font_style="H4"))
        
        input_card = MDCard(orientation='vertical', padding="15dp", spacing="15dp", size_hint_y=None, height="160dp", radius=[15])
        self.in_rub = MDTextField(hint_text="Rubles", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Luna", mode="rectangle", input_filter="float")
        input_card.add_widget(self.in_rub)
        input_card.add_widget(self.in_luna)
        container.add_widget(input_card)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        container.add_widget(btn)
        
        grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.res_list = self.create_res_box("Listing Price", "0")
        self.res_rate = self.create_res_box("Exchange Rate", "0")
        grid.add_widget(self.res_list)
        grid.add_widget(self.res_rate)
        container.add_widget(grid)
        
        container.add_widget(MDFillRoundFlatButton(text="BACK", md_bg_color=(0.4, 0.4, 0.4, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
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
            rubles = float(self.in_rub.text)
            luna = float(self.in_luna.text)
            
            # Listing Price = Luna * 1.35
            list_price = luna * 1.35
            
            # Exchange Rate = (Luna / Rubles) * 1,000,000
            rate = 0
            if rubles > 0:
                rate = (luna / rubles) * 1000000.0
            
            self.res_list.val_label.text = f"{math.ceil(list_price):,.0f}"
            self.res_rate.val_label.text = f"{int(rate):,.0f}"
        except:
            self.res_list.val_label.text = "Error"

# --- 2. CRAFTING ---
class CraftingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        container.add_widget(MDLabel(text="Tier Calculator", halign="center", font_style="H4"))
        
        container.add_widget(MDLabel(text="I Want To Make:", theme_text_color="Secondary"))
        grid_target = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.in_qty = MDTextField(hint_text="Qty Cards", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4, 5, or 6)", mode="rectangle", input_filter="int")
        grid_target.add_widget(self.in_qty)
        grid_target.add_widget(self.in_tier)
        container.add_widget(grid_target)
        
        container.add_widget(MDLabel(text="I Have:", theme_text_color="Secondary"))
        grid_inv = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.inv_t3 = MDTextField(hint_text="T3", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5", mode="rectangle", input_filter="int")
        self.inv_t6 = MDTextField(hint_text="T6", mode="rectangle", input_filter="int")
        grid_inv.add_widget(self.inv_t3)
        grid_inv.add_widget(self.inv_t4)
        grid_inv.add_widget(self.inv_t5)
        grid_inv.add_widget(self.inv_t6)
        container.add_widget(grid_inv)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.2, 0.6, 0.8, 1), on_release=self.calc)
        container.add_widget(btn)
        
        self.res_card = MDCard(orientation='vertical', padding="15dp", spacing="10dp", size_hint_y=None, height="200dp", md_bg_color=(0.15, 0.15, 0.15, 1))
        self.res_opt1 = MDLabel(text="", theme_text_color="Primary", font_style="Body1", halign="center")
        self.res_opt2 = MDLabel(text="", theme_text_color="Custom", text_color=(0.4, 0.8, 1, 1), font_style="Body1", halign="center")
        self.res_card.add_widget(MDLabel(text="Missing Resources", theme_text_color="Secondary", font_style="Caption", halign="center"))
        self.res_card.add_widget(self.res_opt1)
        self.res_card.add_widget(self.res_opt2)
        container.add_widget(self.res_card)
        
        container.add_widget(MDFillRoundFlatButton(text="BACK", md_bg_color=(0.4,0.4,0.4,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        scroll.add_widget(container)
        self.add_widget(scroll)

    def calc(self, _):
        try:
            q_target = int(self.in_qty.text or 0)
            t_target = int(self.in_tier.text or 4)
            i3 = int(self.inv_t3.text or 0)
            i4 = int(self.inv_t4.text or 0)
            i5 = int(self.inv_t5.text or 0)
            i6 = int(self.inv_t6.text or 0)
            
            cost_map = {3:1, 4:4, 5:20, 6:120}
            if t_target not in cost_map:
                self.res_opt1.text = "Invalid Tier"
                return
            
            total_needed = q_target * cost_map[t_target]
            owned = (i3 * 1) + (i4 * 4) + (i5 * 20) + (i6 * 100)
            missing = total_needed - owned
            
            if missing <= 0:
                self.res_opt1.text = "You have enough resources!"
                self.res_opt2.text = ""
            else:
                self.res_opt1.text = f"OPTION A:\n{missing} x T3 Cards"
                t4_needed = missing // 4
                t3_rem = missing % 4
                self.res_opt2.text = f"OPTION B:\n{t4_needed} x T4  +  {t3_rem} x T3"
        except: 
            self.res_opt1.text = "Calculation Error"

# --- 3. ADD ACCOUNT SCREEN ---
class AddAccountScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_screen = "" 
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="Create New Account", halign="center", font_style="H5"))
        self.field = MDTextField(hint_text="Enter Account Name", mode="rectangle")
        layout.add_widget(self.field)
        btn_save = MDFillRoundFlatButton(text="SAVE ACCOUNT", size_hint=(1, None), md_bg_color=(0.2, 0.8, 0.2, 1), on_release=self.save)
        layout.add_widget(btn_save)
        btn_cancel = MDFlatButton(text="CANCEL", size_hint=(1, None), on_release=self.cancel)
        layout.add_widget(btn_cancel)
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
            if name not in data["accounts"]: data["accounts"][name] = {"items": {}}
        elif self.target_screen == 'card_list':
            if name not in data["cards"]: data["cards"][name] = []
        save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = self.target_screen

# --- 4. INVENTORY LIST ---
class InventoryListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # NAVIGATION BAR
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        # FIXED: Custom WHITE icon color so it is visible
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Inventory", halign="center", font_style="H6"))
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

        self.empty_lbl = MDLabel(text="No Accounts. Tap +", halign="center", valign="center", theme_text_color="Secondary")
        self.add_widget(self.empty_lbl)

    def on_enter(self):
        # CRASH FIX: Schedule this to run AFTER the screen loads
        Clock.schedule_once(self.refresh_list, 0.1)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        accounts = data.get("accounts", {})
        
        if not accounts:
            self.empty_lbl.opacity = 1
        else:
            self.empty_lbl.opacity = 0
            for name, details in accounts.items():
                item = TwoLineAvatarIconListItem(
                    text=name, 
                    secondary_text=f"Items: {len(details.get('items', {}))}",
                    on_release=lambda x, n=name: self.open_account(n)
                )
                icon_src = "assets/bas.png" if os.path.exists("assets/bas.png") else "assets/hack.png"
                if os.path.exists(icon_src): item.add_widget(ImageLeftWidget(source=icon_src))
                else: item.add_widget(IconRightWidget(icon="account"))
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
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=self.go_back))
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
        self.bs = None

    def load_account(self, name):
        self.account_name = name
        self.toolbar_lbl.text = name
        # Crash Fix: Schedule refresh
        Clock.schedule_once(self.refresh_items, 0.1)

    def refresh_items(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        for item_name, qty in items.items():
            img_src = ITEM_MAP.get(item_name, "assets/hack.png")
            if not os.path.exists(img_src): img_src = "assets/hack.png"
            row = TwoLineAvatarIconListItem(
                text=item_name, 
                secondary_text=f"Quantity: {qty}",
                on_release=lambda x, i=item_name, q=qty: self.edit_item(i, q)
            )
            row.add_widget(ImageLeftWidget(source=img_src))
            self.list_view.add_widget(row)

    def show_item_selector(self, _):
        self.bs = MDGridBottomSheet()
        for name, src in ITEM_MAP.items():
            if not os.path.exists(src): continue
            self.bs.add_item(name, lambda x, n=name: self.ask_qty(n), icon_src=src)
        self.bs.open()

    def ask_qty(self, item_name):
        if self.bs: self.bs.dismiss()
        self.manager.get_screen('edit_item_qty').setup(self.account_name, item_name, 0, mode="add")
        self.manager.current = 'edit_item_qty'

    def edit_item(self, item_name, current_qty):
        self.manager.get_screen('edit_item_qty').setup(self.account_name, item_name, current_qty, mode="edit")
        self.manager.current = 'edit_item_qty'

    def delete_account(self, _):
        data = load_data()
        if self.account_name in data["accounts"]:
            del data["accounts"][self.account_name]
            save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'inventory_list'

class EditItemQtyScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        self.item_name = ""
        self.mode = "add"
        
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        self.title_lbl = MDLabel(text="Item", halign="center", font_style="H5")
        layout.add_widget(self.title_lbl)
        
        card = MDCard(orientation='vertical', padding="20dp", spacing="10dp", size_hint_y=None, height="150dp")
        self.field = MDTextField(hint_text="Quantity", input_filter="int", mode="rectangle", font_size="24sp", halign="center")
        card.add_widget(self.field)
        layout.add_widget(card)
        
        self.btn_save = MDFillRoundFlatButton(text="SAVE", size_hint=(1, None), on_release=self.save)
        layout.add_widget(self.btn_save)
        
        self.btn_del = MDFillRoundFlatButton(text="DELETE ITEM", size_hint=(1, None), md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_item)
        layout.add_widget(self.btn_del)
        
        layout.add_widget(MDFlatButton(text="CANCEL", size_hint=(1, None), on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, acc, item, qty, mode):
        self.acc_name = acc
        self.item_name = item
        self.mode = mode
        if mode == "add":
            self.title_lbl.text = f"Add {item}"
            self.field.text = ""
            self.btn_save.text = "ADD TO INVENTORY"
            self.btn_del.opacity = 0 
            self.btn_del.disabled = True
        else:
            self.title_lbl.text = f"Edit {item}"
            self.field.text = str(qty)
            self.btn_save.text = "UPDATE QUANTITY"
            self.btn_del.opacity = 1
            self.btn_del.disabled = False

    def save(self, _):
        if self.field.text:
            qty = int(self.field.text)
            data = load_data()
            if self.mode == "add":
                curr = data["accounts"][self.acc_name]["items"].get(self.item_name, 0)
                data["accounts"][self.acc_name]["items"][self.item_name] = curr + qty
            else:
                data["accounts"][self.acc_name]["items"][self.item_name] = qty
            save_data(data)
        self.go_back()

    def delete_item(self, _):
        data = load_data()
        if self.item_name in data["accounts"][self.acc_name]["items"]:
            del data["accounts"][self.acc_name]["items"][self.item_name]
            save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = 'inventory_edit'
        self.manager.get_screen('inventory_edit').load_account(self.acc_name)

# --- 5. TRADES ---
class TradeListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Select Account", halign="center"))
        layout.add_widget(toolbar)
        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        self.empty_lbl = MDLabel(text="No Accounts", halign="center", theme_text_color="Secondary")
        self.add_widget(self.empty_lbl)

    def on_enter(self):
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        accounts = data.get("accounts", {})
        if not accounts:
            self.empty_lbl.opacity = 1
        else:
            self.empty_lbl.opacity = 0
            for name in accounts:
                item = TwoLineAvatarIconListItem(text=name, secondary_text="Manage Trades", on_release=lambda x, n=name: self.open_recipients(n))
                item.add_widget(IconRightWidget(icon="account-switch"))
                self.list_view.add_widget(item)

    def open_recipients(self, name):
        self.manager.get_screen('trade_recipients').load_account(name)
        self.manager.current = 'trade_recipients'

class TradeRecipientsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'trade_list')))
        self.title_lbl = MDLabel(text="Recipients", halign="center")
        toolbar.add_widget(self.title_lbl)
        layout.add_widget(toolbar)
        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.8, 0.8, 0.2, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.add_recipient)
        self.add_widget(fab)

    def load_account(self, name):
        self.acc_name = name
        self.title_lbl.text = f"Trades: {name}"
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        recipients = data["active_trades"].get(self.acc_name, {})
        for r_name in recipients:
            item_count = len(recipients[r_name])
            row = TwoLineAvatarIconListItem(text=r_name, secondary_text=f"{item_count} Items Pending", on_release=lambda x, r=r_name: self.open_trade_details(r))
            row.add_widget(IconRightWidget(icon="chevron-right"))
            self.list_view.add_widget(row)

    def add_recipient(self, _):
        self.manager.get_screen('add_recipient').setup(self.acc_name)
        self.manager.current = 'add_recipient'

    def open_trade_details(self, recipient):
        self.manager.get_screen('trade_details').load(self.acc_name, recipient)
        self.manager.current = 'trade_details'

class AddRecipientScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="New Recipient", halign="center", font_style="H5"))
        self.field = MDTextField(hint_text="IGN (In Game Name)", mode="rectangle")
        layout.add_widget(self.field)
        layout.add_widget(MDFillRoundFlatButton(text="START TRADING", on_release=self.save))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, acc):
        self.acc_name = acc
        self.field.text = ""

    def save(self, _):
        ign = self.field.text.strip()
        if ign:
            data = load_data()
            if self.acc_name not in data["active_trades"]: data["active_trades"][self.acc_name] = {}
            if ign not in data["active_trades"][self.acc_name]: data["active_trades"][self.acc_name][ign] = []
            save_data(data)
            self.manager.get_screen('trade_recipients').load_account(self.acc_name)
            self.manager.current = 'trade_recipients'
    
    def cancel(self, _):
        self.manager.current = 'trade_recipients'

class TradeDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        self.recipient = ""
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=self.go_back))
        self.title_lbl = MDLabel(text="Trade", halign="center")
        toolbar.add_widget(self.title_lbl)
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

        btns = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        btns.add_widget(MDFillRoundFlatButton(text="ADD ITEM (1)", on_release=self.add_item_sheet))
        btns.add_widget(MDFillRoundFlatButton(text="COMPLETE TRADE", md_bg_color=(0.2,0.8,0.2,1), on_release=self.complete_trade))
        layout.add_widget(btns)
        self.add_widget(layout)
        self.bs = None

    def load(self, acc, recipient):
        self.acc_name = acc
        self.recipient = recipient
        self.title_lbl.text = f"Trading with {recipient}"
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["active_trades"].get(self.acc_name, {}).get(self.recipient, [])
        for idx, item in enumerate(items):
            row = TwoLineAvatarIconListItem(text=item['name'], secondary_text=item['date'])
            icon = IconRightWidget(icon="close-circle", on_release=lambda x, i=idx: self.cancel_item(i))
            img_src = ITEM_MAP.get(item['name'], "assets/hack.png")
            if not os.path.exists(img_src): img_src = "assets/hack.png"
            row.add_widget(ImageLeftWidget(source=img_src))
            row.add_widget(icon)
            self.list_view.add_widget(row)

    def add_item_sheet(self, _):
        self.bs = MDGridBottomSheet()
        for name, src in ITEM_MAP.items():
            if not os.path.exists(src): continue
            self.bs.add_item(name, lambda x, n=name: self.add_item(n), icon_src=src)
        self.bs.open()

    def add_item(self, item_name):
        if self.bs: self.bs.dismiss()
        data = load_data()
        current_inv = data["accounts"].get(self.acc_name, {}).get("items", {}).get(item_name, 0)
        
        if current_inv > 0:
            data["accounts"][self.acc_name]["items"][item_name] = current_inv - 1
            date_str = datetime.now().strftime("%Y-%m-%d")
            new_item = {"name": item_name, "date": date_str}
            data["active_trades"][self.acc_name][self.recipient].append(new_item)
            save_data(data)
            self.refresh_list()

    def cancel_item(self, index):
        data = load_data()
        items = data["active_trades"][self.acc_name][self.recipient]
        item_to_remove = items[index]
        curr = data["accounts"][self.acc_name]["items"].get(item_to_remove['name'], 0)
        data["accounts"][self.acc_name]["items"][item_to_remove['name']] = curr + 1
        del items[index]
        save_data(data)
        self.refresh_list()

    def complete_trade(self, _):
        data = load_data()
        if self.recipient in data["active_trades"][self.acc_name]:
            del data["active_trades"][self.acc_name][self.recipient]
            save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'trade_recipients'
        self.manager.get_screen('trade_recipients').load_account(self.acc_name)

# --- 6. CARDS ---
class CardListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2,0.2,0.2,1))
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        toolbar.add_widget(MDLabel(text="Card Accounts", halign="center"))
        layout.add_widget(toolbar)
        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.6, 0.3, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

        self.empty_lbl = MDLabel(text="No Card Accounts", halign="center", theme_text_color="Secondary")
        self.add_widget(self.empty_lbl)

    def on_enter(self):
        Clock.schedule_once(self.refresh_list, 0.1)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        cards = data.get("cards", {})
        if not cards:
            self.empty_lbl.opacity = 1
        else:
            self.empty_lbl.opacity = 0
            for name in cards:
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
        # FIXED: White Back Button
        toolbar.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1), on_release=lambda x: setattr(self.manager, 'current', 'card_list')))
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
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, dt=0):
        self.list_view.clear_widgets()
        data = load_data()
        cards = data["cards"].get(self.account_name, [])
        for i, c in enumerate(cards):
            row = ThreeLineIconListItem(text=c['name'], secondary_text=f"Tier: {c['tier']}", tertiary_text=f"Qty: {c['qty']}")
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
        if self.account_name in data["cards"]: del data["cards"][self.account_name]
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
        sm.add_widget(EditItemQtyScreen(name='edit_item_qty'))
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(TradeRecipientsScreen(name='trade_recipients'))
        sm.add_widget(AddRecipientScreen(name='add_recipient'))
        sm.add_widget(TradeDetailsScreen(name='trade_details'))
        sm.add_widget(CardListScreen(name='card_list'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        return sm

if __name__ == '__main__':
    UltimateApp().run()
