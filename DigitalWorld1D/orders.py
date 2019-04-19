from kivy.uix.screenmanager import Screen

class My_Orders(Screen):

    # When loading, setup the orders to be active button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"