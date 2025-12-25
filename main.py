from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import math

# --- LOGIC CONSTANTS ---
TIER_VALUES = {
    "T3": 1,
    "T4": 4,
    "T5": 20,
    "T6": 120
}

# =========================================================================
# 1. MAIN MENU SCREEN
# =========================================================================
class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20, pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        # Title
        title = MDLabel(
            text="TOOLKIT",
            halign="center",
            font_style="H3",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(title)

        # Button 1: Black Market
        btn_market = MDFillRoundFlatButton(
            text="BLACK MARKET EXCHANGE",
            font_size=18,
            size_hint=(1, None),
            height=60,
            md_bg_color=(0.9, 0.3, 0.2, 1)  # Red accent
        )
        btn_market.bind(on_release=lambda x: self.change_screen("market"))
        layout.add_widget(btn_market)

        # Button 2: Tier Calc
        btn_tier = MDFillRoundFlatButton(
            text="TIER CRAFTING CALC",
            font_size=18,
            size_hint=(1, None),
            height=60,
            md_bg_color=(0.2, 0.6, 0.8, 1)  # Blue accent
        )
        btn_tier.bind(on_release=lambda x: self.change_screen("tier"))
        layout.add_widget(btn_tier)
        
        # Spacer
        layout.add_widget(Widget())

        self.add_widget(layout)

    def change_screen(self, screen_name):
        self.manager.current = screen_name
        self.manager.transition.direction = 'left'


# =========================================================================
# 2. BLACK MARKET SCREEN
# =========================================================================
class BlackMarketScreen(MDScreen):
    cost_result = StringProperty("0")
    rate_result = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main Layout
        root = MDBoxLayout(orientation='vertical', spacing=10)
        
        # --- App Bar (Back Button) ---
        toolbar = MDBoxLayout(size_hint_y=None, height=60, padding=[10, 0])
        back_btn = MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1))
        back_btn.bind(on_release=self.go_back)
        lbl_title = MDLabel(text="Black Market", font_style="H5", halign="left", theme_text_color="Custom", text_color=(1,1,1,1))
        toolbar.add_widget(back_btn)
        toolbar.add_widget(lbl_title)
        root.add_widget(toolbar)

        # --- Content ---
        content = MDBoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Input: Rubbles
        self.in_rubbles = MDTextField(
            hint_text="Selling Rubbles",
            input_filter="int",
            mode="rectangle",
            line_color_focus=(0.9, 0.3, 0.2, 1)
        )
        content.add_widget(self.in_rubbles)

        # Input: Luna
        self.in_luna = MDTextField(
            hint_text="Receiving Luna",
            input_filter="int",
            mode="rectangle",
            line_color_focus=(0.9, 0.3, 0.2, 1)
        )
        content.add_widget(self.in_luna)

        # Calculate Button
        btn_calc = MDFillRoundFlatButton(
            text="CALCULATE DEAL",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0.9, 0.3, 0.2, 1)
        )
        btn_calc.bind(on_release=self.calculate)
        content.add_widget(btn_calc)

        # Results Grid
        res_grid = MDGridLayout(cols=2, spacing=20, size_hint_y=None, height=150)
        
        # Listing Price Box
        card1 = MDCard(orientation='vertical', padding=10, md_bg_color=(0.2, 0.2, 0.2, 1))
        card1.add_widget(MDLabel(text="LISTING PRICE", font_style="Caption", theme_text_color="Hint"))
        self.lbl_cost = MDLabel(text="0", font_style="H4", theme_text_color="Custom", text_color=(0.9, 0.3, 0.2, 1))
        card1.add_widget(self.lbl_cost)
        
        # Rate Box
        card2 = MDCard(orientation='vertical', padding=10, md_bg_color=(0.2, 0.2, 0.2, 1))
        card2.add_widget(MDLabel(text="EXCHANGE RATE", font_style="Caption", theme_text_color="Hint"))
        self.lbl_rate = MDLabel(text="0", font_style="H4", theme_text_color="Custom", text_color=(0.2, 0.6, 0.9, 1))
        card2.add_widget(self.lbl_rate)

        res_grid.add_widget(card1)
        res_grid.add_widget(card2)
        content.add_widget(res_grid)
        
        # Footer
        content.add_widget(MDLabel(text="*Includes 35% Market Fee", font_style="Caption", halign="center"))
        content.add_widget(Widget()) # Spacer

        root.add_widget(content)
        self.add_widget(root)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def calculate(self, instance):
        try:
            r_val = float(self.in_rubbles.text or 0)
            l_val = float(self.in_luna.text or 0)

            # Logic
            listing_price = math.ceil(l_val * 1.35)
            
            display_rate = 0
            if r_val > 0:
                display_rate = int((l_val / r_val) * 1_000_000)

            self.lbl_cost.text = f"{listing_price:,}"
            self.lbl_rate.text = f"{display_rate}"

        except ValueError:
            self.lbl_cost.text = "ERR"

# =========================================================================
# 3. TIER CALC SCREEN
# =========================================================================
class TierCalcScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main Layout
        root = MDBoxLayout(orientation='vertical')

        # --- App Bar ---
        toolbar = MDBoxLayout(size_hint_y=None, height=60, padding=[10, 0])
        back_btn = MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1,1,1,1))
        back_btn.bind(on_release=self.go_back)
        lbl_title = MDLabel(text="Tier Crafting", font_style="H5", halign="left", theme_text_color="Custom", text_color=(1,1,1,1))
        toolbar.add_widget(back_btn)
        toolbar.add_widget(lbl_title)
        root.add_widget(toolbar)

        # Scroll View for Mobile friendliness
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', padding=20, spacing=15, adaptive_height=True)

        # -- Target Section --
        content.add_widget(MDLabel(text="TARGET", theme_text_color="Secondary", font_style="Button"))
        target_grid = MDGridLayout(cols=2, spacing=10, size_hint_y=None, height=80)
        
        self.in_qty = MDTextField(hint_text="Qty", text="1", input_filter="int", mode="rectangle")
        self.in_tier = MDTextField(hint_text="Tier (T4/T5/T6)", text="T6", mode="rectangle") # Using Text field for simplicity in mobile
        
        target_grid.add_widget(self.in_qty)
        target_grid.add_widget(self.in_tier)
        content.add_widget(target_grid)

        # -- Inventory Section --
        content.add_widget(MDLabel(text="INVENTORY", theme_text_color="Secondary", font_style="Button"))
        
        self.inv_inputs = {}
        inv_grid = MDGridLayout(cols=4, spacing=10, size_hint_y=None, height=80)
        
        for tier in ["T6", "T5", "T4", "T3"]:
            field = MDTextField(hint_text=tier, input_filter="int", mode="fill")
            self.inv_inputs[tier] = field
            inv_grid.add_widget(field)
            
        content.add_widget(inv_grid)

        # Button
        btn_calc = MDFillRoundFlatButton(
            text="CALCULATE RESOURCES",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        btn_calc.bind(on_release=self.calculate)
        content.add_widget(btn_calc)

        # -- Results --
        self.lbl_status = MDLabel(
            text="Ready to calculate", 
            halign="center", 
            font_style="H6", 
            theme_text_color="Hint"
        )
        content.add_widget(self.lbl_status)
        
        self.lbl_breakdown = MDLabel(
            text="", 
            halign="left",
            theme_text_color="Custom",
            text_color=(1,1,1,1)
        )
        content.add_widget(self.lbl_breakdown)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def get_breakdown(self, deficit, max_tier):
        if deficit <= 0: return ""
        results = []
        remaining = deficit
        tiers = ["T6", "T5", "T4", "T3"] if max_tier == "T6" else ["T5", "T4", "T3"]
        
        for t in tiers:
            val = TIER_VALUES[t]
            if remaining >= val:
                count = remaining // val
                remaining = remaining % val
                results.append(f"{count} {t}")
        if remaining > 0: results.append(f"{remaining} T3")
        return " + ".join(results)

    def calculate(self, instance):
        try:
            # Inputs
            t_tier = self.in_tier.text.upper()
            if t_tier not in TIER_VALUES: t_tier = "T6" # Default fallback
            
            t_qty = int(self.in_qty.text or 0)
            goal_pts = t_qty * TIER_VALUES[t_tier]

            curr_pts = 0
            for tier, field in self.inv_inputs.items():
                curr_pts += int(field.text or 0) * TIER_VALUES[tier]

            deficit = goal_pts - curr_pts

            if deficit <= 0:
                self.lbl_status.text = "COMPLETE!"
                self.lbl_status.text_color = (0, 1, 0, 1)
                self.lbl_breakdown.text = "You have enough resources."
            else:
                self.lbl_status.text = f"MISSING: {deficit} POINTS"
                self.lbl_status.text_color = (1, 0.3, 0.3, 1)
                
                # Logic text
                pure_t3 = f"Base: {deficit} x T3"
                efficient = f"Mixed: {self.get_breakdown(deficit, 'T5')}"
                
                self.lbl_breakdown.text = f"{pure_t3}\n\n{efficient}"

        except ValueError:
            self.lbl_status.text = "Error: Check inputs"

# =========================================================================
# APP BUILD
# =========================================================================
class UltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        
        sm = MDScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BlackMarketScreen(name='market'))
        sm.add_widget(TierCalcScreen(name='tier'))
        return sm

if __name__ == "__main__":
    UltimateApp().run()
