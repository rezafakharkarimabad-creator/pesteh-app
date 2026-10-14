# test_font.py
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window

import arabic_reshaper
from bidi.algorithm import get_display

Window.size = (600, 500)

# ثبت همه فونت‌های موجود
LabelBase.register(name="VazirRegular", fn_regular="Vazirmatn-Regular.ttf")
LabelBase.register(name="VazirBold", fn_regular="Vazirmatn-Bold.ttf")
LabelBase.register(name="VazirMedium", fn_regular="Vazirmatn-Medium.ttf")
LabelBase.register(name="VazirLight", fn_regular="Vazirmatn-Light.ttf")
LabelBase.register(name="VazirSemiBold", fn_regular="Vazirmatn-SemiBold.ttf")


def fa(text):
    return get_display(arabic_reshaper.reshape(str(text)))


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(
            text=fa("تست Regular - سلام دنیا"),
            font_name="VazirRegular",
            font_size=28,
        ))
        layout.add_widget(Label(
            text=fa("تست Bold - سلام دنیا"),
            font_name="VazirBold",
            font_size=28,
        ))
        layout.add_widget(Label(
            text=fa("تست Medium - سلام دنیا"),
            font_name="VazirMedium",
            font_size=28,
        ))
        layout.add_widget(Label(
            text=fa("تست Light - سلام دنیا"),
            font_name="VazirLight",
            font_size=28,
        ))
        layout.add_widget(Label(
            text=fa("تست SemiBold - سلام دنیا"),
            font_name="VazirSemiBold",
            font_size=28,
        ))

        return layout


TestApp().run()