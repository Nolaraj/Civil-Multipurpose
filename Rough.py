# main.py
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.factory import Factory
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




if __name__ == "__main__":
    Window.minimum_width, Window.minimum_height = (800, 600)
    app = CivilEstimationApp()

    # inject app into another class
    # helper = SomeOtherClass(app)
    # helper.do_something()  # works before app.run()

    app.run()