import json
import os
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform

# --- VERSION 24.0 (LAYOUT ISOLATION) ---

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
        return {"inventory": {}, "cards": {}}
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if "inventory" not in data: data["inventory"] = {}
            if "cards" not in data: data["cards"] = {}
            return data
    except:
        return {"inventory": {}, "cards": {}}

def save_data(data):
    try:
        with open(get_data_path(), "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.1, 0.1, 0.1, 1)

class MenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="20dp", padding="30dp")
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        layout.adaptive_height = True

        layout.add_widget(MDLabel(text="ULTIMATE TOOLKIT", halign="center", font_style="H4", theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        
        btns = [
            ("BLACK MARKET", (0.9, 0.3, 0.2, 1), 'market'),
            ("TIER CRAFTING", (0.2, 0.6, 0.8, 1), 'crafting'),
            ("INVENTORY", (0.3, 0.7, 0.3, 1), 'inventory_list'),
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list')
        ]

        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="18sp", size_hint=(1, None), height="60dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)
        
        self.add_widget(layout)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

# --- 1. BLACK MARKET (Working) ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="20dp")
        
        # Header
        header = MDBoxLayout(size_hint_y=None, height="50dp")
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        layout.add_widget(header)

        # Content
        self.in_rub = MDTextField(hint_text="Rubles", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Luna", mode="rectangle", input_filter="float")
        layout.add_widget(self.in_rub)
        layout.add_widget(self.in_luna)
        
        btn = MDRaisedButton(text="CALCULATE", size_hint=(1, None), md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        layout.add_widget(btn)
        
        self.res_lbl = MDLabel(text="Result: 0", halign="center", theme_text_color="Custom", text_color=(0,1,0,1))
        layout.add_widget(self.res_lbl)
        
        layout.add_widget(MDLabel()) # Spacer
        self.add_widget(layout)

    def calc(self, _):
        try:
            luna = float(self.in_luna.text)
            self.res_lbl.text = f"Listing: {int(luna * 1.35):,}"
        except:
            self.res_lbl.text = "Error"

# --- 2. TIER CRAFTING (Working) ---
class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="20dp")
        
        header = MDBoxLayout(size_hint_y=None, height="50dp")
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Tier Calc", halign="center", font_style="H5"))
        layout.add_widget(header)

        self.in_qty = MDTextField(hint_text="Qty Cards", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4-6)", mode="rectangle", input_filter="int")
        layout.add_widget(self.in_qty)
        layout.add_widget(self.in_tier)
        
        btn = MDRaisedButton(text="CALCULATE", size_hint=(1, None), md_bg_color=(0.2, 0.6, 0.8, 1), on_release=self.calc)
        layout.add_widget(btn)
        
        self.res_lbl = MDLabel(text="", halign="center", theme_text_color="Custom", text_color=(0,1,0,1))
        layout.add_widget(self.res_lbl)
        
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def calc(self, _):
        try:
            qty = int(self.in_qty.text)
            tier = int(self.in_tier.text)
            cost_map = {4:4, 5:20, 6:120}
            if tier in cost_map:
                needed = qty * cost_map[tier]
                self.res_lbl.text = f"You need {needed} Tier 3 cards"
            else:
                self.res_lbl.text = "Invalid Tier (4, 5, 6 only)"
        except:
            self.res_lbl.text = "Error"

# --- 3. INVENTORY (CRASH TEST MODE) ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NO SCROLLVIEW. NO LISTS. JUST A BOX.
        layout = MDBoxLayout(orientation='vertical', padding="40dp", spacing="20dp")
        
        layout.add_widget(MDLabel(text="INVENTORY SAFE MODE", halign="center", font_style="H5"))
        
        btn_back = MDRaisedButton(
            text="GO BACK TO MENU", 
            size_hint=(1, None), 
            height="50dp",
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=lambda x: setattr(self.manager, 'current', 'menu')
        )
        layout.add_widget(btn_back)
        
        btn_add = MDRaisedButton(
            text="ADD ACCOUNT (TEST)", 
            size_hint=(1, None), 
            height="50dp",
            on_release=self.go_add
        )
        layout.add_widget(btn_add)
        
        layout.add_widget(MDLabel()) # Spacer
        self.add_widget(layout)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

# --- 4. CARDS (CRASH TEST MODE) ---
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NO SCROLLVIEW. NO LISTS. JUST A BOX.
        layout = MDBoxLayout(orientation='vertical', padding="40dp", spacing="20dp")
        
        layout.add_widget(MDLabel(text="CARDS SAFE MODE", halign="center", font_style="H5"))
        
        btn_back = MDRaisedButton(
            text="GO BACK TO MENU", 
            size_hint=(1, None), 
            height="50dp",
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=lambda x: setattr(self.manager, 'current', 'menu')
        )
        layout.add_widget(btn_back)
        
        btn_add = MDRaisedButton(
            text="ADD ACCOUNT (TEST)", 
            size_hint=(1, None), 
            height="50dp",
            on_release=self.go_add
        )
        layout.add_widget(btn_add)
        
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

# --- 5. ADD ACCOUNT (Shared) ---
class AddAccountScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_screen = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        
        layout.add_widget(MDLabel(text="Create Account", halign="center", font_style="H5"))
        
        self.field = MDTextField(hint_text="Account Name", mode="rectangle")
        layout.add_widget(self.field)
        
        btn_save = MDRaisedButton(text="SAVE", size_hint=(1, None), on_release=self.save)
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
        if name:
            data = load_data()
            if self.target_screen == 'inventory_list':
                data["inventory"][name] = {}
            else:
                data["cards"][name] = {}
            save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = self.target_screen

# --- 6. PLACEHOLDERS (To Prevent 'Not Defined' Errors) ---
class InventoryEditScreen(BaseScreen): pass
class CardEditScreen(BaseScreen): pass
class EditItemQtyScreen(BaseScreen): pass
class TradeListScreen(BaseScreen): pass
class TradeRecipientsScreen(BaseScreen): pass
class AddRecipientScreen(BaseScreen): pass
class TradeDetailsScreen(BaseScreen): pass

# --- APP ---
class UltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(CraftingScreen(name='crafting'))
        sm.add_widget(InventoryListScreen(name='inventory_list'))
        sm.add_widget(CardListScreen(name='card_list'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        
        # Placeholders
        sm.add_widget(InventoryEditScreen(name='inventory_edit'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        sm.add_widget(EditItemQtyScreen(name='edit_item_qty'))
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(TradeRecipientsScreen(name='trade_recipients'))
        sm.add_widget(AddRecipientScreen(name='add_recipient'))
        sm.add_widget(TradeDetailsScreen(name='trade_details'))
        
        return sm

if __name__ == '__main__':
    UltimateApp().run()
