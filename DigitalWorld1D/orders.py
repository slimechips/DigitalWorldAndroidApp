from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import user
import database


class My_Orders(Screen):

    # When loading, setup the orders to be active button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"
        Clock.schedule_interval(self.retrieve_orders, 30)

    def retrieve_orders(self):
        # retrieve list from Firebase
        current_user_uid = user.current_user.uid
        database.check_my_orders(current_user_uid, got_orders)

    def got_orders(self, order_ls):
        order_ls = []
        for order in order_ls:
            order_str = ''
            food_name = order['food_name']
            spec_req = order['special_requests']
            waiting_time = order['est_waiting_time']
            orders_in_q = order['orders_in_q']
            stall = order['stall']
            order_str = """{}\nSpecial Requests: {}\n Estimated Waiting Time: 
                        {}\n Orders in Queue: {}\n Stall: {}""".format(food_name,
                        spec_req, waiting_time, orders_in_q, stall)
            order_ls.append(order_str)
        return order_ls
