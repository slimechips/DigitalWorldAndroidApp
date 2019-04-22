#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

import database

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
        self.food_info = self.food_widget.food_info

    def order(self):
        food = self.food_info
        database.create_order(1, "chicken_rice", food.stall_id, food.food_name,
                              food.food_id, "None", food.price, 2, 
                              self.order_uploaded)

    def order_uploaded(self):
        pass    
    
    def go_back(self):
        self.manager.current = self.manager.previous()

class FoodPicture2(ButtonBehavior, AsyncImage):
    pass
