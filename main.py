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
from kivy.properties import BooleanProperty
from kivy.core.text import LabelBase
import InputData as ID
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
import DatabaseManagement as DM
# import Excel_Mapping as EM
# IntegratedData = EM.DataMapped()
# print(IntegratedData)


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
    LabelBase.register(name='NepaliFont', fn_regular='fonts/Kalimati Regular.otf')
    LabelBase.register(name='MultiLangFont', fn_regular='fonts/NotoSansDevanagari.ttf')
    search_triggered = BooleanProperty(False)
    SearchResults = ListProperty([])
    MappedData  = ID.DataMapped()

    def build(self):
        # Set up the ScreenManager and load screens
        # sm = ScreenManager()
        # sm.add_widget(LoginScreen(name="login_screen"))
        # sm.add_widget(MainScreen(name="main_screen"))
        self.title = "Civil Multipurpose Estimation Software"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        # make sure your screens or .kv files are loaded after this
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

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
    def search_mapped_data(self, category, keyword):
        results = []
        keyword = keyword.lower()


        Titles = ["Title", "Resources", "Labour", "Materials", "Machines"]
        Titlescoded = ["title", "all", "labour", "materials", "machines"]
        category = Titlescoded[Titles.index(category)]

        # ####'labour', 'materials', 'machines' or 'all'
        results = DM.DUDBC_Extractor(category, keyword, resourcetype = "")

        resultsIndexes = results.keys()
        resultsTitles = []
        for item in resultsIndexes:
            title = results[item]["Title_Section"]["Title"][0]
            reference = results[item]["References"]["Reference"][0]
            titlePresentation = str(item) + "_" + reference + "_" + title
            resultsTitles.append(titlePresentation)

        return resultsTitles




    def show_edit_dialog(self, item_text):
        # Find which item was clicked
        item_id = None
        for id, data in self.MappedData.items():
            # Check Title_Section first
            if 'Title_Section' in data:
                for title in data['Title_Section'].get('Title', []):
                    if isinstance(title, str) and title.strip() in item_text:
                        item_id = id
                        break

            # Check First Inner table if not found yet
            if item_id is None and 'First Inner table' in data:
                for category in ['Manpower', 'Materials', 'Machines']:
                    if category in data['First Inner table']:
                        for row in data['First Inner table'][category]:
                            for value in row:
                                if isinstance(value, str) and value.strip() in item_text:
                                    item_id = id
                                    break
                            if item_id is not None:
                                break
                    if item_id is not None:
                        break

            if item_id is not None:
                break

        if item_id is None:
            toast("Could not find item to edit")
            return

            # Create and open the dialog
            self.edit_dialog = MDDialog(
                title=f"[size=20][font=MultiLangFont]Edit Item {item_id}[/font][/size]",
                type="custom",
                content_cls=EditPopupContent(self.MappedData[item_id]),
                buttons=[
                    MDFlatButton(
                        text="[font=MultiLangFont]CANCEL[/font]",
                        markup=True,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.edit_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="[font=MultiLangFont]RESET[/font]",
                        markup=True,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.reset_fields(item_id)
                    ),
                    MDRaisedButton(
                        text="[font=MultiLangFont]SAVE[/font]",
                        markup=True,
                        on_release=lambda x: self.save_edits(item_id)
                    ),
                ],
                size_hint=(None, None),
                size=(800, 600),  # Initial size
                auto_dismiss=False,
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )

            # Make dialog resizable
            if hasattr(self.edit_dialog, 'buttons_controller'):
                self.edit_dialog.buttons_controller.box.padding = "10dp"

            self.edit_dialog.open()

    def save_edits(self, item_id):
        try:
            edited_data = self.MappedData[item_id].copy()

            # Process First Inner table
            if 'First Inner table' in edited_data:
                for field_name, text_field in self.edit_dialog.content_cls.fields.items():
                    if '_' in field_name:  # Skip non-field widgets
                        parts = field_name.split('_')
                        if len(parts) == 3:  # Format: category_rowIdx_colIdx
                            category, row_idx, col_idx = parts
                            row_idx = int(row_idx)
                            col_idx = int(col_idx)

                            if (category in edited_data['First Inner table'] and
                                    row_idx < len(edited_data['First Inner table'][category])):
                                try:
                                    original_val = edited_data['First Inner table'][category][row_idx][col_idx]
                                    if isinstance(original_val, int):
                                        edited_data['First Inner table'][category][row_idx][col_idx] = int(
                                            text_field.text)
                                    elif isinstance(original_val, float):
                                        edited_data['First Inner table'][category][row_idx][col_idx] = float(
                                            text_field.text)
                                    else:
                                        edited_data['First Inner table'][category][row_idx][col_idx] = text_field.text
                                except (ValueError, IndexError):
                                    pass

            # Process other sections
            for section in edited_data:
                if section == 'First Inner table':
                    continue

                for key in edited_data[section]:
                    field_name = f"{section}_{key}"
                    if field_name in self.edit_dialog.content_cls.fields:
                        text_field = self.edit_dialog.content_cls.fields[field_name]
                        original_value = edited_data[section][key]

                        if isinstance(original_value, list):
                            edited_data[section][key] = [x.strip() for x in text_field.text.split(",")]
                        elif isinstance(original_value, int):
                            try:
                                edited_data[section][key] = int(text_field.text)
                            except ValueError:
                                pass
                        elif isinstance(original_value, float):
                            try:
                                edited_data[section][key] = float(text_field.text)
                            except ValueError:
                                pass
                        else:
                            edited_data[section][key] = text_field.text

            self.MappedData[item_id] = edited_data
            self.edit_dialog.dismiss()
            toast("[font=MultiLangFont]Changes saved successfully[/font]", markup=True)

        except Exception as e:
            toast(f"[font=MultiLangFont]Error: {str(e)}[/font]", markup=True)


class EditPopupContent(MDBoxLayout):
    def __init__(self, item_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.padding = "12dp"
        self.size_hint = (1, None)
        self.height = "550dp"  # Initial height (will be adjusted)
        self.original_data = item_data
        self.fields = {}
        self.create_fields()

    def create_fields(self):
        self.clear_widgets()

        # Main container with scroll
        main_scroll = MDScrollView(
            size_hint=(1, 1),
            bar_width=8,
            bar_color=(0.6, 0.6, 0.6, 0.8)
        )
        content_box = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            padding="10dp"
        )
        content_box.bind(minimum_height=content_box.setter('height'))

        # Create sections
        for section, content in self.original_data.items():
            if not content:  # Skip empty sections
                continue

            # Section header
            section_header = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                md_bg_color=(0.9, 0.9, 0.9, 0.3),
                padding="10dp"
            )
            section_header.add_widget(MDLabel(
                text=f"[size=18][b]{section}[/b][/size]",
                markup=True,
                halign="left",
                font_name="MultiLangFont",
                size_hint_x=1
            ))
            content_box.add_widget(section_header)

            # Section content
            if section == "First Inner table":
                self.create_first_inner_table(content, content_box)
            else:
                self.create_regular_section(section, content, content_box)

        main_scroll.add_widget(content_box)
        self.add_widget(main_scroll)

    def create_first_inner_table(self, content, parent):
        # Create a grid for the table
        table_grid = MDGridLayout(
            cols=1,
            spacing="10dp",
            size_hint_y=None,
            padding="5dp"
        )
        table_grid.bind(minimum_height=table_grid.setter('height'))

        # Add titles row (non-editable)
        if 'Title' in content and content['Title']:
            title_row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                spacing="5dp"
            )
            for title in content['Title'][0]:
                title_row.add_widget(MDLabel(
                    text=str(title),
                    size_hint_x=1 / len(content['Title'][0]),
                    halign="center",
                    font_name="MultiLangFont",
                    bold=True
                ))
            table_grid.add_widget(title_row)

        # Add editable rows for each category
        for category in ['Manpower', 'Materials', 'Machines']:
            if category in content and content[category]:
                # Category label
                cat_label = MDLabel(
                    text=category,
                    size_hint_y=None,
                    height="30dp",
                    halign="left",
                    font_name="MultiLangFont",
                    bold=True,
                    padding=("10dp", 0)
                )
                table_grid.add_widget(cat_label)

                # Data rows
                for row_idx, row in enumerate(content[category]):
                    row_box = MDBoxLayout(
                        orientation="horizontal",
                        size_hint_y=None,
                        height="40dp",
                        spacing="5dp"
                    )
                    for col_idx, value in enumerate(row):
                        field = MDTextField(
                            text=str(value),
                            size_hint_x=1 / len(row),
                            multiline=False,
                            font_name="MultiLangFont",
                            mode="rectangle",
                            padding="10dp"
                        )
                        self.fields[f"{category}_{row_idx}_{col_idx}"] = field
                        row_box.add_widget(field)
                    table_grid.add_widget(row_box)

        parent.add_widget(table_grid)

    def create_regular_section(self, section, content, parent):
        for key, value in content.items():
            if not value:  # Skip empty values
                continue

            field_box = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                spacing="10dp"
            )

            # Key label
            field_box.add_widget(MDLabel(
                text=f"{key}:",
                size_hint_x=0.3,
                halign="right",
                font_name="MultiLangFont"
            ))

            # Value field
            if isinstance(value, list):
                field_value = ", ".join(str(x) for x in value)
            else:
                field_value = str(value)

            value_field = MDTextField(
                text=field_value,
                size_hint_x=0.7,
                multiline=False,
                font_name="MultiLangFont",
                mode="rectangle"
            )
            self.fields[f"{section}_{key}"] = value_field
            field_box.add_widget(value_field)

            parent.add_widget(field_box)
if __name__ == "__main__":
    Window.minimum_width, Window.minimum_height = (800, 600)
    CivilEstimationApp().run()
