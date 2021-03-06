from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.logger import Logger

from functools import partial

import user
import database
import appdimens
from importbarcode import gen_barcode_img
# from importbarcode import gen_barcode_image

class My_Orders(Screen):
    def __init__(self, *args, **kwargs):
        # When loading, setup the orders to be active button in nav bar
        super().__init__(*args, **kwargs)
        self.picture = []
        self.order_ls = []
        self.current_bars = []
        self.row_widgets = []
        self.bar_widgets = []
        self.space_widgets = []

    def on_pre_enter(self, *args):
        # Start to update the page with orders info of current user
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["stalls_btn"].state = "normal"
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"
        self.ids["btm_bar"].ids["logout_btn"].state = "normal"
        self.grd = self.ids["orders_grd"]
        self.retrieve_orders(None)
        update_interval = 15 # 15 second update interval for UI
        self.order_updater = Clock.schedule_interval(self.retrieve_orders,
                                                     update_interval)

    def on_leave(self, *args):
        super().on_leave(*args)
        try:
            # Stop order updater when leaving screen
            self.order_updater.cancel()
        except:
            # Order updater has not been scheduled
            pass

    def retrieve_orders(self, dt):
        self.picture = []
        # retrieve list from Firebase
        current_user_uid = user.current_user.uid
        database.check_my_orders(current_user_uid, self.got_orders)

    def got_orders(self, order_ls):
        # Database function returned us info of user's orders
        self.orders_ls = order_ls
        for order in self.orders_ls:
            self.picture.append('')
        for idx, order in enumerate(self.orders_ls):
            self.retrieve_url(order.food_item, order.current_stall, idx)

    def retrieve_url(self, food_name, stall, idx):
        # Call database function to give us picture url of an order
        database.query_picture_url(stall, food_name, idx, self.got_url)

    def got_url(self, pictureURL, idx):
        # Database function returned url of order's picture
        self.picture[idx] = pictureURL
        self.got_datas()
    
    def got_datas(self):
        # Check if all required data for loading page has been received
        if '' not in self.picture:
            self.update_UI()

    def update_UI(self):
        # Update the page UI based on data received
        current_order_ids = []
        Logger.info("Current barcodes: " + str(self.current_bars))
        for idx, order in enumerate(self.orders_ls):
            # Extract the order ids from database data in a list
            current_order_ids.append(order.order_id)
            Logger.info("Order id: " + str(order.order_id))
            if order.order_id in self.current_bars:
                Logger.info("Current order: already loaded")
                # Order was already previously loaded, just update text
                idx = self.current_bars.index(order.order_id)
                label_text = self.get_label_text(order)
                Logger.info("label_txt: " + str(self.row_widgets[idx].children[1]))
                self.row_widgets[idx].children[0].text = label_text
                continue

            # First we create the image of the order
            picture = FoodPicture(source=self.picture[idx], 
                                  size_hint = (0.5, None))
            label_text = self.get_label_text(order)
            label = OrderLabel(text=label_text)

            # Then we generate the barcode of the order
            barcodePath = gen_barcode_img(order.order_id)
            barcode = BarcodeImage(source=barcodePath,
                                   order_id=order.order_id)

            # Add some space below the barcode to seperate the orders
            space = Widget(height=150, size_hint_y=None)
            my_box_layout = OrderRow()
            my_box_layout.add_widget(picture)
            my_box_layout.add_widget(label)
            self.grd.add_widget(my_box_layout)
            self.grd.add_widget(barcode)
            self.grd.add_widget(space)
            self.current_bars.append(order.order_id)
            self.row_widgets.append(my_box_layout)
            self.bar_widgets.append(barcode)
            self.space_widgets.append(space)

        # The below checks if an active order has been removed from the db
        for idx, bar_widget in enumerate(self.bar_widgets):
            print(bar_widget.order_id, current_order_ids)
            if bar_widget.order_id not in current_order_ids:
                # If so, remove the widget from the page
                self.grd.remove_widget(bar_widget)
                self.grd.remove_widget(self.row_widgets[idx])
                self.grd.remove_widget(self.space_widgets[idx])

    def get_label_text(self, order):
        # Gets the formatted label text given an order
        food_name = order.food_item
        waiting_time = order.est_wait
        orders_in_q = order.num_in_q
        stall = order.current_stall
        status = order.status
        stall_name = self.mk_stall_name(stall)

        # Then we create the label of order
        label_text = ("[b][u]{}[/u][/b]\n"
                        "[b]Status: [/b]{}\n"
                        "[b]Arriving: [/b]{} mins\n"
                        "[b]Orders in Queue: [/b]{}\n"
                        "[b]Stall: [/b]{}".format(food_name,
                        status, waiting_time, orders_in_q, stall_name))
        return label_text


    def mk_stall_name(self, stall):
        if stall == 'japanese_stall':
            return 'Japanese'
        elif stall == 'western_stall':
            return 'Western'
        elif stall == 'indian_stall':
            return 'Indian'
        elif stall == 'chicken_rice_stall':
            return 'Chicken Rice'

class FoodPicture(AsyncImage):
    pass

class OrderLabel(Label):
    pass

class OrderRow(BoxLayout):
    pass

class BarcodeImage(Image):
    order_id = NumericProperty()