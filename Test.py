# main.py
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
import pandas as pd
import os
from kivy.factory import Factory
from kivy.properties import BooleanProperty
from kivy.core.text import LabelBase
import InputData as ID
from kivymd.uix.menu import MDDropdownMenu
import DatabaseManagement as DM
from kivy.resources import resource_add_path
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from math import prod
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
import sqlite3
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty, \
    ColorProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from typing import Optional, Any, Dict
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.app import App
objects_cache = {
    "Estimation_Data": {
        "Estimation_Sections": {}  # outer list of sections
    }
}




# Global cache for all dynamically created estimation GUI objects
class LoginScreen(Screen):
    pass
class MainScreen(Screen):
    # def add_estimation_part(self):
    #     new_section = Factory.EstimationPart()
    #     new_section.item_number = len(self.ids.EstimationPart_container.children) + 1
    #     self.ids.EstimationPart_container.add_widget(new_section)
    #     self.ids.scroll_view.scroll_to(new_section)
    def add_estimation_part(self):
        container = self.ids.get('EstimationPart_container')
        scroll_view = self.ids.get('scroll_view')

        if container and scroll_view:
            new_section = Factory.EstimationPart()
            new_section.section_number = len(container.children) + 1
            container.add_widget(new_section)
            scroll_view.scroll_to(new_section)
        else:
            print("add_estimation_part: container or scroll_view not found in ids")
class EstimationScreen(Screen):
    pass
class DesignScreen(Screen):
    pass
class CompletionScreen(Screen):
    pass
class ItemQuantity_Details(BoxLayout):
    index = NumericProperty(0)
    is_expanded = BooleanProperty(True)  # Controls visibility
    base_quantity = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

    def calculate_itemcost(self):

        quantity = 0
        rate = 0
        if self.ids.quantity.text not in ["", "-"]:
            quantity = float(self.ids.quantity.text)
        if self.ids.rate.text not in ["", "-"]:
            rate = float(self.ids.rate.text)
        self.Itemcost = rate * quantity
        self.ids.Item_cost.text = f"Item cost: { self.Itemcost}".rstrip('0').rstrip(
            '.')
    def dimension_specifier(self, dimension):
        if dimension not in ["", "-"]:
            value = float (dimension)
            return value
        else:
            return False
    def calculate_quantity(self, factor = 1):
        # try:
            n= self.dimension_specifier(self.ids.numbers.text)
            l = self.dimension_specifier(self.ids.length.text)
            b = self.dimension_specifier(self.ids.breadth.text)
            h = self.dimension_specifier(self.ids.height.text)
            dimlist = [n, l, b, h]
            numbers = [x for x in dimlist if isinstance(x, (int, float)) and not isinstance(x, bool)]

            if numbers:  # means at least one number exists
                self.base_quantity = prod(numbers)
            else:
                self.base_quantity = 0




            # n = float(self.ids.numbers.text) if self.ids.numbers.text not in ["", "-"] else 1
            # l = float(self.ids.length.text) if self.ids.length.text not in ["", "-"] else 1
            # b = float(self.ids.breadth.text) if self.ids.breadth.text not in ["", "-"] else 1
            # h = float(self.ids.height.text) if self.ids.height.text not in ["", "-"] else 1
            # self.base_quantity = n * l * b * h
            self.ids.quantity.text = str(self.base_quantity) if self.base_quantity == int(
                self.base_quantity) else f"{self.base_quantity:.2f}"
            self.ids.quantity.text = f"{self.base_quantity * factor:.2f}".rstrip('0').rstrip('.')


            self.quantity = float(self.ids.quantity.text) if self.ids.quantity.text not in ["", "-"] else 0

            if float(self.ids.quantity.text) != 0:
                factor = float(self.ids.quantity.text) / self.base_quantity
                self.ids.quantity_factor.text = (
                    f"Quantity factor: {factor:.2f}"
                )
                if abs(factor-1) > 0.001:
                    self.ids.quantity_factor.theme_text_color= "Custom"
                    self.ids.quantity_factor.text_color= 1, 0.41, 0.71, 1  # Pink (RGBA for deep pink)
                else:
                    self.ids.quantity_factor.text_color = [0.7, 0.7, 0.7, 1]  # Darker gray for dark theme

            else:
                self.ids.quantity_factor.text = "[i]Base quantity is zero — cannot compute factor[/i]"
                self.ids.quantity_factor.text_color = [1, 0.0, 0.0, 1]
            self.calculate_itemcost()

        # except:
        #     self.ids.quantity.text = "-"


    def apply_factor(self, factor_text):
        try:
            factor = float(factor_text)
            self.calculate_quantity(factor=factor)
        except ValueError:
            pass
        if self.dialog:
            self.dialog.dismiss()

    def open_factor_dialog(self):
        dialog_content = Factory.FactorDialogContent()

        cancel_btn = MDButton(
            style="text",
            on_release=lambda x: self.dialog.dismiss(),
        )

        cancel_btn.add_widget(MDButtonIcon(icon="close"))  # ✅ Tick Icon
        #cancel_btn.add_widget(MDButtonText(text="CANCEL"))
        apply_btn = MDButton(
            style="text",
            on_release=lambda x: self.apply_factor(dialog_content.ids.factor_input.text),
        )

        apply_btn.add_widget(MDButtonIcon(icon="check"))  # ✅ Tick Icon
        #cancel_btn.add_widget(MDButtonText(text="CANCEL"))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Enter Multiplication Factor"),
            MDDialogContentContainer(dialog_content),
            MDDialogButtonContainer(
                cancel_btn,
                apply_btn,
            ),
        )
        self.dialog.open()
class SearchItem(BoxLayout):

    # def open_editrate_dialog(self):
    #     dialog_content = Factory.FactorDialogContent()
    #     self.dialog = MDDialog(
    #         title="Enter Multiplication Factor",
    #         type="custom",
    #         content_cls=dialog_content,
    #         auto_dismiss=False,
    #         size_hint=(0.85, None),
    #         buttons=[
    #             MDButton(
    #                 style="text",  # replaces MDFlatButton
    #                 text="CANCEL",
    #                 markup=True,
    #                 theme_text_color="Custom",
    #                 text_color=app.theme_cls.primary_color,
    #                 on_release=lambda x: self.dialog.dismiss()
    #             ),
    #             MDButton(
    #                 style="elevated",  # replaces MDRaisedButton
    #                 text="APPLY",
    #                 markup=True,
    #                 theme_text_color="Custom",
    #                 text_color=self.theme_cls.primary_color,
    #                 on_release=lambda x: self.apply_factor(dialog_content.ids.factor_input.text)
    #             ),
    #         ],
    #     )
    #     self.dialog.open()
    def toggle_highlight(self, index):

        self.is_highlighted = not self.is_highlighted
        # Change text color dynamically
        if hasattr(self.ids, "search_textOnly"):
            # self.ids.search_textOnly.color = (
            #     [0.01,0.66,0.1,0.9]
            #     if self.is_highlighted else
            #     app.get_running_app().theme_cls.primaryColor
            # )

            self.canvas.before.clear()
            with self.canvas.before:
                if self.is_highlighted:
                    # Use app theme's on_secondary color
                    Color(*get_color_from_hex("#65F0A5"))  # highlight background
                else:
                    # Transparent background when not highlighted
                    app.get_running_app().theme_cls.backgroundColor

                # Draw rectangle covering the label area
                label = self.ids.search_textOnly
                Rectangle(pos=label.pos, size=label.size)

    def ItemNo_Finder(self, search_item):
        inspector = GUIInspector(root_widget=app.root)
        dynamic_searchResults_container_Obj = inspector.find_nearestparent_with_parent_(search_item, "item_no"  )
        dynamic_searchResults_container_Obj_Props = inspector.get_widget_properties(dynamic_searchResults_container_Obj)
        item_number = dynamic_searchResults_container_Obj_Props["item_no"]
        return item_number

    def ApplyRateAnalysis(self, search_item , fromViewedandApplied = [False, {}]):
        """
        search_item: the instance of SearchItem that was clicked
        """
        # Try to find the RecycleView safely
        item_number = self.ItemNo_Finder( search_item)


        rv = None
        parent = search_item.parent
        while parent:
            if hasattr(parent, 'ids') and 'search_rv' in parent.ids:
                rv = parent.ids.search_rv
                break
            parent = getattr(parent, 'parent', None)

        if rv is None:
            print("Error: Could not find 'search_rv' in parent hierarchy.")
            return

        # Debug: print location of RV
        # print(f"Found RecycleView: {rv}, data length: {len(rv.data)}")

        # Unhighlight all items
        for item in rv.data:
            item['is_highlighted'] = False

        # Highlight the clicked item
        if len(rv.data) > search_item.index:
            rv.data[search_item.index]['is_highlighted'] = True

        # Filter to show only highlighted item if more than 1 item exists
        if len(rv.data) > 1:
            rv.data = [dict(item) for item in rv.data if item.get('is_highlighted', False)] or rv.data[:1]

        # Adjust height dynamically
        rv.height = dp(50) if len(rv.data) == 1 else min(dp(400), len(rv.data) * dp(48))
        rv.refresh_from_data()
        app.toast(f'Selected text {rv.data[0]["text"]}')

        #Call for database handling
        if fromViewedandApplied[0]:
            self.sendAppRateTo_DB(item_number, fromViewedandApplied[1])
        else:
            applied_text = search_item.text  # text from SearchItem
            appliedDataTitlePresentation = applied_text.split("_")
            NormsDBRef = int(appliedDataTitlePresentation[0])
            appliedRateData = app.MappedData[NormsDBRef]
            appliedRateData["NormsDBRef"] = NormsDBRef
            self.sendAppRateTo_DB(item_number, appliedRateData)


    def sendAppRateTo_DB(self,item_number,  appliedRateData):
        app.gui_DB.save_appliedRateAnalysis(item_number, appliedRateData)



    def viewRateItem(self, search_item):
        applied_text = search_item.text
        item_number = self.ItemNo_Finder(search_item)

        applied_text = search_item.text  # text from SearchItem
        appliedDataTitlePresentation = applied_text.split("_")
        NormsDBRef = int(appliedDataTitlePresentation[0])

        rows, appliedRateData = app.gui_DB.load_appliedRateAnalysis(item_number=item_number, norms_ref= NormsDBRef)
        original_unitRate = app.MappedData[NormsDBRef]["Second Inner table"]["Unit Rate"]
        # print(original_unitRate, "dgfsgsdgfsgs")

        if len(rows)<1:
            appliedRateData = app.MappedData[NormsDBRef]
            appliedRateData["NormsDBRef"] = NormsDBRef
            self.sendAppRateTo_DB(item_number, appliedRateData)
            rows, appliedRateData = app.gui_DB.load_appliedRateAnalysis(item_number=item_number)


        font = "MultiLangFont"


        # Keep references to editable fields
        widget_refs = {"Title_Section": {}, "References": {},
                       "First Inner table": {}, "Second Inner table": {}}

        # Popup content layout
        content_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        # Set theme default background
        with content_layout.canvas.before:
            Color(rgba=app.theme_cls.backgroundColor)  # KivyMD theme background
            rect = Rectangle(size=content_layout.size, pos=content_layout.pos)

        # Update rectangle on resize/move
        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size

        content_layout.bind(pos=update_rect, size=update_rect)

        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        def create_header_label(text, font_size=14, bold=True,size_hint_x = 1):
            return MDLabel(
                text=text,
                font_name="MultiLangFont",
                bold=bold,
                theme_text_color="Custom",
                text_color=(0.8,0.5,0.7,1),  # primary color
                size_hint_y=None,
                height=dp(30),
                size_hint_x = size_hint_x,
            )

        def create_row(key, widget):
            """
            Creates a row with label on the left (0.2 width)
            and content widget on the right (0.8 width).
            """
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30), spacing=10)
            row.add_widget(create_header_label(key, size_hint_x=0.2))  # Label left side
            widget.size_hint_x = 0.8  # Content right side
            row.add_widget(widget)
            return row

        # --- NormsDBRef (editable) ---
        norms_input = TextInput(
            text=str(appliedRateData["NormsDBRef"]),
            font_name=font,
            size_hint_y=None, height=dp(30)
        )

        # Dynamically adjust height when text changes
        grid.add_widget(create_row("NormsDBRef", norms_input))


        def adjust_height(instance, value):
            # Adjust height to fit content
            text_height = instance._lines_labels[0].texture_size[1] * len(instance._lines_labels)
            instance.height = max(dp(30), text_height + dp(10))  # +10 padding

        norms_input.bind(text=adjust_height)

        # --- Title Section ---
        if appliedRateData["Title_Section"]:
            for key, values in appliedRateData["Title_Section"].items():
                for i, v in enumerate(values):
                    ti = TextInput(
                        text=str(v),
                        font_name=font,
                        size_hint_y=None, height=dp(30)
                    )
                    grid.add_widget(create_row(key, ti))
                    widget_refs["Title_Section"].setdefault(key, []).append(ti)
                    print("")

        # --- References ---
        if appliedRateData["References"]:
            for key, values in appliedRateData["References"].items():
                for i, v in enumerate(values):
                    ti = TextInput(
                        text=str(v),
                        font_name=font,
                        size_hint_y=None, height=dp(30)
                    )
                    grid.add_widget(create_row(key, ti))
                    widget_refs["References"].setdefault(key, []).append(ti)

        # --- First Inner Table (Transposed & Editable) ---

        fit = appliedRateData["First Inner table"]
        if any([fit["Manpower"], fit["Materials"], fit["Machines"], fit["Others"]]):

            categories = ["Manpower", "Materials", "Machines", "Others"]
            titles = fit["Title"][0]
            num_titles = len(titles)

            table = GridLayout(cols=num_titles + 1, spacing=5, size_hint_y=None)
            table.bind(minimum_height=table.setter("height"))

            # Header row
            table.add_widget(Label(text="", bold=True, font_name=font,
                                   size_hint_y=None, height=dp(30)))
            for t in titles:
                table.add_widget(Label(text=t, bold=True, font_name=font,
                                       size_hint_y=None, height=dp(30),color=(0.8,0.5,0.7,1),
                                       ))

            # Rows for categories
            for category in categories:
                entries = fit[category]
                if not entries:
                    continue

                widget_refs["First Inner table"][category] = []

                for row_values in entries:  # iterate over all rows dynamically
                    table.add_widget(create_header_label(category))
                    row_widgets = []  # list for this row of widgets

                    for i in range(num_titles):
                        val = str(row_values[i]) if i < len(row_values) else ""
                        ti = TextInput(text=val, font_name=font,
                                       size_hint_y=None, height=dp(60), multiline=True)
                        table.add_widget(ti)
                        row_widgets.append(ti)

                    # Append this row's widgets as a sublist
                    widget_refs["First Inner table"][category].append(row_widgets)

            grid.add_widget(table)

        # --- Second Inner Table (Transposed & Editable) ---
        if appliedRateData["Second Inner table"]:

            sec_table = appliedRateData["Second Inner table"]
            keys = list(sec_table.keys())
            max_rows = max(len(v) for v in sec_table.values())

            table2 = GridLayout(cols=len(keys), spacing=5, size_hint_y=None)
            table2.bind(minimum_height=table2.setter("height"))

            # Headers
            for k in keys:
                table2.add_widget(create_header_label(k))

            # Values
            for r in range(max_rows):
                for k in keys:
                    values = sec_table[k]
                    val = values[r] if r < len(values) else ""
                    ti = TextInput(text=str(val), font_name=font,input_filter= "float",
                                   size_hint_y=None, height=dp(30))
                    table2.add_widget(ti)
                    widget_refs["Second Inner table"].setdefault(k, []).append(ti)

            grid.add_widget(table2)

        # Add scroll
        scroll.add_widget(grid)
        content_layout.add_widget(scroll)

        # --- Buttons ---
        print(widget_refs["Second Inner table"]["Unit Rate"][0].text, "sfsdfsf")

        tolerance = abs(original_unitRate[0] - float(widget_refs["Second Inner table"]["Unit Rate"][0].text))
        ConfirmationLabel = MDLabel(
                text=f"Original unit rate {original_unitRate[0]}",
                font_name="MultiLangFont",
                italic=True,
                bold=True,
                theme_text_color="Custom",
                text_color=(0.8,0.5,0.7,1),  # primary color
                size_hint_y=None,
                height=dp(30),
                halign= "right",
                size_hint_x = 0.7,
            )
        if tolerance>1:
            ConfirmationLabel.text_color = (1,0, 0, 1)

        content_layout.add_widget(ConfirmationLabel)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10, padding=[10, 0])

        def on_apply(instance):
            # Collect back into appliedRateData
            def to_float_safe(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return val

            new_data = {
                "NormsDBRef": norms_input.text,
                "Title_Section": {k: [ti.text for ti in v] for k, v in widget_refs["Title_Section"].items()},
                "References": {k: [ti.text for ti in v] for k, v in widget_refs["References"].items()},
                "First Inner table": {
                    "Title": [fit["Title"][0]],  # titles unchanged
                    "Manpower": [[to_float_safe(ti.text) for ti in row] for row in
                                 widget_refs["First Inner table"].get("Manpower", [])],
                    "Materials": [[to_float_safe(ti.text) for ti in row] for row in
                                  widget_refs["First Inner table"].get("Materials", [])],
                    "Machines": [[to_float_safe(ti.text) for ti in row] for row in
                                 widget_refs["First Inner table"].get("Machines", [])],
                    "Others": [[to_float_safe(ti.text) for ti in row] for row in
                               widget_refs["First Inner table"].get("Others", [])],
                },
                "Second Inner table": {
                    k: [to_float_safe(ti.text) for ti in v]
                    for k, v in widget_refs["Second Inner table"].items()
                }
            }

            # Save back to DB
            # print("Afterwareds data", new_data)
            self.ApplyRateAnalysis(search_item, fromViewedandApplied=[True, new_data])

            popup.dismiss()

        def on_cancel(instance):
            popup.dismiss()




        apply_btn = MDButton(
            style="text",
            on_release=on_apply,

        )
        apply_btn.add_widget(MDButtonIcon(icon="check"))  # ✅ Tick Icon

        cancel_btn = MDButton(
            style="text",
            on_release=on_cancel,

        )
        cancel_btn.add_widget(MDButtonIcon(icon="close"))  # ✅ Tick Icon


        btn_layout.add_widget(apply_btn)
        btn_layout.add_widget(cancel_btn)

        content_layout.add_widget(btn_layout)

        # Popup
        popup = Popup(
            title=f"Edit Rate Analysis for Item {item_number}",
            content=content_layout,
            size_hint=(0.95, 0.95),
            auto_dismiss=False
        )
        popup.open()



class ContentField(MDTextField):
    """MDTextField with Tab/Shift+Tab navigation."""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab':
            self.focus_next(forward='shift' not in modifiers)
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def focus_next(self, forward=True):
        # Only consider siblings that are MDTextFields
        siblings = [c for c in self.parent.children if isinstance(c, MDTextField)]
        siblings = list(reversed(siblings))  # Kivy children list is reversed
        idx = siblings.index(self)
        next_idx = (idx + 1) % len(siblings) if forward else (idx - 1) % len(siblings)
        siblings[next_idx].focus = True

class GUIInspector:
    """Class to inspect Kivy/KivyMD GUI tree and extract widget properties"""

    def __init__(self, root_widget: Optional[Widget] = None):
        self.root_widget = root_widget
        self.widget_cache = {}
        self.lines = self._walk_tree(self.root_widget)


    def set_root_widget(self, root_widget: Widget):
        self.root_widget = root_widget
        self.widget_cache.clear()

    def _widget_label(self, widget: Widget) -> str:
        cls_name = widget.__class__.__name__
        ids_list = []
        try:
            if hasattr(widget, "ids") and widget.ids:
                ids_list = list(widget.ids.keys())
        except Exception:
            ids_list = []
        if ids_list:
            return f"{cls_name}(ids: {', '.join(ids_list)})"
        return cls_name

    def _walk_tree(self, widget: Widget, path: Optional[list] = None) -> list:
        if path is None:
            path = [self._widget_label(widget)]
        lines = []

        lines.append(" > ".join(path))

        # Cache ids
        if hasattr(widget, "ids") and widget.ids:
            for k, v in widget.ids.items():
                self.widget_cache[k] = v

        if hasattr(widget, "children"):
            for child in reversed(widget.children):
                path.append(self._widget_label(child))
                lines.extend(self._walk_tree(child, path))
                path.pop()

        return lines

    def print_all_widgets_with_ids(self):
        if not self.root_widget:
            print("No root widget set!")
            return
        print("\nGUI Tree with ids:")
        print("=" * 60)
        for line in self.lines:
            print(line)

    def get_widget_by_id(self, widget_id: str) -> Optional[Widget]:
        return self.widget_cache.get(widget_id, None)

    def get_widget_properties(self, widget: Widget) -> Dict[str, Any]:
        """Return all properties and attributes of a widget"""
        properties = {}

        # Kivy properties
        try:
            for prop_name in widget.property_names():
                try:
                    properties[prop_name] = getattr(widget, prop_name)
                except Exception as e:
                    properties[prop_name] = f"Error reading: {e}"
        except Exception:
            pass

        # Python attributes
        for attr_name in dir(widget):
            if not attr_name.startswith("_") and not callable(getattr(widget, attr_name, None)):
                try:
                    if attr_name not in properties:
                        properties[attr_name] = getattr(widget, attr_name)
                except Exception as e:
                    properties[attr_name] = f"Error reading: {e}"

        return properties

    def print_get_widget_properties(self, widget: Widget) -> Dict[str, Any]:
        properties = self.get_widget_properties(widget)
        for k,v in properties.items():
            print(k,v)


    def print_all_texts(self, widget, property = "text"):
        """Recursively collect all widgets and print their text if available."""

        def collect_all_children(widget, include_self=True):
            widgets = []
            if include_self:
                widgets.append(widget)
            if hasattr(widget, "children") and widget.children:
                for child in reversed(widget.children):  # Kivy keeps children reversed
                    widgets.extend(collect_all_children(child, include_self=True))
            return widgets



        all_widgets = collect_all_children(widget)
        print(f"Total collected: {len(all_widgets)} widgets")
        for w in all_widgets:
            txt = getattr(w, property, None)
            if txt not in (None, ""):  # only print if text exists and not empty
                print(f"{w.__class__.__name__} (id={getattr(w, 'id', None)}): {txt}")

    def print_all_texts_with_ids(self, widget, parent_ids=None):
        """Recursively collect all widgets and print id (from parent.ids) and text if available."""

        # Create mapping of widget instance -> KV id
        widget_to_id = {}
        if parent_ids:
            for k, v in parent_ids.items():
                widget_to_id[id(v)] = k  # use Python id() to map

        def collect_all_children(widget, include_self=True):
            widgets = []
            if include_self:
                widgets.append(widget)
            if hasattr(widget, "children") and widget.children:
                for child in reversed(widget.children):
                    widgets.extend(collect_all_children(child, include_self=True))
            return widgets

        all_widgets = collect_all_children(widget)
        print(f"Total collected: {len(all_widgets)} widgets\n")

        for w in all_widgets:
            kv_id = widget_to_id.get(id(w), None)
            txt = getattr(w, "text", None)
            if txt not in (None, ""):
                print(f"Widget KV ID: {kv_id} | Class: {w.__class__.__name__} | Text: {txt}")

    def print_widget_properties_recursive(self, widget, level: int = 0):
        """Print all properties of a widget and its children recursively"""
        # widget = self.get_widget_by_id(widget_id) #widget_id can be set to widget in function definition if id is to be used
        # if not widget:
        #     print(f"Widget with id '{widget_id}' not found!")
        #     return

        indent = "    " * level  # Indentation for child widgets


        def print_props(w, lvl):
            indent = "    " * lvl
            print(f"\n{indent}Properties of {w.__class__.__name__} (id: {getattr(w, 'id', None)}):")
            print(f"{indent}" + "=" * 50)
            props = self.get_widget_properties(w)
            for k, v in props.items():
                if isinstance(v, (list, tuple)) and len(v) > 5:
                    v_str = f"{type(v).__name__} with {len(v)} items"
                elif isinstance(v, dict) and len(v) > 3:
                    v_str = f"dict with {len(v)} items"
                else:
                    v_str = str(v)
                print(f"{indent}{k:.<30} {v_str}")

            # Recursively print children
            if hasattr(w, "children") and w.children:
                for child in reversed(w.children):  # maintain Kivy child order
                    print_props(child, lvl + 1)

        print_props(widget, level)
    def change_object_property(self, widget_object: Widget, property_name: str, new_value: str):
        import re
        from kivy.clock import Clock

        if not widget_object:
            print("Invalid widget object provided!")
            return False

        if not hasattr(widget_object, property_name):
            print(f"Property '{property_name}' does not exist on {widget_object.__class__.__name__}")
            return False

        try:
            current_value = getattr(widget_object, property_name)

            # Type conversion
            if isinstance(current_value, bool):
                converted_value = new_value.lower() in ("true", "1", "yes", "on")
            elif isinstance(current_value, int):
                converted_value = int(new_value)
            elif isinstance(current_value, float):
                converted_value = float(new_value)
            elif isinstance(current_value, list):
                converted_value = [x.strip() for x in new_value.split(",")]
            elif isinstance(current_value, tuple):
                converted_value = tuple(x.strip() for x in new_value.split(","))
            elif current_value is None:
                if new_value.lower() in ("true", "false"):
                    converted_value = new_value.lower() == "true"
                elif re.match(r"^-?\d+\.\d+$", new_value):
                    converted_value = float(new_value)
                elif new_value.isdigit() or (new_value.startswith("-") and new_value[1:].isdigit()):
                    converted_value = int(new_value)
                else:
                    converted_value = new_value
            else:
                converted_value = new_value

            # Set the property
            setattr(widget_object, property_name, converted_value)

            # Force GUI refresh if canvas exists
            def update(dt):
                if hasattr(widget_object, 'canvas'):
                    widget_object.canvas.ask_update()

            Clock.schedule_once(update, 0)
            widget_object.canvas.ask_update()

            print(f"Successfully set {widget_object.__class__.__name__}.{property_name} to {converted_value}")
            return True

        except Exception as e:
            print(f"Error changing property: {e}")
            return False

    def find_nearestparent_with_parent_(self, child, target_attribute, target_value = ""):
        """
        Flows Down the levels
        """
        # Check if child itself has the attribute and value
        if hasattr(child, target_attribute) and target_value =="":
            return child

        if hasattr(child, target_attribute):
            if getattr(child, target_attribute) == target_value:
                return child

        # If child has parent, recursively search them
        if hasattr(child, "parent"):
            parent = child.parent
            result = self.find_nearestparent_with_parent_(parent, target_attribute, target_value)
            if result is not None:
                return result
        return None

    def find_parent_with_child_(self, parent, target_attribute, target_value):
        """
        Flows Down the levels
        """
        # Check if parent itself has the attribute and value
        if hasattr(parent, target_attribute):
            if getattr(parent, target_attribute) == target_value:
                return parent

        # If parent has children, recursively search them
        if hasattr(parent, "children"):
            for child in parent.children:
                result = self.find_parent_with_child_(child, target_attribute, target_value)
                if result is not None:
                    return result
        return None

    # def find_object_with_attribute_(self, parent, target_attribute, target_value):
    #     """
    #     Flows Down the levels
    #     """
    #     # Check if parent itself has the attribute and value
    #     if hasattr(parent, target_attribute):
    #         if getattr(parent, target_attribute) == target_value:
    #             return parent
    #
    #     # If parent has children, recursively search them
    #     if hasattr(parent, "children"):
    #         for child in parent.children:
    #             result = self.find_parent_with_child_(child, target_attribute, target_value)
    #             if result is not None:
    #                 return result
    #     return None


################################Calcualtions for Quantity Estimation
################################-------------------------------------------------------------------------------
class MenuHeader(MDBoxLayout):
    '''Header for the dropdown menu.'''
class CivilEstimationApp(MDApp):

    search_triggered = BooleanProperty(False)
    SearchResults = ListProperty([])
    MappedData  = ID.DataMapped()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.load_kv_files()

        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main_screen"))
        self.sm.add_widget(EstimationScreen(name="estimation_screen"))



        # main_screen = self.sm.get_screen("main_screen")
        # est_screen = self.sm.get_screen("estimation_screen")
        # container = main_screen.ids.get('dynamic_sections_container')
        # scroll_view = main_screen.ids.get('scroll_view')





    def build(self):
        self.theme_cls.theme_style = "Light"  # Force light theme
        self.theme_cls.primary_palette = "Blue"  # Optional
        # self.theme_cls.primary_palette = "Orange"
        # self.theme_cls.theme_style = "Light"
        # dropdown items
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        resource_add_path(font_dir)
        LabelBase.register(name='NepaliFont', fn_regular='fonts/Kalimati Regular.otf')
        LabelBase.register(name='MultiLangFont', fn_regular='fonts/NotoSansDevanagari.ttf')
        LabelBase.register(name='Preeti', fn_regular='fonts/Preeti Normal.otf')
        LabelBase.register(name='Mangal', fn_regular='fonts/Mangal Regular.otf')
        LabelBase.register(            name="MultiLangFont",                   fn_regular=os.path.join(font_dir, "NotoSansDevanagari.ttf"),        )
        LabelBase.register(name='NotoSansDevanagari_ExtraCondensed-SemiBold', fn_regular='fonts/NotoSansDevanagari_ExtraCondensed-SemiBold.ttf')
        LabelBase.register(name='NotoSansDevanagari-Medium', fn_regular='fonts/NotoSansDevanagari-Medium.ttf')



        menu_items = [
            {"text": "Title", "viewclass": "MDMenuItem", "on_release": lambda x="Title": self.set_item(x)},
            {"text": "Resources", "viewclass": "MDMenuItem", "on_release": lambda x="Resources": self.set_item(x)},
            {"text": "Labour", "viewclass": "MDMenuItem", "on_release": lambda x="Labour": self.set_item(x)},
            {"text": "Materials", "viewclass": "MDMenuItem", "on_release": lambda x="Materials": self.set_item(x)},
            {"text": "Machines", "viewclass": "MDMenuItem", "on_release": lambda x="Machines": self.set_item(x)},
        ]


        # 🔹 Create one database handler for the app
        self.gui_DB = DM.GUIDatabase()
        return self.sm

    def on_start(self):
        Clock.schedule_once(self._post_start, 0)
    def on_stop(self):
        """Close DB when app exits"""
        self.gui_DB.conn.close()
    def _post_start(self, *args):
        inspector = GUIInspector(root_widget=app.root)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewSectionButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'NewSectionButton' not found!")

        inspector = GUIInspector(root_widget=app.root)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewItemButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'ITem' not found!")

    #____________________________________________________Themes

    def initialize_theme(self):
        """Load saved theme or use defaults"""
        try:
            saved = self.theme_store.get('theme')
            self.theme_cls.primary_palette = saved['palette']
            self.theme_cls.theme_style = saved['style']
            self.theme_cls.accent_palette = saved.get('accent', 'Amber')
        except:
            # Default theme
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.theme_style = "Light"
            self.theme_cls.accent_palette = "Amber"
            self.save_theme_settings()
    def save_theme_settings(self):
        """Save current theme to storage"""
        self.theme_store.put('theme',
                             palette=self.theme_cls.primary_palette,
                             style=self.theme_cls.theme_style,
                             accent=self.theme_cls.accent_palette
                             )
    def setup_theme_menu(self):
        """Create the theme selection dropdown menu"""
        theme_items = [
            {"text": "Light Theme", "viewclass": "OneLineListItem",
             "on_release": lambda x="Light": self.change_theme(style=x)},
            {"text": "Dark Theme", "viewclass": "OneLineListItem",
             "on_release": lambda x="Dark": self.change_theme(style=x)},
            {"text": "Palettes", "viewclass": "OneLineListItem", "divider": None},
            *[{"text": palette, "viewclass": "OneLineListItem",
               "on_release": lambda x=palette: self.change_theme(palette=x)}
              for palette in ["Green", "Blue", "Teal", "Red", "Purple", "Orange"]],
            {"text": "Accent Colors", "viewclass": "OneLineListItem", "divider": None},
            *[{"text": f"Accent: {accent}", "viewclass": "OneLineListItem",
               "on_release": lambda x=accent: self.change_theme(accent=x)}
              for accent in ["Amber", "Pink", "LightBlue", "Lime"]]
        ]

        self.theme_menu = MDDropdownMenu(
            items=theme_items,
            width_mult=4,
            max_height=dp(300)
        )
    def change_theme(self, palette=None, style=None, accent=None):
        """Change theme settings"""
        if palette:
            self.theme_cls.primary_palette = palette
        if style:
            self.theme_cls.theme_style = style
        if accent:
            self.theme_cls.accent_palette = accent

        self.save_theme_settings()
        if self.theme_menu:
            self.theme_menu.dismiss()
    def open_theme_menu(self, caller):
        """Open theme selection menu"""
        if not self.theme_menu:
            self.setup_theme_menu()
        self.theme_menu.caller = caller
        self.theme_menu.open()
    # ################################Themes

    def inspect_gui(self):
        """Method to call from your app to inspect the GUI with proper ID detection"""
        inspector = GUIInspector()

        # Use the screen manager or current screen as root
        root_widget = self.sm  # or self.sm.current_screen

        print("🧭 Starting comprehensive GUI inspection...")
        print("🆔 = Real ID from widget properties")
        print("🔹 = Generated ID for inspection")
        print()

        # Print complete tree structure
        widgets_info = inspector.print_all_widgets_tree(root_widget)

        # Search for common widget patterns
        print("\n🔎 COMMON WIDGET SEARCH:")
        common_patterns = ['button', 'input', 'text', 'field', 'label', 'dropdown', 'search']
        for pattern in common_patterns:
            inspector.find_widgets_by_pattern(root_widget, pattern)

        return inspector, widgets_info


    def restart_estimation(self):
        # # ==========================================================DEBUG and Inspector====================================================
        # inspector = GUIInspector(root_widget=app.root)
        # #Initialize it before searching for any widgets below
        # inspector.print_all_widgets_with_ids()
        #
        # widget_id = "ItemQuantity_Details_"
        # inspector.print_widget_properties_recursive(widget_id)
        #
        # # ##########Change a property example
        # widget = inspector.get_widget_by_id(widget_id)
        # inspector.change_object_property(widget, "text", "Enter keyword...")
        # inspector.change_object_property(widget, "font_size", "40")
        # # print("ALL widgets with ids")
        # # inspector.print_all_widgets_with_ids()
        #
        # ##########Penetrate to the object that the properties children holds(can also be done to other properties objects) and modify their specific property
        # children_widgets = widget.children  #widget.theme_cls, widget.proxy_ref or sth else
        #
        # ######Change the value of widget children (focus is used to update the values in some cases)
        # # inspector.change_object_property(children_widgets[0], "text", "Enter keyword...")
        # # inspector.change_object_property(widget, "focus", "True")
        # # inspector.change_object_property(widget, "focus", "False")





        # ----------------------------------------------------------------------------  #----------------------------------------------------------------------------
        # Usage example in your restart_estimation function or anywhere you have est_screen:
        # sm = self.sm
        main_screen = self.sm.get_screen("main_screen")
        est_screen = self.sm.get_screen("estimation_screen")
        container = main_screen.ids.get('dynamic_sections_container')
        scroll_view = main_screen.ids.get('scroll_view')

        if container:
            container.clear_widgets()
            new_section = Factory.EstimationPart()
            new_section.section_number = 1
            container.add_widget(new_section)
        else:
            print("dynamic_sections_container not found!")

        if scroll_view:
            scroll_view.scroll_y = 1
        else:
            print("scroll_view not found!")
        # ----------------------------------------------------------------------------  #----------------------------------------------------------------------------



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
        Builder.load_file("screens/Test.kv")

        # Load component KV files
        Builder.load_file("components/rv.kv")
        Builder.load_file("components/dialogs.kv")
        print("Current background color:", self.theme_cls.backgroundColor)

        # inspector = GUIInspector(root_widget=app.root)
        # on_kv_post:
        #    self.dispatch("on_release")

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
        if (category=="Select item" or category == None):
            category = "Title"
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
            # print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", titlePresentation)
        return resultsTitles
    def create_dropdown(self):
        screen = self.sm.get_screen("main_screen")
        try:
            palette_btn = screen.ids.palette_button
        except KeyError:
            print("Error: palette_button not found in ids!")
            return

        menu_items = [
            {"text": f"Color {i}", "on_release": lambda x=f"Color {i}": self.menu_callback(x)}
            for i in range(1, 9)
        ]

        self.menu = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=palette_btn,
            items=menu_items,
            width_mult=4
        )
        # OPEN THE DROPDOWN
        self.menu.open()
    def menu_callback(self, text_item):
        print(f"Selected: {text_item}")
        self.menu.dismiss()

    def open_menu(self, item, values):
        menu_items = [
            {
                "text": values[i],
                "on_release": lambda x=values[i]: self.menu_callback(x)
            } for i in range(len(values))
        ]
        self.menu = MDDropdownMenu(
            caller=item,
            items=menu_items,
            width_mult=4
        )
        self.menu.open()

    def menu_callback(self, text_item):
        self.root.ids.drop_text.text = text_item
        self.menu.dismiss()

    def unhighlight_all_items(self):
        if hasattr(self, 'SearchResults') and self.SearchResults:
            rv = self.root.ids.dynamic_searchResults_container.children[0].ids.search_rv
            for item in rv.data:
                item['is_highlighted'] = False
            rv.refresh_from_data()

    def toast(self, text):
        # temp label to measure text width
        measure_label = Label(
            text=text,
            font_name="NotoSansDevanagari-Medium",
            font_size="11sp"
        )
        measure_label.texture_update()
        text_width = measure_label.texture_size[0]

        snackbar_width = min(text_width + dp(50), Window.width - dp(20))

        snackbar = MDSnackbar(
            size_hint_x=None,
            width=snackbar_width,
            y=dp(24),
        )

        # 🎨 Modern background + border
        with snackbar.canvas.before:
            Color(0.15, 0.15, 0.2, 0.95)
            snackbar.bg = RoundedRectangle(
                radius=[dp(12), dp(12), dp(12), dp(12)],
                pos=snackbar.pos,
                size=snackbar.size,
            )
            Color(0.2, 0.6, 1, 1)
            snackbar.border = RoundedRectangle(
                radius=[dp(12), dp(12), dp(12), dp(12)],
                pos=(snackbar.x - dp(1), snackbar.y - dp(1)),
                size=(snackbar.width + dp(2), snackbar.height + dp(2)),
            )

        def update_canvas(*_):
            snackbar.bg.pos = snackbar.pos
            snackbar.bg.size = snackbar.size
            snackbar.border.pos = (snackbar.x - dp(1), snackbar.y - dp(1))
            snackbar.border.size = (snackbar.width + dp(2), snackbar.height + dp(2))

        snackbar.bind(pos=update_canvas, size=update_canvas)

        # 📝 Label (unchanged)
        label = Label(
            text=text,
            font_name="NotoSansDevanagari-Medium",
            halign="center",
            valign="middle",
            font_size="11sp",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(32),
        )
        label.text_size = (snackbar_width, None)
        label.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))

        # 🔑 Make snackbar height follow label height (+padding)
        def adjust_height(instance, value):
            snackbar.height = instance.texture_size[1] + dp(16)  # padding top+bottom

        label.bind(texture_size=adjust_height)

        snackbar.add_widget(label)

        snackbar.anchor_x = "center"
        snackbar.open()

    #_______________________________________________________________________________Database Works
    ItemsIDs = ["EstimationPartSection_root", "estimation_Section_title",
                "items_section_Title",
        "dropdown",
        "search_keyword_input",
        "search_button",
        "dynamic_saerchResults_container",
        "item_number",
        "item_description",
        "unit",
        "rate",
        "numbers",
        "length",
        "breadth",
        "height",
        "quantity",
        "remarks",
        "calc_info",
        "quantity_factor",
        "Item_cost"
    ]






    def print_all_items(self):
        inspector = GUIInspector(root_widget=app.root)
        # inspector.print_all_widgets_with_ids()
        parent = inspector.get_widget_by_id("dynamic_item_container")
        # children_widgets = parent.children
        # inspector.print_widget_properties_recursive("dynamic_item_container")
        parent = inspector.get_widget_by_id("dynamic_item_container")
        widget = inspector.get_widget_by_id("quantity")
        proerties = inspector.get_widget_properties(widget)
        for k, v in proerties.items():
            print(k, v)

        objects_cache = {
            "Estimation_Data": {
                "Estimation_Sections": []  # outer list of sections
            }
        }


    def cache_forNewSection(self):
        pass
        # objects_cache["Estimation_Data"]["Estimation_Sections"].append([])  #Innermost list is the estsec1, est sec2...
    def cache_forNewItem(self):

        # objects_cache["Estimation_Data"]["Estimation_Sections"][-1].append([]) #Innermost list is the item1, item2...
        # listofInterest =  objects_cache["Estimation_Data"]["Estimation_Sections"][-1][-1]


        inspector = GUIInspector(root_widget=app.root)

        #Itew Number is set as key for all
        ItemNoObj = inspector.get_widget_by_id("item_number")
        ItemNo = inspector.get_widget_by_id("item_number").text


        itemsObjects = {}
        EstimationPartSection_root = inspector.find_nearestparent_with_parent_(ItemNoObj, "name", "EstimationPartSection_root")
        root_childrens =  inspector.get_widget_properties(EstimationPartSection_root)["children"]
        # print(EstimationPartSection_root, "name", root_childrens)

        for items in self.ItemsIDs:
            if items == "dynamic_saerchResults_container":
                for children in root_childrens:
                    dynamicSearch_Parent = inspector.find_parent_with_child_(children, "text", "Dynamic Search")
                    if dynamicSearch_Parent:
                        itemsObjects[items] = dynamicSearch_Parent
                        break

            elif items == "EstimationPartSection_root":
                itemsObjects[items] = EstimationPartSection_root

            elif items == "items_section_Title":
                for children in root_childrens:
                    dynamicSearch_Parent = inspector.find_parent_with_child_(children, "name", "item_number_label")
                    if dynamicSearch_Parent:
                        itemsObjects[items] = dynamicSearch_Parent
                        break

            elif items == "estimation_Section_title":
                for children in root_childrens:
                    dynamicSearch_Parent = inspector.find_parent_with_child_(children, "name", "estimation_Section_title")
                    if dynamicSearch_Parent:
                        itemsObjects[items] = dynamicSearch_Parent
                        break

            else:
                itemsObjects[items] = inspector.get_widget_by_id(items)

        objects_cache["Estimation_Data"]["Estimation_Sections"][ItemNo] = itemsObjects


        print(objects_cache)








    # ======================= CACHE HANDLING =======================


    def add_items_to_section_cache(self, section_dict, section_widget):
        """
        section_widget: The BoxLayout/container holding the items
        """
        items_list = []

        # Assuming section_widget.ids.dynamic_item_container exists
        for item_widget in section_widget.ids.dynamic_item_container.children:
            item_dict = {"Item_Subsection": []}

            # Cache each child/subsection of the item
            for sub_widget in item_widget.children:
                item_dict["Item_Subsection"].append(sub_widget)

            items_list.append(item_dict)

        section_dict["ItemsSection"].append(items_list)


    def add_section_to_cache(self, section_widget):
        """
        Add a dynamically created section into objects_cache
        """
        section_dict = {"ItemsSection": []}  # items inside this section
        objects_cache["Estimation_Data"]["Estimation_Sections"].append(section_dict)

        # Add items inside this section
        self.add_items_to_section_cache(section_dict, section_widget)

    def clear_objects_cache(self):
        """Reset the cache"""
        objects_cache["Estimation_Data"]["Estimation_Sections"] = []

    # Optional: Debug print
    def print_objects_cache(self):
        import pprint
        pprint.pprint(objects_cache)
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

estcalass = EstimationScreen
if __name__ == "__main__":
    Window.minimum_width, Window.minimum_height = (800, 600)
    app = CivilEstimationApp()

    # inject app into another class
    # helper = SomeOtherClass(app)
    # helper.do_something()  # works before app.run()

    app.run()