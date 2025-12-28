import json
import os
import math
import traceback
from functools import partial
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform

# --- VERSION 7.0 (NO CARDS / SETTINGS ADDED) ---

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

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

def reset_all_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

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
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list'),
            ("SETTINGS / RESET", (0.4, 0.4, 0.4, 1), 'settings')
        ]

        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="16sp", size_hint=(1, None), height="55dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)
        
        self.add_widget(layout)
        
        ver = MDLabel(text="v7.0", halign="right", theme_text_color="Secondary", font_style="Caption", pos_hint={'right': 0.95, 'y': 0.02}, size_hint=(None, None), size=("100dp", "20dp"))
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.current = route

# --- SETTINGS SCREEN (NEW) ---
class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        
        layout.add_widget(
