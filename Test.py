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
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
import json
import json
from datetime import datetime
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivy.uix.boxlayout import BoxLayout

objects_cache = {
    "Estimation_Data": {
        "Estimation_Sections": {}  # outer list of sections
    }
}
# Global cache for all dynamically created estimation GUI objects
def safe_float(value):
    try:
        return float(value)
    except:
        return value
class ProgressManager:
    """Global progress bar manager for long operations"""

    def __init__(self, app):
        self.app = app
        self.dialog = None
        self.progress_widget = None
        self.label = None

    def show(self, message="Processing..."):
        """Show progress dialog"""
        if self.dialog:
            self.dismiss()

        content = BoxLayout(orientation="vertical", spacing=20, padding=20)
        content.size_hint_y = None
        content.height = 150

        self.progress_widget = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=(48, 48),
            pos_hint={"center_x": 0.5}
        )

        from kivymd.uix.label import MDLabel
        self.label = MDLabel(
            text=message,
            halign="center",
            theme_text_color="Primary"
        )

        content.add_widget(self.progress_widget)
        content.add_widget(self.label)

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Please Wait"),
            MDDialogContentContainer(content),
            auto_dismiss=False
        )
        self.dialog.open()

    def update(self, message):
        """Update progress message"""
        if self.label:
            self.label.text = message

    def dismiss(self):
        """Dismiss progress dialog"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

class GUI_DB_Handle():
    def sendGenInfoQEst_toDB(self):
        app.gui_DB.save_GenInfo_QEstimation(ObjectsCache=objects_cache)
    def sendAppRateTo_DB(self,item_number,  appliedRateData):
        app.gui_DB.save_appliedRateAnalysis(item_number, appliedRateData)
def find_values_by_key(data, target_key):
    """
    Recursively find all values for a given key in a nested dict/list structure.

    Parameters:
        data (dict or list): The nested data.
        target_key (str): The key to search for.

    Returns:
        list: All values corresponding to the target key.
    """
    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            else:
                results.extend(find_values_by_key(value, target_key))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_values_by_key(item, target_key))

    return results
def ItemNo_Finder(insiderObjectAny):
    inspector = GUIInspector(root_widget=app.root)
    ItemQuantity_Details = inspector.find_nearestparent_with_parent_(insiderObjectAny, "item_no"  )
    ItemQuantity_Details_Props = inspector.get_widget_properties(ItemQuantity_Details)
    item_number = ItemQuantity_Details_Props["item_no"]
    return item_number
def subItemsFinder(ItemNo):
    subItemsAll = list(objects_cache["Estimation_Data"]["Estimation_Sections"].keys())
    matched_keys = [k for k in subItemsAll if k.startswith(f"{ItemNo}.")]
    return matched_keys
def DimObjsList_for_Specific_Item(inside_Object, reqDimAttribute = "rate"):
    ItemNo = str(ItemNo_Finder(inside_Object))
    AvailKeys = objects_cache['Estimation_Data']['Estimation_Sections'].keys()
    ReqKeys = []
    ReqObjs = []
    for key in AvailKeys:
        key = str(key)
        key_itemNo = ".".join(key.split(".")[0:2])
        if ItemNo == key_itemNo:
            ReqKeys.append(key)
    for key in ReqKeys:
        # print(objects_cache['Estimation_Data']['Estimation_Sections'][key], "DEBIG")
        obj = objects_cache['Estimation_Data']['Estimation_Sections'][key][reqDimAttribute]
        ReqObjs.append((obj))
    return ReqObjs
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

    def open_export_dialog(self):
        # Popup content layout
        content_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        with content_layout.canvas.before:
            Color(rgba=app.theme_cls.backgroundColor)  # KivyMD theme background
            rect = Rectangle(size=content_layout.size, pos=content_layout.pos)

        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size

        content_layout.bind(pos=update_rect, size=update_rect)

        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(
            cols=1,
            spacing=dp(10),  # vertical spacing between rows
            padding=[0, 5, 0, 5],  # top/bottom padding
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter("height"))

        def create_header_label(text, font_size=14, bold=True, size_hint_x=1):
            return MDLabel(
                text=text,
                font_name="MultiLangFont",
                bold=bold,
                theme_text_color="Custom",
                text_color=(0.8, 0.5, 0.7, 1),
                size_hint_y=None,
                height=dp(30),
                size_hint_x=size_hint_x,
            )

        def create_row(key, widget):
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=10)
            row.add_widget(create_header_label(key, size_hint_x=0.5))
            widget.size_hint_x = 0.5
            row.add_widget(widget)
            return row

        # Input fields
        contingency_input = MDTextField(hint_text="Enter contingency value", mode="outlined",     size_hint_y= None, height = dp(35), text="4")
        vat_input = MDTextField(hint_text="Enter VAT percentage", mode="outlined",     size_hint_y= None, height = dp(35), text="13")
        physical_input = MDTextField(hint_text="Enter Physical Contingency %", mode="outlined",     size_hint_y= None, height = dp(35), text="10")
        price_adj_input = MDTextField(hint_text="Enter Price Adjustment Contingency %", mode="outlined",     size_hint_y= None, height = dp(35), text="10")

        # Checkboxes
        pdf_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=10)
        pdf_checkbox = MDCheckbox(size_hint=(None, None), size=(dp(30), dp(30)), pos_hint={"center_y": 0.5})
        pdf_box.add_widget(pdf_checkbox)
        pdf_box.add_widget(MDLabel(text="Dispatch PDF", valign="center"))

        # Print row
        print_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=10)
        print_checkbox = MDCheckbox(size_hint=(None, None), size=(dp(30), dp(30)), pos_hint={"center_y": 0.5})
        print_box.add_widget(print_checkbox)
        print_box.add_widget(MDLabel(text="Print", valign="center"))

        # --- Enforce auto-check rule ---
        def on_print_active(instance, value):
            if value:  # Print checked
                pdf_checkbox.active = True
                pdf_checkbox.disabled = True  # lock PDF
            else:  # Print unchecked
                pdf_checkbox.disabled = False  # unlock PDF

        print_checkbox.bind(active=on_print_active)

        # Add rows
        grid.add_widget(create_row("Contingency (on %):", contingency_input))
        grid.add_widget(create_row("VAT (on %):", vat_input))
        grid.add_widget(create_row("Physical Contingency (on %):", physical_input))
        grid.add_widget(create_row("Price Adjustment (on %):", price_adj_input))
        grid.add_widget(pdf_box)
        grid.add_widget(print_box)

        scroll.add_widget(grid)
        content_layout.add_widget(scroll)

        # Footer buttons
        footer = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50), spacing=10)
        cancel_btn = MDButton(            on_release=lambda x: popup.dismiss(),        )
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        accept_btn = MDButton(            on_release=lambda x: on_apply(),        )
        accept_btn.add_widget(MDButtonText(text="Accept"))
        footer.add_widget(Widget())

        footer.add_widget(cancel_btn)
        footer.add_widget(accept_btn)
        content_layout.add_widget(footer)

        # Create popup
        popup = Popup(            title="Export Options",            content=content_layout,            size_hint=(0.8, 0.8),            auto_dismiss=False,        )

        def on_apply():
            valuesDict = {
                "contingency": contingency_input.text,
                "vat": vat_input.text,
                "physical_contingency": physical_input.text,
                "price_adjustment": price_adj_input.text,
                "pdf": pdf_checkbox.active,
                "print": print_checkbox.active,
            }



            try:
                app.gui_DB.save_PrimaryKeys(valuesDict)
                app.GUIHandle.sendGenInfoQEst_toDB()

                db_out = DM.DB_Output()

                db_out.SheetsTitle_Writing()
                db_out.QuantityEstSheet_Writing()
                db_out.AOC_writing()
                db_out.SummaryWriting()
                db_out.BOQ_Writing()
                db_out.RateAnalysisDataWriting()

                if valuesDict["pdf"]:
                    db_out.excel_to_pdf_merge()
                if valuesDict["print"]:
                    db_out.PrintPDF()



                popup.dismiss()
            except Exception as e:
                app.toast(f'"Error:", {e}')
                print("Error:", e)
                popup.dismiss()


        popup.open()

        def on_cancel(instance):
            popup.dismiss()


class EstimationScreen(Screen):
    pass
class DesignScreen(Screen):
    pass
class CompletionScreen(Screen):
    pass
class ItemQuantity_Details(BoxLayout):
    index = NumericProperty(0)
    is_expanded = BooleanProperty(True)  # Controls visibility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))


    def apply_factor(self, factor_text):
        try:
            factor = float(factor_text)
            self.calculate_quantity(factor=factor)
        except ValueError:
            pass
        if self.dialog:
            self.dialog.dismiss()
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
    def setAppliedrateTonewSubitem(self, new_subitem):
        itemNo = ItemNo_Finder(new_subitem)
        rows,  appliedRateData = app.gui_DB.load_appliedRateAnalysis(itemNo)
        if rows:
            Unitrate  = appliedRateData["Second Inner table"]["Unit Rate"][0]
            """
            Apply rate analysis or cached rate to the new SubItemRow
            """

            itemNosKeys = objects_cache["Estimation_Data"]["Estimation_Sections"].keys()
            keys_list = list(itemNosKeys)
            matched_keys = [k for k in keys_list if k.startswith(f"{itemNo}.")]

            for key in matched_keys:
                rateObj = objects_cache["Estimation_Data"]["Estimation_Sections"][f"{key}"]["rate"]
                rateObj.text = Unitrate

        # print(inspector.get_widget_properties(new_subitem))

        def delay_and_apply():
            try:
                # Get the rate widget inside the new SubItemRow
                rate_widget = new_subitem.ids.get("rate", None)

                if rate_widget:
                    rate_widget.text = Unitrate
                else:
                    print("⚠️ Could not find 'rate' field in SubItemRow")


            except Exception as e:
                print(f"Error in setAppliedrateTonewSubitem: {e}")

        # delay_and_apply()
        # Clock.schedule_once(delay_and_apply, 0.2)
    def delete_self(self):
        """Remove this SubItemRow from its parent container"""
        ItemNo = self.item_no
        itemNosKeys = objects_cache["Estimation_Data"]["Estimation_Sections"].keys()
        keys_list = list(itemNosKeys)
        matched_keys = [k for k in keys_list if k.startswith(f"{ItemNo}.")]

        if len(matched_keys)<= 1:
            return
        latest = max(matched_keys, key=lambda k: list(map(int, k.split('.'))))

        SubItemRow_base = objects_cache["Estimation_Data"]["Estimation_Sections"][f"{latest}"]["SubItemRow_baseObj"]

        if SubItemRow_base:
            dimensions_container = SubItemRow_base.parent
            SubItemRow_base.clear_widgets()

            if SubItemRow_base and SubItemRow_base.parent:
                SubItemRow_base.parent.remove_widget(SubItemRow_base)
            for idx, widget in enumerate(dimensions_container.children[::-1], 1):  # reverse order
                widget.subitem_number = idx
                # Update the UI label/text if you have one
                if hasattr(widget, "MDButtonText"):
                    widget.MDButtonText.text = f"Subitem {idx}"

            #Deletion of the data from the database
            objects_cache["Estimation_Data"]["Estimation_Sections"].pop(latest, None)
            app.gui_DB.delete_SubItemData_(latest)

class EstimationPart(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
    def delete_self(self):
        """Remove this ItemRow from its parent container"""
        sectionNo = self.section_no
        itemNosKeys = objects_cache["Estimation_Data"]["Estimation_Sections"].keys()
        subItemskeys_list = list(itemNosKeys)
        ItemKeysList = [k.rsplit('.', 1)[0] for k in subItemskeys_list]
        unique_ItemKeysList = list(dict.fromkeys(ItemKeysList))
        matched_keys_ItemNo = [k for k in unique_ItemKeysList if k.startswith(f"{sectionNo}.")]
        if len(matched_keys_ItemNo)<= 1:
            return
        latestItem = max(matched_keys_ItemNo, key=lambda k: list(map(int, k.split('.'))))
        matched_keys_SubItemNo = [k for k in subItemskeys_list if k.startswith(f"{latestItem}.")]


        latestdim_ItemnoObj = objects_cache["Estimation_Data"]["Estimation_Sections"][f"{matched_keys_SubItemNo[0]}"]["item_number"]
        inspector = GUIInspector(root_widget=app.root)
        ItemRow_base = inspector.find_nearestparent_with_parent_(latestdim_ItemnoObj, "name", "ItemRow_base")

        if ItemRow_base:
            ItemRow_base.clear_widgets()
            for item in matched_keys_SubItemNo:
                objects_cache["Estimation_Data"]["Estimation_Sections"].pop(item, None)


            # 2️⃣ Remove the widget from container
            dimensions_container = ItemRow_base.parent
            if ItemRow_base and ItemRow_base.parent:
                ItemRow_base.parent.remove_widget(ItemRow_base)
            for idx, widget in enumerate(dimensions_container.children[::-1], 1):  # reverse order
                widget.item_number = idx
                # Update the UI label/text if you have one
                if hasattr(widget, "MDButtonText"):
                    widget.MDButtonText.text = f"Subitem {idx}"

            # Deletion of the data from the database
            for value in matched_keys_SubItemNo:
                #Deletion ofthe data in the dimensionbox
                app.gui_DB.delete_SubItemData_(value)
            #For the deletion of the data from the rate ana
            # print(objects_cache["Estimation_Data"]["Estimation_Sections"].keys())

    def click_subitem(self):
        inspector = GUIInspector(root_widget=self)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewSubItemButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'ITem' not found!")
    # Clock.schedule_once(click_subitem, 0.3)  # delay in seconds
class SubItemRow(BoxLayout):   # or MDBoxLayout, depending on your base
    base_quantity = NumericProperty(0.0)

    def dimension_specifier(self, dimension):
        if dimension not in ["", "-"]:
            value = float(dimension)
            return value
        else:
            return False

    def calculate_quantity(self, factor=1):
        # try:
        n = self.dimension_specifier(self.ids.numbers.text)
        l = self.dimension_specifier(self.ids.length.text)
        b = self.dimension_specifier(self.ids.breadth.text)
        h = self.dimension_specifier(self.ids.height.text)
        dimlist = [n, l, b, h]
        numbers = [x for x in dimlist if isinstance(x, (int, float)) and not isinstance(x, bool)]

        if numbers:  # means at least one number exists
            self.base_quantity = prod(numbers)
        else:
            self.base_quantity = 0


        self.ids.quantity.text = str(self.base_quantity) if self.base_quantity == int(
            self.base_quantity) else f"{self.base_quantity:.2f}"
        self.ids.quantity.text = f"{self.base_quantity * factor:.2f}".rstrip('0').rstrip('.')

        self.quantity = float(self.ids.quantity.text) if self.ids.quantity.text not in ["", "-"] else 0

        def quantityfactorcomp():
            ItemNo = ItemNo_Finder(self.ids.numbers)
            snNo = str(
                ItemNo) + ".1"  # Could be taken any as all the dimensions box SN key contains same object of calc, quantity and cost objects
            quantity_factor = objects_cache["Estimation_Data"]["Estimation_Sections"][snNo]["quantity_factor"]
            if float(self.ids.quantity.text) != 0:
                factor = float(self.ids.quantity.text) / self.base_quantity
                quantity_factor.text = (
                    f"Item Quantity: {factor:.2f}"
                )
                if abs(factor - 1) > 0.001:
                    quantity_factor.theme_text_color = "Custom"
                    quantity_factor.text_color = 1, 0.41, 0.71, 1  # Pink (RGBA for deep pink)
                else:
                    quantity_factor.text_color = [0.7, 0.7, 0.7, 1]  # Darker gray for dark theme

            else:
                quantity_factor.text = "[i]Base quantity is zero — cannot compute factor[/i]"
                quantity_factor.text_color = [1, 0.0, 0.0, 1]

        quantityfactorcomp()
        self.calculate_itemcost()

    def calculate_itemcost(self):
        ItemNo  = ItemNo_Finder(self.ids.numbers)
        snNo = str(ItemNo) + ".1"   #Could be taken any as all the dimensions box SN key contains same object of calc, quantity and cost objects
        quantity_factor = objects_cache["Estimation_Data"]["Estimation_Sections"][snNo]["quantity_factor"]
        Item_cost = objects_cache["Estimation_Data"]["Estimation_Sections"][snNo]["Item_cost"]


        #Total item quantity computations
        qntyObjsList = DimObjsList_for_Specific_Item(self.ids.numbers, reqDimAttribute="quantity")
        qntyValueList = [x.text for x in qntyObjsList]
        def safe_float(x):
            try:
                return float(x)
            except (ValueError, TypeError):
                return 0.0
        totalQntyValue = sum(safe_float(v) for v in qntyValueList)
        if totalQntyValue<0:
            quantity_factor.text_color = [1, 0.0, 0.0, 1]
            quantity_factor.text = (f"Item Quantity: {totalQntyValue:.2f}"        )
        else:
            quantity_factor.text_color = app.theme_cls.disabledTextColor
            quantity_factor.text = (f"Item Quantity: {totalQntyValue:.2f}"        )

        #Computations of the Item costs
        quantity = 0
        rate = 0
        if self.ids.quantity.text not in ["", "-"]:
            quantity = float(self.ids.quantity.text)
        if self.ids.rate.text not in ["", "-"]:
            rate = float(self.ids.rate.text)
        self.Itemcost = rate * totalQntyValue
        Item_cost.text = f"Item cost: {self.Itemcost:.2f}".rstrip('0').rstrip('.')

class SearchItem(BoxLayout):

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

    def search_textOnlyFinder(self, search_item):
        inspector = GUIInspector(root_widget=app.root)
        dynamic_searchResults_container_Obj = inspector.find_nearestparent_with_parent_(search_item, "item_no")
        search_textOnlyObj = inspector.find_parent_with_child_(dynamic_searchResults_container_Obj, "name", "search_textOnly")
        return search_textOnlyObj



    def ApplyRateAnalysis(self, search_item , fromViewedandApplied = [False, {}]):
        """
        search_item: the instance of SearchItem that was clicked
        """
        # Try to find the RecycleView safely
        item_number = ItemNo_Finder( search_item)

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
        applied_text = search_item.text  # text from SearchItem
        appliedDataTitlePresentation = applied_text.split("_")
        NormsDBRef = int(appliedDataTitlePresentation[0])
        original_unitRate = app.MappedData[NormsDBRef]["Second Inner table"]["Unit Rate"]
        search_textOnlyObj = self.search_textOnlyFinder(search_item)

        if fromViewedandApplied[0]:
            app.GUIHandle.sendAppRateTo_DB(item_number, fromViewedandApplied[1])
            # self.sendAppRateTo_DB(item_number, fromViewedandApplied[1])

            # Apply the rate to the quantity estimation database rate section
            rate_Objs = DimObjsList_for_Specific_Item(search_item)
            for rate_Obj in rate_Objs:
                rateValue =  "{:.2f}".format(  find_values_by_key(fromViewedandApplied[1], "Unit Rate")[0][0])
                rate_Obj.text =rateValue

            rateDeviation = abs(original_unitRate[0] - float(fromViewedandApplied[1]["Second Inner table"]["Unit Rate"][0]))
            if rateDeviation > 1:
                search_textOnlyObj.color = "#FF69B4" #(225, 22, 122, 1)
            else:
                search_textOnlyObj.color = app.theme_cls.primaryColor

        else:
            appliedRateData = app.MappedData[NormsDBRef]
            appliedRateData["NormsDBRef"] = NormsDBRef
            app.GUIHandle.sendAppRateTo_DB(item_number, appliedRateData)
            # self.sendAppRateTo_DB(item_number, appliedRateData)

            # Apply the rate to the quantity estimation database rate section
            rate_Objs = DimObjsList_for_Specific_Item(search_item)
            # rate_Obj.text = "{:.2f}".format(find_values_by_key(appliedRateData, "Unit Rate")[0][0])
            for rate_Obj in rate_Objs:
                rateValue =  "{:.2f}".format(find_values_by_key(appliedRateData, "Unit Rate")[0][0])
                rate_Obj.text =rateValue
            search_textOnlyObj.color = app.theme_cls.primaryColor
        app.GUIHandle.sendGenInfoQEst_toDB()
        # self.sendGenInfoQEst_toDB(objects_cache)
    def viewRateItem(self, search_item):
        item_number = ItemNo_Finder(search_item)
        applied_text = search_item.text  # text from SearchItem

        appliedDataTitlePresentation = applied_text.split("_")
        NormsDBRef = int(appliedDataTitlePresentation[0])

        rows, appliedRateData = app.gui_DB.load_appliedRateAnalysis(item_number=item_number, norms_ref= NormsDBRef)
        original_unitRate = app.MappedData[NormsDBRef]["Second Inner table"]["Unit Rate"]
        # print(original_unitRate, "dgfsgsdgfsgs")

        if len(rows)<1:
            appliedRateData = app.MappedData[NormsDBRef]
            appliedRateData["NormsDBRef"] = NormsDBRef
            app.GUIHandle.sendAppRateTo_DB(item_number,appliedRateData)
            # self.sendAppRateTo_DB(item_number, appliedRateData)
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
        rateDeviation = abs(original_unitRate[0] - float(widget_refs["Second Inner table"]["Unit Rate"][0].text))

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
        if rateDeviation>1:
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

class ExportDialogContent(MDBoxLayout):
    pass


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

    def find_parent_with_child_(self, parent, target_attribute, target_value= ""):
        """
        Flows Down the levels
        """
        # Check if parent itself has the attribute and value
        if hasattr(parent, target_attribute) and target_value =="":
            return parent

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
        self.searchCOntainterChildrens = {}




        # main_screen = self.sm.get_screen("main_screen")
        # est_screen = self.sm.get_screen("estimation_screen")
        # container = main_screen.ids.get('dynamic_sections_container')
        # scroll_view = main_screen.ids.get('scroll_view')

        self.progress = ProgressManager(self)





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
        self.GUIHandle = GUI_DB_Handle()
        return self.sm

    def on_start(self):
        Clock.schedule_once(self._post_start, 0)
    def on_stop(self):
        """Close DB when app exits"""
        self.gui_DB.conn.close()
    def _post_start(self, *args):
        self.clickNewSection()
        self.clickNewItem()
        # self.clickNewSubItem()

    def clickNewSection(self):
        inspector = GUIInspector(root_widget=app.root)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewSectionButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'NewSectionButton' not found!")

    def clickNewItem(self):
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

    def restart_estimation(self):
        main_screen = self.sm.get_screen("main_screen")
        est_screen = self.sm.get_screen("estimation_screen")
        container = main_screen.ids.get('dynamic_sections_container')
        scroll_view = main_screen.ids.get('scroll_view')

        if container:
            container.clear_widgets()
            new_section = Factory.EstimationPart()
            new_section.section_number = 1
            container.add_widget(new_section)

            #Clear database, Object cache dictionary (Only for the quantity estimation and Rate analysis table
            objects_cache["Estimation_Data"]["Estimation_Sections"] = {            }
            self.gui_DB.ResetRate_QunatityEstimation()





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
    GenInfo_IDs = ["office", "projectname", "budgetsubheadingno", "fiscalyear", "projectcompletiontime", "projectlocation", "officeCode"]
    def cache_forNewSection(self):
        inspector = GUIInspector(root_widget=app.root)
        # estimation_screen = inspector.get_widget_by_id("estimation_screen")
        itemsObjects = {}

        for items in self.GenInfo_IDs:
            itemsObjects[items] = inspector.get_widget_by_id(items)

        objects_cache["Estimation_Data"]["General_Information"] = itemsObjects


        # objects_cache["Estimation_Data"]["Estimation_Sections"].append([])  #Innermost list is the estsec1, est sec2...
    def cache_forNewItem(self, ItemRowBase):
        try:
            #Rule never go up for the widget object collection except for the estimation section data
            inspector = GUIInspector(root_widget=app.root)
            itemsObjects = {}

            #Level 1 of the estimation gui data
            estimationSectionBase = inspector.find_nearestparent_with_parent_(ItemRowBase, "name", "EstimationPartSection_root")
            estChildrens = inspector.get_widget_properties(estimationSectionBase)["children"]

            #Level 2 of the estimation gui data
            itemSectionBase = ItemRowBase
            itemChildrens = inspector.get_widget_properties(itemSectionBase)["children"]

            #Level 3 of the estimation gui data
            SubItemSectionBase = inspector.find_parent_with_child_( ItemRowBase, "name", "SubItemRow_base")
            subItemChildrens = inspector.get_widget_properties(SubItemSectionBase)["children"]
            item_numberField  =inspector.find_parent_with_child_(ItemRowBase, "name", "item_number")
            item_numberFieldValue = inspector.get_widget_properties(item_numberField)["text"]





            def CachebasedOnParentChild():
                for items in self.ItemsIDs:
                    if items == "dynamic_saerchResults_container":
                        itemsObjects[items] = inspector.find_parent_with_child_(itemSectionBase, "text", "Dynamic Search")
                    elif items == "EstimationPartSection_root":
                        itemsObjects[items] = estimationSectionBase
                    elif items == "items_section_Title":
                        itemsObjects[items] = inspector.find_parent_with_child_(itemSectionBase, "name", "item_number_label")
                    elif items == "estimation_Section_title":
                        itemsObjects[items] = inspector.find_parent_with_child_(estimationSectionBase, "name", "estimation_Section_title")
                    # elif items in ["unit",        "rate",        "numbers",        "length",        "breadth",        "height",        "quantity",        "remarks"]:
                    #
                    #     query = "item_" + items
                    #     obj = inspector.find_parent_with_child_(SubItemSectionBase, "name", query)
                    #     itemsObjects[items] = obj
                    else:
                        try:
                            IDs =       SubItemSectionBase.ids
                            obj = IDs[items]
                            itemsObjects[items] = obj
                        except:
                            itemsObjects[items] = inspector.get_widget_by_id(items)
                if SubItemSectionBase:
                    itemsObjects["SubItemRow_baseObj"] = SubItemSectionBase

                objects_cache["Estimation_Data"]["Estimation_Sections"][item_numberFieldValue] = itemsObjects

            CachebasedOnParentChild()

        except Exception as e:
            print(f"Error in cache_forNewItem: {e}")
            import traceback
            traceback.print_exc()




























    #_______________________________________________________________________________File saving and retrieving, _# ENHANCED SAVE/LOAD FUNCTIONS



    def save_gui_state(self, filename=None):
        """Save complete GUI state including database references"""
        if not filename:
            filename = f"gui_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        self.progress.show("Saving state...")

        def do_save(dt):
            try:
                state = self._collect_gui_state()

                self.progress.update("Writing to file...")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)

                self.progress.dismiss()
                self.toast(f"Saved to {filename}")
                return filename
            except Exception as e:
                self.progress.dismiss()
                print(f"Save error: {e}")
                import traceback
                traceback.print_exc()
                self.toast(f"Error saving: {e}")
                return None

        Clock.schedule_once(do_save, 0.1)

    def load_gui_state(self, filename):
        """Load complete GUI state"""
        if not filename:
            return False

        self.progress.show("Loading state...")

        def do_load(dt):
            try:
                self.progress.update("Reading file...")
                with open(filename, "r", encoding="utf-8") as f:
                    state = json.load(f)

                self.progress.update("Clearing current state...")
                self.restart_estimation()

                # Wait for clear to complete
                Clock.schedule_once(lambda dt: self._restore_gui_state(state), 0.2)

            except Exception as e:
                self.progress.dismiss()
                print(f"Load error: {e}")
                import traceback
                traceback.print_exc()
                self.toast(f"Error loading: {e}")
                return False

        Clock.schedule_once(do_load, 0.1)
        return True

    # ENHANCED DATA COLLECTION

    def _collect_gui_state(self):
        """Collect complete logical data from GUI including database state"""
        main_screen = self.sm.get_screen("main_screen")

        # Collect general information
        gen_info = {}
        for field_id in self.GenInfo_IDs:
            try:
                widget = main_screen.ids.get(field_id)
                if widget and hasattr(widget, 'text'):
                    gen_info[field_id] = widget.text
            except Exception as e:
                print(f"Error collecting {field_id}: {e}")

        # Collect estimation sections
        container = main_screen.ids.get('dynamic_sections_container')
        if not container:
            return {
                "general_info": gen_info,
                "sections": [],
                "database_state": {},
                "timestamp": datetime.now().isoformat(),
                "version": "1.1"
            }

        sections = []
        for section_widget in reversed(container.children):
            section_data = self._collect_section(section_widget)
            if section_data:
                sections.append(section_data)

        # Collect database state for rate analysis
        db_state = self._collect_database_state()

        return {
            "general_info": gen_info,
            "sections": sections,
            "database_state": db_state,
            "objects_cache_keys": list(objects_cache["Estimation_Data"]["Estimation_Sections"].keys()),
            "timestamp": datetime.now().isoformat(),
            "version": "1.1"
        }

    def _collect_database_state(self):
        """Collect all rate analysis data from database"""
        db_state = {}
        try:
            # Get all item numbers that have applied rates
            cursor = self.gui_DB.conn.cursor()
            cursor.execute("SELECT DISTINCT item_number FROM applied_rate_analysis")
            item_numbers = [row[0] for row in cursor.fetchall()]

            for item_no in item_numbers:
                rows, applied_data = self.gui_DB.load_appliedRateAnalysis(item_no)
                if rows and applied_data:
                    db_state[item_no] = applied_data

        except Exception as e:
            print(f"Error collecting database state: {e}")

        return db_state

    def _collect_section(self, section_widget):
        """Collect data from one EstimationPart"""
        try:
            section_data = {
                "section_number": getattr(section_widget, 'section_number', 1),
                "section_title": section_widget.ids.section_header.text,
                "items": []
            }

            item_container = section_widget.ids.get('dynamic_item_container')
            if not item_container:
                return section_data

            # Collect items in reverse order (Kivy stores reversed)
            for item_widget in reversed(item_container.children):
                item_data = self._collect_item(item_widget)
                if item_data:
                    section_data["items"].append(item_data)

            return section_data
        except Exception as e:
            print(f"Error collecting section: {e}")
            return None

    def _collect_item(self, item_widget):
        """Collect complete data from one ItemQuantity_Details including search state"""
        try:
            item_no = getattr(item_widget, 'item_no', '1.1')

            item_data = {
                "item_number": getattr(item_widget, 'item_number', 1),
                "section_number": getattr(item_widget, 'section_number', 1),
                "item_no": item_no,
                "item_number_label": item_widget.ids.item_number_label.text,
                "dropdown_text": item_widget.ids.dropdown.text,
                "search_keyword": item_widget.ids.search_keyword_input.text,
                "search_results": None,
                "applied_rate_ref": None,
                "subitems": []
            }

            # Check if search results exist
            search_container = item_widget.ids.get('dynamic_searchResults_container')
            if search_container and search_container.children:
                # Get search results widget
                search_widget = search_container.children[0]
                if hasattr(search_widget, 'ids') and 'search_rv' in search_widget.ids:
                    rv = search_widget.ids.search_rv
                    item_data["search_results"] = {
                        "data": list(rv.data),
                        "visible": True
                    }

            # Check database for applied rate
            try:
                rows, applied_data = self.gui_DB.load_appliedRateAnalysis(item_no)
                if rows and applied_data:
                    item_data["applied_rate_ref"] = applied_data.get("NormsDBRef")
            except:
                pass

            # Collect subitems
            dims_container = item_widget.ids.get('dimensions_container')
            if dims_container:
                for subitem_widget in reversed(dims_container.children):
                    subitem_data = self._collect_subitem(subitem_widget)
                    if subitem_data:
                        item_data["subitems"].append(subitem_data)

            return item_data
        except Exception as e:
            print(f"Error collecting item: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _collect_subitem(self, subitem_widget):
        """Collect data from one SubItemRow"""
        try:
            def get_text(widget, field_id):
                try:
                    field = widget.ids.get(field_id)
                    return field.text if field and hasattr(field, 'text') else "-"
                except:
                    return "-"

            return {
                "section_number": getattr(subitem_widget, 'section_number', 1),
                "item_number": getattr(subitem_widget, 'item_number', 1),
                "subitem_number": getattr(subitem_widget, 'subitem_number', 1),
                "item_description": get_text(subitem_widget, 'item_description'),
                "unit": get_text(subitem_widget, 'unit'),
                "rate": get_text(subitem_widget, 'rate'),
                "numbers": get_text(subitem_widget, 'numbers'),
                "length": get_text(subitem_widget, 'length'),
                "breadth": get_text(subitem_widget, 'breadth'),
                "height": get_text(subitem_widget, 'height'),
                "quantity": get_text(subitem_widget, 'quantity'),
                "remarks": get_text(subitem_widget, 'remarks')
            }
        except Exception as e:
            print(f"Error collecting subitem: {e}")
            return None

    # ENHANCED RESTORATION

    def _restore_gui_state(self, state):
        """Restore complete GUI from logical data"""
        from kivy.factory import Factory

        try:
            self.progress.update("Restoring general info...")
            main_screen = self.sm.get_screen("main_screen")

            # Restore general information
            gen_info = state.get("general_info", {})
            for field_id, text_value in gen_info.items():
                try:
                    widget = main_screen.ids.get(field_id)
                    if widget and hasattr(widget, 'text'):
                        widget.text = str(text_value) if text_value is not None else ""
                except Exception as e:
                    print(f"Error restoring {field_id}: {e}")

            # Get containers
            container = main_screen.ids.get('dynamic_sections_container')
            scroll_view = main_screen.ids.get('scroll_view')

            if not container:
                print("Container not found!")
                self.progress.dismiss()
                return False

            # Clear and reset
            container.clear_widgets()
            objects_cache["Estimation_Data"]["Estimation_Sections"] = {}

            # Restore database state first
            db_state = state.get("database_state", {})
            if db_state:
                self.progress.update("Restoring database state...")
                self._restore_database_state(db_state)

            # Restore sections
            sections = state.get("sections", [])
            total_sections = len(sections)

            for idx, section_data in enumerate(sections, 1):
                self.progress.update(f"Restoring section {idx}/{total_sections}...")
                self._restore_section(section_data, container, scroll_view)

            # Update cache
            self.progress.update("Updating cache...")
            Clock.schedule_once(lambda dt: self.cache_forNewSection(), 0.1)

            # Final cleanup
            Clock.schedule_once(lambda dt: self._finalize_restore(), 0.3)

            return True

        except Exception as e:
            self.progress.dismiss()
            print(f"Error in restore_gui_state: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _restore_database_state(self, db_state):
        """Restore rate analysis data to database"""
        for item_no, applied_data in db_state.items():
            try:
                self.GUIHandle.sendAppRateTo_DB(item_no, applied_data)
            except Exception as e:
                print(f"Error restoring DB for {item_no}: {e}")

    def _restore_section(self, section_data, container, scroll_view):
        """Restore one EstimationPart section"""
        from kivy.factory import Factory

        try:
            new_section = Factory.EstimationPart()
            new_section.section_number = section_data.get("section_number", 1)

            # Set section title
            section_title = section_data.get("section_title", f"Estimation Section {new_section.section_number}")
            Clock.schedule_once(
                lambda dt: setattr(new_section.ids.section_header, 'text', section_title),
                0.05
            )

            container.add_widget(new_section)

            # Restore items
            item_container = new_section.ids.get('dynamic_item_container')
            if item_container:
                for item_data in section_data.get("items", []):
                    self._restore_item(item_data, item_container, new_section)

        except Exception as e:
            print(f"Error restoring section: {e}")
            import traceback
            traceback.print_exc()

    def _restore_item(self, item_data, item_container, section_widget):
        """Restore one ItemQuantity_Details with complete state"""
        from kivy.factory import Factory

        try:
            new_item = Factory.ItemQuantity_Details()
            new_item.item_number = item_data.get("item_number", 1)
            new_item.section_number = item_data.get("section_number", 1)

            item_container.add_widget(new_item)

            # Restore item properties with delay
            def restore_item_props(dt):
                try:
                    # Set item number label
                    if "item_number_label" in item_data:
                        new_item.ids.item_number_label.text = item_data["item_number_label"]

                    # Set dropdown
                    if "dropdown_text" in item_data:
                        new_item.ids.dropdown.text = item_data["dropdown_text"]

                    # Set search keyword
                    if "search_keyword" in item_data:
                        new_item.ids.search_keyword_input.text = item_data["search_keyword"]

                    # Restore search results if they existed
                    search_results = item_data.get("search_results")
                    if search_results and search_results.get("visible"):
                        Clock.schedule_once(
                            lambda dt: self._restore_search_results(new_item, search_results),
                            0.1
                        )

                except Exception as e:
                    print(f"Error in restore_item_props: {e}")

            Clock.schedule_once(restore_item_props, 0.05)

            # Restore subitems
            dims_container = new_item.ids.get('dimensions_container')
            if dims_container:
                for subitem_data in item_data.get("subitems", []):
                    self._restore_subitem(subitem_data, dims_container, new_item, item_data)

        except Exception as e:
            print(f"Error restoring item: {e}")
            import traceback
            traceback.print_exc()

    def _restore_search_results(self, item_widget, search_results):
        """Restore search results for an item"""
        from kivy.factory import Factory

        try:
            search_container = item_widget.ids.get('dynamic_searchResults_container')
            item_no_val = getattr(item_widget, "item_no", None)

            if not search_container:
                return

            search_container.clear_widgets()
            search_widget = Factory.Search_Results()
            search_container.add_widget(search_widget)
            if item_no_val:
                self.searchCOntainterChildrens[str(item_no_val)] = {
                    "container": search_container,
                    "widget": search_widget,
                }

            # Restore data
            rv_data = search_results.get("data", [])
            search_widget.ids.search_rv.data = rv_data

            self._auto_apply_single_search_results()


        except Exception as e:
            print(f"Error restoring search results: {e}")

    def _auto_apply_single_search_results(self):
        """Auto-apply rate analysis if search results contain only one item by simulating button click"""

        def _find_and_click_apply( rv, item_key):
            """Run after RV has rendered to find the 'check' icon."""
            try:
                from kivy.app import App
                app = App.get_running_app()
                inspector = GUIInspector(root_widget=app.root)

                # find the first SearchItem
                recycle_layout = None
                for child in rv.children:
                    if hasattr(child, 'default_size'):  # RecycleBoxLayout
                        recycle_layout = child
                        break

                if not recycle_layout or not recycle_layout.children:
                    print(f"No SearchItem widgets yet for {item_key}")
                    return

                search_item_widget = recycle_layout.children[0]

                # recursively find check icon
                def find_apply_button(widget):
                    if hasattr(widget, 'icon') and widget.icon == "check":
                        return widget
                    for c in getattr(widget, 'children', []):
                        btn = find_apply_button(c)
                        if btn:
                            return btn
                    return None

                apply_button = find_apply_button(search_item_widget)
                if apply_button:
                    print(f"Clicking apply button for {item_key}")
                    apply_button.dispatch('on_release')
                else:
                    print(f"No apply button found in {item_key}")

            except Exception as e:
                print(f"Error in _find_and_click_apply for {item_key}: {e}")

        try:
            # Iterate through all items in objects_cache
            cache_keys = list(objects_cache["Estimation_Data"]["Estimation_Sections"].keys())

            for item_key in cache_keys:
                # Only process main item keys (x.y format, not x.y.z)
                if safe_float(item_key.split(".")[-1]) == 1:
                    print(item_key, "inside")

                    try:
                        item_cache = objects_cache["Estimation_Data"]["Estimation_Sections"].get(item_key)
                        if not item_cache:
                            continue

                        # Get search results container
                        item_no = ".".join(item_key.split(".")[0:2])
                        search_entry = self.searchCOntainterChildrens.get(str(item_no))
                        if not search_entry:
                            continue

                        search_container = search_entry["container"]
                        search_widget = search_entry["widget"]

                        rv = search_widget.ids.search_rv
                        Clock.schedule_once(
                            lambda dt, rv=rv, item_key=item_key: _find_and_click_apply(rv, item_key), 0.1)


                    except Exception as e:
                        print(f"Error processing item {item_key}: {e}")
                        import traceback
                        traceback.print_exc()
                        continue

        except Exception as e:
            print(f"Error in _auto_apply_single_search_results: {e}")
            import traceback
            traceback.print_exc()("Second Inner table", {}).get("Unit Rate", [0])[0]

    def _restore_subitem(self, subitem_data, dims_container, item_widget, item_data):
        """Restore one SubItemRow with all field values"""
        from kivy.factory import Factory

        try:
            new_subitem = Factory.SubItemRow()
            new_subitem.section_number = subitem_data.get("section_number", 1)
            new_subitem.item_number = subitem_data.get("item_number", 1)
            new_subitem.subitem_number = subitem_data.get("subitem_number", 1)

            dims_container.add_widget(new_subitem)

            # Cache BEFORE setting values

            # Clock.schedule_once(lambda dt: self.cache_forNewItem(item_widget), 0.02)

            #The main problem here is that the object cache dooesnot have any information of the subitem number ie stored in it.
            #So when the sub item number is called upon it must set the values and their objects
            # it is now solved when the gui is
            self.cache_forNewItem(item_widget)
            inspector = GUIInspector(root_widget=app.root)
            props = inspector.get_widget_properties(item_widget)


            # Set field values with proper delay
            def set_subitem_values(dt):
                try:
                    fields = {
                        'item_description': subitem_data.get('item_description', '-'),
                        'unit': subitem_data.get('unit', '-'),
                        'rate': subitem_data.get('rate', '-'),
                        'numbers': subitem_data.get('numbers', '-'),
                        'length': subitem_data.get('length', '-'),
                        'breadth': subitem_data.get('breadth', '-'),
                        'height': subitem_data.get('height', '-'),
                        'remarks': subitem_data.get('remarks', '-')
                    }

                    for field_id, value in fields.items():
                        field = new_subitem.ids.get(field_id)
                        if field and hasattr(field, 'text'):
                            # Convert None or empty to "-"
                            text_value = str(value) if value not in [None, ''] else "-"
                            field.text = text_value

                    # Apply rate from database if exists
                    item_no = item_data.get("item_no")
                    applied_ref = item_data.get("applied_rate_ref")

                    if item_no and applied_ref:
                        Clock.schedule_once(
                            lambda dt: self._apply_saved_rate(item_no, new_subitem),
                            0.1
                        )
                    else:
                        # Just trigger calculation
                        if hasattr(new_subitem, 'calculate_quantity'):
                            Clock.schedule_once(
                                lambda dt: new_subitem.calculate_quantity(),
                                0.15
                            )

                except Exception as e:
                    print(f"Error setting subitem values: {e}")
                    import traceback
                    traceback.print_exc()

            Clock.schedule_once(set_subitem_values, 0.05)

        except Exception as e:
            print(f"Error restoring subitem: {e}")
            import traceback
            traceback.print_exc()

    def _apply_saved_rate(self, item_no, subitem_widget):
        """Apply saved rate from database to subitem"""
        try:
            rows, applied_data = self.gui_DB.load_appliedRateAnalysis(item_no)
            if rows and applied_data:
                unit_rate = applied_data.get("Second Inner table", {}).get("Unit Rate", [0])[0]
                rate_field = subitem_widget.ids.get("rate")
                if rate_field:
                    rate_field.text = "{:.2f}".format(float(unit_rate))

                # Trigger calculation
                if hasattr(subitem_widget, 'calculate_quantity'):
                    subitem_widget.calculate_quantity()
        except Exception as e:
            print(f"Error applying saved rate: {e}")

    def _finalize_restore(self):
        """Final cleanup after restore"""
        try:
            # Force all calculations
            main_screen = self.sm.get_screen("main_screen")
            container = main_screen.ids.get('dynamic_sections_container')

            if container:
                for section in container.children:
                    item_container = section.ids.get('dynamic_item_container')
                    if item_container:
                        for item in item_container.children:
                            dims_container = item.ids.get('dimensions_container')
                            if dims_container:
                                for subitem in dims_container.children:
                                    if hasattr(subitem, 'calculate_quantity'):
                                        try:
                                            subitem.calculate_quantity()
                                        except:
                                            pass
            #set the scroll to latest
            main_screen = self.sm.get_screen("main_screen")
            est_screen = self.sm.get_screen("estimation_screen")
            container = main_screen.ids.get('dynamic_sections_container')
            scroll_view = main_screen.ids.get('scroll_view')
            if scroll_view:
                scroll_view.scroll_y = 1
            else:
                print("scroll_view not found!")


            # Save current state to DB
            self.GUIHandle.sendGenInfoQEst_toDB()

            self.progress.dismiss()
            self.toast("State restored successfully!")

        except Exception as e:
            self.progress.dismiss()
            print(f"Error in finalize_restore: {e}")


    # =============================# FIX: Enhanced file dialogs with proper callbacks

    def open_save_dialog(self):
        """Open dialog for saving GUI state"""
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        filename_input = MDTextField(
            hint_text="Enter filename (without extension)",
            text=f"gui_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            size_hint_y=None,
            height=dp(40)
        )

        content.add_widget(filename_input)

        def on_save(instance):
            filename = filename_input.text.strip()
            if not filename.endswith('.json'):
                filename += '.json'
            popup.dismiss()
            # Use Clock to ensure dialog closes before showing progress
            Clock.schedule_once(lambda dt: self.save_gui_state(filename), 0.1)

        def on_cancel(instance):
            popup.dismiss()

        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)

        save_btn = MDButton(on_release=on_save)
        save_btn.add_widget(MDButtonText(text="Save"))

        cancel_btn = MDButton(on_release=on_cancel)
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)

        content.add_widget(btn_layout)

        popup = Popup(
            title="Save GUI State",
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        popup.open()


    def open_load_dialog(self):
        """Open dialog for loading GUI state with file browser"""
        import os
        from kivy.uix.filechooser import FileChooserListView

        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # File chooser
        filechooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.json'],
            size_hint=(1, 0.8)
        )
        content.add_widget(filechooser)

        # Selected file label
        from kivymd.uix.label import MDLabel
        selected_label = MDLabel(
            text="No file selected",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Secondary"
        )
        content.add_widget(selected_label)

        def on_selection(instance, value):
            if value:
                selected_label.text = f"Selected: {os.path.basename(value[0])}"

        filechooser.bind(selection=on_selection)

        def on_load(instance):
            if filechooser.selection:
                filename = filechooser.selection[0]
                popup.dismiss()
                # Use Clock to ensure dialog closes before showing progress
                Clock.schedule_once(lambda dt: self.load_gui_state(filename), 0.1)

            else:
                self.toast("Please select a file")

        def on_cancel(instance):
            popup.dismiss()

        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)

        load_btn = MDButton(on_release=on_load)
        load_btn.add_widget(MDButtonText(text="Load"))

        cancel_btn = MDButton(on_release=on_cancel)
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        btn_layout.add_widget(load_btn)
        btn_layout.add_widget(cancel_btn)

        content.add_widget(btn_layout)

        popup = Popup(
            title="Load GUI State",
            content=content,
            size_hint=(0.7, 0.7),
            auto_dismiss=False
        )
        popup.open()





if __name__ == "__main__":
    Window.minimum_width, Window.minimum_height = (800, 600)
    app = CivilEstimationApp()

    # inject app into another class
    # helper = SomeOtherClass(app)
    # helper.do_something()  # works before app.run()

    app.run()