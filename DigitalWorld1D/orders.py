from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import user
import database
import appdimens
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from functools import partial

class FoodPicture(ButtonBehavior, AsyncImage):
    def on_release(self):
        super().on_release()
        self.parent.parent.parent.parent.goto_confirm(self)

class My_Orders(Screen):
    # When loading, setup the orders to be active button in nav bar

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.picture = []
        self.got_orders = []
        self.grd = self.ids["orders_grd"]
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"
        self.retrieve_orders(None)
        Clock.schedule_interval(self.retrieve_orders, 30)

    def retrieve_orders(self, dt):
        # retrieve list from Firebase
        current_user_uid = user.current_user.uid
        database.check_my_orders(current_user_uid, self.got_orders)

    def got_orders(self, order_ls):
        self.orders = order_ls
        for order in self.orders:
            self.got_orders.append('')
        for idx, order in enumerate(self.orders):
            self.retrieve_url(self.order.food_item, self.order.stall_id)

    def retrieve_url(self, idx):
        database.query_picture_url(stall, food_name, idx, got_url)

    def got_url(self, pictureURL, idx):
        self.picture[idx] = pictureURL
        self.got_datas()
    
    def got_datas(self):
        if '' not in self.picture:
            self.update_UI()

    def update_UI(self):
        for order in order_ls:
            picture = FoodPicture(source=order.photo_url)
            food_name = order.food_item
            waiting_time = order.est_wait
            orders_in_q = order.num_in_q
            stall = order.current_stall
            label_text = """{}\nEstimated Waiting Time: 
                        {}\n Orders in Queue: {}\n Stall: {}""".format(food_name,
                        waiting_time, orders_in_q, stall)
            label = Label(text=label_text, font_size=40, 
                          color=[0, 0, 0, 1], 
                          height=appdimens.stall_screen_height)
            self.grd.add_widget(picture)
            self.grd.add_widget(label)