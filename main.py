import flet as ft
import math

# ==========================================
# 1. الدوال الرياضية (نفس اللوجيك بتاعك بالظبط)
# ==========================================
def sum_f(a, b): return a + b
def sub_f(a, b): return a - b
def multiply_f(a, b): return a * b
def division_f(a, b): return a / b if b != 0 else "Error: Div/0"
def power_f(a, b): return a ** b
def fac_f(v):
    try: return math.factorial(int(v)) if v >= 0 else "Error"
    except: return "Error"
def square_root_f(a): return a ** 0.5 if a >= 0 else "Error"
def celsius_to_fahrenheit_f(c): return (c * 9/5) + 32
def even_or_odd_f(a): return "Even" if a % 2 == 0 else "Odd"
def positive_or_negative_f(a):
    if a < 0: return "Negative"
    elif a == 0: return "Zero"
    else: return "Positive"
def inches_to_cm_f(a): return a * 2.54
def format_seconds_f(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"
def usd_to_egp_f(usd): return usd * 54.33
def mb_to_gb_f(mb): return mb / 1024
def kmh_to_ms_f(kmh): return kmh / 3.6
def to_rad(d): return d * 3.1415926535 / 180
def sin_f(x): return math.sin(to_rad(x))
def cos_f(x): return math.cos(to_rad(x))
def tan_f(x): 
    try: return math.tan(to_rad(x))
    except: return "Error"
def cosec_f(x):
    s = sin_f(x)
    return 1/s if s != 0 else "Undefined"
def sec_f(x):
    c = cos_f(x)
    return 1/c if c != 0 else "Undefined"
def cot_f(x):
    t = tan_f(x)
    return 1/t if t != 0 and t != "Error" else "Undefined"

# ==========================================
# 2. واجهة التطبيق (Flet UI)
# ==========================================
def main(page: ft.Page):
    page.title = "AXIS Scientific"
    page.bgcolor = "#121212"
    page.window.width = 420
    page.window.height = 800
    page.horizontal_alignment = "center"
    page.scroll = "auto" # السماح بالسحب (Scroll) عشان الشاشات الصغيرة

    # المتغيرات الخاصة بالذاكرة
    numbers_list = []

    # شريط الهيستوري (History)
    history_label = ft.Text(value="", color="#888888", size=14, text_align=ft.TextAlign.RIGHT, width=380)
    
    # شاشة الإدخال
    display = ft.TextField(
        value="0", text_align=ft.TextAlign.RIGHT, width=380, 
        text_size=36, bgcolor="#1E1E1E", color="#FFFFFF", border_color="transparent", read_only=True
    )

    # ==========================================
    # 3. معالجة الضغطات والعمليات
    # ==========================================
    def button_clicked(e):
        op = e.control.data
        
        # الأزرار القياسية
        if op == "C":
            display.value = "0"
            history_label.value = ""
            numbers_list.clear()
        elif op == "=":
            try:
                expr = display.value.replace('×', '*').replace('÷', '/')
                res = eval(expr)
                history_label.value = f"{display.value} ="
                display.value = str(res)
            except:
                display.value = "Error"
        elif op in ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.', '+', '-', '*', '/', '(', ')']:
            if display.value == "0" or display.value == "Error":
                display.value = str(op)
            else:
                display.value += str(op)
        
        # الأزرار العلمية المتقدمة
        else:
            try:
                val_str = display.value
                if val_str == "Error" or val_str == "Undefined": return
                val = float(val_str)
                res = 0
                
                if op == 'AddL':
                    numbers_list.append(val)
                    history_label.value = f"List: {numbers_list}"
                    display.value = "0"
                    page.update()
                    return
                
                if op == 'AvgL':
                    if not numbers_list:
                        display.value = "Error: Empty List"
                    else:
                        res = sum(numbers_list) / len(numbers_list)
                        history_label.value = f"Avg({numbers_list}) ="
                elif op == 'MaxL':
                    if not numbers_list:
                        display.value = "Error: Empty List"
                    else:
                        res = max(numbers_list)
                        history_label.value = f"Max({numbers_list}) ="
                elif op == 'sin': res = sin_f(val)
                elif op == 'cos': res = cos_f(val)
                elif op == 'tan': res = tan_f(val)
                elif op == 'csc': res = cosec_f(val)
                elif op == 'sec': res = sec_f(val)
                elif op == 'cot': res = cot_f(val)
                elif op == '√': res = square_root_f(val)
                elif op == 'x²': res = val**2
                elif op == 'n!': res = fac_f(val)
                elif op == 'C→F': res = celsius_to_fahrenheit_f(val)
                elif op == 'In→Cm': res = inches_to_cm_f(val)
                elif op == 'Sec→Hms': res = format_seconds_f(val)
                elif op == '$→EGP': res = usd_to_egp_f(val)
                elif op == 'MB→GB': res = mb_to_gb_f(val)
                elif op == 'KM→MS': res = kmh_to_ms_f(val)
                elif op == 'E/O': res = even_or_odd_f(val)
                elif op == 'P/N': res = positive_or_negative_f(val)
                
                if op not in ['AvgL', 'MaxL']:
                    history_label.value = f"{op}({val})"
                
                # تنسيق الناتج النهائي
                formatted = f"{res:.4f}".rstrip('0').rstrip('.') if isinstance(res, float) else str(res)
                display.value = formatted

            except Exception as ex:
                display.value = "Error"

        page.update()

    # ==========================================
    # 4. تصميم ورسم الأزرار (بناءً على التحديث الجديد)
    # ==========================================
    def create_btn(btn_text, data, bgcolor="#2C2C2C", color="#FFFFFF", width=70, height=60, font_size=16):
        # تصغير الخط تلقائياً للكلمات الطويلة
        if len(btn_text) > 3: font_size = 11 
        
        return ft.ElevatedButton(
            content=ft.Text(value=btn_text, size=font_size, weight="bold"),
            data=data, on_click=button_clicked,
            bgcolor=bgcolor, color=color, 
            width=width, height=height,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=0)
        )

    # تجميع صفوف الأزرار العلمية (5 زراير في الصف)
    sci_rows = [
        ft.Row([create_btn('sin', 'sin'), create_btn('cos', 'cos'), create_btn('tan', 'tan'), create_btn('√', '√'), create_btn('x²', 'x²')], alignment="center", spacing=5),
        ft.Row([create_btn('csc', 'csc'), create_btn('sec', 'sec'), create_btn('cot', 'cot'), create_btn('n!', 'n!'), create_btn('C→F', 'C→F')], alignment="center", spacing=5),
        ft.Row([create_btn('In→Cm', 'In→Cm'), create_btn('Sec→Hms', 'Sec→Hms'), create_btn('$→EGP', '$→EGP'), create_btn('MB→GB', 'MB→GB'), create_btn('KM→MS', 'KM→MS')], alignment="center", spacing=5),
        ft.Row([create_btn('E/O', 'E/O'), create_btn('P/N', 'P/N'), create_btn('AddL', 'AddL', color="#00D2FF"), create_btn('AvgL', 'AvgL', color="#00D2FF"), create_btn('MaxL', 'MaxL', color="#00D2FF")], alignment="center", spacing=5)
    ]

    # فاصل جمالي بين الأزرار العلمية والعادية
    divider = ft.Divider(height=20, color="#333333")

    # تجميع صفوف الأزرار العادية (4 زراير في الصف - حجم أكبر)
    std_rows = [
        ft.Row([create_btn('C', 'C', bgcolor="#D32F2F", width=88), create_btn('(', '(', width=88), create_btn(')', ')', width=88), create_btn('/', '/', color="#FF9500", width=88)], alignment="center", spacing=5),
        ft.Row([create_btn('7', '7', bgcolor="#333333", width=88), create_btn('8', '8', bgcolor="#333333", width=88), create_btn('9', '9', bgcolor="#333333", width=88), create_btn('*', '*', color="#FF9500", width=88)], alignment="center", spacing=5),
        ft.Row([create_btn('4', '4', bgcolor="#333333", width=88), create_btn('5', '5', bgcolor="#333333", width=88), create_btn('6', '6', bgcolor="#333333", width=88), create_btn('-', '-', color="#FF9500", width=88)], alignment="center", spacing=5),
        ft.Row([create_btn('1', '1', bgcolor="#333333", width=88), create_btn('2', '2', bgcolor="#333333", width=88), create_btn('3', '3', bgcolor="#333333", width=88), create_btn('+', '+', color="#FF9500", width=88)], alignment="center", spacing=5),
        ft.Row([create_btn('0', '0', bgcolor="#333333", width=182), create_btn('.', '.', bgcolor="#333333", width=88), create_btn('=', '=', bgcolor="#388E3C", width=88)], alignment="center", spacing=5)
    ]

    # رسم كل العناصر على الشاشة
    page.add(history_label, display, ft.Container(height=10)) # مسافة بسيطة
    for row in sci_rows: page.add(row)
    page.add(divider)
    for row in std_rows: page.add(row)

# تشغيل التطبيق
ft.app(target=main)