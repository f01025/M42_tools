import json
import os
from functools import partial
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
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

# --- DATA HANDLING ---
def get_data_path():
    app = MDApp.get_running_app()
    if platform == 'android':
        return os.path.join(app.user_data_dir, "data.json")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def load_data():
    path = get_data_path()
    if not os.path.exists(path):
        return {"accounts": {}, "cards": {}}
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if "accounts" not in data: data["accounts"] = {}
            if "cards" not in data: data["cards"] = {}
            return data
    except:
        return {"accounts": {}, "cards": {}}

def save_data(data):
    try:
        with open(get_data_path(), "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

# --- UI CLASSES ---
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

        layout.add_widget(MDLabel(text="ULTIMATE TOOLKIT", halign="center", font_style="H4", theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        
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
        
        layout.add_widget(MDLabel(size_hint_y=None, height="20dp"))
        settings_btn = MDIconButton(icon="cog", theme_text_color="Custom", text_color=(0.5, 0.5, 0.5, 1), pos_hint={'center_x': 0.5}, on_release=lambda x: self.go_to('settings'))
        layout.add_widget(settings_btn)
        
        self.add_widget(layout)

    def go_to(self, route):
        self.manager.transition = NoTransition()
        self.manager.current = route

class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="20dp", padding="40dp")
        layout.add_widget(MDFillRoundFlatButton(text="< BACK", md_bg_color=(0.3, 0.3, 0.3, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        layout.add_widget(MDLabel(text="Settings", halign="center", font_style="H5"))
        btn_reset = MDFillRoundFlatButton(text="RESET DATA", md_bg_color=(0.8, 0, 0, 1), size_hint=(1, None), on_release=self.reset_data)
        layout.add_widget(btn_reset)
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def reset_data(self, _):
        if os.path.exists(get_data_path()):
            os.remove(get_data_path())
        self.manager.current = 'menu'

# --- 1. BLACK MARKET (FIXED LAYOUT) ---
class MarketScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Vertical Box to stack Header -> Scroll
        root = MDBoxLayout(orientation='vertical')
        
        # Header (Fixed Top)
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Black Market", halign="center", font_style="H5"))
        root.add_widget(header)

        # Scrollable Content
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

# --- 2. CRAFTING (FIXED LAYOUT) ---
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

# --- HELPER SCREENS ---
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

class AddItemScreen(BaseScreen):
    # SIMPLE ADD ITEM SCREEN (Replaces Bottom Sheet crash)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="20dp")
        layout.add_widget(MDLabel(text="Add Item", halign="center", font_style="H5"))
        self.name_field = MDTextField(hint_text="Item Name", mode="rectangle")
        layout.add_widget(self.name_field)
        self.qty_field = MDTextField(hint_text="Quantity", mode="rectangle", input_filter="int")
        layout.add_widget(self.qty_field)
        layout.add_widget(MDFillRoundFlatButton(text="SAVE", on_release=self.save))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, account_name):
        self.account_name = account_name
        self.name_field.text = ""
        self.qty_field.text = ""

    def save(self, _):
        item = self.name_field.text.strip()
        qty = self.qty_field.text
        if item and qty:
            data = load_data()
            if self.account_name in data["accounts"]:
                data["accounts"][self.account_name]["items"][item] = int(qty)
                save_data(data)
        self.manager.current = 'inventory_edit'
        self.manager.get_screen('inventory_edit').load_account(self.account_name)

    def cancel(self, _):
        self.manager.current = 'inventory_edit'

class AddCardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        layout = MDBoxLayout(orientation='vertical', padding="30dp", spacing="10dp")
        layout.add_widget(MDLabel(text="Add Card", halign="center", font_style="H5"))
        self.name_f = MDTextField(hint_text="Card Name", mode="rectangle")
        layout.add_widget(self.name_f)
        self.tier_f = MDTextField(hint_text="Tier (2-6)", mode="rectangle", input_filter="int")
        layout.add_widget(self.tier_f)
        self.qty_f = MDTextField(hint_text="Quantity", mode="rectangle", input_filter="int")
        layout.add_widget(self.qty_f)
        layout.add_widget(MDFillRoundFlatButton(text="SAVE", on_release=self.save))
        layout.add_widget(MDFlatButton(text="CANCEL", on_release=self.cancel))
        layout.add_widget(MDLabel())
        self.add_widget(layout)

    def setup(self, account_name):
        self.account_name = account_name
        self.name_f.text = ""
        self.tier_f.text = ""
        self.qty_f.text = ""

    def save(self, _):
        if self.name_f.text and self.tier_f.text and self.qty_f.text:
            data = load_data()
            if self.account_name in data["cards"]:
                new_card = {
                    "name": self.name_f.text,
                    "tier": self.tier_f.text,
                    "qty": int(self.qty_f.text)
                }
                data["cards"][self.account_name].append(new_card)
                save_data(data)
        self.manager.current = 'card_edit'
        self.manager.get_screen('card_edit').load_account(self.account_name)

    def cancel(self, _):
        self.manager.current = 'card_edit'

# --- 4. INVENTORY SCREENS (TEXT ONLY - NO IMAGES) ---
class InventoryListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< MENU", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'menu')))
        header.add_widget(MDLabel(text="Inventory", halign="center", font_style="H6"))
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        fab = MDFloatingActionButton(icon="plus", md_bg_color=(0.2, 0.6, 0.8, 1), pos_hint={'right': 0.95, 'y': 0.05})
        fab.bind(on_release=self.go_add)
        self.add_widget(fab)
        self.add_widget(main_box)

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
            self.list_view.add_widget(OneLineListItem(text="No Accounts"))
        for name in accounts:
            # TEXT ONLY to prevent crash
            item = TwoLineListItem(
                text=name, 
                secondary_text="Tap to view items",
                on_release=lambda x, n=name: self.open_account(n)
            )
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
        footer.add_widget(MDFillRoundFlatButton(text="ADD ITEM", size_hint_x=0.7, on_release=self.go_add_item))
        footer.add_widget(MDIconButton(icon="trash-can", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account))
        main_box.add_widget(footer)
        self.add_widget(main_box)

    def load_account(self, name):
        self.account_name = name
        self.toolbar_lbl.text = name
        self.refresh_items()

    def refresh_items(self):
        self.list_view.clear_widgets()
        data = load_data()
        items = data["accounts"].get(self.account_name, {}).get("items", {})
        for item_name, qty in items.items():
            # TEXT ONLY to prevent crash
            row = TwoLineListItem(
                text=str(item_name), 
                secondary_text=f"Quantity: {qty}"
            )
            self.list_view.add_widget(row)

    def go_add_item(self, _):
        self.manager.get_screen('add_item').setup(self.account_name)
        self.manager.current = 'add_item'

    def delete_account(self, _):
        data = load_data()
        if self.account_name in data["accounts"]:
            del data["accounts"][self.account_name]
            save_data(data)
        self.go_back(None)

    def go_back(self, _):
        self.manager.current = 'inventory_list'

# --- 5. CARD SCREENS (TEXT ONLY) ---
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
        self.add_widget(main_box)

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
            # TEXT ONLY
            item = TwoLineListItem(
                text=str(name), 
                secondary_text="Tap to view", 
                on_release=lambda x, n=name: self.open_cards(n)
            )
            self.list_view.add_widget(item)

    def open_cards(self, name):
        self.manager.get_screen('card_edit').load_account(name)
        self.manager.current = 'card_edit'

class CardEditScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_name = ""
        main_box = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        header.add_widget(MDFillRoundFlatButton(text="< BACK", size_hint=(0.3, 1), md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: setattr(self.manager, 'current', 'card_list')))
        self.title_lbl = MDLabel(text="Cards", halign="center")
        header.add_widget(self.title_lbl)
        main_box.add_widget(header)

        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        main_box.add_widget(scroll)
        
        footer = MDBoxLayout(size_hint_y=None, height="60dp", padding="5dp", spacing="10dp")
        footer.add_widget(MDFillRoundFlatButton(text="ADD CARD", size_hint_x=0.7, on_release=self.go_add_card))
        footer.add_widget(MDIconButton(icon="trash-can", md_bg_color=(0.8,0.2,0.2,1), on_release=self.delete_account))
        main_box.add_widget(footer)
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
            # TEXT ONLY
            row = TwoLineListItem(
                text=str(c.get('name', 'Unknown')), 
                secondary_text=f"Tier: {c.get('tier', '?')} | Qty: {c.get('qty', 0)}"
            )
            self.list_view.add_widget(row)

    def go_add_card(self, _):
        self.manager.get_screen('add_card').setup(self.account_name)
        self.manager.current = 'add_card'

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
        
        # Safe Data Init
        if not os.path.exists(get_data_path()):
            save_data({"accounts": {}, "cards": {}, "active_trades": {}})

        sm = ScreenManager(transition=NoTransition())
        # Define ALL screens (Order matters for definition, not adding)
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(CraftingScreen(name='crafting'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(AddItemScreen(name='add_item'))
        sm.add_widget(AddCardScreen(name='add_card'))
        sm.add_widget(InventoryListScreen(name='inventory_list'))
        sm.add_widget(InventoryEditScreen(name='inventory_edit'))
        sm.add_widget(CardListScreen(name='card_list'))
        sm.add_widget(CardEditScreen(name='card_edit'))
        return sm

if __name__ == '__main__':
    UltimateApp().run()
