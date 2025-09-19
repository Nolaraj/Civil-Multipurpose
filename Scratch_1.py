import os
import hashlib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle

# Set window size and styling
Window.size = (1280, 720)
Window.minimum_width, Window.minimum_height = (1024, 600)
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background

# Security Configuration
USER_CREDENTIALS_FILE = 'user_credentials.dat'
SALT = b'fixed_salt_for_hashing'

Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
#:import Factory kivy.factory.Factory

<CustomButton@Button>:
    background_normal: ''
    background_color: (0, 0, 0, 0)
    size_hint: None, None
    height: dp(45)
    width: dp(120) if not self.text.endswith('Item') else dp(150)
    canvas.before:
        Color:
            rgba: hex('#3498db') if not self.disabled else hex('#bdc3c7')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]
    font_size: '14sp'
    bold: True
    color: hex('#ffffff')

<CustomTextInput@TextInput>:
    size_hint_y: None
    height: dp(40)
    padding: [10, (self.height - self.line_height)/2, 10, (self.height - self.line_height)/2]
    background_normal: ''
    background_active: ''
    background_color: hex('#ffffff')
    canvas.before:
        Color:
            rgba: hex('#bdc3c7')
        Line:
            width: 1
            rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

<CustomLabel@Label>:
    font_size: '14sp'
    color: hex('#2c3e50')
    size_hint_y: None
    height: dp(30)

<SelectableLabel>:
    canvas.before:
        Color:
            rgba: hex('#3498db') if self.selected else hex('#ecf0f1')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5]
    color: hex('#2c3e50') if not self.selected else hex('#ffffff')
    bold: True if self.selected else False
    halign: 'left'
    valign: 'middle'
    padding: (15, 0)
    font_size: '14sp'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(50)
        spacing: dp(30)
        canvas.before:
            Color:
                rgba: hex('#ffffff')
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(100)
            spacing: dp(10)

            Label:
                text: 'CIVIL ESTIMATION SOFTWARE'
                font_size: '24sp'
                bold: True
                color: hex('#3498db')
                size_hint_y: None
                height: dp(40)

            Label:
                text: 'Secure Login'
                font_size: '16sp'
                color: hex('#7f8c8d')
                size_hint_y: None
                height: dp(30)

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(15)
            size_hint_y: None
            height: dp(180)
            padding: [dp(50), 0]

            CustomLabel:
                text: 'Username:'

            CustomTextInput:
                id: username
                hint_text: 'Enter your username'

            CustomLabel:
                text: 'Password:'

            CustomTextInput:
                id: password
                password: True
                hint_text: 'Enter your password'

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: [dp(100), 0]

            CustomButton:
                text: 'LOGIN'
                on_press: root.login()
                background_color: hex('#3498db')

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)

        # Header Panel
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)

            CustomTextInput:
                id: search_input
                hint_text: 'Search items...'
                size_hint_x: 0.7
                on_text: root.search_items(self.text)
                icon_right: 'magnify'

            CustomButton:
                text: 'Clear Search'
                size_hint_x: 0.3
                on_press: root.search_items('')
                background_color: hex('#e74c3c')

        # Toolbar Panel
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            CustomButton:
                text: 'Add Item'
                on_press: root.add_item()
                background_color: hex('#2ecc71')

            CustomButton:
                text: 'Update Item'
                on_press: root.update_item()
                background_color: hex('#3498db')

            CustomButton:
                text: 'Delete Item'
                on_press: root.delete_item()
                background_color: hex('#e74c3c')

            CustomButton:
                text: 'Clear Fields'
                on_press: root.clear_fields()
                background_color: hex('#f39c12')

        # Main Content Area
        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)

            # Items List
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.6
                spacing: dp(10)

                Label:
                    text: 'ITEMS LIST'
                    font_size: '16sp'
                    bold: True
                    color: hex('#2c3e50')
                    size_hint_y: None
                    height: dp(30)

                RV:
                    id: rv
                    bar_width: dp(10)
                    bar_color: hex('#3498db')
                    bar_inactive_color: hex('#bdc3c7')

            # Item Details Panel
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.4
                spacing: dp(10)

                Label:
                    text: 'ITEM DETAILS'
                    font_size: '16sp'
                    bold: True
                    color: hex('#2c3e50')
                    size_hint_y: None
                    height: dp(30)

                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: max(self.minimum_height, root.height * 0.5)
                        spacing: dp(10)
                        padding: dp(10)

                        GridLayout:
                            cols: 2
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(300)

                            CustomLabel:
                                text: 'Item Code:'
                            CustomTextInput:
                                id: item_code
                                hint_text: 'Item code'

                            CustomLabel:
                                text: 'Description:'
                            CustomTextInput:
                                id: description
                                hint_text: 'Item description'

                            CustomLabel:
                                text: 'Unit:'
                            CustomTextInput:
                                id: unit
                                hint_text: 'Measurement unit'

                            CustomLabel:
                                text: 'Rate:'
                            CustomTextInput:
                                id: rate
                                input_filter: 'float'
                                hint_text: 'Rate per unit'

                            CustomLabel:
                                text: 'Quantity:'
                            CustomTextInput:
                                id: quantity
                                input_filter: 'float'
                                hint_text: 'Quantity'
                                on_text: root.calculate_amount()

                            CustomLabel:
                                text: 'Amount:'
                            Label:
                                id: amount
                                text: '0.00'
                                font_size: '14sp'
                                color: hex('#e74c3c')
                                bold: True
                                size_hint_y: None
                                height: dp(40)

                # Report Buttons
                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(10)

                    CustomButton:
                        text: 'Abstract'
                        on_press: root.generate_abstract()
                        background_color: hex('#9b59b6')
                        width: dp(150)

                    CustomButton:
                        text: 'Summary'
                        on_press: root.generate_summary()
                        background_color: hex('#1abc9c')
                        width: dp(150)
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = False
    selectable = True

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.selected_item = rv.data[index]


class RV(RecycleView):
    selected_item = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.viewclass = 'SelectableLabel'
        self.layout_manager = SelectableRecycleBoxLayout()
        self.layout_manager.default_size = (None, dp(45))
        self.layout_manager.default_size_hint = (1, None)
        self.layout_manager.orientation = 'vertical'
        self.layout_manager.spacing = dp(5)
        self.add_widget(self.layout_manager)


class LoginScreen(Screen):
    def verify_credentials(self, username, password):
        if not os.path.exists(USER_CREDENTIALS_FILE):
            return False

        with open(USER_CREDENTIALS_FILE, 'r') as f:
            stored_username, stored_hash = f.read().split(':')

        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            SALT,
            100000
        ).hex()

        return username == stored_username and hashed_password == stored_hash

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.verify_credentials(username, password):
            self.manager.current = 'main'
        else:
            popup = Popup(title='Login Failed',
                          content=Label(text='Invalid username or password'),
                          size_hint=(0.6, 0.3),
                          separator_color=[0.8, 0, 0, 1])
            popup.open()


class MainScreen(Screen):
    excel_data = ListProperty([])
    selected_item = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Initialize with sample data
        self.excel_data = [
            {'item_code': 'C001', 'description': 'Concrete (Grade M20)', 'unit': 'm³', 'rate': 6500, 'quantity': 15,
             'amount': 97500},
            {'item_code': 'S002', 'description': 'Steel (Fe500)', 'unit': 'kg', 'rate': 85, 'quantity': 750,
             'amount': 63750},
            {'item_code': 'B003', 'description': 'Bricks (Clay)', 'unit': '1000 nos', 'rate': 5500, 'quantity': 8,
             'amount': 44000},
            {'item_code': 'F004', 'description': 'Formwork (Plywood)', 'unit': 'm²', 'rate': 350, 'quantity': 120,
             'amount': 42000},
            {'item_code': 'A005', 'description': 'Aggregate (20mm)', 'unit': 'm³', 'rate': 1200, 'quantity': 25,
             'amount': 30000}
        ]

    def on_enter(self, *args):
        """Called when the screen is displayed"""
        self.update_rv_data()

    def update_rv_data(self):
        if hasattr(self, 'ids') and 'rv' in self.ids:
            self.ids.rv.data = [
                {'text': f"{item['item_code']} - {item['description']}", 'item_data': item}
                for item in self.excel_data
            ]

    def search_items(self, query):
        if not query:
            self.update_rv_data()
            return

        filtered_data = [
            item for item in self.excel_data
            if query.lower() in str(item['item_code']).lower() or
               query.lower() in str(item['description']).lower()
        ]

        if hasattr(self, 'ids') and 'rv' in self.ids:
            self.ids.rv.data = [
                {'text': f"{item['item_code']} - {item['description']}", 'item_data': item}
                for item in filtered_data
            ]

    def on_selected_item(self, instance, value):
        if value:
            self.ids.item_code.text = str(value['item_data']['item_code'])
            self.ids.description.text = str(value['item_data']['description'])
            self.ids.unit.text = str(value['item_data']['unit'])
            self.ids.rate.text = str(value['item_data']['rate'])
            self.ids.quantity.text = str(value['item_data']['quantity'])
            self.ids.amount.text = f"{value['item_data']['amount']:.2f}"

    def calculate_amount(self):
        try:
            rate = float(self.ids.rate.text) if self.ids.rate.text else 0
            quantity = float(self.ids.quantity.text) if self.ids.quantity.text else 0
            amount = rate * quantity
            self.ids.amount.text = f"{amount:.2f}"
        except ValueError:
            self.ids.amount.text = "0.00"

    def add_item(self):
        try:
            new_item = {
                'item_code': self.ids.item_code.text,
                'description': self.ids.description.text,
                'unit': self.ids.unit.text,
                'rate': float(self.ids.rate.text) if self.ids.rate.text else 0,
                'quantity': float(self.ids.quantity.text) if self.ids.quantity.text else 0,
                'amount': float(self.ids.rate.text) * float(
                    self.ids.quantity.text) if self.ids.rate.text and self.ids.quantity.text else 0
            }

            if not new_item['item_code']:
                raise ValueError("Item code is required")

            self.excel_data.append(new_item)
            self.update_rv_data()
            self.clear_fields()

            popup = Popup(title='Success',
                          content=Label(text='Item added successfully'),
                          size_hint=(0.5, 0.2))
            popup.open()
        except ValueError as e:
            popup = Popup(title='Error',
                          content=Label(text=str(e)),
                          size_hint=(0.6, 0.3))
            popup.open()

    def update_item(self):
        if not self.selected_item:
            popup = Popup(title='Error',
                          content=Label(text='Please select an item first'),
                          size_hint=(0.6, 0.3))
            popup.open()
            return

        try:
            updated_item = {
                'item_code': self.ids.item_code.text,
                'description': self.ids.description.text,
                'unit': self.ids.unit.text,
                'rate': float(self.ids.rate.text) if self.ids.rate.text else 0,
                'quantity': float(self.ids.quantity.text) if self.ids.quantity.text else 0,
                'amount': float(self.ids.rate.text) * float(
                    self.ids.quantity.text) if self.ids.rate.text and self.ids.quantity.text else 0
            }

            for idx, item in enumerate(self.excel_data):
                if item['item_code'] == self.selected_item['item_data']['item_code']:
                    self.excel_data[idx] = updated_item
                    break

            self.update_rv_data()
            self.clear_fields()

            popup = Popup(title='Success',
                          content=Label(text='Item updated successfully'),
                          size_hint=(0.5, 0.2))
            popup.open()
        except ValueError as e:
            popup = Popup(title='Error',
                          content=Label(text=str(e)),
                          size_hint=(0.6, 0.3))
            popup.open()

    def delete_item(self):
        if not self.selected_item:
            popup = Popup(title='Error',
                          content=Label(text='Please select an item first'),
                          size_hint=(0.6, 0.3))
            popup.open()
            return

        self.excel_data = [
            item for item in self.excel_data
            if item['item_code'] != self.selected_item['item_data']['item_code']
        ]

        self.update_rv_data()
        self.clear_fields()

        popup = Popup(title='Success',
                      content=Label(text='Item deleted successfully'),
                      size_hint=(0.5, 0.2))
        popup.open()

    def clear_fields(self):
        self.ids.item_code.text = ""
        self.ids.description.text = ""
        self.ids.unit.text = ""
        self.ids.rate.text = ""
        self.ids.quantity.text = ""
        self.ids.amount.text = "0.00"
        self.selected_item = None

    def generate_abstract(self):
        total = sum(item.get('amount', 0) for item in self.excel_data)

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text='ABSTRACT OF COST', font_size='18sp', bold=True, color=(0.2, 0.4, 0.6, 1)))
        content.add_widget(Label(text=f"Total Items: {len(self.excel_data)}", font_size='14sp'))
        content.add_widget(
            Label(text=f"Total Cost: ₹{total:,.2f}", font_size='20sp', bold=True, color=(0.8, 0.2, 0.2, 1)))

        popup = Popup(title='Abstract of Cost',
                      content=content,
                      size_hint=(0.7, 0.5),
                      separator_color=[0.2, 0.6, 0.8, 1])
        popup.open()

    def generate_summary(self):
        content = ScrollView()
        grid = GridLayout(cols=6, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Header row
        headers = ['Code', 'Description', 'Unit', 'Rate (₹)', 'Qty', 'Amount (₹)']
        for header in headers:
            lbl = Label(text=header, size_hint_y=None, height=dp(40), bold=True, color=(0.2, 0.4, 0.6, 1))
            grid.add_widget(lbl)

        # Data rows
        for item in self.excel_data:
            grid.add_widget(Label(text=str(item['item_code']), size_hint_y=None, height=dp(35)))
            grid.add_widget(Label(text=str(item['description']), size_hint_y=None, height=dp(35)))
            grid.add_widget(Label(text=str(item['unit']), size_hint_y=None, height=dp(35)))
            grid.add_widget(Label(text=f"{item['rate']:,.2f}", size_hint_y=None, height=dp(35)))
            grid.add_widget(Label(text=f"{item['quantity']:,.2f}", size_hint_y=None, height=dp(35)))
            grid.add_widget(Label(text=f"{item.get('amount', 0):,.2f}", size_hint_y=None, height=dp(35)))

        # Total row
        total = sum(item.get('amount', 0) for item in self.excel_data)
        grid.add_widget(Label(text='TOTAL', size_hint_y=None, height=dp(40), bold=True, color=(0.8, 0.2, 0.2, 1)))
        grid.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
        grid.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
        grid.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
        grid.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
        grid.add_widget(
            Label(text=f"₹{total:,.2f}", size_hint_y=None, height=dp(40), bold=True, color=(0.8, 0.2, 0.2, 1)))

        content.add_widget(grid)

        popup = Popup(title='Summary Report',
                      content=content,
                      size_hint=(0.9, 0.8),
                      separator_color=[0.2, 0.6, 0.8, 1])
        popup.open()


class EstimationApp(App):
    def build(self):
        if not os.path.exists(USER_CREDENTIALS_FILE):
            self.create_default_user()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

    def create_default_user(self):
        username = "admin"
        password = "admin123"

        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            SALT,
            100000
        ).hex()

        with open(USER_CREDENTIALS_FILE, 'w') as f:
            f.write(f"{username}:{hashed_password}")


if __name__ == '__main__':
    EstimationApp().run()