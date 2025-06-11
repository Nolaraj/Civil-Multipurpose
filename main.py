# main.py
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import os
import hashlib
import json
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as hex
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import pandas as pd
import os
from kivy.factory import Factory

# ScreenManager to handle transitions between multiple screens
class LoginScreen(Screen):
    pass
class MainScreen(Screen):
    def add_estimation_part(self):
        new_section = Factory.EstimationPart()
        new_section.item_number = len(self.ids.EstimationPart_container.children) + 1
        self.ids.EstimationPart_container.add_widget(new_section)
        self.ids.scroll_view.scroll_to(new_section)

class EstimationScreen(Screen):
    pass
class DesignScreen(Screen):
    pass

class CompletionScreen(Screen):
    pass

class CivilEstimationApp(MDApp):
    def build(self):
        # Set up the ScreenManager and load screens
        # sm = ScreenManager()
        # sm.add_widget(LoginScreen(name="login_screen"))
        # sm.add_widget(MainScreen(name="main_screen"))
        self.title = "Civil Multipurpose Estimation Software"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # Load KV components and screens
        self.load_kv_files()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(EstimationScreen(name="estimation_screen"))

        return sm

    def login(self, username, password):
        # Your login logic goes here
        if username == "" and password == "":  # example check
            print("Login successful!")
            # Proceed to the main screen or navigate
            self.root.current = "main_screen"  # assuming the screen name is "main_screen"
        else:
            print("Invalid login credentials!")
            # You can show a popup dialog for error message
            self.show_error("Invalid credentials, try again.")

    def show_error(self, message):
        dialog = MDDialog(
            title="Login Error",
            text=message,
            size_hint=(0.8, None),
            height=dp(200),
            auto_dismiss=True
        )
        dialog.open()
    def load_kv_files(self):
        # Load screen KV files
        Builder.load_file("screens/login.kv")
        Builder.load_file("screens/main.kv")

        # Load component KV files
        Builder.load_file("components/rv.kv")
        Builder.load_file("components/dialogs.kv")



    def show_export_menu(self):
        print("Export menu triggered")

    def show_help(self):
        print("Help dialog triggered")
    def browse_file(self):
        content = FileChooserListView(
            path=".",
            filters=["*.xlsx"],
            size_hint=(1, 1)
        )

        popup = Popup(
            title="Select Excel File",
            content=content,
            size_hint=(0.9, 0.9)
        )

        def on_selection(instance, value):
            if value:
                selected_file = value[0]
                self.root.get_screen("main").ids.import_file_path.text = selected_file
                popup.dismiss()

        content.bind(on_selection=on_selection)
        popup.open()
    def import_excel(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        filechooser = FileChooserListView(filters=['*.xlsx'])
        content.add_widget(filechooser)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        select_btn = Button(text="Import")
        cancel_btn = Button(text="Cancel")
        btn_box.add_widget(select_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        popup = Popup(title="Import Excel File",
                      content=content,
                      size_hint=(0.9, 0.9))

        def load_file(instance):
            selected = filechooser.selection
            if selected:
                try:
                    df = pd.read_excel(selected[0])
                    print("Imported Data:\n", df)
                    # You can now use this DataFrame as needed
                    popup.dismiss()
                except Exception as e:
                    print("Error reading file:", e)

        select_btn.bind(on_release=load_file)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def export_excel(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        filechooser = FileChooserListView(path=os.getcwd())
        content.add_widget(filechooser)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_btn = Button(text="Export Here")
        cancel_btn = Button(text="Cancel")
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        popup = Popup(title="Export Excel File",
                      content=content,
                      size_hint=(0.9, 0.9))

        def save_file(instance):
            selected_path = filechooser.path
            if selected_path:
                try:
                    # Example dummy data
                    data = {
                        "Item": ["Cement", "Sand", "Aggregate"],
                        "Quantity": [50, 100, 75],
                        "Unit": ["bags", "cft", "cft"]
                    }
                    df = pd.DataFrame(data)
                    file_path = os.path.join(selected_path, "exported_data.xlsx")
                    df.to_excel(file_path, index=False)
                    print(f"Data exported to {file_path}")
                    popup.dismiss()
                except Exception as e:
                    print("Error writing file:", e)

        save_btn.bind(on_release=save_file)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        popup.open()


if __name__ == "__main__":
    Window.minimum_width, Window.minimum_height = (800, 600)
    CivilEstimationApp().run()
