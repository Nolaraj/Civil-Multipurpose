from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase

# Register NotoSansDevanagari for Nepali
LabelBase.register(name="NotoSansDevanagari", fn_regular="fonts/NotoSansDevanagari.ttf")

KV = """
BoxLayout:
    orientation: "vertical"
    padding: dp(20)
    spacing: dp(20)

    # Row with half-width Label
    BoxLayout:
        orientation: "horizontal"
        spacing: dp(8)
        size_hint_y: None
        height: self.minimum_height

        Label:
            text: "नेपाल सुन्दर छ। यो उदाहरण हो जहाँ टेक्स्ट दुई वा बढी लाइनमा देखिन्छ।"
            font_name: "NotoSansDevanagari"
            font_size: "32sp"
            halign: "left"
            valign: "top"
            text_size: self.width, None
            size_hint_x: 0.5
            size_hint_y: None
            height: self.texture_size[1]
        #Widget:
        #    size_hint_x: 0.5


    # Full-width Label
    Label:
        text: "नेपाल हाम्रो गौरव हो। यो अर्को उदाहरण हो।"
        font_name: "NotoSansDevanagari"
        font_size: "32sp"
        halign: "center"
        valign: "middle"
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
"""

class NepaliTextApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    NepaliTextApp().run()
