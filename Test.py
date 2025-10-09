# main.py
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.scrollview import MDScrollView
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.graphics import RoundedRectangle
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import (    MDDialogButtonContainer,)
from kivymd.uix.button import MDButtonIcon, MDButtonText
from math import prod
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, ObjectProperty
from typing import Optional, Any, Dict
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivy.utils import get_color_from_hex
import json, os
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDExtendedFabButton, MDExtendedFabButtonIcon, MDExtendedFabButtonText
from kivymd.uix.behaviors import HoverBehavior
import webbrowser
import sys
import InputData as ID
import DatabaseManagement as DM
from kivymd.uix.label import MDLabel
import re
from kivy.clock import Clock
import traceback
from kivy.factory import Factory
from kivy.app import App
import os
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.label import MDLabel


objects_cache = {
    "Estimation_Data": {
        "Estimation_Sections": {}  # outer list of sections
    }
}
# Global cache for all dynamically created estimation GUI objects
def resourece_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, rel_path)
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

                def toasttextconfiner(boolval, val):
                    if boolval:
                        return f"Data written successfully to {val}"
                    else:
                        return f"Writing failed to {val}"



                titleret = db_out.SheetsTitle_Writing()  # When the erroro of the io ie file not found occurs then enforce the Sheets Title function
                app.toast(toasttextconfiner(titleret, "SheetsTitle"))
                coverret = db_out.CoverPage_Writing()
                app.toast(toasttextconfiner(coverret, "Cover Page"))

                qestret = db_out.QuantityEstSheet_Writing()
                app.toast(toasttextconfiner(qestret, "Quantity Estimation sheet"))

                aocret = db_out.AOC_writing()
                app.toast(toasttextconfiner(aocret, "Abstract of Cost"))

                summaryret = db_out.SummaryWriting()
                app.toast(toasttextconfiner(summaryret, "Summary sheet"))

                boqret = db_out.BOQ_Writing()
                app.toast(toasttextconfiner(boqret, "BOQ sheet"))

                rateanalysisret = db_out.RateAnalysisDataWriting()
                app.toast(toasttextconfiner(rateanalysisret, "Rate Analysis sheet"))

                postproret = db_out.PostProcessingExcel()
                app.toast(toasttextconfiner(postproret, "Postprocessing criteria"))


                if valuesDict["pdf"]:
                    excelpdtoutret = db_out.excel_to_pdf_merge()
                    app.toast(toasttextconfiner(postproret, "Excel to PDF format"))

                if valuesDict["print"]:
                    printpdfret = db_out.PrintPDF()
                    app.toast(toasttextconfiner(postproret, "Printer"))

                popup.dismiss()
            except Exception as e:
                app.toast(f'"Error:", {e}')
                print("Error:", e)
                popup.dismiss()


        popup.open()

        def on_cancel(instance):
            popup.dismiss()
    def click_item(self):
        inspector = GUIInspector(root_widget=self)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewItemButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'ITem' not found!")
    def click_NewSection(self):
        inspector = GUIInspector(root_widget=self)  # use self.root, not app.root
        widget = inspector.get_widget_by_id("NewSectionButton")
        if widget:
            widget.dispatch("on_release")
        else:
            print("Widget with id 'ITem' not found!")
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
class HoverFab(MDExtendedFabButton, HoverBehavior):
    def on_enter(self, *args):
        self.fab_state = "expand"

    def on_leave(self, *args):
        self.fab_state = "collapse"

# Academic Software Themes for KivyMD
# Optimized for readability, focus, and extended use

THEMES = {
    "classic_light": {
        "backgroundColor": "#FAFAFA",
        "disabledTextColor": "#9E9E9E",
        "errorColor": "#B00020",
        "errorContainerColor": "#F9DEDC",
        "inverseOnSurfaceColor": "#F5F5F5",
        "inversePrimaryColor": "#90CAF9",
        "inverseSurfaceColor": "#212121",
        "neutral_paletteKeyColorColor": "#757575",
        "neutral_variant_paletteKeyColorColor": "#616161",
        "onBackgroundColor": "#1A1A1A",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#410002",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D36",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#004A77",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1A1A1A",
        "onSecondaryFixedColor": "#0A1929",
        "onSecondaryFixedVariantColor": "#455A64",
        "onSurfaceColor": "#1A1A1A",
        "onSurfaceLightColor": "#424242",
        "onSurfaceVariantColor": "#424242",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1A1A1A",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#757575",
        "outlineVariantColor": "#C2C2C2",
        "primaryColor": "#1976D2",
        "primaryContainerColor": "#BBDEFB",
        "primaryFixedColor": "#D6E9FF",
        "primaryFixedDimColor": "#90CAF9",
        "primary_paletteKeyColorColor": "#1976D2",
        "rippleColor": "#1976D233",
        "scrimColor": "#000000",
        "secondaryColor": "#546E7A",
        "secondaryContainerColor": "#CFE8FC",
        "secondaryFixedColor": "#D1E8FF",
        "secondaryFixedDimColor": "#B0BEC5",
        "secondary_paletteKeyColorColor": "#546E7A",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#FAFAFA",
        "surfaceColor": "#FFFFFF",
        "surfaceContainerColor": "#F5F5F5",
        "surfaceContainerHighColor": "#EEEEEE",
        "surfaceContainerHighestColor": "#E0E0E0",
        "surfaceContainerLowColor": "#F8F8F8",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#EEEEEE",
        "surfaceTintColor": "#1976D2",
        "surfaceVariantColor": "#E0E0E0",
        "tertiaryColor": "#8D6E63",
        "tertiaryContainerColor": "#FFECDF",
        "tertiaryFixedColor": "#FFDCC0",
        "tertiaryFixedDimColor": "#D7CCC8",
        "tertiary_paletteKeyColorColor": "#8D6E63",
        "transparentColor": "#00000000"
    },

    "solarized_light": {
        "backgroundColor": "#FDF6E3",
        "disabledTextColor": "#93A1A1",
        "errorColor": "#DC322F",
        "errorContainerColor": "#FDD8D6",
        "inverseOnSurfaceColor": "#FDF6E3",
        "inversePrimaryColor": "#268BD2",
        "inverseSurfaceColor": "#002B36",
        "neutral_paletteKeyColorColor": "#839496",
        "neutral_variant_paletteKeyColorColor": "#657B83",
        "onBackgroundColor": "#002B36",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D2E",
        "onPrimaryFixedColor": "#001D2E",
        "onPrimaryFixedVariantColor": "#073642",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#073642",
        "onSecondaryFixedColor": "#002B36",
        "onSecondaryFixedVariantColor": "#586E75",
        "onSurfaceColor": "#002B36",
        "onSurfaceLightColor": "#073642",
        "onSurfaceVariantColor": "#586E75",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#2E1E00",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#93A1A1",
        "outlineVariantColor": "#D3CBBA",
        "primaryColor": "#268BD2",
        "primaryContainerColor": "#C3E7FF",
        "primaryFixedColor": "#D5EFFF",
        "primaryFixedDimColor": "#B7D9EB",
        "primary_paletteKeyColorColor": "#268BD2",
        "rippleColor": "#268BD233",
        "scrimColor": "#000000",
        "secondaryColor": "#2AA198",
        "secondaryContainerColor": "#C5F5EF",
        "secondaryFixedColor": "#D4F6F1",
        "secondaryFixedDimColor": "#B5E5DD",
        "secondary_paletteKeyColorColor": "#2AA198",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#FDF6E3",
        "surfaceColor": "#FDF6E3",
        "surfaceContainerColor": "#F5EED9",
        "surfaceContainerHighColor": "#EDE5D2",
        "surfaceContainerHighestColor": "#E7DFCC",
        "surfaceContainerLowColor": "#FAF3E0",
        "surfaceContainerLowestColor": "#FFFDF7",
        "surfaceDimColor": "#EEE8D5",
        "surfaceTintColor": "#268BD2",
        "surfaceVariantColor": "#EEE8D5",
        "tertiaryColor": "#B58900",
        "tertiaryContainerColor": "#FFE9B8",
        "tertiaryFixedColor": "#FFF0CC",
        "tertiaryFixedDimColor": "#E5D3A3",
        "tertiary_paletteKeyColorColor": "#B58900",
        "transparentColor": "#00000000"
    },

    "paper_white": {
        "backgroundColor": "#FFFFFF",
        "disabledTextColor": "#A0A0A0",
        "errorColor": "#C62828",
        "errorContainerColor": "#FDEAEB",
        "inverseOnSurfaceColor": "#FAFAFA",
        "inversePrimaryColor": "#64B5F6",
        "inverseSurfaceColor": "#1C1C1C",
        "neutral_paletteKeyColorColor": "#6B6B6B",
        "neutral_variant_paletteKeyColorColor": "#5E5E5E",
        "onBackgroundColor": "#000000",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#400000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001A33",
        "onPrimaryFixedColor": "#001A33",
        "onPrimaryFixedVariantColor": "#003D7A",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1A1A1A",
        "onSecondaryFixedColor": "#000000",
        "onSecondaryFixedVariantColor": "#424242",
        "onSurfaceColor": "#000000",
        "onSurfaceLightColor": "#3C3C3C",
        "onSurfaceVariantColor": "#3C3C3C",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1A1A1A",
        "onTertiaryFixedColor": "#1E1E1E",
        "onTertiaryFixedVariantColor": "#4A4A4A",
        "outlineColor": "#6B6B6B",
        "outlineVariantColor": "#CCCCCC",
        "primaryColor": "#0D47A1",
        "primaryContainerColor": "#C5D9F1",
        "primaryFixedColor": "#D6E6FF",
        "primaryFixedDimColor": "#A8C8E7",
        "primary_paletteKeyColorColor": "#0D47A1",
        "rippleColor": "#0D47A133",
        "scrimColor": "#000000",
        "secondaryColor": "#424242",
        "secondaryContainerColor": "#E8E8E8",
        "secondaryFixedColor": "#F5F5F5",
        "secondaryFixedDimColor": "#D4D4D4",
        "secondary_paletteKeyColorColor": "#424242",
        "shadowColor": "#00000020",
        "surfaceBrightColor": "#FFFFFF",
        "surfaceColor": "#FFFFFF",
        "surfaceContainerColor": "#FAFAFA",
        "surfaceContainerHighColor": "#F5F5F5",
        "surfaceContainerHighestColor": "#EEEEEE",
        "surfaceContainerLowColor": "#FCFCFC",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#F8F8F8",
        "surfaceTintColor": "#0D47A1",
        "surfaceVariantColor": "#F0F0F0",
        "tertiaryColor": "#616161",
        "tertiaryContainerColor": "#E8E8E8",
        "tertiaryFixedColor": "#F2F2F2",
        "tertiaryFixedDimColor": "#D7D7D7",
        "tertiary_paletteKeyColorColor": "#616161",
        "transparentColor": "#00000000"
    },

    "midnight": {
        "backgroundColor": "#000000",
        "disabledTextColor": "#666666",
        "errorColor": "#CF6679",
        "errorContainerColor": "#93000A",
        "inverseOnSurfaceColor": "#121212",
        "inversePrimaryColor": "#0D47A1",
        "inverseSurfaceColor": "#E3E3E3",
        "neutral_paletteKeyColorColor": "#8B8B8B",
        "neutral_variant_paletteKeyColorColor": "#9E9E9E",
        "onBackgroundColor": "#E3E3E3",
        "onErrorColor": "#690005",
        "onErrorContainerColor": "#FFDAD6",
        "onPrimaryColor": "#003258",
        "onPrimaryContainerColor": "#D1E4FF",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#00497D",
        "onSecondaryColor": "#003549",
        "onSecondaryContainerColor": "#BCE9FF",
        "onSecondaryFixedColor": "#001F28",
        "onSecondaryFixedVariantColor": "#004E64",
        "onSurfaceColor": "#E3E3E3",
        "onSurfaceLightColor": "#C7C7C7",
        "onSurfaceVariantColor": "#C2C7CF",
        "onTertiaryColor": "#3A2E5C",
        "onTertiaryContainerColor": "#E5DEFF",
        "onTertiaryFixedColor": "#21174A",
        "onTertiaryFixedVariantColor": "#524372",
        "outlineColor": "#8C9199",
        "outlineVariantColor": "#42474E",
        "primaryColor": "#9ECAFF",
        "primaryContainerColor": "#00497D",
        "primaryFixedColor": "#D1E4FF",
        "primaryFixedDimColor": "#9ECAFF",
        "primary_paletteKeyColorColor": "#4A8FDB",
        "rippleColor": "#9ECAFF33",
        "scrimColor": "#000000",
        "secondaryColor": "#B1CBD8",
        "secondaryContainerColor": "#004E64",
        "secondaryFixedColor": "#BCE9FF",
        "secondaryFixedDimColor": "#6DD3F5",
        "secondary_paletteKeyColorColor": "#37B5D4",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#1A1A1A",
        "surfaceColor": "#000000",
        "surfaceContainerColor": "#0F0F0F",
        "surfaceContainerHighColor": "#1A1A1A",
        "surfaceContainerHighestColor": "#252525",
        "surfaceContainerLowColor": "#0A0A0A",
        "surfaceContainerLowestColor": "#000000",
        "surfaceDimColor": "#0A0A0A",
        "surfaceTintColor": "#9ECAFF",
        "surfaceVariantColor": "#1A1A1A",
        "tertiaryColor": "#C9BFFF",
        "tertiaryContainerColor": "#524372",
        "tertiaryFixedColor": "#E5DEFF",
        "tertiaryFixedDimColor": "#C9BFFF",
        "tertiary_paletteKeyColorColor": "#8B7DB8",
        "transparentColor": "#00000000"
    },

    "charcoal": {
        "backgroundColor": "#1E1E1E",
        "disabledTextColor": "#707070",
        "errorColor": "#F2B8B5",
        "errorContainerColor": "#8C1D18",
        "inverseOnSurfaceColor": "#2A2A2A",
        "inversePrimaryColor": "#1565C0",
        "inverseSurfaceColor": "#E0E0E0",
        "neutral_paletteKeyColorColor": "#8E8E8E",
        "neutral_variant_paletteKeyColorColor": "#A1A1A1",
        "onBackgroundColor": "#E8E8E8",
        "onErrorColor": "#601410",
        "onErrorContainerColor": "#FFDAD6",
        "onPrimaryColor": "#00315C",
        "onPrimaryContainerColor": "#D4E3FF",
        "onPrimaryFixedColor": "#001C38",
        "onPrimaryFixedVariantColor": "#004A77",
        "onSecondaryColor": "#00344A",
        "onSecondaryContainerColor": "#BFEAFF",
        "onSecondaryFixedColor": "#001E2B",
        "onSecondaryFixedVariantColor": "#004D64",
        "onSurfaceColor": "#E8E8E8",
        "onSurfaceLightColor": "#CBCBCB",
        "onSurfaceVariantColor": "#C5C6CA",
        "onTertiaryColor": "#3D2E54",
        "onTertiaryContainerColor": "#E8DEFF",
        "onTertiaryFixedColor": "#24163F",
        "onTertiaryFixedVariantColor": "#55426C",
        "outlineColor": "#8F9094",
        "outlineVariantColor": "#44474F",
        "primaryColor": "#A8C7FA",
        "primaryContainerColor": "#004A77",
        "primaryFixedColor": "#D4E3FF",
        "primaryFixedDimColor": "#A8C7FA",
        "primary_paletteKeyColorColor": "#5398DB",
        "rippleColor": "#A8C7FA33",
        "scrimColor": "#000000",
        "secondaryColor": "#B4CBD8",
        "secondaryContainerColor": "#004D64",
        "secondaryFixedColor": "#BFEAFF",
        "secondaryFixedDimColor": "#72D3F4",
        "secondary_paletteKeyColorColor": "#40B6D5",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#3E3E3E",
        "surfaceColor": "#2A2A2A",
        "surfaceContainerColor": "#242424",
        "surfaceContainerHighColor": "#2F2F2F",
        "surfaceContainerHighestColor": "#3A3A3A",
        "surfaceContainerLowColor": "#1F1F1F",
        "surfaceContainerLowestColor": "#1A1A1A",
        "surfaceDimColor": "#1E1E1E",
        "surfaceTintColor": "#A8C7FA",
        "surfaceVariantColor": "#2F2F2F",
        "tertiaryColor": "#CCBFFF",
        "tertiaryContainerColor": "#55426C",
        "tertiaryFixedColor": "#E8DEFF",
        "tertiaryFixedDimColor": "#CCBFFF",
        "tertiary_paletteKeyColorColor": "#9380BA",
        "transparentColor": "#00000000"
    },

    "solarized_dark": {
        "backgroundColor": "#002B36",
        "disabledTextColor": "#586E75",
        "errorColor": "#DC322F",
        "errorContainerColor": "#8C1D18",
        "inverseOnSurfaceColor": "#073642",
        "inversePrimaryColor": "#268BD2",
        "inverseSurfaceColor": "#FDF6E3",
        "neutral_paletteKeyColorColor": "#839496",
        "neutral_variant_paletteKeyColorColor": "#657B83",
        "onBackgroundColor": "#93A1A1",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#FFDAD6",
        "onPrimaryColor": "#00171F",
        "onPrimaryContainerColor": "#C3E7FF",
        "onPrimaryFixedColor": "#001D2E",
        "onPrimaryFixedVariantColor": "#004570",
        "onSecondaryColor": "#00171F",
        "onSecondaryContainerColor": "#C5F5EF",
        "onSecondaryFixedColor": "#001F1E",
        "onSecondaryFixedVariantColor": "#00504B",
        "onSurfaceColor": "#93A1A1",
        "onSurfaceLightColor": "#839496",
        "onSurfaceVariantColor": "#839496",
        "onTertiaryColor": "#2E1E00",
        "onTertiaryContainerColor": "#FFE9B8",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#657B83",
        "outlineVariantColor": "#073642",
        "primaryColor": "#268BD2",
        "primaryContainerColor": "#004570",
        "primaryFixedColor": "#C3E7FF",
        "primaryFixedDimColor": "#81C7F5",
        "primary_paletteKeyColorColor": "#268BD2",
        "rippleColor": "#268BD233",
        "scrimColor": "#000000",
        "secondaryColor": "#2AA198",
        "secondaryContainerColor": "#00504B",
        "secondaryFixedColor": "#C5F5EF",
        "secondaryFixedDimColor": "#70D9D0",
        "secondary_paletteKeyColorColor": "#2AA198",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#0F3643",
        "surfaceColor": "#073642",
        "surfaceContainerColor": "#062D38",
        "surfaceContainerHighColor": "#0F3643",
        "surfaceContainerHighestColor": "#19404E",
        "surfaceContainerLowColor": "#052732",
        "surfaceContainerLowestColor": "#00222B",
        "surfaceDimColor": "#002B36",
        "surfaceTintColor": "#268BD2",
        "surfaceVariantColor": "#0A3240",
        "tertiaryColor": "#B58900",
        "tertiaryContainerColor": "#5D4E2A",
        "tertiaryFixedColor": "#FFE9B8",
        "tertiaryFixedDimColor": "#D6BE70",
        "tertiary_paletteKeyColorColor": "#B58900",
        "transparentColor": "#00000000"
    },

    "ocean_blue": {
        "backgroundColor": "#E3F2FD",
        "disabledTextColor": "#78909C",
        "errorColor": "#B71C1C",
        "errorContainerColor": "#FFCDD2",
        "inverseOnSurfaceColor": "#E1F5FE",
        "inversePrimaryColor": "#64B5F6",
        "inverseSurfaceColor": "#01579B",
        "neutral_paletteKeyColorColor": "#607D8B",
        "neutral_variant_paletteKeyColorColor": "#546E7A",
        "onBackgroundColor": "#01579B",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D30",
        "onPrimaryFixedColor": "#001D30",
        "onPrimaryFixedVariantColor": "#004667",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#001E2E",
        "onSecondaryFixedColor": "#001E2E",
        "onSecondaryFixedVariantColor": "#00415A",
        "onSurfaceColor": "#01579B",
        "onSurfaceLightColor": "#0277BD",
        "onSurfaceVariantColor": "#455A64",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#001E30",
        "onTertiaryFixedColor": "#001E30",
        "onTertiaryFixedVariantColor": "#004667",
        "outlineColor": "#607D8B",
        "outlineVariantColor": "#B0BEC5",
        "primaryColor": "#0277BD",
        "primaryContainerColor": "#B3E5FC",
        "primaryFixedColor": "#C6EAFF",
        "primaryFixedDimColor": "#84D4F5",
        "primary_paletteKeyColorColor": "#0277BD",
        "rippleColor": "#0277BD33",
        "scrimColor": "#000000",
        "secondaryColor": "#006C95",
        "secondaryContainerColor": "#B3E5FC",
        "secondaryFixedColor": "#C6EAFF",
        "secondaryFixedDimColor": "#6DD4F5",
        "secondary_paletteKeyColorColor": "#006C95",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#E3F2FD",
        "surfaceColor": "#F0F9FF",
        "surfaceContainerColor": "#E3F2FD",
        "surfaceContainerHighColor": "#D4EBFA",
        "surfaceContainerHighestColor": "#C5E4F7",
        "surfaceContainerLowColor": "#EBF6FF",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#D6EDFA",
        "surfaceTintColor": "#0277BD",
        "surfaceVariantColor": "#CFE8F3",
        "tertiaryColor": "#004D73",
        "tertiaryContainerColor": "#C6EAFF",
        "tertiaryFixedColor": "#D6F0FF",
        "tertiaryFixedDimColor": "#9FDDF5",
        "tertiary_paletteKeyColorColor": "#0086C3",
        "transparentColor": "#00000000"
    },

    "forest_green": {
        "backgroundColor": "#E8F5E9",
        "disabledTextColor": "#78909C",
        "errorColor": "#C62828",
        "errorContainerColor": "#FFCDD2",
        "inverseOnSurfaceColor": "#E8F5E9",
        "inversePrimaryColor": "#66BB6A",
        "inverseSurfaceColor": "#1B5E20",
        "neutral_paletteKeyColorColor": "#607D8B",
        "neutral_variant_paletteKeyColorColor": "#546E7A",
        "onBackgroundColor": "#1B5E20",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#002106",
        "onPrimaryFixedColor": "#002106",
        "onPrimaryFixedVariantColor": "#00530F",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#0E1F13",
        "onSecondaryFixedColor": "#0E1F13",
        "onSecondaryFixedVariantColor": "#2D4A35",
        "onSurfaceColor": "#1B5E20",
        "onSurfaceLightColor": "#2E7D32",
        "onSurfaceVariantColor": "#424242",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1A2E00",
        "onTertiaryFixedColor": "#1A2E00",
        "onTertiaryFixedVariantColor": "#3D5F00",
        "outlineColor": "#607D8B",
        "outlineVariantColor": "#C8E6C9",
        "primaryColor": "#2E7D32",
        "primaryContainerColor": "#C8E6C9",
        "primaryFixedColor": "#DCEDC8",
        "primaryFixedDimColor": "#A5D6A7",
        "primary_paletteKeyColorColor": "#2E7D32",
        "rippleColor": "#2E7D3233",
        "scrimColor": "#000000",
        "secondaryColor": "#558B2F",
        "secondaryContainerColor": "#DCEDC8",
        "secondaryFixedColor": "#E5F3D6",
        "secondaryFixedDimColor": "#C5E1A5",
        "secondary_paletteKeyColorColor": "#558B2F",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#E8F5E9",
        "surfaceColor": "#F1F8F2",
        "surfaceContainerColor": "#E8F5E9",
        "surfaceContainerHighColor": "#DCEDC8",
        "surfaceContainerHighestColor": "#C8E6C9",
        "surfaceContainerLowColor": "#F1F8F2",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#DFF0E0",
        "surfaceTintColor": "#2E7D32",
        "surfaceVariantColor": "#D7EDD9",
        "tertiaryColor": "#689F38",
        "tertiaryContainerColor": "#E7F5D5",
        "tertiaryFixedColor": "#F1F8E9",
        "tertiaryFixedDimColor": "#DCEDC8",
        "tertiary_paletteKeyColorColor": "#7CB342",
        "transparentColor": "#00000000"
    },
    "gruvbox_light": {
        "backgroundColor": "#FBF1C7",
        "disabledTextColor": "#A89984",
        "errorColor": "#CC241D",
        "errorContainerColor": "#F9D7D5",
        "inverseOnSurfaceColor": "#F9F5D7",
        "inversePrimaryColor": "#458588",
        "inverseSurfaceColor": "#282828",
        "neutral_paletteKeyColorColor": "#7C6F64",
        "neutral_variant_paletteKeyColorColor": "#665C54",
        "onBackgroundColor": "#282828",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#3C0A00",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001E2B",
        "onPrimaryFixedColor": "#001E2B",
        "onPrimaryFixedVariantColor": "#003F58",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1F2B00",
        "onSecondaryFixedColor": "#1F2B00",
        "onSecondaryFixedVariantColor": "#3F5700",
        "onSurfaceColor": "#282828",
        "onSurfaceLightColor": "#3C3836",
        "onSurfaceVariantColor": "#504945",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#2D1700",
        "onTertiaryFixedColor": "#2D1700",
        "onTertiaryFixedVariantColor": "#5A3800",
        "outlineColor": "#928374",
        "outlineVariantColor": "#EBDBB2",
        "primaryColor": "#458588",
        "primaryContainerColor": "#D5E4E8",
        "primaryFixedColor": "#E3EFF2",
        "primaryFixedDimColor": "#BDD6DC",
        "primary_paletteKeyColorColor": "#458588",
        "rippleColor": "#45858833",
        "scrimColor": "#000000",
        "secondaryColor": "#98971A",
        "secondaryContainerColor": "#E8E5C8",
        "secondaryFixedColor": "#F2EFCC",
        "secondaryFixedDimColor": "#D9D6A3",
        "secondary_paletteKeyColorColor": "#98971A",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#FBF1C7",
        "surfaceColor": "#FBF1C7",
        "surfaceContainerColor": "#F2E5BC",
        "surfaceContainerHighColor": "#EBDBB2",
        "surfaceContainerHighestColor": "#E0CFA1",
        "surfaceContainerLowColor": "#F9F5D7",
        "surfaceContainerLowestColor": "#FFFBDD",
        "surfaceDimColor": "#F2E5BC",
        "surfaceTintColor": "#458588",
        "surfaceVariantColor": "#EBDBB2",
        "tertiaryColor": "#D65D0E",
        "tertiaryContainerColor": "#FADEC9",
        "tertiaryFixedColor": "#FFE9D5",
        "tertiaryFixedDimColor": "#F4D0A3",
        "tertiary_paletteKeyColorColor": "#D65D0E",
        "transparentColor": "#00000000"
    },

    "catppuccin_latte": {
        "backgroundColor": "#EFF1F5",
        "disabledTextColor": "#9CA0B0",
        "errorColor": "#D20F39",
        "errorContainerColor": "#F4DBE0",
        "inverseOnSurfaceColor": "#E6E9EF",
        "inversePrimaryColor": "#7287FD",
        "inverseSurfaceColor": "#1E1E2E",
        "neutral_paletteKeyColorColor": "#6C6F85",
        "neutral_variant_paletteKeyColorColor": "#5C5F77",
        "onBackgroundColor": "#1E1E2E",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#410002",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001847",
        "onPrimaryFixedColor": "#001847",
        "onPrimaryFixedVariantColor": "#003976",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#001B3D",
        "onSecondaryFixedColor": "#001B3D",
        "onSecondaryFixedVariantColor": "#00396E",
        "onSurfaceColor": "#1E1E2E",
        "onSurfaceLightColor": "#4C4F69",
        "onSurfaceVariantColor": "#5C5F77",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1F1A3C",
        "onTertiaryFixedColor": "#1F1A3C",
        "onTertiaryFixedVariantColor": "#3E3660",
        "outlineColor": "#7C7F93",
        "outlineVariantColor": "#CCD0DA",
        "primaryColor": "#1E66F5",
        "primaryContainerColor": "#D4E1FF",
        "primaryFixedColor": "#E0EBFF",
        "primaryFixedDimColor": "#ADC6FF",
        "primary_paletteKeyColorColor": "#1E66F5",
        "rippleColor": "#1E66F533",
        "scrimColor": "#000000",
        "secondaryColor": "#04A5E5",
        "secondaryContainerColor": "#CEE9F7",
        "secondaryFixedColor": "#E0F3FF",
        "secondaryFixedDimColor": "#A6D8F0",
        "secondary_paletteKeyColorColor": "#04A5E5",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#EFF1F5",
        "surfaceColor": "#EFF1F5",
        "surfaceContainerColor": "#E6E9EF",
        "surfaceContainerHighColor": "#DCE0E8",
        "surfaceContainerHighestColor": "#CCD0DA",
        "surfaceContainerLowColor": "#E9ECF0",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#DFE1E8",
        "surfaceTintColor": "#1E66F5",
        "surfaceVariantColor": "#DCE0E8",
        "tertiaryColor": "#8839EF",
        "tertiaryContainerColor": "#E8DBFF",
        "tertiaryFixedColor": "#F2E7FF",
        "tertiaryFixedDimColor": "#D5BAFF",
        "tertiary_paletteKeyColorColor": "#8839EF",
        "transparentColor": "#00000000"
    },

    "dracula": {
        "backgroundColor": "#282A36",
        "disabledTextColor": "#6272A4",
        "errorColor": "#FF5555",
        "errorContainerColor": "#5C0F13",
        "inverseOnSurfaceColor": "#2E3142",
        "inversePrimaryColor": "#BD93F9",
        "inverseSurfaceColor": "#F8F8F2",
        "neutral_paletteKeyColorColor": "#6272A4",
        "neutral_variant_paletteKeyColorColor": "#44475A",
        "onBackgroundColor": "#F8F8F2",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6D9",
        "onPrimaryColor": "#2B0048",
        "onPrimaryContainerColor": "#EEDDFF",
        "onPrimaryFixedColor": "#2B0048",
        "onPrimaryFixedVariantColor": "#5A0097",
        "onSecondaryColor": "#002B3D",
        "onSecondaryContainerColor": "#C9F0FF",
        "onSecondaryFixedColor": "#001F2A",
        "onSecondaryFixedVariantColor": "#004F6A",
        "onSurfaceColor": "#F8F8F2",
        "onSurfaceLightColor": "#E8E8E0",
        "onSurfaceVariantColor": "#C2C4D4",
        "onTertiaryColor": "#00381F",
        "onTertiaryContainerColor": "#BFFFD9",
        "onTertiaryFixedColor": "#002112",
        "onTertiaryFixedVariantColor": "#00533A",
        "outlineColor": "#6272A4",
        "outlineVariantColor": "#44475A",
        "primaryColor": "#BD93F9",
        "primaryContainerColor": "#5A0097",
        "primaryFixedColor": "#EEDDFF",
        "primaryFixedDimColor": "#D5BAFF",
        "primary_paletteKeyColorColor": "#BD93F9",
        "rippleColor": "#BD93F933",
        "scrimColor": "#000000",
        "secondaryColor": "#8BE9FD",
        "secondaryContainerColor": "#004F6A",
        "secondaryFixedColor": "#C9F0FF",
        "secondaryFixedDimColor": "#5DD4F0",
        "secondary_paletteKeyColorColor": "#8BE9FD",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#383A4A",
        "surfaceColor": "#282A36",
        "surfaceContainerColor": "#21222C",
        "surfaceContainerHighColor": "#2F3241",
        "surfaceContainerHighestColor": "#3A3C4C",
        "surfaceContainerLowColor": "#1E1F29",
        "surfaceContainerLowestColor": "#191A21",
        "surfaceDimColor": "#21222C",
        "surfaceTintColor": "#BD93F9",
        "surfaceVariantColor": "#2F3241",
        "tertiaryColor": "#50FA7B",
        "tertiaryContainerColor": "#00533A",
        "tertiaryFixedColor": "#BFFFD9",
        "tertiaryFixedDimColor": "#34E89E",
        "tertiary_paletteKeyColorColor": "#50FA7B",
        "transparentColor": "#00000000"
    },

    "tokyo_night": {
        "backgroundColor": "#1A1B26",
        "disabledTextColor": "#565F89",
        "errorColor": "#F7768E",
        "errorContainerColor": "#5C0F1E",
        "inverseOnSurfaceColor": "#24283B",
        "inversePrimaryColor": "#7AA2F7",
        "inverseSurfaceColor": "#D5D6DB",
        "neutral_paletteKeyColorColor": "#565F89",
        "neutral_variant_paletteKeyColorColor": "#414868",
        "onBackgroundColor": "#C0CAF5",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#001A41",
        "onPrimaryContainerColor": "#D6E3FF",
        "onPrimaryFixedColor": "#001A41",
        "onPrimaryFixedVariantColor": "#003C7E",
        "onSecondaryColor": "#002133",
        "onSecondaryContainerColor": "#BDE9FF",
        "onSecondaryFixedColor": "#001E2E",
        "onSecondaryFixedVariantColor": "#004863",
        "onSurfaceColor": "#C0CAF5",
        "onSurfaceLightColor": "#A9B1D6",
        "onSurfaceVariantColor": "#787C99",
        "onTertiaryColor": "#00261A",
        "onTertiaryContainerColor": "#B3F5DC",
        "onTertiaryFixedColor": "#001A12",
        "onTertiaryFixedVariantColor": "#004D39",
        "outlineColor": "#565F89",
        "outlineVariantColor": "#2C3047",
        "primaryColor": "#7AA2F7",
        "primaryContainerColor": "#003C7E",
        "primaryFixedColor": "#D6E3FF",
        "primaryFixedDimColor": "#A9C7FF",
        "primary_paletteKeyColorColor": "#7AA2F7",
        "rippleColor": "#7AA2F733",
        "scrimColor": "#000000",
        "secondaryColor": "#7DCFFF",
        "secondaryContainerColor": "#004863",
        "secondaryFixedColor": "#BDE9FF",
        "secondaryFixedDimColor": "#5AC5F7",
        "secondary_paletteKeyColorColor": "#7DCFFF",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#2F3549",
        "surfaceColor": "#1A1B26",
        "surfaceContainerColor": "#16161E",
        "surfaceContainerHighColor": "#24283B",
        "surfaceContainerHighestColor": "#32344A",
        "surfaceContainerLowColor": "#13131A",
        "surfaceContainerLowestColor": "#0F0F14",
        "surfaceDimColor": "#13141F",
        "surfaceTintColor": "#7AA2F7",
        "surfaceVariantColor": "#24283B",
        "tertiaryColor": "#73DACA",
        "tertiaryContainerColor": "#004D39",
        "tertiaryFixedColor": "#B3F5DC",
        "tertiaryFixedDimColor": "#4FD9B8",
        "tertiary_paletteKeyColorColor": "#73DACA",
        "transparentColor": "#00000000"
    },

    "monokai_pro": {
        "backgroundColor": "#2D2A2E",
        "disabledTextColor": "#727072",
        "errorColor": "#FF6188",
        "errorContainerColor": "#5C0F21",
        "inverseOnSurfaceColor": "#39363A",
        "inversePrimaryColor": "#A9DC76",
        "inverseSurfaceColor": "#FCFCFA",
        "neutral_paletteKeyColorColor": "#727072",
        "neutral_variant_paletteKeyColorColor": "#5B595C",
        "onBackgroundColor": "#FCFCFA",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#0E2000",
        "onPrimaryContainerColor": "#C7F5A3",
        "onPrimaryFixedColor": "#0E2000",
        "onPrimaryFixedVariantColor": "#1F4100",
        "onSecondaryColor": "#001D36",
        "onSecondaryContainerColor": "#C3E7FF",
        "onSecondaryFixedColor": "#001D36",
        "onSecondaryFixedVariantColor": "#00426D",
        "onSurfaceColor": "#FCFCFA",
        "onSurfaceLightColor": "#E6E6E3",
        "onSurfaceVariantColor": "#C1BFC4",
        "onTertiaryColor": "#2B0048",
        "onTertiaryContainerColor": "#EFD6FF",
        "onTertiaryFixedColor": "#2B0048",
        "onTertiaryFixedVariantColor": "#5A0097",
        "outlineColor": "#939094",
        "outlineVariantColor": "#403E41",
        "primaryColor": "#A9DC76",
        "primaryContainerColor": "#1F4100",
        "primaryFixedColor": "#C7F5A3",
        "primaryFixedDimColor": "#AFE37C",
        "primary_paletteKeyColorColor": "#A9DC76",
        "rippleColor": "#A9DC7633",
        "scrimColor": "#000000",
        "secondaryColor": "#78DCE8",
        "secondaryContainerColor": "#00426D",
        "secondaryFixedColor": "#C3E7FF",
        "secondaryFixedDimColor": "#5AC4DE",
        "secondary_paletteKeyColorColor": "#78DCE8",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#423F43",
        "surfaceColor": "#2D2A2E",
        "surfaceContainerColor": "#221F22",
        "surfaceContainerHighColor": "#39363A",
        "surfaceContainerHighestColor": "#49464A",
        "surfaceContainerLowColor": "#1E1B1E",
        "surfaceContainerLowestColor": "#19171A",
        "surfaceDimColor": "#221F22",
        "surfaceTintColor": "#A9DC76",
        "surfaceVariantColor": "#39363A",
        "tertiaryColor": "#AB9DF2",
        "tertiaryContainerColor": "#5A0097",
        "tertiaryFixedColor": "#EFD6FF",
        "tertiaryFixedDimColor": "#D5BAFF",
        "tertiary_paletteKeyColorColor": "#AB9DF2",
        "transparentColor": "#00000000"
    },

    "one_dark": {
        "backgroundColor": "#282C34",
        "disabledTextColor": "#5C6370",
        "errorColor": "#E06C75",
        "errorContainerColor": "#5C1018",
        "inverseOnSurfaceColor": "#2C323C",
        "inversePrimaryColor": "#61AFEF",
        "inverseSurfaceColor": "#ABB2BF",
        "neutral_paletteKeyColorColor": "#5C6370",
        "neutral_variant_paletteKeyColorColor": "#4B5263",
        "onBackgroundColor": "#ABB2BF",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DA",
        "onPrimaryColor": "#001D35",
        "onPrimaryContainerColor": "#D1E4FF",
        "onPrimaryFixedColor": "#001D35",
        "onPrimaryFixedVariantColor": "#003E78",
        "onSecondaryColor": "#001B3D",
        "onSecondaryContainerColor": "#D1E4FF",
        "onSecondaryFixedColor": "#001938",
        "onSecondaryFixedVariantColor": "#003A6F",
        "onSurfaceColor": "#ABB2BF",
        "onSurfaceLightColor": "#9DA5B4",
        "onSurfaceVariantColor": "#828997",
        "onTertiaryColor": "#002114",
        "onTertiaryContainerColor": "#B3F5D7",
        "onTertiaryFixedColor": "#001A12",
        "onTertiaryFixedVariantColor": "#00492F",
        "outlineColor": "#6B7280",
        "outlineVariantColor": "#3E4451",
        "primaryColor": "#61AFEF",
        "primaryContainerColor": "#003E78",
        "primaryFixedColor": "#D1E4FF",
        "primaryFixedDimColor": "#9CC7F5",
        "primary_paletteKeyColorColor": "#61AFEF",
        "rippleColor": "#61AFEF33",
        "scrimColor": "#000000",
        "secondaryColor": "#56B6C2",
        "secondaryContainerColor": "#003A6F",
        "secondaryFixedColor": "#D1E4FF",
        "secondaryFixedDimColor": "#68D4E0",
        "secondary_paletteKeyColorColor": "#56B6C2",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#3A3F4B",
        "surfaceColor": "#282C34",
        "surfaceContainerColor": "#21252B",
        "surfaceContainerHighColor": "#2C313A",
        "surfaceContainerHighestColor": "#3A3F4B",
        "surfaceContainerLowColor": "#1C1F26",
        "surfaceContainerLowestColor": "#181A1F",
        "surfaceDimColor": "#21252B",
        "surfaceTintColor": "#61AFEF",
        "surfaceVariantColor": "#2C313A",
        "tertiaryColor": "#98C379",
        "tertiaryContainerColor": "#00492F",
        "tertiaryFixedColor": "#B3F5D7",
        "tertiaryFixedDimColor": "#7DE5A8",
        "tertiary_paletteKeyColorColor": "#98C379",
        "transparentColor": "#00000000"
    },

    "github_light": {
        "backgroundColor": "#FFFFFF",
        "disabledTextColor": "#8B949E",
        "errorColor": "#CF222E",
        "errorContainerColor": "#FFEBE9",
        "inverseOnSurfaceColor": "#F6F8FA",
        "inversePrimaryColor": "#58A6FF",
        "inverseSurfaceColor": "#24292F",
        "neutral_paletteKeyColorColor": "#656D76",
        "neutral_variant_paletteKeyColorColor": "#57606A",
        "onBackgroundColor": "#24292F",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0F1A",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D3A",
        "onPrimaryFixedColor": "#001D3A",
        "onPrimaryFixedVariantColor": "#003D73",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#001D2C",
        "onSecondaryFixedColor": "#001D2C",
        "onSecondaryFixedVariantColor": "#00415A",
        "onSurfaceColor": "#24292F",
        "onSurfaceLightColor": "#57606A",
        "onSurfaceVariantColor": "#656D76",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#002112",
        "onTertiaryFixedColor": "#002112",
        "onTertiaryFixedVariantColor": "#00472F",
        "outlineColor": "#8B949E",
        "outlineVariantColor": "#D0D7DE",
        "primaryColor": "#0969DA",
        "primaryContainerColor": "#D8E7FF",
        "primaryFixedColor": "#E7F0FF",
        "primaryFixedDimColor": "#B8D4FF",
        "primary_paletteKeyColorColor": "#0969DA",
        "rippleColor": "#0969DA33",
        "scrimColor": "#000000",
        "secondaryColor": "#218BFF",
        "secondaryContainerColor": "#CEE9FF",
        "secondaryFixedColor": "#E0F2FF",
        "secondaryFixedDimColor": "#A4D8FF",
        "secondary_paletteKeyColorColor": "#218BFF",
        "shadowColor": "#00000020",
        "surfaceBrightColor": "#FFFFFF",
        "surfaceColor": "#FFFFFF",
        "surfaceContainerColor": "#F6F8FA",
        "surfaceContainerHighColor": "#EAEEF2",
        "surfaceContainerHighestColor": "#D0D7DE",
        "surfaceContainerLowColor": "#F9FAFB",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#F6F8FA",
        "surfaceTintColor": "#0969DA",
        "surfaceVariantColor": "#EAEEF2",
        "tertiaryColor": "#1A7F37",
        "tertiaryContainerColor": "#DAFBE1",
        "tertiaryFixedColor": "#E7FEE9",
        "tertiaryFixedDimColor": "#B4F1B8",
        "tertiary_paletteKeyColorColor": "#1A7F37",
        "transparentColor": "#00000000"
    },

    "classic_light": {
        "backgroundColor": "#FAFAFA",
        "disabledTextColor": "#9E9E9E",
        "errorColor": "#B00020",
        "errorContainerColor": "#F9DEDC",
        "inverseOnSurfaceColor": "#F5F5F5",
        "inversePrimaryColor": "#90CAF9",
        "inverseSurfaceColor": "#212121",
        "neutral_paletteKeyColorColor": "#757575",
        "neutral_variant_paletteKeyColorColor": "#616161",
        "onBackgroundColor": "#1A1A1A",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#410002",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D36",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#004A77",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1A1A1A",
        "onSecondaryFixedColor": "#0A1929",
        "onSecondaryFixedVariantColor": "#455A64",
        "onSurfaceColor": "#1A1A1A",
        "onSurfaceLightColor": "#424242",
        "onSurfaceVariantColor": "#424242",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1A1A1A",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#757575",
        "outlineVariantColor": "#C2C2C2",
        "primaryColor": "#1976D2",
        "primaryContainerColor": "#BBDEFB",
        "primaryFixedColor": "#D6E9FF",
        "primaryFixedDimColor": "#90CAF9",
        "primary_paletteKeyColorColor": "#1976D2",
        "rippleColor": "#1976D233",
        "scrimColor": "#000000",
        "secondaryColor": "#546E7A",
        "secondaryContainerColor": "#CFE8FC",
        "secondaryFixedColor": "#D1E8FF",
        "secondaryFixedDimColor": "#B0BEC5",
        "secondary_paletteKeyColorColor": "#81A1C1",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#ECEFF4",
        "surfaceColor": "#ECEFF4",
        "surfaceContainerColor": "#E5E9F0",
        "surfaceContainerHighColor": "#D8DEE9",
        "surfaceContainerHighestColor": "#D0D7E3",
        "surfaceContainerLowColor": "#E9EDF3",
        "surfaceContainerLowestColor": "#F5F7FA",
        "surfaceDimColor": "#E0E5EB",
        "surfaceTintColor": "#5E81AC",
        "surfaceVariantColor": "#D8DEE9",
        "tertiaryColor": "#88C0D0",
        "tertiaryContainerColor": "#E5F0F3",
        "tertiaryFixedColor": "#EDF5F7",
        "tertiaryFixedDimColor": "#C8E2E8",
        "tertiary_paletteKeyColorColor": "#8FBCBB",
        "transparentColor": "#00000000"
    },

    "gruvbox_light": {
        "backgroundColor": "#FBF1C7",
        "disabledTextColor": "#A89984",
        "errorColor": "#CC241D",
        "errorContainerColor": "#F9D7D5",
        "inverseOnSurfaceColor": "#F9F5D7",
        "inversePrimaryColor": "#458588",
        "inverseSurfaceColor": "#282828",
        "neutral_paletteKeyColorColor": "#7C6F64",
        "neutral_variant_paletteKeyColorColor": "#665C54",
        "onBackgroundColor": "#282828",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#3C0A00",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001E2B",
        "onPrimaryFixedColor": "#001E2B",
        "onPrimaryFixedVariantColor": "#003F58",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1F2B00",
        "onSecondaryFixedColor": "#1F2B00",
        "onSecondaryFixedVariantColor": "#3F5700",
        "onSurfaceColor": "#282828",
        "onSurfaceLightColor": "#3C3836",
        "onSurfaceVariantColor": "#504945",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#2D1700",
        "onTertiaryFixedColor": "#2D1700",
        "onTertiaryFixedVariantColor": "#5A3800",
        "outlineColor": "#928374",
        "outlineVariantColor": "#EBDBB2",
        "primaryColor": "#458588",
        "primaryContainerColor": "#D5E4E8",
        "primaryFixedColor": "#E3EFF2",
        "primaryFixedDimColor": "#BDD6DC",
        "primary_paletteKeyColorColor": "#458588",
        "rippleColor": "#45858833",
        "scrimColor": "#000000",
        "secondaryColor": "#98971A",
        "secondaryContainerColor": "#E8E5C8",
        "secondaryFixedColor": "#F2EFCC",
        "secondaryFixedDimColor": "#D9D6A3",
        "secondary_paletteKeyColorColor": "#98971A",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#FBF1C7",
        "surfaceColor": "#FBF1C7",
        "surfaceContainerColor": "#F2E5BC",
        "surfaceContainerHighColor": "#EBDBB2",
        "surfaceContainerHighestColor": "#E0CFA1",
        "surfaceContainerLowColor": "#F9F5D7",
        "surfaceContainerLowestColor": "#FFFBDD",
        "surfaceDimColor": "#F2E5BC",
        "surfaceTintColor": "#458588",
        "surfaceVariantColor": "#EBDBB2",
        "tertiaryColor": "#D65D0E",
        "tertiaryContainerColor": "#FADEC9",
        "tertiaryFixedColor": "#FFE9D5",
        "tertiaryFixedDimColor": "#F4D0A3",
        "tertiary_paletteKeyColorColor": "#D65D0E",
        "transparentColor": "#00000000"
    },

    "catppuccin_latte": {
        "backgroundColor": "#EFF1F5",
        "disabledTextColor": "#9CA0B0",
        "errorColor": "#D20F39",
        "errorContainerColor": "#F4DBE0",
        "inverseOnSurfaceColor": "#E6E9EF",
        "inversePrimaryColor": "#7287FD",
        "inverseSurfaceColor": "#1E1E2E",
        "neutral_paletteKeyColorColor": "#6C6F85",
        "neutral_variant_paletteKeyColorColor": "#5C5F77",
        "onBackgroundColor": "#1E1E2E",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#410002",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001847",
        "onPrimaryFixedColor": "#001847",
        "onPrimaryFixedVariantColor": "#003976",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#001B3D",
        "onSecondaryFixedColor": "#001B3D",
        "onSecondaryFixedVariantColor": "#00396E",
        "onSurfaceColor": "#1E1E2E",
        "onSurfaceLightColor": "#4C4F69",
        "onSurfaceVariantColor": "#5C5F77",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#1F1A3C",
        "onTertiaryFixedColor": "#1F1A3C",
        "onTertiaryFixedVariantColor": "#3E3660",
        "outlineColor": "#7C7F93",
        "outlineVariantColor": "#CCD0DA",
        "primaryColor": "#1E66F5",
        "primaryContainerColor": "#D4E1FF",
        "primaryFixedColor": "#E0EBFF",
        "primaryFixedDimColor": "#ADC6FF",
        "primary_paletteKeyColorColor": "#1E66F5",
        "rippleColor": "#1E66F533",
        "scrimColor": "#000000",
        "secondaryColor": "#04A5E5",
        "secondaryContainerColor": "#CEE9F7",
        "secondaryFixedColor": "#E0F3FF",
        "secondaryFixedDimColor": "#A6D8F0",
        "secondary_paletteKeyColorColor": "#04A5E5",
        "shadowColor": "#00000033",
        "surfaceBrightColor": "#EFF1F5",
        "surfaceColor": "#EFF1F5",
        "surfaceContainerColor": "#E6E9EF",
        "surfaceContainerHighColor": "#DCE0E8",
        "surfaceContainerHighestColor": "#CCD0DA",
        "surfaceContainerLowColor": "#E9ECF0",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#DFE1E8",
        "surfaceTintColor": "#1E66F5",
        "surfaceVariantColor": "#DCE0E8",
        "tertiaryColor": "#8839EF",
        "tertiaryContainerColor": "#E8DBFF",
        "tertiaryFixedColor": "#F2E7FF",
        "tertiaryFixedDimColor": "#D5BAFF",
        "tertiary_paletteKeyColorColor": "#8839EF",
        "transparentColor": "#00000000"
    },

    "dracula": {
        "backgroundColor": "#282A36",
        "disabledTextColor": "#6272A4",
        "errorColor": "#FF5555",
        "errorContainerColor": "#5C0F13",
        "inverseOnSurfaceColor": "#2E3142",
        "inversePrimaryColor": "#BD93F9",
        "inverseSurfaceColor": "#F8F8F2",
        "neutral_paletteKeyColorColor": "#6272A4",
        "neutral_variant_paletteKeyColorColor": "#44475A",
        "onBackgroundColor": "#F8F8F2",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6D9",
        "onPrimaryColor": "#2B0048",
        "onPrimaryContainerColor": "#EEDDFF",
        "onPrimaryFixedColor": "#2B0048",
        "onPrimaryFixedVariantColor": "#5A0097",
        "onSecondaryColor": "#002B3D",
        "onSecondaryContainerColor": "#C9F0FF",
        "onSecondaryFixedColor": "#001F2A",
        "onSecondaryFixedVariantColor": "#004F6A",
        "onSurfaceColor": "#F8F8F2",
        "onSurfaceLightColor": "#E8E8E0",
        "onSurfaceVariantColor": "#C2C4D4",
        "onTertiaryColor": "#00381F",
        "onTertiaryContainerColor": "#BFFFD9",
        "onTertiaryFixedColor": "#002112",
        "onTertiaryFixedVariantColor": "#00533A",
        "outlineColor": "#6272A4",
        "outlineVariantColor": "#44475A",
        "primaryColor": "#BD93F9",
        "primaryContainerColor": "#5A0097",
        "primaryFixedColor": "#EEDDFF",
        "primaryFixedDimColor": "#D5BAFF",
        "primary_paletteKeyColorColor": "#BD93F9",
        "rippleColor": "#BD93F933",
        "scrimColor": "#000000",
        "secondaryColor": "#8BE9FD",
        "secondaryContainerColor": "#004F6A",
        "secondaryFixedColor": "#C9F0FF",
        "secondaryFixedDimColor": "#5DD4F0",
        "secondary_paletteKeyColorColor": "#8BE9FD",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#383A4A",
        "surfaceColor": "#282A36",
        "surfaceContainerColor": "#21222C",
        "surfaceContainerHighColor": "#2F3241",
        "surfaceContainerHighestColor": "#3A3C4C",
        "surfaceContainerLowColor": "#1E1F29",
        "surfaceContainerLowestColor": "#191A21",
        "surfaceDimColor": "#21222C",
        "surfaceTintColor": "#BD93F9",
        "surfaceVariantColor": "#2F3241",
        "tertiaryColor": "#50FA7B",
        "tertiaryContainerColor": "#00533A",
        "tertiaryFixedColor": "#BFFFD9",
        "tertiaryFixedDimColor": "#34E89E",
        "tertiary_paletteKeyColorColor": "#50FA7B",
        "transparentColor": "#00000000"
    },

    "tokyo_night": {
        "backgroundColor": "#1A1B26",
        "disabledTextColor": "#565F89",
        "errorColor": "#F7768E",
        "errorContainerColor": "#5C0F1E",
        "inverseOnSurfaceColor": "#24283B",
        "inversePrimaryColor": "#7AA2F7",
        "inverseSurfaceColor": "#D5D6DB",
        "neutral_paletteKeyColorColor": "#565F89",
        "neutral_variant_paletteKeyColorColor": "#414868",
        "onBackgroundColor": "#C0CAF5",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#001A41",
        "onPrimaryContainerColor": "#D6E3FF",
        "onPrimaryFixedColor": "#001A41",
        "onPrimaryFixedVariantColor": "#003C7E",
        "onSecondaryColor": "#002133",
        "onSecondaryContainerColor": "#BDE9FF",
        "onSecondaryFixedColor": "#001E2E",
        "onSecondaryFixedVariantColor": "#004863",
        "onSurfaceColor": "#C0CAF5",
        "onSurfaceLightColor": "#A9B1D6",
        "onSurfaceVariantColor": "#787C99",
        "onTertiaryColor": "#00261A",
        "onTertiaryContainerColor": "#B3F5DC",
        "onTertiaryFixedColor": "#001A12",
        "onTertiaryFixedVariantColor": "#004D39",
        "outlineColor": "#565F89",
        "outlineVariantColor": "#2C3047",
        "primaryColor": "#7AA2F7",
        "primaryContainerColor": "#003C7E",
        "primaryFixedColor": "#D6E3FF",
        "primaryFixedDimColor": "#A9C7FF",
        "primary_paletteKeyColorColor": "#7AA2F7",
        "rippleColor": "#7AA2F733",
        "scrimColor": "#000000",
        "secondaryColor": "#7DCFFF",
        "secondaryContainerColor": "#004863",
        "secondaryFixedColor": "#BDE9FF",
        "secondaryFixedDimColor": "#5AC5F7",
        "secondary_paletteKeyColorColor": "#7DCFFF",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#2F3549",
        "surfaceColor": "#1A1B26",
        "surfaceContainerColor": "#16161E",
        "surfaceContainerHighColor": "#24283B",
        "surfaceContainerHighestColor": "#32344A",
        "surfaceContainerLowColor": "#13131A",
        "surfaceContainerLowestColor": "#0F0F14",
        "surfaceDimColor": "#13141F",
        "surfaceTintColor": "#7AA2F7",
        "surfaceVariantColor": "#24283B",
        "tertiaryColor": "#73DACA",
        "tertiaryContainerColor": "#004D39",
        "tertiaryFixedColor": "#B3F5DC",
        "tertiaryFixedDimColor": "#4FD9B8",
        "tertiary_paletteKeyColorColor": "#73DACA",
        "transparentColor": "#00000000"
    },

    "monokai_pro": {
        "backgroundColor": "#2D2A2E",
        "disabledTextColor": "#727072",
        "errorColor": "#FF6188",
        "errorContainerColor": "#5C0F21",
        "inverseOnSurfaceColor": "#39363A",
        "inversePrimaryColor": "#A9DC76",
        "inverseSurfaceColor": "#FCFCFA",
        "neutral_paletteKeyColorColor": "#727072",
        "neutral_variant_paletteKeyColorColor": "#5B595C",
        "onBackgroundColor": "#FCFCFA",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#0E2000",
        "onPrimaryContainerColor": "#C7F5A3",
        "onPrimaryFixedColor": "#0E2000",
        "onPrimaryFixedVariantColor": "#1F4100",
        "onSecondaryColor": "#001D36",
        "onSecondaryContainerColor": "#C3E7FF",
        "onSecondaryFixedColor": "#001D36",
        "onSecondaryFixedVariantColor": "#00426D",
        "onSurfaceColor": "#FCFCFA",
        "onSurfaceLightColor": "#E6E6E3",
        "onSurfaceVariantColor": "#C1BFC4",
        "onTertiaryColor": "#2B0048",
        "onTertiaryContainerColor": "#EFD6FF",
        "onTertiaryFixedColor": "#2B0048",
        "onTertiaryFixedVariantColor": "#5A0097",
        "outlineColor": "#939094",
        "outlineVariantColor": "#403E41",
        "primaryColor": "#A9DC76",
        "primaryContainerColor": "#1F4100",
        "primaryFixedColor": "#C7F5A3",
        "primaryFixedDimColor": "#AFE37C",
        "primary_paletteKeyColorColor": "#A9DC76",
        "rippleColor": "#A9DC7633",
        "scrimColor": "#000000",
        "secondaryColor": "#78DCE8",
        "secondaryContainerColor": "#00426D",
        "secondaryFixedColor": "#C3E7FF",
        "secondaryFixedDimColor": "#5AC4DE",
        "secondary_paletteKeyColorColor": "#78DCE8",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#423F43",
        "surfaceColor": "#2D2A2E",
        "surfaceContainerColor": "#221F22",
        "surfaceContainerHighColor": "#39363A",
        "surfaceContainerHighestColor": "#49464A",
        "surfaceContainerLowColor": "#1E1B1E",
        "surfaceContainerLowestColor": "#19171A",
        "surfaceDimColor": "#221F22",
        "surfaceTintColor": "#A9DC76",
        "surfaceVariantColor": "#39363A",
        "tertiaryColor": "#AB9DF2",
        "tertiaryContainerColor": "#5A0097",
        "tertiaryFixedColor": "#EFD6FF",
        "tertiaryFixedDimColor": "#D5BAFF",
        "tertiary_paletteKeyColorColor": "#AB9DF2",
        "transparentColor": "#00000000"
    },

    "one_dark": {
        "backgroundColor": "#282C34",
        "disabledTextColor": "#5C6370",
        "errorColor": "#E06C75",
        "errorContainerColor": "#5C1018",
        "inverseOnSurfaceColor": "#2C323C",
        "inversePrimaryColor": "#61AFEF",
        "inverseSurfaceColor": "#ABB2BF",
        "neutral_paletteKeyColorColor": "#5C6370",
        "neutral_variant_paletteKeyColorColor": "#4B5263",
        "onBackgroundColor": "#ABB2BF",
        "onErrorColor": "#2B0000",
        "onErrorContainerColor": "#FFD6DA",
        "onPrimaryColor": "#001D35",
        "onPrimaryContainerColor": "#D1E4FF",
        "onPrimaryFixedColor": "#001D35",
        "onPrimaryFixedVariantColor": "#003E78",
        "onSecondaryColor": "#001B3D",
        "onSecondaryContainerColor": "#D1E4FF",
        "onSecondaryFixedColor": "#001938",
        "onSecondaryFixedVariantColor": "#003A6F",
        "onSurfaceColor": "#ABB2BF",
        "onSurfaceLightColor": "#9DA5B4",
        "onSurfaceVariantColor": "#828997",
        "onTertiaryColor": "#002114",
        "onTertiaryContainerColor": "#B3F5D7",
        "onTertiaryFixedColor": "#001A12",
        "onTertiaryFixedVariantColor": "#00492F",
        "outlineColor": "#6B7280",
        "outlineVariantColor": "#3E4451",
        "primaryColor": "#61AFEF",
        "primaryContainerColor": "#003E78",
        "primaryFixedColor": "#D1E4FF",
        "primaryFixedDimColor": "#9CC7F5",
        "primary_paletteKeyColorColor": "#61AFEF",
        "rippleColor": "#61AFEF33",
        "scrimColor": "#000000",
        "secondaryColor": "#56B6C2",
        "secondaryContainerColor": "#003A6F",
        "secondaryFixedColor": "#D1E4FF",
        "secondaryFixedDimColor": "#68D4E0",
        "secondary_paletteKeyColorColor": "#56B6C2",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#3A3F4B",
        "surfaceColor": "#282C34",
        "surfaceContainerColor": "#21252B",
        "surfaceContainerHighColor": "#2C313A",
        "surfaceContainerHighestColor": "#3A3F4B",
        "surfaceContainerLowColor": "#1C1F26",
        "surfaceContainerLowestColor": "#181A1F",
        "surfaceDimColor": "#21252B",
        "surfaceTintColor": "#61AFEF",
        "surfaceVariantColor": "#2C313A",
        "tertiaryColor": "#98C379",
        "tertiaryContainerColor": "#00492F",
        "tertiaryFixedColor": "#B3F5D7",
        "tertiaryFixedDimColor": "#7DE5A8",
        "tertiary_paletteKeyColorColor": "#98C379",
        "transparentColor": "#00000000"
    },

    "material_design": {
        "backgroundColor": "#FAFAFA",
        "disabledTextColor": "#9E9E9E",
        "errorColor": "#B00020",
        "errorContainerColor": "#F9DEDC",
        "inverseOnSurfaceColor": "#F5F5F5",
        "inversePrimaryColor": "#BB86FC",
        "inverseSurfaceColor": "#121212",
        "neutral_paletteKeyColorColor": "#757575",
        "neutral_variant_paletteKeyColorColor": "#616161",
        "onBackgroundColor": "#212121",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#410002",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#21005D",
        "onPrimaryFixedColor": "#21005D",
        "onPrimaryFixedVariantColor": "#4F378B",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1D192B",
        "onSecondaryFixedColor": "#1D192B",
        "onSecondaryFixedVariantColor": "#4A4458",
        "onSurfaceColor": "#212121",
        "onSurfaceLightColor": "#424242",
        "onSurfaceVariantColor": "#49454F",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#31111D",
        "onTertiaryFixedColor": "#31111D",
        "onTertiaryFixedVariantColor": "#633B48",
        "outlineColor": "#79747E",
        "outlineVariantColor": "#CAC4D0",
        "primaryColor": "#6750A4",
        "primaryContainerColor": "#EADDFF",
        "primaryFixedColor": "#EADDFF",
        "primaryFixedDimColor": "#D0BCFF",
        "primary_paletteKeyColorColor": "#6750A4",
        "rippleColor": "#6750A433",
        "scrimColor": "#000000",
        "secondaryColor": "#625B71",
        "secondaryContainerColor": "#E8DEF8",
        "secondaryFixedColor": "#E8DEF8",
        "secondaryFixedDimColor": "#CCC2DC",
        "secondary_paletteKeyColorColor": "#625B71",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#FAFAFA",
        "surfaceColor": "#FFFBFE",
        "surfaceContainerColor": "#F3EDF7",
        "surfaceContainerHighColor": "#ECE6F0",
        "surfaceContainerHighestColor": "#E6E0E9",
        "surfaceContainerLowColor": "#F7F2FA",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#DED8E1",
        "surfaceTintColor": "#6750A4",
        "surfaceVariantColor": "#E7E0EC",
        "tertiaryColor": "#7D5260",
        "tertiaryContainerColor": "#FFD8E4",
        "tertiaryFixedColor": "#FFD8E4",
        "tertiaryFixedDimColor": "#EFB8C8",
        "tertiary_paletteKeyColorColor": "#7D5260",
        "transparentColor": "#00000000"
    },

    "material_dark": {
        "backgroundColor": "#121212",
        "disabledTextColor": "#666666",
        "errorColor": "#CF6679",
        "errorContainerColor": "#93000A",
        "inverseOnSurfaceColor": "#1C1B1F",
        "inversePrimaryColor": "#6750A4",
        "inverseSurfaceColor": "#E6E1E5",
        "neutral_paletteKeyColorColor": "#8E8E8E",
        "neutral_variant_paletteKeyColorColor": "#A1A1A1",
        "onBackgroundColor": "#E6E1E5",
        "onErrorColor": "#690005",
        "onErrorContainerColor": "#FFDAD6",
        "onPrimaryColor": "#381E72",
        "onPrimaryContainerColor": "#EADDFF",
        "onPrimaryFixedColor": "#21005D",
        "onPrimaryFixedVariantColor": "#4F378B",
        "onSecondaryColor": "#332D41",
        "onSecondaryContainerColor": "#E8DEF8",
        "onSecondaryFixedColor": "#1D192B",
        "onSecondaryFixedVariantColor": "#4A4458",
        "onSurfaceColor": "#E6E1E5",
        "onSurfaceLightColor": "#CAC4D0",
        "onSurfaceVariantColor": "#CAC4D0",
        "onTertiaryColor": "#492532",
        "onTertiaryContainerColor": "#FFD8E4",
        "onTertiaryFixedColor": "#31111D",
        "onTertiaryFixedVariantColor": "#633B48",
        "outlineColor": "#938F99",
        "outlineVariantColor": "#49454F",
        "primaryColor": "#D0BCFF",
        "primaryContainerColor": "#4F378B",
        "primaryFixedColor": "#EADDFF",
        "primaryFixedDimColor": "#D0BCFF",
        "primary_paletteKeyColorColor": "#D0BCFF",
        "rippleColor": "#D0BCFF33",
        "scrimColor": "#000000",
        "secondaryColor": "#CCC2DC",
        "secondaryContainerColor": "#4A4458",
        "secondaryFixedColor": "#E8DEF8",
        "secondaryFixedDimColor": "#CCC2DC",
        "secondary_paletteKeyColorColor": "#CCC2DC",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#3B383E",
        "surfaceColor": "#1C1B1F",
        "surfaceContainerColor": "#211F26",
        "surfaceContainerHighColor": "#2B2930",
        "surfaceContainerHighestColor": "#36343B",
        "surfaceContainerLowColor": "#1C1B1F",
        "surfaceContainerLowestColor": "#0F0D13",
        "surfaceDimColor": "#141218",
        "surfaceTintColor": "#D0BCFF",
        "surfaceVariantColor": "#49454F",
        "tertiaryColor": "#EFB8C8",
        "tertiaryContainerColor": "#633B48",
        "tertiaryFixedColor": "#FFD8E4",
        "tertiaryFixedDimColor": "#EFB8C8",
        "tertiary_paletteKeyColorColor": "#EFB8C8",
        "transparentColor": "#00000000"
    },

    "nord_dark": {
        "backgroundColor": "#2E3440",
        "disabledTextColor": "#4C566A",
        "errorColor": "#BF616A",
        "errorContainerColor": "#5C0F1A",
        "inverseOnSurfaceColor": "#3B4252",
        "inversePrimaryColor": "#5E81AC",
        "inverseSurfaceColor": "#ECEFF4",
        "neutral_paletteKeyColorColor": "#4C566A",
        "neutral_variant_paletteKeyColorColor": "#434C5E",
        "onBackgroundColor": "#ECEFF4",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#002033",
        "onPrimaryContainerColor": "#D8DEE9",
        "onPrimaryFixedColor": "#001F29",
        "onPrimaryFixedVariantColor": "#00455E",
        "onSecondaryColor": "#00232F",
        "onSecondaryContainerColor": "#C9E5F5",
        "onSecondaryFixedColor": "#001E28",
        "onSecondaryFixedVariantColor": "#004154",
        "onSurfaceColor": "#ECEFF4",
        "onSurfaceLightColor": "#D8DEE9",
        "onSurfaceVariantColor": "#C1C9D2",
        "onTertiaryColor": "#1A2E38",
        "onTertiaryContainerColor": "#D4E5EC",
        "onTertiaryFixedColor": "#1F2B38",
        "onTertiaryFixedVariantColor": "#37475A",
        "outlineColor": "#8FBCBB",
        "outlineVariantColor": "#4C566A",
        "primaryColor": "#88C0D0",
        "primaryContainerColor": "#00455E",
        "primaryFixedColor": "#D8DEE9",
        "primaryFixedDimColor": "#A3D4E5",
        "primary_paletteKeyColorColor": "#88C0D0",
        "rippleColor": "#88C0D033",
        "scrimColor": "#000000",
        "secondaryColor": "#81A1C1",
        "secondaryContainerColor": "#004154",
        "secondaryFixedColor": "#C9E5F5",
        "secondaryFixedDimColor": "#99C5DC",
        "secondary_paletteKeyColorColor": "#81A1C1",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#434C5E",
        "surfaceColor": "#2E3440",
        "surfaceContainerColor": "#242933",
        "surfaceContainerHighColor": "#3B4252",
        "surfaceContainerHighestColor": "#4C566A",
        "surfaceContainerLowColor": "#1F232C",
        "surfaceContainerLowestColor": "#191C24",
        "surfaceDimColor": "#242933",
        "surfaceTintColor": "#88C0D0",
        "surfaceVariantColor": "#3B4252",
        "tertiaryColor": "#8FBCBB",
        "tertiaryContainerColor": "#37475A",
        "tertiaryFixedColor": "#D4E5EC",
        "tertiaryFixedDimColor": "#B0D4D3",
        "tertiary_paletteKeyColorColor": "#8FBCBB",
        "transparentColor": "#00000000"
    },

    "gruvbox_dark": {
        "backgroundColor": "#282828",
        "disabledTextColor": "#665C54",
        "errorColor": "#FB4934",
        "errorContainerColor": "#5C0F1A",
        "inverseOnSurfaceColor": "#3C3836",
        "inversePrimaryColor": "#458588",
        "inverseSurfaceColor": "#EBDBB2",
        "neutral_paletteKeyColorColor": "#7C6F64",
        "neutral_variant_paletteKeyColorColor": "#665C54",
        "onBackgroundColor": "#EBDBB2",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#001E2B",
        "onPrimaryContainerColor": "#D5E4E8",
        "onPrimaryFixedColor": "#001E2B",
        "onPrimaryFixedVariantColor": "#003F58",
        "onSecondaryColor": "#1F2B00",
        "onSecondaryContainerColor": "#E8E5C8",
        "onSecondaryFixedColor": "#1F2B00",
        "onSecondaryFixedVariantColor": "#3F5700",
        "onSurfaceColor": "#EBDBB2",
        "onSurfaceLightColor": "#D5C4A1",
        "onSurfaceVariantColor": "#BDAE93",
        "onTertiaryColor": "#2D1700",
        "onTertiaryContainerColor": "#FADEC9",
        "onTertiaryFixedColor": "#2D1700",
        "onTertiaryFixedVariantColor": "#5A3800",
        "outlineColor": "#928374",
        "outlineVariantColor": "#504945",
        "primaryColor": "#83A598",
        "primaryContainerColor": "#003F58",
        "primaryFixedColor": "#D5E4E8",
        "primaryFixedDimColor": "#A8C7D0",
        "primary_paletteKeyColorColor": "#83A598",
        "rippleColor": "#83A59833",
        "scrimColor": "#000000",
        "secondaryColor": "#B8BB26",
        "secondaryContainerColor": "#3F5700",
        "secondaryFixedColor": "#E8E5C8",
        "secondaryFixedDimColor": "#CCD48A",
        "secondary_paletteKeyColorColor": "#B8BB26",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#504945",
        "surfaceColor": "#282828",
        "surfaceContainerColor": "#1D2021",
        "surfaceContainerHighColor": "#3C3836",
        "surfaceContainerHighestColor": "#504945",
        "surfaceContainerLowColor": "#1D2021",
        "surfaceContainerLowestColor": "#1B1B1B",
        "surfaceDimColor": "#1D2021",
        "surfaceTintColor": "#83A598",
        "surfaceVariantColor": "#3C3836",
        "tertiaryColor": "#FABD2F",
        "tertiaryContainerColor": "#5A3800",
        "tertiaryFixedColor": "#FADEC9",
        "tertiaryFixedDimColor": "#E5CA8E",
        "tertiary_paletteKeyColorColor": "#FABD2F",
        "transparentColor": "#00000000"
    },

    "ayu_light": {
        "backgroundColor": "#FAFAFA",
        "disabledTextColor": "#ABB0B6",
        "errorColor": "#E65050",
        "errorContainerColor": "#FFDAD6",
        "inverseOnSurfaceColor": "#F8F9FA",
        "inversePrimaryColor": "#36A3D9",
        "inverseSurfaceColor": "#242936",
        "neutral_paletteKeyColorColor": "#8A9199",
        "neutral_variant_paletteKeyColorColor": "#6C7680",
        "onBackgroundColor": "#242936",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D30",
        "onPrimaryFixedColor": "#001D30",
        "onPrimaryFixedVariantColor": "#00486A",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#1F2B00",
        "onSecondaryFixedColor": "#1F2B00",
        "onSecondaryFixedVariantColor": "#3F5700",
        "onSurfaceColor": "#242936",
        "onSurfaceLightColor": "#575F66",
        "onSurfaceVariantColor": "#6C7680",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#2E1E00",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#ABB0B6",
        "outlineVariantColor": "#E7EAF0",
        "primaryColor": "#399EE6",
        "primaryContainerColor": "#C8E6F7",
        "primaryFixedColor": "#D6EDFF",
        "primaryFixedDimColor": "#A4D5F0",
        "primary_paletteKeyColorColor": "#399EE6",
        "rippleColor": "#399EE633",
        "scrimColor": "#000000",
        "secondaryColor": "#86B300",
        "secondaryContainerColor": "#E5F3C8",
        "secondaryFixedColor": "#F0F9D6",
        "secondaryFixedDimColor": "#D0E89E",
        "secondary_paletteKeyColorColor": "#86B300",
        "shadowColor": "#00000020",
        "surfaceBrightColor": "#FAFAFA",
        "surfaceColor": "#FAFAFA",
        "surfaceContainerColor": "#F3F4F5",
        "surfaceContainerHighColor": "#ECEEF0",
        "surfaceContainerHighestColor": "#E7EAF0",
        "surfaceContainerLowColor": "#F8F9FA",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#F0F1F2",
        "surfaceTintColor": "#399EE6",
        "surfaceVariantColor": "#E7EAF0",
        "tertiaryColor": "#F2AE49",
        "tertiaryContainerColor": "#FFE9C8",
        "tertiaryFixedColor": "#FFF0D6",
        "tertiaryFixedDimColor": "#FFDBA3",
        "tertiary_paletteKeyColorColor": "#F2AE49",
        "transparentColor": "#00000000"
    },

    "ayu_dark": {
        "backgroundColor": "#0A0E14",
        "disabledTextColor": "#3E4B59",
        "errorColor": "#D95757",
        "errorContainerColor": "#5C0F1A",
        "inverseOnSurfaceColor": "#0F131A",
        "inversePrimaryColor": "#399EE6",
        "inverseSurfaceColor": "#C9CCD0",
        "neutral_paletteKeyColorColor": "#4D5566",
        "neutral_variant_paletteKeyColorColor": "#3E4B59",
        "onBackgroundColor": "#B3B1AD",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#001D30",
        "onPrimaryContainerColor": "#C8E6F7",
        "onPrimaryFixedColor": "#001D30",
        "onPrimaryFixedVariantColor": "#00486A",
        "onSecondaryColor": "#1F2B00",
        "onSecondaryContainerColor": "#E5F3C8",
        "onSecondaryFixedColor": "#1F2B00",
        "onSecondaryFixedVariantColor": "#3F5700",
        "onSurfaceColor": "#B3B1AD",
        "onSurfaceLightColor": "#8A9199",
        "onSurfaceVariantColor": "#707A8C",
        "onTertiaryColor": "#2E1E00",
        "onTertiaryContainerColor": "#FFE9C8",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#4D5566",
        "outlineVariantColor": "#1F2430",
        "primaryColor": "#59C2FF",
        "primaryContainerColor": "#00486A",
        "primaryFixedColor": "#C8E6F7",
        "primaryFixedDimColor": "#7DD4F5",
        "primary_paletteKeyColorColor": "#59C2FF",
        "rippleColor": "#59C2FF33",
        "scrimColor": "#000000",
        "secondaryColor": "#95E454",
        "secondaryContainerColor": "#3F5700",
        "secondaryFixedColor": "#E5F3C8",
        "secondaryFixedDimColor": "#B5E77C",
        "secondary_paletteKeyColorColor": "#95E454",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#1F2430",
        "surfaceColor": "#0F131A",
        "surfaceContainerColor": "#0A0E14",
        "surfaceContainerHighColor": "#1F2430",
        "surfaceContainerHighestColor": "#272D38",
        "surfaceContainerLowColor": "#0B0E14",
        "surfaceContainerLowestColor": "#000000",
        "surfaceDimColor": "#0B0E14",
        "surfaceTintColor": "#59C2FF",
        "surfaceVariantColor": "#1F2430",
        "tertiaryColor": "#FFB454",
        "tertiaryContainerColor": "#5D4E2A",
        "tertiaryFixedColor": "#FFE9C8",
        "tertiaryFixedDimColor": "#FFCC7C",
        "tertiary_paletteKeyColorColor": "#FFB454",
        "transparentColor": "#00000000"
    },

    "atom_one_light": {
        "backgroundColor": "#FAFAFA",
        "disabledTextColor": "#A0A1A7",
        "errorColor": "#E45649",
        "errorContainerColor": "#FFDAD6",
        "inverseOnSurfaceColor": "#F9F9F9",
        "inversePrimaryColor": "#4078F2",
        "inverseSurfaceColor": "#282C34",
        "neutral_paletteKeyColorColor": "#9D9D9F",
        "neutral_variant_paletteKeyColorColor": "#737378",
        "onBackgroundColor": "#383A42",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D36",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#003C75",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#002106",
        "onSecondaryFixedColor": "#002106",
        "onSecondaryFixedVariantColor": "#00530F",
        "onSurfaceColor": "#383A42",
        "onSurfaceLightColor": "#696C77",
        "onSurfaceVariantColor": "#9D9D9F",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#2E1E00",
        "onTertiaryFixedColor": "#2E1E00",
        "onTertiaryFixedVariantColor": "#5D4E2A",
        "outlineColor": "#C2C2C4",
        "outlineVariantColor": "#E5E5E6",
        "primaryColor": "#4078F2",
        "primaryContainerColor": "#D4E2FF",
        "primaryFixedColor": "#E0EBFF",
        "primaryFixedDimColor": "#B3CEFF",
        "primary_paletteKeyColorColor": "#4078F2",
        "rippleColor": "#4078F233",
        "scrimColor": "#000000",
        "secondaryColor": "#50A14F",
        "secondaryContainerColor": "#C8E6C9",
        "secondaryFixedColor": "#DCEDC8",
        "secondaryFixedDimColor": "#A5D6A7",
        "secondary_paletteKeyColorColor": "#50A14F",
        "shadowColor": "#00000020",
        "surfaceBrightColor": "#FAFAFA",
        "surfaceColor": "#FAFAFA",
        "surfaceContainerColor": "#F5F5F5",
        "surfaceContainerHighColor": "#EFEFEF",
        "surfaceContainerHighestColor": "#E5E5E6",
        "surfaceContainerLowColor": "#F9F9F9",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#F0F0F1",
        "surfaceTintColor": "#4078F2",
        "surfaceVariantColor": "#E5E5E6",
        "tertiaryColor": "#C18401",
        "tertiaryContainerColor": "#FFE9B8",
        "tertiaryFixedColor": "#FFF0CC",
        "tertiaryFixedDimColor": "#FFD88A",
        "tertiary_paletteKeyColorColor": "#C18401",
        "transparentColor": "#00000000"
    },

    "vs_code_light": {
        "backgroundColor": "#FFFFFF",
        "disabledTextColor": "#999999",
        "errorColor": "#E51400",
        "errorContainerColor": "#FFDAD6",
        "inverseOnSurfaceColor": "#F3F3F3",
        "inversePrimaryColor": "#007ACC",
        "inverseSurfaceColor": "#1E1E1E",
        "neutral_paletteKeyColorColor": "#6E6E6E",
        "neutral_variant_paletteKeyColorColor": "#5A5A5A",
        "onBackgroundColor": "#000000",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#5C0000",
        "onPrimaryColor": "#FFFFFF",
        "onPrimaryContainerColor": "#001D36",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#003E78",
        "onSecondaryColor": "#FFFFFF",
        "onSecondaryContainerColor": "#001B3D",
        "onSecondaryFixedColor": "#001B3D",
        "onSecondaryFixedVariantColor": "#003A6F",
        "onSurfaceColor": "#000000",
        "onSurfaceLightColor": "#3B3B3B",
        "onSurfaceVariantColor": "#616161",
        "onTertiaryColor": "#FFFFFF",
        "onTertiaryContainerColor": "#002114",
        "onTertiaryFixedColor": "#002114",
        "onTertiaryFixedVariantColor": "#00492F",
        "outlineColor": "#D4D4D4",
        "outlineVariantColor": "#E8E8E8",
        "primaryColor": "#007ACC",
        "primaryContainerColor": "#C5E7FF",
        "primaryFixedColor": "#D6EDFF",
        "primaryFixedDimColor": "#9DD4F5",
        "primary_paletteKeyColorColor": "#007ACC",
        "rippleColor": "#007ACC33",
        "scrimColor": "#000000",
        "secondaryColor": "#0066BF",
        "secondaryContainerColor": "#CEE5FF",
        "secondaryFixedColor": "#E0F0FF",
        "secondaryFixedDimColor": "#A8D5F5",
        "secondary_paletteKeyColorColor": "#0066BF",
        "shadowColor": "#00000020",
        "surfaceBrightColor": "#FFFFFF",
        "surfaceColor": "#FFFFFF",
        "surfaceContainerColor": "#F3F3F3",
        "surfaceContainerHighColor": "#EEEEEE",
        "surfaceContainerHighestColor": "#E8E8E8",
        "surfaceContainerLowColor": "#F8F8F8",
        "surfaceContainerLowestColor": "#FFFFFF",
        "surfaceDimColor": "#F5F5F5",
        "surfaceTintColor": "#007ACC",
        "surfaceVariantColor": "#F0F0F0",
        "tertiaryColor": "#008000",
        "tertiaryContainerColor": "#D4F3D4",
        "tertiaryFixedColor": "#E5F9E5",
        "tertiaryFixedDimColor": "#B8EAB8",
        "tertiary_paletteKeyColorColor": "#008000",
        "transparentColor": "#00000000"
    },

    "vs_code_dark": {
        "backgroundColor": "#1E1E1E",
        "disabledTextColor": "#666666",
        "errorColor": "#F48771",
        "errorContainerColor": "#5C0F1A",
        "inverseOnSurfaceColor": "#252526",
        "inversePrimaryColor": "#007ACC",
        "inverseSurfaceColor": "#D4D4D4",
        "neutral_paletteKeyColorColor": "#858585",
        "neutral_variant_paletteKeyColorColor": "#6E6E6E",
        "onBackgroundColor": "#CCCCCC",
        "onErrorColor": "#FFFFFF",
        "onErrorContainerColor": "#FFD6DD",
        "onPrimaryColor": "#001D36",
        "onPrimaryContainerColor": "#C5E7FF",
        "onPrimaryFixedColor": "#001D36",
        "onPrimaryFixedVariantColor": "#003E78",
        "onSecondaryColor": "#001B3D",
        "onSecondaryContainerColor": "#CEE5FF",
        "onSecondaryFixedColor": "#001B3D",
        "onSecondaryFixedVariantColor": "#003A6F",
        "onSurfaceColor": "#CCCCCC",
        "onSurfaceLightColor": "#B0B0B0",
        "onSurfaceVariantColor": "#B0B0B0",
        "onTertiaryColor": "#002114",
        "onTertiaryContainerColor": "#D4F3D4",
        "onTertiaryFixedColor": "#002114",
        "onTertiaryFixedVariantColor": "#00492F",
        "outlineColor": "#858585",
        "outlineVariantColor": "#3C3C3C",
        "primaryColor": "#4FC1FF",
        "primaryContainerColor": "#003E78",
        "primaryFixedColor": "#C5E7FF",
        "primaryFixedDimColor": "#7DD4F5",
        "primary_paletteKeyColorColor": "#4FC1FF",
        "rippleColor": "#4FC1FF33",
        "scrimColor": "#000000",
        "secondaryColor": "#569CD6",
        "secondaryContainerColor": "#003A6F",
        "secondaryFixedColor": "#CEE5FF",
        "secondaryFixedDimColor": "#84C5F0",
        "secondary_paletteKeyColorColor": "#569CD6",
        "shadowColor": "#000000",
        "surfaceBrightColor": "#3C3C3C",
        "surfaceColor": "#1E1E1E",
        "surfaceContainerColor": "#252526",
        "surfaceContainerHighColor": "#2D2D30",
        "surfaceContainerHighestColor": "#3C3C3C",
        "surfaceContainerLowColor": "#1A1A1A",
        "surfaceContainerLowestColor": "#141414",
        "surfaceDimColor": "#F6F8FA",
        "surfaceTintColor": "#0969DA",
        "surfaceVariantColor": "#EAEEF2",
        "tertiaryColor": "#1A7F37",
        "tertiaryContainerColor": "#DAFBE1",
        "tertiaryFixedColor": "#E7FEE9",
        "tertiaryFixedDimColor": "#B4F1B8",
        "tertiary_paletteKeyColorColor": "#1A7F37",
        "transparentColor": "#00000000"
    }
}


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
    dialog = ObjectProperty(None)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create theme storage first
        self.dialog = None

        self.THEMES = THEMES

        self.active_theme_name = list(self.THEMES.keys())[9]
        self.theme_data = self.THEMES[self.active_theme_name]  # dict for the active theme

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

        self.apply_theme(self.active_theme_name)



        # self.theme_cls.theme_style = "Light"
        # dropdown items
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        resource_add_path(font_dir)
        LabelBase.register(name='NepaliFont', fn_regular=resourece_path('fonts/Kalimati Regular.otf'))
        LabelBase.register(name='MultiLangFont', fn_regular= resourece_path('fonts/NotoSansDevanagari.ttf'))
        LabelBase.register(name='Preeti', fn_regular=resourece_path('fonts/Preeti Normal.otf'))
        LabelBase.register(name='Mangal', fn_regular=resourece_path('fonts/Mangal Regular.otf'))
        LabelBase.register(            name="MultiLangFont",                   fn_regular=os.path.join(font_dir, "NotoSansDevanagari.ttf"),        )
        LabelBase.register(name='NotoSansDevanagari_ExtraCondensed-SemiBold', fn_regular=resourece_path('fonts/NotoSansDevanagari_ExtraCondensed-SemiBold.ttf'))
        LabelBase.register(name='NotoSansDevanagari-Medium', fn_regular=resourece_path('fonts/NotoSansDevanagari-Medium.ttf'))



        # 🔹 Create one database handler for the app
        self.gui_DB = DM.GUIDatabase()
        self.GUIHandle = GUI_DB_Handle()
        return self.sm

    def on_start(self):
        # Clock.schedule_once(self._post_start, 0)
        # Schedule the welcome label removal after 3 seconds
        main_screen = self.sm.get_screen("main_screen")
        Clock.schedule_once(lambda dt: self.remove_welcome(main_screen), 7)
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
    def remove_welcome(self, screen):
        # Remove the welcome label
        welcome_box = screen.ids.welcome_label
        if welcome_box:
            welcome_box.parent.remove_widget(welcome_box)
        # MDStackLayout automatically adjusts its size
    def open_help_dialog(self):
        # dialog_content = Factory.HelpDialog()
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Card
        card = MDCard(
            style="elevated",
            pos_hint={"center_x": 0.5},
            padding="4dp",
            size_hint=(None, None),
            size=("240dp", "100dp"),
            theme_shadow_color="Custom",
            shadow_color="green",
            theme_bg_color="Custom",
            md_bg_color="white",
            md_bg_color_disabled="grey",
            theme_shadow_offset="Custom",
            shadow_offset=(1, -2),
            theme_shadow_softness="Custom",
            shadow_softness=1,
            theme_elevation_level="Custom",
            elevation_level=2,
        )


        # Add FAB
        fabbutton1 = HoverFab(
            pos_hint={"center_x": 0.5},
            elevation_level=5,
            fab_state="collapse"
        )

        fabbutton1.add_widget(MDExtendedFabButtonIcon(icon="facebook"))
        fabbutton1.add_widget(MDExtendedFabButtonText(text="Nolaraj Poudel"))
        fabbutton1.bind(on_release=lambda instance: self.open_link("https://www.facebook.com/nolaraj/"))

        scroll = ScrollView(size_hint=(1, None), size=(400, 300))

        layout.add_widget(card)
        card.add_widget(fabbutton1)


        scroll.add_widget(layout)

        cancel_btn = MDButton(
            style="outlined",
            size_hint=(None, None),
            size=(dp(60), dp(40)),  # bigger for touch target
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.dialog.dismiss()
        )
        cancel_btn.add_widget(MDButtonIcon(icon="close"))  # ✅ Tick Icon
        #cancel_btn.add_widget(MDButtonText(text="CANCEL"))

        #cancel_btn.add_widget(MDButtonText(text="CANCEL"))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="About me"),
            MDDialogContentContainer(scroll),
            MDDialogButtonContainer(
                cancel_btn,
            ),
        )
        self.dialog.open()
    def open_link(self, url):
        webbrowser.open(url)
    #____________________________________________________Themes

    def apply_theme(self, theme_name: str):
        if theme_name not in self.THEMES:
            print(f"⚠️ Theme '{theme_name}' not found.")
            return

        self.active_theme_name = theme_name
        self.theme_data = self.THEMES[theme_name]

        for key, hex_color in self.theme_data.items():
            color_value = get_color_from_hex(hex_color)
            if hasattr(self.theme_cls, key):
                setattr(self.theme_cls, key, color_value)

        # if "Light" in theme_name:
        #     self.theme_cls.theme_style = "Light"
        # else:
        #     self.theme_cls.theme_style = "Dark"

        # print(f"✅ Theme '{theme_name}' applied successfully.")

    def open_theme_dialog(self):
        ThemeKeys = list(self.THEMES.keys())
        self.theme_buttons = {}  # store button references

        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(1),
            size_hint_y=None,
            pos_hint={'center_x': 0.5}  # center layout horizontally
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        for theme_name in ThemeKeys:
            btn = MDButton(
                size_hint=(None, None),  # allow fixed width and height
                width=dp(250),  # button width smaller than content layout width for centering
                height=dp(36),
                on_release=lambda x, tn=theme_name: self._on_theme_button_press(tn),
                style="outlined" if theme_name == self.active_theme_name else "text",
                pos_hint={'center_x': 0.5}  # center button inside layout
            )
            btn.add_widget(
                MDButtonText(
                    text=theme_name,
                    halign="center",
                    text_color=app.theme_cls.primaryColor
                )
            )

            content_layout.add_widget(btn)
            self.theme_buttons[theme_name] = btn  # store reference

        # Scroll view
        scroll_view = MDScrollView(
            size_hint=(1, None),
            height=min(dp(36) * len(ThemeKeys) + dp(1) * (len(ThemeKeys) - 1), dp(250)),
            bar_width=dp(8),  # ✅ thicker scrollbar
        )
        scroll_view.scroll_type = ['bars', 'content']
        scroll_view.bar_color = app.theme_cls.primaryColor  # ✅ scrollbar color matches theme
        scroll_view.bar_inactive_color = app.theme_cls.onSurfaceVariantColor  # faded inactive color
        scroll_view.scroll_wheel_distance = dp(40)  # smoother scrolling
        scroll_view.add_widget(content_layout)
        # Cancel button
        cancel_btn = MDButton(
            style="outlined",
            size_hint=(None, None),
            size=(dp(60), dp(40)),  # bigger for touch target
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.dialog.dismiss()
        )
        cancel_btn.add_widget(MDButtonIcon(icon="close", halign="center"))

        # Dialog
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Select Theme"),
            MDDialogContentContainer(scroll_view),
            MDDialogButtonContainer(cancel_btn),
        )
        self.dialog.open()
    def _on_theme_button_press(self, theme_name):
        # Apply theme
        self.apply_theme(theme_name)

        # Update button styles
        for tn, btn in self.theme_buttons.items():
            if tn == theme_name:
                btn.style = "outlined"
            else:
                btn.style = "text"

        # Update active theme tracker
        self.active_theme_name = theme_name
    def apply_and_close(self, theme_name):
        self.apply_theme(theme_name)
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = None
    # ################################Themes END

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
        Builder.load_file(        resourece_path("screens/login.kv"))
        Builder.load_file(   resourece_path("screens/Test.kv"))

        # Load component KV files
        Builder.load_file(   resourece_path("components/rv.kv"))
        Builder.load_file(   resourece_path("components/dialogs.kv"))

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
            traceback.print_exc()

    def _restore_item(self, item_data, item_container, section_widget):
        """Restore one ItemQuantity_Details with complete state"""

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
            traceback.print_exc()

    def _restore_search_results(self, item_widget, search_results):
        """Restore search results for an item"""

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
                        traceback.print_exc()
                        continue

        except Exception as e:
            print(f"Error in _auto_apply_single_search_results: {e}")
            traceback.print_exc()("Second Inner table", {}).get("Unit Rate", [0])[0]

    def _restore_subitem(self, subitem_data, dims_container, item_widget, item_data):
        """Restore one SubItemRow with all field values"""

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
                    traceback.print_exc()

            Clock.schedule_once(set_subitem_values, 0.05)

        except Exception as e:
            print(f"Error restoring subitem: {e}")
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


        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # File chooser
        filechooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.json'],
            size_hint=(1, 0.8)
        )
        content.add_widget(filechooser)

        # Selected file label
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