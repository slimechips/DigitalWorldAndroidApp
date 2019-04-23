from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar import ActionBar
import appdimens 

# LogoutBottomNavBar inheriting from ActionBar
class LogoutBottomNavBar(ActionBar):
    pass

# Logout_Confirm inheriting from Screen
# Define default button and title font sizes for this Screen
class Logout_Confirm(Screen):
    _button_font_size = appdimens.button_font_size
    _title_font_size = appdimens.title_font_size
    
    # When loading, set all buttons to be inactive button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["logout_btm_bar"].ids["stalls_btn"].state = "normal"
        self.ids["logout_btm_bar"].ids["my_orders_btn"].state = "normal"