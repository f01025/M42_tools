import json
import os
import traceback
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

# --- VERSION 21.0 (ERROR CATCHER) ---

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

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
            # FORCE DATA REPAIR
            if not isinstance(data, dict): return {"accounts": {}, "cards": {}, "active_trades": {}}
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

# --- ASSET HELPER ---
def get_img_path(name):
    # This prevents crashes if image is missing
    base_dir = os.path.dirname(os.path.abspath(__file__))
    asset_dir = os.path.join(base_dir, 'assets')
    
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
    full_path = os.path.join(asset_dir, fname)
    
    # Verify file exists
    if os.path.exists(full_path):
        return full_path
    return None # Return None if missing

class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.1, 0.1, 0.1, 1)

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
        
        layout.add_widget(MDLabel(size_hint_y=None, height="20dp"))
        settings_btn = MDIconButton(icon="cog", theme_text_color="Custom", text_color=(0.5, 0.5, 0.5, 1), pos_hint={'center_x': 0.5}, on_release=lambda x: self.go_to('settings'))
        layout.add_widget(settings_btn)
        self.add_widget(layout)
        
        ver = MDLabel(text="v21.0 Debug", halign="right", theme_text_color="Secondary", font_style="Caption", pos_hint={'right': 0.95, 'y': 0.02}, size_hint=(None, None), size=("100dp", "20dp"))
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="20dp", padding="40dp")
        layout.add_widget(MDFillRoundFlatButton(text="< BACK TO MENU", md_bg_color=(0.3, 0.3, 0.3, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        layout.add_widget(MDLabel(text="Settings", halign="center", font_style="H5"))
        btn_reset = MDFillRoundFlatButton(text="DELETE ALL DATA", md_bg_color=(0.8, 0, 0, 1), size_hint=(1, None), on_release=self.reset_data)
        layout.add_widget(btn_reset)
        layout.add_widget(MDLabel()) 
        self.add_widget(layout)

    def reset_data(self, _):
        if os.path.exists(get_data_path()):
            os.remove(get_data_path())
        self.manager.current = 'menu'

class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Simplified for brevity, same as working version
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        main_box.add_widget(header)
        self.add_widget(main_box)

class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Tier Calc", halign="center", font_style="H5"))
        main_box.add_widget(header)
        self.add_widget(main_box)

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

# --- INVENTORY LIST (WITH CRASH CATCHER) ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="My Inventory", halign="center", font_style="H6"))
        main_box.add_widget(header)

        # ERROR DISPLAY LABEL
        self.err_label = MDLabel(text="", halign="center", theme_text_color="Error", size_hint_y=None, height="50dp")
        main_box.add_widget(self.err_label)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)
        self.add_widget(main_box)

    def on_enter(self):
        # Delay load to allow screen to render first
        Clock.schedule_once(self.refresh_list, 0.5)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

    def refresh_list(self, dt=0):
        try:
            self.list_view.clear_widgets()
            data = load_data()
            accounts = data.get("accounts", {})
            if not accounts:
                self.err_label.text = "No Accounts Found"
            else:
                self.err_label.text = "" # Clear error
                for name, details in accounts.items():
                    # TRY TO USE FANCY LIST ITEM
                    item = TwoLineAvatarIconListItem(
                        text=str(name), 
                        secondary_text=f"Items: {len(details.get('items', {}))}",
                        on_release=lambda x, n=name: self.open_account(n)
                    )
                    item.add_widget(IconLeftWidget(icon="account-circle"))
                    self.list_view.add_widget(item)
        except Exception as e:
            # IF IT FAILS, SHOW ERROR ON SCREEN INSTEAD OF CRASHING
            self.err_label.text = f"CRASH PREVENTED:\n{str(e)}"

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

        self.err_label = MDLabel(text="", halign="center", theme_text_color="Error", size_hint_y=None, height="30dp")
        main_box.add_widget(self.err_label)

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
        Clock.schedule_once(self.refresh_items, 0.2)

    def refresh_items(self, dt=0):
        try:
            self.list_view.clear_widgets()
            data = load_data()
            items = data["accounts"].get(self.account_name, {}).get("items", {})
            for item_name, qty in items.items():
                img_path = get_img_path(item_name)
                
                row = TwoLineAvatarIconListItem(
                    text=str(item_name), 
                    secondary_text=f"Quantity: {qty}",
                    on_release=lambda x, i=item_name, q=qty: self.edit_item(i, q)
                )
                
                if img_path:
                    row.add_widget(ImageLeftWidget(source=img_path))
                else:
                    row.add_widget(IconLeftWidget(icon="cube"))
                    
                self.list_view.add_widget(row)
        except Exception as e:
            self.err_label.text = f"Error: {str(e)}"

    def show_item_selector(self, _):
        self.bs = MDGridBottomSheet()
        items = ["Hack Envelope", "Nobi Envelope", "Beach Envelope", "Halloween Envelope", 
                 "Xmas Envelope", "Toy Envelope", "Ghost Envelope", "NYPC Envelope", 
                 "Santa Envelope", "10th Anniversary", "4th Anniversary", "Puni Envelope", 
                 "Negative Envelope", "Dice Envelope", "Surprise Envelope", "Luxury Envelope", "Basic Envelope"]
        for name in items:
            path = get_img_path(name)
            if path:
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
            try:
                qty = int(self.field.text)
                data = load_data()
                if self.mode == "add":
                    curr = data["accounts"][self.acc_name]["items"].get(self.item_name, 0)
                    data["accounts"][self.acc_name]["items"][self.item_name] = curr + qty
                else:
                    data["accounts"][self.acc_name]["items"][self.item_name] = qty
                save_data(data)
            except:
                pass
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

# --- 6. CARDS (WITH CRASH CATCHER) ---
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Card Accounts", halign="center"))
        main_box.add_widget(header)

        self.err_label = MDLabel(text="", halign="center", theme_text_color="Error", size_hint_y=None, height="50dp")
        main_box.add_widget(self.err_label)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)

        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.6, 0.3, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)
        self.add_widget(main_box)

    def on_enter(self):
        Clock.schedule_once(self.refresh_list, 0.5)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def refresh_list(self, dt=0):
        try:
            self.list_view.clear_widgets()
            data = load_data()
            cards = data.get("cards", {})
            if not cards:
                self.err_label.text = "No Accounts Found"
            else:
                self.err_label.text = ""
                for name in cards:
                    # SAFE LIST ITEM
                    item = TwoLineAvatarIconListItem(
                        text=str(name), 
                        secondary_text="Tap to view cards", 
                        on_release=lambda x, n=name: self.open_cards(n)
                    )
                    item.add_widget(IconLeftWidget(icon="cards"))
                    self.list_view.add_widget(item)
        except Exception as e:
            self.err_label.text = f"CRASH PREVENTED:\n{str(e)}"

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

        # ADD CARD FORM
        form = MDBoxLayout(orientation='vertical', size_hint_y=None, height="160dp", padding="10dp", spacing="10dp")
        self.in_name = MDTextField(hint_text="Card Name", mode="rectangle")
        row = MDBoxLayout(spacing="10dp")
        self.in_tier = MDTextField(hint_text="Tier (2-6)", mode="rectangle", input_filter="int")
        self.in_qty = MDTextField(hint_text="Quantity", mode="rectangle", input_filter="int")
        row.add_widget(self.in_tier)
        row.add_widget(self.in_qty)
        form.add_widget(self.in_name)
        form.add_widget(row)
        btn_add = MDFillRoundFlatButton(text="ADD CARD", on_release=self.add_card)
        form.add_widget(btn_add)
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
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, dt=0):
        try:
            self.list_view.clear_widgets()
            data = load_data()
            if self.account_name not in data["cards"]:
                data["cards"][self.account_name] = []
                save_data(data)
            
            cards = data["cards"].get(self.account_name, [])
            for i, c in enumerate(cards):
                # SAFE LIST ITEM
                row = ThreeLineIconListItem(
                    text=str(c.get('name', 'Unknown')), 
                    secondary_text=f"Tier: {c.get('tier', '?')}", 
                    tertiary_text=f"Qty: {c.get('qty', 0)}"
                )
                row.add_widget(IconRightWidget(icon="delete", on_release=lambda x, idx=i: self.delete_card(idx)))
                self.list_view.add_widget(row)
        except:
            pass

    def add_card(self, _):
        if self.in_name.text and self.in_qty.text and self.in_tier.text:
            try:
                tier = int(self.in_tier.text)
                if tier < 2 or tier > 6: return 
                
                data = load_data()
                new_card = {"name": self.in_name.text, "tier": str(tier), "qty": int(self.in_qty.text)}
                data["cards"][self.account_name].append(new_card)
                save_data(data)
                self.refresh_list()
                self.in_name.text = ""
                self.in_qty.text = ""
                self.in_tier.text = ""
            except:
                pass

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
        for name in accounts:
            item = TwoLineAvatarIconListItem(text=name, secondary_text="Manage Trades", on_release=lambda x, n=name: self.open_recipients(n))
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
        
        main_box.add_widget(MDFillRoundFlatButton(text="ADD RECIPIENT", size_hint=(1, None), on_release=self.add_recipient))
        self.add_widget(main_box)

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
            item = TwoLineAvatarIconListItem(text=r_name, secondary_text=f"{count} Items Pending", on_release=lambda x, r=r_name: self.open_trade_details(r))
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

        main_box.add_widget(MDFillRoundFlatButton(text="ADD ITEM (1)", size_hint=(1, None), on_release=self.add_item_sheet))
        main_box.add_widget(MDFillRoundFlatButton(text="COMPLETE TRADE", size_hint=(1, None), md_bg_color=(0.2,0.8,0.2,1), on_release=self.complete_trade))
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
            img_path = get_img_path(item.get('name', ''))
            row = TwoLineAvatarIconListItem(
                text=str(item.get('name', 'Unknown')), 
                secondary_text=str(item.get('date', ''))
            )
            if img_path:
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
            if path:
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
            date_str = "Now"
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
