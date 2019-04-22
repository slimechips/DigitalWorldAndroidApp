from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import user
import database
import appdimens
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from functools import partial
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
# from importbarcode import gen_barcode_image

class FoodPicture(ButtonBehavior, AsyncImage):
    def on_release(self):
        super().on_release()
        self.parent.parent.parent.parent.goto_confirm(self)

class My_Orders(Screen):
    # When loading, setup the orders to be active button in nav bar

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.picture = []
        self.orders_ls = []
        self.box = self.ids["orders_box"]
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"
        self.retrieve_orders(None)
        Clock.schedule_interval(self.retrieve_orders, 30)

    def retrieve_orders(self, dt):
        # retrieve list from Firebase
        current_user_uid = user.current_user.uid
        database.check_my_orders(current_user_uid, self.got_orders)

    def got_orders(self, order_ls):
        self.orders_ls = order_ls
        for order in self.orders_ls:
            self.picture.append('')
        for idx, order in enumerate(self.orders_ls):
            self.retrieve_url(order.food_item, order.stall_id, idx)

    def retrieve_url(self, food_name, stall, idx):
        database.query_picture_url(stall, food_name, idx, self.got_url)

    def got_url(self, pictureURL, idx):
        self.picture[idx] = pictureURL
        self.got_datas()
    
    def got_datas(self):
        if '' not in self.picture:
            self.update_UI()

    def update_UI(self):
        for idx, order in enumerate(self.orders_ls):
            picture = FoodPicture(source=self.picture[idx], size_hint = (0.5, 1))
            if picture:
                print('Picture LOADED')
            food_name = order.food_item
            waiting_time = order.est_wait
            orders_in_q = order.num_in_q
            stall = order.current_stall
            status = order.status
            stall_name = self.mk_stall_name(stall)
            my_box_layout = BoxLayout(orientation="horizontal", size_hint_y=None)
            label_text = """[b][u]{}[/u][/b]\n[b]Status: [/b]{}\n[b]Arriving:[/b] {} mins\n[b]Orders in Queue:[/b] {}\n[b]Stall:[/b] {}""".format(food_name,
                        status, waiting_time, orders_in_q, stall_name)
            label = Label(text=label_text, size_hint = (0.5, 1), font_size=40, 
                          color=[0, 0, 0, 1], 
                          height=appdimens.stall_screen_height, markup = True)
            self.my_box_layout.add_widget(picture)
            self.my_box_layout.add_widget(label)
            self.box.add_widget(my_box_layout)

    def mk_stall_name(self, stall):
        if stall == 'japanese_stall':
            return 'Japanese'
        elif stall == 'western_stall':
            return 'Western'
        elif stall == 'indian_stall':
            return 'Indian'
        elif stall == 'chicken_rice_stall':
            return 'Chicken Rice'

    def gen_barcode_image(barcode_no):
        pass