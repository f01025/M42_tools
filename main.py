import json
import os
import traceback
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

if platform not in ['android', 'ios']:
    Window.size = (360, 800)

# --- SAFE DATA HANDLING ---
def get_data_path():
    app = MDApp.get_running_app()
    if platform == 'android':
        return os.path.join(app.user_data_dir, "data.json")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def load_data():
    # Helper to load data safely
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

# --- SCREENS ---
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
            ("INVENTORY", (0.3, 0.7, 0.3, 1), 'inventory_list'),
            ("CARDS", (0.6, 0.3, 0.8, 1), 'card_list')
        ]

        for text, color, route in btns:
            btn = MDFillRoundFlatButton(
                text=text, font_size="16sp", size_hint=(1, None), height="55dp",
                md_bg_color=color, on_release=lambda x, r=route: self.go_to(r)
            )
            layout.add_widget(btn)
        
        self.add_widget(layout)
        
        # Version Label
        ver = MDLabel(text="v17.0 Clean", halign="right", theme_text_color="Secondary", font_style="Caption", pos_hint={'right': 0.95, 'y': 0.02}, size_hint=(None, None), size=("100dp", "20dp"))
        self.add_widget(ver)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

# --- 1. BLACK MARKET (Restored) ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Root is Vertical
        root = MDBoxLayout(orientation='vertical')
        
        # HEADER
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        root.add_widget(header)

        # SCROLL CONTENT
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        
        self.in_rub = MDTextField(hint_text="Rubles", mode="rectangle", input_filter="float")
        self.in_luna = MDTextField(hint_text="Luna", mode="rectangle", input_filter="float")
        content.add_widget(self.in_rub)
        content.add_widget(self.in_luna)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.9, 0.3, 0.2, 1), on_release=self.calc)
        content.add_widget(btn)
        
        grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)
        self.res_list = self.create_res_box("Listing Price", "0")
        self.res_rate = self.create_res_box("Exchange Rate", "0")
        grid.add_widget(self.res_list)
        grid.add_widget(self.res_rate)
        content.add_widget(grid)
        
        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

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

# --- 2. CRAFTING (Restored) ---
class CraftingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Tier Calc", halign="center", font_style="H5"))
        root.add_widget(header)

        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp", adaptive_height=True)
        
        self.in_qty = MDTextField(hint_text="Qty Cards", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4, 5, or 6)", mode="rectangle", input_filter="int")
        content.add_widget(self.in_qty)
        content.add_widget(self.in_tier)
        
        self.inv_t3 = MDTextField(hint_text="T3", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5", mode="rectangle", input_filter="int")
        self.inv_t6 = MDTextField(hint_text="T6", mode="rectangle", input_filter="int")
        content.add_widget(self.inv_t3)
        content.add_widget(self.inv_t4)
        content.add_widget(self.inv_t5)
        content.add_widget(self.inv_t6)
        
        btn = MDFillRoundFlatButton(text="CALCULATE", size_hint=(1, None), height="50dp", md_bg_color=(0.2, 0.6, 0.8, 1), on_release=self.calc)
        content.add_widget(btn)
        
        self.res_card = MDCard(orientation='vertical', padding="15dp", spacing="10dp", size_hint_y=None, height="200dp", md_bg_color=(0.15, 0.15, 0.15, 1))
        self.res_opt1 = MDLabel(text="", theme_text_color="Primary", font_style="Body1", halign="center")
        self.res_opt2 = MDLabel(text="", theme_text_color="Custom", text_color=(0.4, 0.8, 1, 1), font_style="Body1", halign="center")
        self.res_card.add_widget(MDLabel(text="Missing Resources", theme_text_color="Secondary", font_style="Caption", halign="center"))
        self.res_card.add_widget(self.res_opt1)
        self.res_card.add_widget(self.res_opt2)
        content.add_widget(self.res_card)
        
        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

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

# --- 3. ADD ACCOUNT (Shared) ---
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
        
        # LOGIC: Only Create Name Key. No items/cards yet.
        if self.target_screen == 'inventory_list':
            if name not in data["inventory"]: 
                data["inventory"][name] = {}
        elif self.target_screen == 'card_list':
            if name not in data["cards"]: 
                data["cards"][name] = {}
        
        save_data(data)
        self.go_back()

    def cancel(self, _):
        self.go_back()

    def go_back(self):
        self.manager.current = self.target_screen

# --- 4. INVENTORY LIST (Clean, No Item Loading) ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Inventory", halign="center", font_style="H6"))
        root.add_widget(header)

        # Scrollable Area for Accounts
        scroll = MDScrollView()
        self.grid = MDGridLayout(cols=1, spacing="10dp", padding="15dp", adaptive_height=True)
        scroll.add_widget(self.grid)
        root.add_widget(scroll)
        
        self.add_widget(root)
        
        # Floating Action Button
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

    def on_enter(self):
        self.refresh_list()

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('inventory_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.grid.clear_widgets()
        data = load_data()
        accounts = data.get("inventory", {})
        
        if not accounts:
            self.grid.add_widget(MDLabel(text="No Accounts", halign="center"))
        
        for name in accounts:
            # Simple Button for Account
            btn = MDFillRoundFlatButton(
                text=name, 
                size_hint=(1, None), 
                height="60dp", 
                md_bg_color=(0.3, 0.3, 0.3, 1)
            )
            self.grid.add_widget(btn)

# --- 5. CARD LIST (Clean, No Item Loading) ---
class CardListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Cards", halign="center", font_style="H6"))
        root.add_widget(header)

        scroll = MDScrollView()
        self.grid = MDGridLayout(cols=1, spacing="10dp", padding="15dp", adaptive_height=True)
        scroll.add_widget(self.grid)
        root.add_widget(scroll)
        
        self.add_widget(root)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.6, 0.3, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)

    def on_enter(self):
        self.refresh_list()

    def go_add(self, _):
        self.manager.get_screen('add_account').setup('card_list')
        self.manager.current = 'add_account'

    def refresh_list(self):
        self.grid.clear_widgets()
        data = load_data()
        accounts = data.get("cards", {})
        
        if not accounts:
            self.grid.add_widget(MDLabel(text="No Accounts", halign="center"))
        
        for name in accounts:
            btn = MDFillRoundFlatButton(
                text=name, 
                size_hint=(1, None), 
                height="60dp", 
                md_bg_color=(0.3, 0.3, 0.3, 1)
            )
            self.grid.add_widget(btn)

# --- APP ---
class UltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        # FORCE DATA WIPE ON STARTUP (To Fix Crash)
        try:
            path = get_data_path()
            if os.path.exists(path):
                os.remove(path)
        except:
            pass

        try:
            sm = ScreenManager(transition=NoTransition())
            sm.add_widget(MenuScreen(name='menu'))
            sm.add_widget(MarketScreen(name='market'))
            sm.add_widget(CraftingScreen(name='crafting'))
            sm.add_widget(InventoryListScreen(name='inventory_list'))
            sm.add_widget(CardListScreen(name='card_list'))
            sm.add_widget(AddAccountScreen(name='add_account'))
            return sm
        except Exception as e:
            return MDLabel(text=f"Fatal Error: {e}", halign="center")

if __name__ == '__main__':
    UltimateApp().run()
