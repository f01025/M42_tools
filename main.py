import json
import os
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform

# --- VERSION 17.0 (SKELETON MODE - NO DATA LOADING) ---

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

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
        
        # Navigation Buttons
        btns = [
            ("BLACK MARKET", (0.9, 0.3, 0.2, 1), 'market'),
            ("TIER CRAFTING", (0.2, 0.6, 0.8, 1), 'crafting'),
            ("MY INVENTORY", (0.3, 0.7, 0.3, 1), 'inventory_list'), # Target 1
            ("TRADES", (0.8, 0.8, 0.2, 1), 'trade_list'),
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list')             # Target 2
        ]

        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="16sp", size_hint=(1, None), height="55dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)
        
        self.add_widget(layout)
        
        ver = MDLabel(text="v17.0 Skeleton", halign="right", theme_text_color="Secondary", font_style="Caption", pos_hint={'right': 0.95, 'y': 0.02}, size_hint=(None, None), size=("100dp", "20dp"))
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

# --- 1. BLACK MARKET (Working Logic Kept) ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
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
        
        self.res_label = MDLabel(text="Result: 0", halign="center", font_style="H5", theme_text_color="Custom", text_color=(0,1,0,1))
        container.add_widget(self.res_label)
        
        scroll.add_widget(container)
        main_box.add_widget(scroll)
        self.add_widget(main_box)

    def calc(self, _):
        try:
            luna = float(self.in_luna.text)
            self.res_label.text = f"Listing: {int(luna * 1.35):,}"
        except:
            self.res_label.text = "Error"

# --- 2. CRAFTING (Working Logic Kept) ---
class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Tier Calc", halign="center", font_style="H5"))
        main_box.add_widget(header)
        self.add_widget(main_box)

# --- 3. INVENTORY (SKELETON MODE) ---
# Logic Disabled. Just UI to test crashing.
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        # HEADER
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Inventory (Safe Mode)", halign="center", font_style="H6"))
        main_box.add_widget(header)

        # STATIC BODY
        body = MDBoxLayout(orientation='vertical', padding="20dp", spacing="20dp")
        body.add_widget(MDLabel(text="Accounts Logic Disabled", halign="center"))
        body.add_widget(MDLabel(text="If you see this, the crash is fixed.", halign="center", theme_text_color="Custom", text_color=(0,1,0,1)))
        
        main_box.add_widget(body)
        self.add_widget(main_box)

# --- 4. CARDS (SKELETON MODE) ---
# Logic Disabled. Just UI to test crashing.
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        
        # HEADER
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Cards (Safe Mode)", halign="center"))
        main_box.add_widget(header)

        # STATIC BODY
        body = MDBoxLayout(orientation='vertical', padding="20dp", spacing="20dp")
        body.add_widget(MDLabel(text="Cards Logic Disabled", halign="center"))
        body.add_widget(MDLabel(text="If you see this, the crash is fixed.", halign="center", theme_text_color="Custom", text_color=(0,1,0,1)))
        
        main_box.add_widget(body)
        self.add_widget(main_box)

# --- PLACEHOLDERS FOR OTHER SCREENS ---
# These exist so the code doesn't break, but they are empty.
class TradeListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="Trades Placeholder", halign="center"))
        self.add_widget(MDFillRoundFlatButton(text="BACK", pos_hint={'center_x':0.5, 'center_y':0.2}, on_release=lambda x: setattr(self.manager, 'current', 'menu')))

class InventoryEditScreen(BaseScreen): pass
class AddAccountScreen(BaseScreen): pass
class EditItemQtyScreen(BaseScreen): pass
class TradeRecipientsScreen(BaseScreen): pass
class AddRecipientScreen(BaseScreen): pass
class TradeDetailsScreen(BaseScreen): pass
class CardEditScreen(BaseScreen): pass

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
        
        # Placeholders
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(InventoryEditScreen(name='inventory_edit'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(EditItemQtyScreen(name='edit_item_qty'))
        sm.add_widget(TradeRecipientsScreen(name='trade_recipients'))
        sm.add_widget(AddRecipientScreen(name='add_recipient'))
        sm.add_widget(TradeDetailsScreen(name='trade_details'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        
        return sm

if __name__ == '__main__':
    UltimateApp().run()
