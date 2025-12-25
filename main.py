from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

# FIX: Only resize window if running on PC (Windows/Linux/MacOS)
# On Android, we skip this so the app fills the screen automatically.
if platform not in ['android', 'ios']:
    Window.size = (360, 800)

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout centered
        layout = MDBoxLayout(orientation='vertical', spacing="20dp", padding="30dp")
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        layout.adaptive_height = True  # This shrinks the layout to fit content

        # Title
        title = MDLabel(
            text="TOOLKIT",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H3",
            size_hint_y=None,
            height="100dp"
        )

        # BIG BUTTON 1: Black Market
        btn_market = MDFillRoundFlatButton(
            text="BLACK MARKET EXCHANGE",
            font_size="18sp",  # Increased font size
            size_hint=(1, None),
            height="60dp",     # Taller button
            md_bg_color=(0.9, 0.3, 0.2, 1), # Red/Orange
            on_release=self.go_market
        )

        # BIG BUTTON 2: Tier Crafting
        btn_craft = MDFillRoundFlatButton(
            text="TIER CRAFTING CALC",
            font_size="18sp",  # Increased font size
            size_hint=(1, None),
            height="60dp",     # Taller button
            md_bg_color=(0.2, 0.6, 0.8, 1), # Blue
            on_release=self.go_crafting
        )

        layout.add_widget(title)
        layout.add_widget(btn_market)
        layout.add_widget(btn_craft)
        self.add_widget(layout)

    def go_market(self, instance):
        self.manager.current = 'market'

    def go_crafting(self, instance):
        self.manager.current = 'crafting'


class MarketScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ScrollView ensures content never gets cut off on small screens
        scroll = MDScrollView()
        
        # Main Container
        container = MDBoxLayout(
            orientation='vertical', 
            spacing="25dp", 
            padding="20dp",
            adaptive_height=True, # Critical for ScrollView
            pos_hint={"top": 1}   # Starts at the top
        )

        # Spacer to push content down slightly from status bar
        container.add_widget(MDLabel(size_hint_y=None, height="20dp"))

        # Header
        header = MDLabel(
            text="Black Market",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height="50dp"
        )
        container.add_widget(header)

        # Input Card
        card = MDCard(
            orientation='vertical',
            padding="20dp",
            spacing="20dp",
            size_hint=(1, None),
            height="200dp", # Fixed height for inputs
            radius=[15],
            md_bg_color=(0.15, 0.15, 0.15, 1) # Dark grey background
        )

        self.input_rubbles = MDTextField(
            hint_text="Selling Rubbles",
            mode="rectangle",
            input_filter="float",
            font_size="18sp"
        )
        
        self.input_luna = MDTextField(
            hint_text="Receiving Luna",
            mode="rectangle",
            input_filter="float",
            font_size="18sp"
        )

        card.add_widget(self.input_rubbles)
        card.add_widget(self.input_luna)
        container.add_widget(card)

        # Action Button
        btn_calc = MDFillRoundFlatButton(
            text="CALCULATE DEAL",
            font_size="20sp",
            size_hint=(1, None),
            height="60dp",
            md_bg_color=(0.9, 0.3, 0.2, 1),
            on_release=self.calculate
        )
        container.add_widget(btn_calc)

        # Results Area (Grid for 2 big boxes)
        results_grid = MDGridLayout(cols=2, spacing="10dp", size_hint_y=None, height="100dp")
        
        # Result 1
        self.res_listing = self.create_result_box("LISTING PRICE", "0")
        # Result 2
        self.res_rate = self.create_result_box("EXCHANGE RATE", "0")
        
        results_grid.add_widget(self.res_listing)
        results_grid.add_widget(self.res_rate)
        container.add_widget(results_grid)

        # Back Button
        btn_back = MDFillRoundFlatButton(
            text="BACK TO MENU",
            size_hint=(1, None),
            height="50dp",
            md_bg_color=(0.4, 0.4, 0.4, 1),
            on_release=self.go_back
        )
        container.add_widget(btn_back)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def create_result_box(self, title, value):
        box = MDCard(orientation='vertical', padding="10dp", md_bg_color=(0.2, 0.2, 0.2, 1))
        lbl_title = MDLabel(text=title, font_style="Caption", theme_text_color="Secondary")
        self.lbl_value_ref = MDLabel(text=value, font_style="H5", halign="center", theme_text_color="Custom", text_color=(0.9, 0.3, 0.2, 1))
        box.add_widget(lbl_title)
        box.add_widget(self.lbl_value_ref)
        # Store reference manually since I'm creating a new object (simple hack for this example)
        box.value_label = self.lbl_value_ref 
        return box

    def calculate(self, instance):
        try:
            r = float(self.input_rubbles.text)
            l = float(self.input_luna.text)
            
            # Fee calculation (35%)
            fee = r * 0.35
            profit = r - fee
            rate = profit / l if l > 0 else 0
            
            self.res_listing.value_label.text = f"{profit:,.0f}"
            self.res_rate.value_label.text = f"{rate:,.0f}"
            self.res_rate.value_label.text_color = (0.2, 0.6, 0.8, 1) # Blue
            
        except ValueError:
            self.res_listing.value_label.text = "Error"

    def go_back(self, instance):
        self.manager.current = 'menu'


class CraftingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ScrollView prevents overlap on small screens
        scroll = MDScrollView()
        
        container = MDBoxLayout(
            orientation='vertical', 
            spacing="20dp", 
            padding="20dp",
            adaptive_height=True
        )

        # Header
        header = MDLabel(
            text="Tier Crafting",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height="50dp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        container.add_widget(header)

        # Section 1: Target
        container.add_widget(MDLabel(text="TARGET ITEM", theme_text_color="Secondary", size_hint_y=None, height="30dp"))
        
        target_grid = MDGridLayout(cols=2, spacing="15dp", size_hint_y=None, height="80dp")
        self.in_qty = MDTextField(hint_text="Quantity", mode="rectangle", input_filter="int")
        self.in_tier = MDTextField(hint_text="Tier (4/5/6)", mode="rectangle", input_filter="int")
        target_grid.add_widget(self.in_qty)
        target_grid.add_widget(self.in_tier)
        container.add_widget(target_grid)

        # Section 2: Inventory
        container.add_widget(MDLabel(text="YOUR INVENTORY", theme_text_color="Secondary", size_hint_y=None, height="30dp"))
        
        # Grid for Inventory Inputs (2x2)
        inv_grid = MDGridLayout(cols=2, spacing="15dp", adaptive_height=True)
        
        self.inv_t6 = MDTextField(hint_text="T6 Count", mode="rectangle", input_filter="int")
        self.inv_t5 = MDTextField(hint_text="T5 Count", mode="rectangle", input_filter="int")
        self.inv_t4 = MDTextField(hint_text="T4 Count", mode="rectangle", input_filter="int")
        self.inv_t3 = MDTextField(hint_text="T3 Count", mode="rectangle", input_filter="int")
        
        inv_grid.add_widget(self.inv_t6)
        inv_grid.add_widget(self.inv_t5)
        inv_grid.add_widget(self.inv_t4)
        inv_grid.add_widget(self.inv_t3)
        container.add_widget(inv_grid)

        # Spacer
        container.add_widget(MDLabel(size_hint_y=None, height="10dp"))

        # Calculate Button
        btn_calc = MDFillRoundFlatButton(
            text="CALCULATE RESOURCES",
            font_size="18sp",
            size_hint=(1, None),
            height="60dp",
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_release=self.calculate
        )
        container.add_widget(btn_calc)

        # Result Label
        self.result_lbl = MDLabel(
            text="Ready to calculate",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height="50dp"
        )
        container.add_widget(self.result_lbl)

        # Back Button
        btn_back = MDFillRoundFlatButton(
            text="BACK TO MENU",
            size_hint=(1, None),
            height="50dp",
            md_bg_color=(0.4, 0.4, 0.4, 1),
            on_release=self.go_back
        )
        container.add_widget(btn_back)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def calculate(self, instance):
        # Placeholder logic - replace with your real math
        self.result_lbl.text = "Calculation Complete (Logic Placeholder)"

    def go_back(self, instance):
        self.manager.current = 'menu'


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(CraftingScreen(name='crafting'))
        return sm

if __name__ == '__main__':
    MyApp().run()
