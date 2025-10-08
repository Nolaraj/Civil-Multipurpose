from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
<DashboardCard@MDCard>:
    style: "elevated"
    pos_hint: {"center_x": .5, "center_y": .5}
    padding: "4dp"
    size_hint: None, None
    size: "240dp", "100dp"
    # Sets custom properties.
    theme_shadow_color: "Custom"
    shadow_color: "green"
    theme_bg_color: "Custom"
    md_bg_color: "white"
    md_bg_color_disabled: "grey"
    theme_shadow_offset: "Custom"
    shadow_offset: (1, -2)
    theme_shadow_softness: "Custom"
    shadow_softness: 1
    theme_elevation_level: "Custom"
    elevation_level: 2

    RelativeLayout:

        MDIconButton:
            icon: "dots-vertical"
            pos_hint: {"top": 1, "right": 1}

        MDLabel:
            text: "Elevated"
            adaptive_size: True
            color: "pink"
            pos: "12dp", "12dp"
            bold: True

MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDCard:
        style: "elevated"
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: "4dp"
        size_hint: None, None
        size: "240dp", "100dp"
        # Sets custom properties.
        theme_shadow_color: "Custom"
        shadow_color: "green"
        theme_bg_color: "Custom"
        md_bg_color: "white"
        md_bg_color_disabled: "grey"
        theme_shadow_offset: "Custom"
        shadow_offset: (1, -2)
        theme_shadow_softness: "Custom"
        shadow_softness: 1
        theme_elevation_level: "Custom"
        elevation_level: 2

        RelativeLayout:

            MDIconButton:
                icon: "dots-vertical"
                pos_hint: {"top": 1, "right": 1}

            MDLabel:
                text: "Elevated"
                adaptive_size: True
                color: "grey"
                pos: "12dp", "12dp"
                bold: True


'''


class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    # === Functionalities ===
    def open_estimation(self):
        print("📘 Estimation Section Opened")

    def open_analysis(self):
        print("📊 Analysis Section Opened")

    def open_reports(self):
        print("📄 Reports Section Opened")

    def open_settings(self):
        print("⚙️ Settings Opened")


Example().run()
