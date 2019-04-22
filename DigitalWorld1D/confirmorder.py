#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.logger import Logger

import database
import user

class ConfirmOrder(Screen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        orig_food_widget = self.manager.food_item
        self.food_widget = FoodPicture2(id=orig_food_widget.id,
                                   source=orig_food_widget.source)
        orig_food_label = self.manager.food_item.food_label
        self.food_label = Label(text=orig_food_label.text, 
                           font_size=orig_food_label.font_size, 
                           color=orig_food_label.color, 
                           height=orig_food_label.height)
        self.ids["grid_layout"].add_widget(self.food_widget, 2)
        self.ids["grid_layout"].add_widget(self.food_label, 2)
        self.food_info = orig_food_widget.food_info

    def order(self, num_in_q=None):
        food = self.food_info
        stall_name = self.manager.current_stall
        if num_in_q == None:
            database.get_num_in_q(stall_name, self.order)
        else:
            database.create_order(user.current_user.uid, stall_name, 
                                food.stall_id, 
                                food.food_name,
                                food.food_id, "None", food.price,
                                num_in_q,
                                food.waiting_time,
                                self.order_uploaded)

    def order_uploaded(self):
        Logger.info("Order: Uploaded")
        self.manager.current = "my_orders"
    
    def go_back(self):
        self.manager.current = self.manager.previous()

class FoodPicture2(ButtonBehavior, AsyncImage):
    pass
