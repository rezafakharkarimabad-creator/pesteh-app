# main.py
# اپلیکیشن محاسبه‌گر پسته - شرکت فتاح توزین

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import platform
from kivy.clock import Clock

# کتابخانه‌های فارسی
import arabic_reshaper
from bidi.algorithm import get_display

# =========================================================
# ثبت فونت‌ها
# =========================================================
LabelBase.register(
    name="Vazir",
    fn_regular="Vazirmatn-Regular.ttf",
    fn_bold="Vazirmatn-Bold.ttf",
)
LabelBase.register(
    name="Roboto",
    fn_regular="Vazirmatn-Regular.ttf",
    fn_bold="Vazirmatn-Bold.ttf",
)
LabelBase.register(
    name="RobotoRegular",
    fn_regular="Vazirmatn-Regular.ttf",
    fn_bold="Vazirmatn-Bold.ttf",
)
LabelBase.register(
    name="RobotoBold",
    fn_regular="Vazirmatn-Bold.ttf",
    fn_bold="Vazirmatn-Bold.ttf",
)
LabelBase.register(
    name="RobotoMedium",
    fn_regular="Vazirmatn-Medium.ttf",
    fn_bold="Vazirmatn-Bold.ttf",
)

Window.size = (400, 720)


# =========================================================
# اطلاعات شرکت فتاح توزین
# =========================================================
COMPANY_NAME = "شرکت فتاح توزین"
COMPANY_SLOGAN_LINE_1 = "فروش و تعمیرات انواع باسکول‌های صنعتی"
COMPANY_SLOGAN_LINE_2 = "و جاده‌ای"
COMPANY_SLOGAN_LINE_3 = "و انواع ترازوهای انس‌گیری با دقت بالا"
COMPANY_SERVICES = [
    "طراحی سیستم‌های خاص توزین",
    "اتوماسیون‌های بر پایه وزنی",
]
COMPANY_PHONE = "09133573782"
COMPANY_PHONE_FA = "۰۹۱۳۳۵۷۳۷۸۲"
COMPANY_MANAGER = "مهندس فخار"

BRAND_COLOR = (0.85, 0.45, 0.10, 1)
BRAND_LIGHT = (1.0, 0.96, 0.90, 1)

ANS_STANDARD = 141.8


# =========================================================
# تابع نمایش متن فارسی (RTL)
# =========================================================

def fa(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


# =========================================================
# توابع محاسباتی
# =========================================================

def calc_ans(weight, count):
    if weight <= 0 or count <= 0:
        return None
    return (ANS_STANDARD * count) / (5 * weight)


def calc_maghz(total_weight, kernel_weight):
    if total_weight <= 0:
        return None
    if kernel_weight < 0 or kernel_weight > total_weight:
        return None
    return (kernel_weight / total_weight) * 100


def calc_quality(maghz_per_100):
    if maghz_per_100 is None:
        return None
    return (maghz_per_100 / 50) * 100


def calc_price(base_price, quality_pct):
    if base_price <= 0 or quality_pct is None:
        return None
    return base_price * (quality_pct / 100)


# =========================================================
# کارت نمایش نتیجه
# =========================================================

class ResultCard(MDCard):
    def __init__(self, height=dp(220), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(6)
        self.size_hint_y = None
        self.height = height
        self.md_bg_color = (0.95, 0.97, 0.95, 1)
        self.radius = [15]
        self.elevation = 3

        self.title = MDLabel(
            text=fa("نتیجه"),
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.18, 0.49, 0.20, 1),
            size_hint_y=None,
            height=dp(36),
        )
        self.add_widget(self.title)

        self.result_label = MDLabel(
            text="-",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0.78, 0.16, 0.16, 1),
            size_hint_y=None,
            height=dp(60),
        )
        self.add_widget(self.result_label)

        self.detail_label = MDLabel(
            text="",
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(100),
        )
        self.add_widget(self.detail_label)

    def set_result(self, main, detail):
        self.result_label.text = main
        self.detail_label.text = fa(detail)


# =========================================================
# بنر تبلیغاتی بالای صفحه
# =========================================================

class TopBanner(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(48)
        self.md_bg_color = BRAND_COLOR
        self.radius = [0]
        self.elevation = 6
        self.padding = (dp(12), 0)

        name_label = MDLabel(
            text=fa(COMPANY_NAME),
            halign="left",
            valign="middle",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.55,
        )
        self.add_widget(name_label)

        phone_label = MDLabel(
            text=fa(f"☎ {COMPANY_PHONE_FA}"),
            halign="right",
            valign="middle",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.45,
        )
        self.add_widget(phone_label)


# =========================================================
# تب ۱: انس‌گیری
# =========================================================

class AnsTab(MDBottomNavigationItem):
    name = "ans"
    text = fa("انس‌گیری")
    icon = "nut"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.help_dialog = None

        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            adaptive_height=True,
        )

        layout.add_widget(MDLabel(
            text=fa("محاسبه انس پسته"),
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.18, 0.49, 0.20, 1),
            size_hint_y=None,
            height=dp(50),
        ))

        layout.add_widget(MDLabel(
            text=fa("وزن و تعداد را وارد کن"),
            halign="center",
            font_style="Caption",
            size_hint_y=None,
            height=dp(30),
        ))

        self.weight_input = MDTextField(
            hint_text=fa("وزن کل (گرم)"),
            input_filter="float",
            mode="rectangle",
        )
        layout.add_widget(self.weight_input)

        self.count_input = MDTextField(
            hint_text=fa("تعداد پسته"),
            input_filter="int",
            mode="rectangle",
        )
        layout.add_widget(self.count_input)

        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50),
        )
        btn_layout.add_widget(MDRaisedButton(
            text=fa("محاسبه"),
            md_bg_color=(0.18, 0.49, 0.20, 1),
            on_release=self.calculate,
            size_hint_x=0.4,
        ))
        btn_layout.add_widget(MDFlatButton(
            text=fa("پاک کردن"),
            on_release=self.clear,
            size_hint_x=0.3,
        ))
        btn_layout.add_widget(MDFlatButton(
            text=fa("راهنما"),
            on_release=self.show_help,
            size_hint_x=0.3,
        ))
        layout.add_widget(btn_layout)

        self.result_card = ResultCard()
        layout.add_widget(self.result_card)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def calculate(self, *args):
        try:
            w = float(self.weight_input.text)
            c = int(self.count_input.text)
        except (ValueError, TypeError):
            self.result_card.set_result("خطا", "عدد معتبر وارد کن")
            return

        ans = calc_ans(w, c)
        if ans is None:
            self.result_card.set_result("خطا", "وزن و تعداد باید مثبت باشند")
            return

        avg = w / c
        self.result_card.set_result(
            f"{ans:.2f}",
            f"وزن میانگین: {avg:.3f} گرم"
        )

    def clear(self, *args):
        self.weight_input.text = ""
        self.count_input.text = ""
        self.result_card.set_result("-", "")

    def show_help(self, *args):
        if not self.help_dialog:
            content = MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                padding=dp(15),
                size_hint_y=None,
                height=dp(260),
            )

            lines = [
                "برای انس‌گیری نیازی نیست که ۱۴۲ گرم را روی ترازو بگذارید.",
                "کافیست تعدادی از دانه‌های پسته را بشمارید و روی ترازو بگذارید.",
                "سپس در این نرم‌افزار مقدار وزن و تعداد دانه‌های پسته را وارد کنید.",
                "نرم‌افزار همه محاسبات را بر حسب ۱۴۲ گرم برای شما محاسبه می‌کند.",
            ]

            for line in lines:
                lbl = MDLabel(
                    text=fa(line),
                    halign="right",
                    valign="top",
                    font_style="Body1",
                    size_hint_y=None,
                    height=dp(50),
                    text_size=(dp(260), None),
                )
                content.add_widget(lbl)

            self.help_dialog = MDDialog(
                title=fa("راهنمای انس‌گیری"),
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text=fa("فهمیدم"),
                        on_release=lambda x: self.help_dialog.dismiss(),
                    ),
                ],
            )
        self.help_dialog.open()


# =========================================================
# تب ۲: دهن‌بست
# =========================================================

class DehansetTab(MDBottomNavigationItem):
    name = "dehanset"
    text = fa("دهن‌بست")
    icon = "target"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
            adaptive_height=True,
        )

        layout.add_widget(MDLabel(
            text=fa("محاسبه گرم مغز در ۱۰۰ گرم"),
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.18, 0.49, 0.20, 1),
            size_hint_y=None,
            height=dp(50),
        ))

        self.total_input = MDTextField(
            hint_text=fa("وزن کل پسته (گرم)"),
            input_filter="float",
            mode="rectangle",
        )
        layout.add_widget(self.total_input)

        self.kernel_input = MDTextField(
            hint_text=fa("وزن مغز (گرم)"),
            input_filter="float",
            mode="rectangle",
        )
        layout.add_widget(self.kernel_input)

        self.base_price_input = MDTextField(
            hint_text=fa("قیمت مبنا (تومان) - برای ۵۰ گرم مغز"),
            input_filter="float",
            mode="rectangle",
        )
        layout.add_widget(self.base_price_input)

        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
        )
        btn_layout.add_widget(MDRaisedButton(
            text=fa("محاسبه"),
            md_bg_color=(0.18, 0.49, 0.20, 1),
            on_release=self.calculate,
            size_hint_x=0.5,
        ))
        btn_layout.add_widget(MDFlatButton(
            text=fa("پاک کردن"),
            on_release=self.clear,
            size_hint_x=0.5,
        ))
        layout.add_widget(btn_layout)

        self.result_card = ResultCard(height=dp(280))
        layout.add_widget(self.result_card)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def calculate(self, *args):
        try:
            total = float(self.total_input.text)
            kernel = float(self.kernel_input.text)
        except (ValueError, TypeError):
            self.result_card.set_result("خطا", "عدد معتبر وارد کن")
            return

        maghz = calc_maghz(total, kernel)
        if maghz is None:
            if total <= 0:
                self.result_card.set_result("خطا", "وزن کل باید مثبت باشد")
            elif kernel > total:
                self.result_card.set_result("خطا", "وزن مغز بیشتر از وزن کل است")
            else:
                self.result_card.set_result("خطا", "مقادیر معتبر وارد کن")
            return

        quality = calc_quality(maghz)

        base_price_text = self.base_price_input.text.strip()
        detail_lines = [
            f"در ۱۰۰ گرم پسته، {maghz:.2f} گرم مغز وجود دارد",
            f"درصد کیفیت: {quality:.1f}%",
        ]

        if base_price_text:
            try:
                base_price = float(base_price_text)
                price = calc_price(base_price, quality)
                if price is not None:
                    detail_lines.append(f"قیمت نهایی: {price:,.0f} تومان")
            except ValueError:
                detail_lines.append("قیمت مبنا نامعتبر است")

        self.result_card.set_result(
            f"{maghz:.2f}",
            "\n".join(detail_lines)
        )

    def clear(self, *args):
        self.total_input.text = ""
        self.kernel_input.text = ""
        self.base_price_input.text = ""
        self.result_card.set_result("-", "")


# =========================================================
# تب ۳: محاسبه قیمت
# =========================================================

class PriceTab(MDBottomNavigationItem):
    name = "price"
    text = fa("قیمت")
    icon = "cash"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
            adaptive_height=True,
        )

        layout.add_widget(MDLabel(
            text=fa("محاسبه قیمت نهایی"),
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.18, 0.49, 0.20, 1),
            size_hint_y=None,
            height=dp(50),
        ))

        self.base_input = MDTextField(
            hint_text=fa("قیمت پایه هر کیلو (تومان)"),
            input_filter="float",
            mode="rectangle",
        )
        layout.add_widget(self.base_input)

        self.maghz_input = MDTextField(
            hint_text=fa("گرم مغز در ۱۰۰ گرم"),
            input_filter="float",
            mode="rectangle",
            text="50",
        )
        layout.add_widget(self.maghz_input)

        self.tochin_input = MDTextField(
            hint_text=fa("درصد توچین"),
            input_filter="float",
            mode="rectangle",
            text="3",
        )
        layout.add_widget(self.tochin_input)

        self.profit_input = MDTextField(
            hint_text=fa("درصد سود فروشنده"),
            input_filter="float",
            mode="rectangle",
            text="10",
        )
        layout.add_widget(self.profit_input)

        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
        )
        btn_layout.add_widget(MDRaisedButton(
            text=fa("محاسبه"),
            md_bg_color=(0.18, 0.49, 0.20, 1),
            on_release=self.calculate,
            size_hint_x=0.5,
        ))
        btn_layout.add_widget(MDFlatButton(
            text=fa("پاک کردن"),
            on_release=self.clear,
            size_hint_x=0.5,
        ))
        layout.add_widget(btn_layout)

        self.result_card = ResultCard(height=dp(250))
        layout.add_widget(self.result_card)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def calculate(self, *args):
        try:
            base = float(self.base_input.text)
            maghz = float(self.maghz_input.text or 0)
            toc = float(self.tochin_input.text or 0)
            pro = float(self.profit_input.text or 0)
        except (ValueError, TypeError):
            self.result_card.set_result("خطا", "عدد معتبر وارد کن")
            return

        if maghz <= 0:
            self.result_card.set_result("خطا", "گرم مغز باید مثبت باشد")
            return

        quality_factor = maghz / 50
        effective_price = base / quality_factor
        final_price = effective_price * (1 + pro / 100)

        self.result_card.set_result(
            f"{final_price:,.0f} تومان",
            f"قیمت مؤثر: {effective_price:,.0f} تومان\n"
            f"کیفیت: {quality_factor*100:.0f}%\n"
            f"سود: {pro:.0f}%"
        )

    def clear(self, *args):
        self.base_input.text = ""
        self.maghz_input.text = "50"
        self.tochin_input.text = "3"
        self.profit_input.text = "10"
        self.result_card.set_result("-", "")


# =========================================================
# تب ۴: شرکت فتاح توزین (تبلیغاتی)
# =========================================================

class AboutTab(MDBottomNavigationItem):
    name = "about"
    text = fa("درباره ما")
    icon = "information"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            adaptive_height=True,
        )

        logo_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(190),
            md_bg_color=BRAND_LIGHT,
            radius=[15],
            elevation=3,
        )

        logo_card.add_widget(MDLabel(
            text=fa(COMPANY_NAME),
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=BRAND_COLOR,
            size_hint_y=None,
            height=dp(55),
        ))

        logo_card.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_1),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        logo_card.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_2),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        logo_card.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_3),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        layout.add_widget(logo_card)

        services_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(180),
            md_bg_color=(0.97, 0.97, 0.97, 1),
            radius=[15],
            elevation=2,
        )

        services_card.add_widget(MDLabel(
            text=fa("خدمات تخصصی"),
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=BRAND_COLOR,
            size_hint_y=None,
            height=dp(40),
        ))

        for service in COMPANY_SERVICES:
            services_card.add_widget(MDLabel(
                text=fa(f"• {service}"),
                halign="center",
                font_style="Body1",
                size_hint_y=None,
                height=dp(35),
            ))

        layout.add_widget(services_card)

        contact_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(180),
            md_bg_color=(0.95, 0.97, 0.95, 1),
            radius=[15],
            elevation=3,
        )

        contact_card.add_widget(MDLabel(
            text=fa("اطلاعات تماس"),
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=BRAND_COLOR,
            size_hint_y=None,
            height=dp(40),
        ))

        contact_card.add_widget(MDLabel(
            text=fa(f"مدیریت: {COMPANY_MANAGER}"),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(35),
        ))

        contact_card.add_widget(MDLabel(
            text=fa(f"تلفن: {COMPANY_PHONE_FA}"),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(35),
        ))

        layout.add_widget(contact_card)

        layout.add_widget(MDRaisedButton(
            text=fa("تماس با ما"),
            md_bg_color=BRAND_COLOR,
            size_hint_x=1,
            size_hint_y=None,
            height=dp(55),
            on_release=self.call_phone,
        ))

        layout.add_widget(MDLabel(
            text=fa("از باغ تا سفره شما، با ضمانت کیفیت"),
            halign="center",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(50),
        ))

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def call_phone(self, *args):
        if platform == "android":
            try:
                from jnius import autoclass, cast
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                intent = Intent(Intent.ACTION_DIAL)
                intent.setData(Uri.parse(f"tel:{COMPANY_PHONE}"))
                current_activity = cast("android.app.Activity", PythonActivity.mActivity)
                current_activity.startActivity(intent)
            except Exception as e:
                print(f"خطا در تماس: {e}")
        else:
            print(f"شماره تماس: {COMPANY_PHONE}")
            print("(فقط روی اندروید تماس گرفته می‌شود)")


# =========================================================
# اپلیکیشن اصلی
# =========================================================

class PestehApp(MDApp):
    def build(self):
        self.title = "Pesteh"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        self.theme_cls.font_styles["H1"] = ["Vazir", 96, False, -1.5]
        self.theme_cls.font_styles["H2"] = ["Vazir", 60, False, -0.5]
        self.theme_cls.font_styles["H3"] = ["Vazir", 48, False, 0]
        self.theme_cls.font_styles["H4"] = ["Vazir", 34, False, 0.25]
        self.theme_cls.font_styles["H5"] = ["Vazir", 24, False, 0]
        self.theme_cls.font_styles["H6"] = ["Vazir", 20, False, 0.15]
        self.theme_cls.font_styles["Subtitle1"] = ["Vazir", 16, False, 0.15]
        self.theme_cls.font_styles["Subtitle2"] = ["Vazir", 14, False, 0.1]
        self.theme_cls.font_styles["Body1"] = ["Vazir", 16, False, 0.5]
        self.theme_cls.font_styles["Body2"] = ["Vazir", 14, False, 0.25]
        self.theme_cls.font_styles["Button"] = ["Vazir", 14, True, 1.25]
        self.theme_cls.font_styles["Caption"] = ["Vazir", 12, False, 0.4]
        self.theme_cls.font_styles["Overline"] = ["Vazir", 10, False, 1.5]

        # صفحه اصلی - یک BoxLayout عمودی از بالا به پایین
        root = MDBoxLayout(orientation="vertical")

        # ۱. نوار بالا (toolbar)
        toolbar = MDTopAppBar(
            title=fa("محاسبه‌گر پسته"),
            elevation=4,
        )
        root.add_widget(toolbar)

        # ۲. بنر تبلیغاتی (زیر toolbar)
        banner = TopBanner()
        root.add_widget(banner)

        # ۳. ناوبری پایین (تب‌ها) - فضای باقی‌مانده را پر می‌کند
        bottom_nav = MDBottomNavigation()
        bottom_nav.add_widget(AnsTab())
        bottom_nav.add_widget(DehansetTab())
        bottom_nav.add_widget(PriceTab())
        bottom_nav.add_widget(AboutTab())

        root.add_widget(bottom_nav)

        Clock.schedule_once(self.show_welcome_ad, 0.5)

        return root

    def show_welcome_ad(self, dt):
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(15),
            size_hint_y=None,
            height=dp(400),
        )

        content.add_widget(MDLabel(
            text=fa(COMPANY_NAME),
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=BRAND_COLOR,
            size_hint_y=None,
            height=dp(55),
        ))

        content.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_1),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        content.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_2),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        content.add_widget(MDLabel(
            text=fa(COMPANY_SLOGAN_LINE_3),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(28),
        ))

        content.add_widget(MDLabel(
            text="",
            size_hint_y=None,
            height=dp(8),
        ))

        for service in COMPANY_SERVICES:
            content.add_widget(MDLabel(
                text=fa(f"• {service}"),
                halign="center",
                font_style="Body2",
                size_hint_y=None,
                height=dp(28),
            ))

        content.add_widget(MDLabel(
            text="",
            size_hint_y=None,
            height=dp(8),
        ))

        content.add_widget(MDLabel(
            text=fa(f"تلفن: {COMPANY_PHONE_FA}"),
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=BRAND_COLOR,
            size_hint_y=None,
            height=dp(40),
        ))

        content.add_widget(MDLabel(
            text=fa(COMPANY_MANAGER),
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30),
        ))

        self.welcome_dialog = MDDialog(
            title=fa("به محاسبه‌گر پسته خوش آمدید"),
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text=fa("ورود به برنامه"),
                    md_bg_color=BRAND_COLOR,
                    on_release=lambda x: self.welcome_dialog.dismiss(),
                ),
            ],
        )
        self.welcome_dialog.open()


if __name__ == "__main__":
    PestehApp().run()