import json
import os
import math
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, ThreeLineIconListItem, IconLeftWidget, OneLineAvatarIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

# --- VERSION 8.0 (RESTORATION & SAFETY) ---

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

# --- STORAGE & DATA ---
def get_data_path():
    app = MDApp.get_running_app()
    if platform == 'android':
        return os.path.join(app.user_data_dir, "data.json")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def load_data():
    path = get_data_path()
    if not os.path.exists(path):
        return {"accounts": {}, "cards": {}, "active_trades": {}}
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if "accounts" not in data: data["accounts"] = {}
            if "cards" not in data: data["cards"] = {}
            if "active_trades" not in data: data["active_trades"] = {}
            return data
    except:
        return {"accounts": {}, "cards": {}, "active_trades": {}}

def save_data(data):
    try:
        with open(get_data_path(), "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

# --- ASSET HELPER (CRASH PREVENTER) ---
def get_img_path(name):
    # Map names to files
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
    fname = mapping.get(name, "hack.png")
    # Return absolute path
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', fname)

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
        
        # Reset Data (Hidden in a small text button at bottom)
        layout.add_widget(MDLabel(size_hint_y=None, height="20dp"))
        reset = MDFlatButton(text="Reset All Data", theme_text_color="Error", pos_hint={'center_x': 0.5}, on_release=self.reset_data)
        layout.add_widget(reset)

        self.add_widget(layout)
        
        ver = MDLabel(text="v8.0 Restore", halign="right", theme_text_color="Secondary", font_style="Caption", pos_hint={'right': 0.95, 'y': 0.02}, size_hint=(None, None), size=("100dp", "20dp"))
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

    def reset_data(self, _):
        if os.path.exists(get_data_path()):
            os.remove(get_data_path())

# --- 1. BLACK MARKET ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        # HEADER
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        
        self.in_rub = MDTextField(hint_text="Rubles", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Luna", mode="rectangle", input_filter="float")
        container.add_widget(self.in_rub)
        container.add_widget(self.in_luna)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        container.add_widget(btn)
        
        grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.res_list = self.create_res_box("Listing Price", "0")
        self.res_rate = self.create_res_box("Exchange Rate", "0")
        grid.add_widget(self.res_list)
        grid.add_widget(self.res_rate)
        container.add_widget(grid)
        
        scroll.add_widget(container)
        main_box.add_widget(scroll)
        self.add_widget(main_box)

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
            list_price = luna * 1.35
            rate = 0
            if rubles > 0:
                rate = (luna / rubles) * 1000000.0
            self.res_list.val_label.text = f"{math.ceil(list_price):,.0f}"
            self.res_rate.val_label.text = f"{int(rate):,.0f}"
        except:
            self.res_list.val_label.text = "Error"

# --- 2. CRAFTING ---
class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Tier Calc", halign="center", font_style="H5"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        container = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        
        self.in_qty = MDTextField(hint_text="Qty Cards", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4, 5, or 6)", mode="rectangle", input_filter="int")
        container.add_widget(self.in_qty)
        container.add_widget(self.in_tier)
        
        self.inv_t3 = MDTextField(hint_text="T3", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5", mode="rectangle", input_filter="int")
        self.inv_t6 = MDTextField(hint_text="T6", mode="rectangle", input_filter="int")
        container.add_widget(self.inv_t3)
        container.add_widget(self.inv_t4)
        container.add_widget(self.inv_t5)
        container.add_widget(self.inv_t6)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.2, 0.6, 0.8, 1), on_release=self.calc)
        container.add_widget(btn)
        
        self.res_card = MDCard(orientation='vertical', padding="15dp", spacing="10dp", size_hint_y=None, height="200dp", md_bg_color=(0.15, 0.15, 0.15, 1))
        self.res_opt1 = MDLabel(text="", theme_text_color="Primary", font_style="Body1", halign="center")
        self.res_opt2 = MDLabel(text="", theme_text_color="Custom", text_color=(0.4, 0.8, 1, 1), font_style="Body1", halign="center")
        self.res_card.add_widget(MDLabel(text="Missing Resources", theme_text_color="Secondary", font_style="Caption", halign="center"))
        self.res_card.add_widget(self.res_opt1)
        self.res_card.add_widget(self.res_opt2)
        container.add_widget(self.res_card)
        
        scroll.add_widget(container)
        main_box.add_widget(scroll)
        self.add_widget(main_box)

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
            self.res_opt1.text = "Error"

# --- 3. ADD ACCOUNT SCREEN ---
class AddAccountScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_screen = "" 
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="Create Account", halign="center", font_style="H5"))
        self.field = MDTextField(hint_text="Name", mode="rectangle")
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

# --- 4. INVENTORY (RESTORED LISTS) ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="My Inventory", halign="center", font_style="H6"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        self.add_widget(main_box)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

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
            self.list_view.add_widget(OneLineListItem(text="No Accounts. Tap + to add."))
        for name, details in accounts.items():
            # Use Standard List Item with Icon
            item = TwoLineAvatarIconListItem(
                text=name, 
                secondary_text=f"Items: {len(details.get('items', {}))}",
                on_release=lambda x, n=name: self.open_account(n)
            )
            item.add_widget(IconLeftWidget(icon="account-circle"))
            self.list_view.add_widget(item)

    def open_account(self, name):
        self.manager.get_screen('inventory_edit').load_account(name)
        self.manager.current = 'inventory_edit'

class InventoryEditScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=self.go_back))
        self.toolbar_lbl = MDLabel(text="Items", halign="center", font_style="H6")
        header.add_widget(self.toolbar_lbl)
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        footer = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        footer.add_widget(MDFillRoundFlatButton(text="ADD ITEM", size_hint_x=0.7, on_release=self.show_item_selector))
        footer.add_widget(MDIconButton(icon="trash-can", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account))
        main_box.add_widget(footer)
        self.add_widget(main_box)
        self.bs = None

    def load_account(self, name):
        self.account_name = name
        self.toolbar_lbl.text = name
        self.refresh_items()

    def refresh_items(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        for item_name, qty in items.items():
            # --- IMAGE SAFETY CHECK ---
            img_path = get_img_path(item_name)
            
            row = TwoLineAvatarIconListItem(
                text=item_name, 
                secondary_text=f"Quantity: {qty}",
                on_release=lambda x, i=item_name, q=qty: self.edit_item(i, q)
            )
            
            # Check if file exists. If yes, use Image. If no, use Icon.
            if os.path.exists(img_path):
                row.add_widget(ImageLeftWidget(source=img_path))
            else:
                row.add_widget(IconLeftWidget(icon="cube"))
                
            self.list_view.add_widget(row)

    def show_item_selector(self, _):
        self.bs = MDGridBottomSheet()
        items = ["Hack Envelope", "Nobi Envelope", "Beach Envelope", "Halloween Envelope", 
                 "Xmas Envelope", "Toy Envelope", "Ghost Envelope", "NYPC Envelope", 
                 "Santa Envelope", "10th Anniversary", "4th Anniversary", "Puni Envelope", 
                 "Negative Envelope", "Dice Envelope", "Surprise Envelope", "Luxury Envelope", "Basic Envelope"]
        for name in items:
            path = get_img_path(name)
            # Only add to sheet if image exists, else use default icon
            if os.path.exists(path):
                self.bs.add_item(name, lambda x, n=name: self.ask_qty(n), icon_src=path)
            else:
                self.bs.add_item(name, lambda x, n=name: self.ask_qty(n), icon_src="android")
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

class EditItemQtyScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        self.item_name = ""
        self.mode = "add"
        
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        self.title_lbl = MDLabel(text="Item", halign="center", font_style="H5")
        layout.add_widget(self.title_lbl)
        
        self.field = MDTextField(hint_text="Quantity", input_filter="int", mode="rectangle")
        layout.add_widget(self.field)
        
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
            self.btn_save.text = "ADD"
            self.btn_del.opacity = 0 
            self.btn_del.disabled = True
        else:
            self.title_lbl.text = f"Edit {item}"
            self.field.text = str(qty)
            self.btn_save.text = "UPDATE"
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
class TradeListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Select Account", halign="center"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        self.add_widget(main_box)

    def on_enter(self):
        self.refresh_list()

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        accounts = data.get("accounts", {})
        if not accounts:
            self.list_view.add_widget(OneLineListItem(text="No Accounts"))
        for name in accounts:
            item = TwoLineAvatarIconListItem(
                text=name, 
                secondary_text="Tap to Trade",
                on_release=lambda x, n=name: self.open_recipients(n)
            )
            item.add_widget(IconLeftWidget(icon="account-circle"))
            self.list_view.add_widget(item)

    def open_recipients(self, name):
        self.manager.get_screen('trade_recipients').load_account(name)
        self.manager.current = 'trade_recipients'

class TradeRecipientsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'trade_list')))
        self.title_lbl = MDLabel(text="Recipients", halign="center")
        header.add_widget(self.title_lbl)
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.8, 0.8, 0.2, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.add_recipient)
        self.add_widget(fab)

    def load_account(self, name):
        self.acc_name = name
        self.title_lbl.text = f"Trades: {name}"
        self.refresh_list()

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        recipients = data["active_trades"].get(self.acc_name, {})
        for r_name in recipients:
            count = len(recipients[r_name])
            item = TwoLineAvatarIconListItem(
                text=r_name, 
                secondary_text=f"{count} Items Pending",
                on_release=lambda x, r=r_name: self.open_trade_details(r)
            )
            item.add_widget(IconLeftWidget(icon="account"))
            item.add_widget(IconRightWidget(icon="chevron-right"))
            self.list_view.add_widget(item)

    def add_recipient(self, _):
        self.manager.get_screen('add_recipient').setup(self.acc_name)
        self.manager.current = 'add_recipient'

    def open_trade_details(self, recipient):
        self.manager.get_screen('trade_details').load(self.acc_name, recipient)
        self.manager.current = 'trade_details'

class AddRecipientScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="New Recipient", halign="center", font_style="H5"))
        self.field = MDTextField(hint_text="IGN", mode="rectangle")
        layout.add_widget(self.field)
        layout.add_widget(MDFillRoundFlatButton(text="START", on_release=self.save))
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

class TradeDetailsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.acc_name = ""
        self.recipient = ""
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=self.go_back))
        self.title_lbl = MDLabel(text="Trade", halign="center")
        header.add_widget(self.title_lbl)
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)

        btns = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        btns.add_widget(MDFillRoundFlatButton(text="ADD ITEM (1)", on_release=self.add_item_sheet))
        btns.add_widget(MDFillRoundFlatButton(text="COMPLETE TRADE", md_bg_color=(0.2,0.8,0.2,1), on_release=self.complete_trade))
        main_box.add_widget(btns)
        self.add_widget(main_box)
        self.bs = None

    def load(self, acc, recipient):
        self.acc_name = acc
        self.recipient = recipient
        self.title_lbl.text = f"Trading with {recipient}"
        self.refresh_list()

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["active_trades"].get(self.acc_name, {}).get(self.recipient, [])
        for idx, item in enumerate(items):
            # SAFE IMAGE CHECK
            img_path = get_img_path(item['name'])
            row = TwoLineAvatarIconListItem(
                text=item['name'], 
                secondary_text=item['date']
            )
            if os.path.exists(img_path):
                row.add_widget(ImageLeftWidget(source=img_path))
            else:
                row.add_widget(IconLeftWidget(icon="cube"))
                
            row.add_widget(IconRightWidget(icon="close-circle", on_release=lambda x, i=idx: self.cancel_item(i)))
            self.list_view.add_widget(row)

    def add_item_sheet(self, _):
        self.bs = MDGridBottomSheet()
        items = ["Hack Envelope", "Nobi Envelope", "Beach Envelope", "Halloween Envelope", 
                 "Xmas Envelope", "Toy Envelope", "Ghost Envelope", "NYPC Envelope", 
                 "Santa Envelope", "10th Anniversary", "4th Anniversary", "Puni Envelope", 
                 "Negative Envelope", "Dice Envelope", "Surprise Envelope", "Luxury Envelope", "Basic Envelope"]
        for name in items:
            path = get_img_path(name)
            if os.path.exists(path):
                self.bs.add_item(name, lambda x, n=name: self.add_item(n), icon_src=path)
            else:
                self.bs.add_item(name, lambda x, n=name: self.add_item(n), icon_src="android")
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
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Card Accounts", halign="center"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)

        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.6, 0.3, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

    def on_enter(self):
        self.refresh_list()

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.list_view.clear_widgets()
        data = load_data()
        cards = data.get("cards", {})
        if not cards:
            self.list_view.add_widget(OneLineListItem(text="No Accounts"))
        for name in cards:
            item = TwoLineAvatarIconListItem(
                text=name, 
                secondary_text="Tap to view cards", 
                on_release=lambda x, n=name: self.open_cards(n)
            )
            item.add_widget(IconLeftWidget(icon="cards"))
            item.add_widget(IconRightWidget(icon="chevron-right"))
            self.list_view.add_widget(item)

    def open_cards(self, name):
        self.manager.get_screen('card_edit').load_account(name)
        self.manager.current = 'card_edit'

class CardEditScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        main_box = MDBoxLayout(orientation='vertical', padding="10dp")
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'card_list')))
        self.title_lbl = MDLabel(text="Cards", halign="center")
        header.add_widget(self.title_lbl)
        main_box.add_widget(header)

        form = MDBoxLayout(orientation='vertical', size_hint_y=None, height="140dp", padding="10dp", spacing="5dp")
        row1 = MDBoxLayout(spacing="10dp")
        self.in_name = MDTextField(hint_text="Name")
        self.in_tier = MDTextField(hint_text="Tier")
        row1.add_widget(self.in_name)
        row1.add_widget(self.in_tier)
        row2 = MDBoxLayout(spacing="10dp")
        self.in_qty = MDTextField(hint_text="Qty", input_filter="int")
        btn = MDRaisedButton(text="ADD", on_release=self.add_card)
        row2.add_widget(self.in_qty)
        row2.add_widget(btn)
        form.add_widget(row1)
        form.add_widget(row2)
        main_box.add_widget(form)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        del_btn = MDFillRoundFlatButton(text="DELETE ACCOUNT", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account)
        main_box.add_widget(del_btn)
        self.add_widget(main_box)

    def load_account(self, name):
        self.account_name = name
        self.title_lbl.text = f"{name}'s Cards"
        self.refresh_list()

    def refresh_list(self):
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
        try:
            sm = ScreenManager(transition=NoTransition())
            sm.add_widget(MenuScreen(name='menu'))
            sm.add_widget(SettingsScreen(name='settings'))
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
        except Exception as e:
            return MDLabel(text=f"Fatal Error: {e}", halign="center")

if __name__ == '__main__':
    UltimateApp().run()
