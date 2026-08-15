import sys
import os
import ctypes
import customtkinter as ctk
import tkinter.ttk as ttk
import math
import calendar
import re
import time, threading
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

def bordered_optionmenu(parent, border_color="#996515", border_width=2, corner_radius=6, **kwargs):
    
    fg_color = kwargs.get("fg_color", "#202020")
    wrapper = ctk.CTkFrame(parent,
                            border_width=border_width,
                            border_color=border_color,
                            corner_radius=corner_radius,
                            fg_color=fg_color)
    kwargs.setdefault("corner_radius", corner_radius)
    kwargs.setdefault("button_hover_color", "#2b2b2b")   
    kwargs.setdefault("dropdown_hover_color", "#2b2b2b") 
    menu = ctk.CTkOptionMenu(wrapper, **kwargs)
    menu.pack(padx=border_width, pady=border_width, fill="both", expand=True)
    return wrapper, menu

def load_icons():
    icons = {}
    icons["title_icon"] = ctk.CTkImage(
        dark_image=Image.open(resource_path("Icons/Sidebar.png")).convert("RGBA"),
        size=(28, 28))
    icons["home_icon"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Home_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Home.png")).convert("RGBA"),
        size=(30,30))
    icons["home_icon_large"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Home_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Home.png")).convert("RGBA"),
        size=(70,70))
    icons["conversion"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Conversion_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Conversion.png")).convert("RGBA"),
        size=(30,30))
    icons["conversion_large"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Conversion_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Conversion.png")).convert("RGBA"),
        size=(70,70))
    icons["Single_investment"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Single_investment_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Single_investment.png")).convert("RGBA"),
        size=(30,30))
    icons["Single_investment_large"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Single_investment_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Single_investment.png")).convert("RGBA"),
        size=(70,70))
    icons["Annuity"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Annuity_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Annuity.png")).convert("RGBA"),
        size=(30,30))
    icons["Annuity_large"] = ctk.CTkImage(
        light_image = Image.open(resource_path("Icons/Annuity_light.png")).convert("RGBA"),
        dark_image = Image.open(resource_path("Icons/Annuity.png")).convert("RGBA"),
        size=(70,70))
    icons["Increasing_annuity"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Increasing_annuity_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Increasing_annuity.png")).convert("RGBA"),
            size=(30,30))
    icons["Increasing_annuity_large"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Increasing_annuity_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Increasing_annuity.png")).convert("RGBA"),
            size=(70,70))
    icons["Loan"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Loan_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Loan.png")).convert("RGBA"),
            size=(30,30))
    icons["Loan_large"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Loan_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Loan.png")).convert("RGBA"),
            size=(70,70))
    icons["About"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/About_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/About.png")).convert("RGBA"),
            size=(30,30))
    icons["About_large"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/About_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/About.png")).convert("RGBA"),
            size=(70,70))
    icons["Settings"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Settings_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Settings.png")).convert("RGBA"),
            size=(30,30))
    icons["Settings_large"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Settings_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Settings.png")).convert("RGBA"),
            size=(70,70))
    icons["Calendar"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Calendar_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Calendar.png")).convert("RGBA"),
            size=(30,30))
    icons["Calendar_large"] = ctk.CTkImage(
            light_image = Image.open(resource_path("Icons/Calendar_light.png")).convert("RGBA"),
            dark_image = Image.open(resource_path("Icons/Calendar.png")).convert("RGBA"),
            size=(70,70))
    return icons
       
def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

def bind_click_to_copy(label_widget, decimals=None):
    def copy_to_clipboard(event):
        if hasattr(label_widget, "raw_value") and label_widget.raw_value is not None:
            try:
                numeric_value = float(label_widget.raw_value)
                raw_text = label_widget.cget("text")
                if "%" in raw_text:
                    numeric_value *= 100

                if decimals is not None:
                    cleaned = f"{numeric_value:.{decimals}f}"
                else:
                    cleaned = str(numeric_value)
            except ValueError:
                return
        else:
            raw_text = label_widget.cget("text").strip()
            if raw_text == "" or all(ch in "—-–—―•.…" for ch in raw_text):
                return
            cleaned = raw_text.replace("R", "").replace("%", "").replace(" ", "").strip()
            if "," in cleaned and "." in cleaned:
                cleaned = cleaned.replace(",", "")
            elif "," in cleaned and "." not in cleaned:
                cleaned = cleaned.replace(",", ".")
            try:
                numeric_value = float(cleaned)
            except ValueError:
                return
            if decimals is not None:
                cleaned = f"{numeric_value:.{decimals}f}"

        app.clipboard_clear()
        app.clipboard_append(cleaned)
        original_color = label_widget.cget("text_color")
        label_widget.configure(text_color="#202020")
        app.after(150, lambda: label_widget.configure(text_color=original_color))

    label_widget.bind("<Button-1>", copy_to_clipboard)
    label_widget.configure(cursor="hand2")

def skeleton(mode):
    app.geometry("800x450")
    app.after(0, lambda: app.state('zoomed'))

    if mode == "Light":
        sidebar_color = "#F3F3F3"
    elif mode == "Dark":
        sidebar_color = "#202020"
    sidebar = ctk.CTkFrame(app, width=280, corner_radius=0, fg_color=sidebar_color)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    if mode == "Light":
        main_color = "#DBDBDB"
    elif mode == "Dark":
        main_color = "#2B2B2B"
    container = ctk.CTkFrame(app, fg_color=main_color)
    container.pack(side="left", fill="both", expand=True)

    return container, sidebar

def buttons(icons, container, sidebar, mode, home_page, rate_page):
    sidebar_btn = ctk.CTkLabel(sidebar, text="  Kin Calculator", 
                image=icons["title_icon"],
                text_color=("#000000", "#b18223"),
                compound="left",
                fg_color="transparent",
                bg_color = "transparent",
                font=ctk.CTkFont(size=24, weight="bold"),
                anchor="w")
    sidebar_btn.pack(pady=10, fill="x", padx=5)
    ctk.CTkFrame(sidebar, height=2, fg_color=("#000000", "#996515")).pack(padx=10, fill="x", pady=5)

    btn1 = ctk.CTkButton(sidebar,
                    text="Home",
                    text_color=("#000000", "#b18223"),
                    image = icons["home_icon"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    command=lambda: home_page.tkraise(),
                    anchor="w")
    btn1.pack(pady=5, fill="x", padx=5)

    btn2 = ctk.CTkButton(sidebar,
                    text="Rate and Date",
                    text_color=("#000000", "#b18223"),
                    image = icons["conversion"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w",
                    command=lambda: rate_page.tkraise())
    btn2.pack(pady=5, fill="x", padx=5)

    btn3 = ctk.CTkButton(sidebar,
                    text="Single Investment",
                    text_color=("#000000", "#b18223"),
                    image = icons["Single_investment"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w",
                    command=lambda: single_investment_page.tkraise())
    btn3.pack(pady=5, fill="x", padx=5)

    btn4 = ctk.CTkButton(sidebar,
                    text="Annuity",
                    text_color=("#000000", "#b18223"),
                    image = icons["Annuity"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w",
                    command= lambda: annuity_page.tkraise())
    btn4.pack(pady=5, fill="x", padx=5)

    btn5 = ctk.CTkButton(sidebar,
                    text="Increasing Annuity",
                    text_color=("#000000", "#b18223"),
                    image = icons["Increasing_annuity"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w",
                    command= lambda: increasing_annuity_page.tkraise())
    btn5.pack(pady=5, fill="x", padx=5)

    btn6 = ctk.CTkButton(sidebar,
                    text="Loan",
                    text_color=("#000000", "#b18223"),
                    image = icons["Loan"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w",
                    command= lambda: loan_page.tkraise())
    btn6.pack(pady=5, fill="x", padx=5)

    btn7 = ctk.CTkButton(sidebar,
                    text="About",
                    text_color=("#000000", "#b18223"),
                    image = icons["About"],
                    compound = "left",
                    fg_color="transparent",
                    bg_color = "transparent",
                    hover_color="#2b2b2b",
                    font=ctk.CTkFont(size=22),
                    anchor="w", 
                    command=lambda: about_page.tkraise())
    btn7.pack(pady=5, fill="x", padx=5, side="bottom")

def build_home_page(page):
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["home_icon_large"],
                            text="",
                            text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Home",
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))

    quick_actions = ctk.CTkFrame(page, fg_color="transparent")
    quick_actions.pack(expand=True, pady=(25, 0))

    home_actions = (
        ("Rate and Date", icons["conversion_large"], lambda: rate_page.tkraise()),
        ("Single Investment", icons["Single_investment_large"], lambda: single_investment_page.tkraise()),
        ("Annuity", icons["Annuity_large"], lambda: annuity_page.tkraise()),
        ("Increasing Annuity", icons["Increasing_annuity_large"], lambda: increasing_annuity_page.tkraise()),
        ("Loan", icons["Loan_large"], lambda: loan_page.tkraise()),
        ("About", icons["About_large"], lambda: about_page.tkraise()),
    )
    for index, (label, image, command) in enumerate(home_actions):
        ctk.CTkButton(quick_actions,
                      text=label,
                      text_color=("black", "#b18223"),
                      image=image,
                      border_width=3,
                      border_color="#996515",
                      compound="top",
                      anchor="center",
                      width=360,
                      height=300,
                      corner_radius=18,
                      font=ctk.CTkFont(size=22, weight="bold"),
                      fg_color="#202020",
                      hover_color="#2b2b2b",
                      command=command).grid(row=index // 3,
                                             column=index % 3,
                                             padx=12,
                                             pady=12)

def build_rate_page(page):
    var_type = ["Compounded Interest", "Simple Interest", "Continuous Interest"]
    rate_type = ["Effective", "Nominal"]
    rate_type_cont = ["Continuous"]
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["conversion_large"],
                            text="",
                            text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Rate and Date",
                                text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        corner_radius=0,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))
    calculators = ctk.CTkFrame(page, fg_color="transparent")
    calculators.pack(fill="both", expand=True, padx=20)

    rate_lay = ctk.CTkFrame(calculators, fg_color="transparent")
    rate_lay.pack(side="left", fill="both", expand=True, padx=(0, 15))
    divider = ctk.CTkFrame(calculators,
                           width=2,
                           corner_radius=0,
                           fg_color=("#000000", "#996515"))
    divider.pack(side="left", fill="y", pady=10)
    date_lay = ctk.CTkFrame(calculators, fg_color="transparent")
    date_lay.pack(side="left", fill="both", expand=True, padx=(15, 0))

    date_title = ctk.CTkLabel(date_lay, text="Date Calculator",text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=28, weight="bold"))
    date_title.pack(anchor="n", pady=(2, 6))

    def open_date_picker(target_entry):
        try:
            selected_date = datetime.strptime(target_entry.get().strip(), "%Y/%m/%d")
        except ValueError:
            selected_date = datetime.today()

        displayed_year = selected_date.year
        displayed_month = selected_date.month
        picker = ctk.CTkToplevel(page)
        picker.title("Select Date")
        picker.geometry("310x330")
        picker.resizable(False, False)
        picker.transient(page.winfo_toplevel())
        picker.grab_set()

        header = ctk.CTkFrame(picker, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))
        calendar_grid = ctk.CTkFrame(picker, fg_color="transparent")
        calendar_grid.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        month_title = ctk.CTkLabel(header, font=ctk.CTkFont(size=20, weight="bold"))

        def select_date(day):
            target_entry.delete(0, "end")
            target_entry.insert(0, f"{displayed_year:04d}/{displayed_month:02d}/{day:02d}")
            picker.destroy()

        def change_month(offset):
            nonlocal displayed_year, displayed_month
            displayed_month += offset
            if displayed_month == 0:
                displayed_month = 12
                displayed_year -= 1
            elif displayed_month == 13:
                displayed_month = 1
                displayed_year += 1
            render_calendar()

        def render_calendar():
            for child in calendar_grid.winfo_children():
                child.destroy()
            month_title.configure(text=f"{calendar.month_name[displayed_month]} {displayed_year}", text_color=("#000000", "#b18223"))
            for column, weekday in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
                ctk.CTkLabel(calendar_grid, text=weekday, text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=13, weight="bold")).grid(
                    row=0, column=column, padx=2, pady=(0, 3))
            for row, week in enumerate(calendar.monthcalendar(displayed_year, displayed_month), start=1):
                for column, day in enumerate(week):
                    if day:
                        ctk.CTkButton(calendar_grid,
                                      text=str(day),
                                      text_color=("#000000", "#b18223"),
                                      border_width=2,
                                      border_color="#996515",
                                      width=34,
                                      height=28,
                                      font=ctk.CTkFont(size=14),
                                      fg_color="#202020",
                                      hover_color="#2b2b2b",
                                      command=lambda chosen_day=day: select_date(chosen_day)).grid(
                                          row=row, column=column, padx=2, pady=2)
                    else:
                        ctk.CTkLabel(calendar_grid, text="", text_color=("#000000", "#b18223"), width=34, height=28).grid(
                            row=row, column=column, padx=2, pady=2)

        ctk.CTkButton(header,
                      text="<",
                      text_color=("#000000", "#b18223"),
                      border_width=2,
                      border_color="#996515",
                      fg_color="#202020",
                      hover_color="#2b2b2b",
                      width=35,
                      command=lambda: change_month(-1)).pack(side="left")
        month_title.pack(side="left", expand=True)
        ctk.CTkButton(header,
                      text=">",
                      text_color=("#000000", "#b18223"),
                      border_width=2,
                      border_color="#996515",
                      fg_color="#202020",
                      hover_color="#2b2b2b",
                      width=35,
                      command=lambda: change_month(1)).pack(side="right")
        render_calendar()

    def create_date_picker(label_text):
        field = ctk.CTkFrame(date_lay, fg_color="transparent")
        field.pack(anchor="n", pady=(0, 6))
        label = ctk.CTkLabel(field,
                             text=label_text,
                             text_color=("#000000", "#b18223"),
                             font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(anchor="w", pady=(0, 2))
        input_row = ctk.CTkFrame(field, fg_color="transparent")
        input_row.pack()
        entry = ctk.CTkEntry(input_row,
                             width=205,
                             font=ctk.CTkFont(size=18),
                             placeholder_text="YYYY/MM/DD")
        entry.pack(side="left", padx=(0, 5))
        calendar_button = ctk.CTkButton(input_row,
                                        text="",
                                        text_color=("#000000", "#b18223"),
                                        image=icons["Calendar"],
                                        border_width=2,
                                        border_color="#996515",
                                        width=40,
                                        height=28,
                                        fg_color="#202020",
                                        hover_color="#2b2b2b",
                                        command=lambda: open_date_picker(entry))
        calendar_button.pack(side="left")
        return entry

    start_date_entry = create_date_picker("Start Date:")
    end_date_entry = create_date_picker("End Date:")
    date_results_frame = ctk.CTkFrame(date_lay, fg_color="transparent")
    date_result_labels = {}

    def create_date_result_field(key, label, decimals):
        result_row = ctk.CTkFrame(date_results_frame, fg_color="transparent")
        result_row.pack(anchor="n", pady=1)
        title = ctk.CTkLabel(result_row,
                             text=label,
                             text_color=("#000000", "#b18223"),
                             font=ctk.CTkFont(size=16, weight="bold"),
                             width=145,
                             anchor="w")
        title.pack(side="left")
        value = ctk.CTkLabel(result_row,
                             text="-",
                             text_color=("#000000", "#b18223"),
                             font=ctk.CTkFont(size=16),
                             width=135,
                             anchor="e")
        value.pack(side="left")
        value.raw_value = None
        bind_click_to_copy(value, decimals=decimals)
        date_result_labels[key] = value

    create_date_result_field("days", "Date Difference:", 6)
    create_date_result_field("years", "Years:", 6)
    create_date_result_field("half_years", "Half-years:", 6)
    create_date_result_field("quarters", "Quarters:", 6)
    date_error_label = ctk.CTkLabel(date_lay,
                                    text="",
                                    font=ctk.CTkFont(size=16),
                                    text_color="red",
                                    wraplength=300)

    def calculate_date_difference():
        for value in date_result_labels.values():
            value.configure(text="-", text_color=("black", "#b18223"))
            value.raw_value = None
        date_error_label.configure(text="", text_color=("black", "#b18223"))
        try:
            start_date = datetime.strptime(start_date_entry.get().strip(), "%Y/%m/%d").date()
            end_date = datetime.strptime(end_date_entry.get().strip(), "%Y/%m/%d").date()
            if end_date < start_date:
                date_error_label.configure(text="End Date must be on or after the Start Date.")
                return
            days_between = (end_date - start_date).days
            years_between = days_between / 365.25
            half_years_between = years_between * 2
            quarters_between = years_between * 4
            result_values = {
                "days": (f"{days_between:,} days", days_between),
                "years": (f"{years_between:.6f}", years_between),
                "half_years": (f"{half_years_between:.6f}", half_years_between),
                "quarters": (f"{quarters_between:.6f}", quarters_between),
            }
            for key, (display_value, raw_value) in result_values.items():
                date_result_labels[key].configure(text=display_value, text_color=("black", "#b18223"))
                date_result_labels[key].raw_value = raw_value
        except ValueError:
            date_error_label.configure(text="Enter both dates in YYYY/MM/DD format.")

    date_calc_btn = ctk.CTkButton(date_lay,
                                  text="Calculate",
                                  text_color=("black", "#b18223"),
                                  border_width=2,
                                  border_color="#996515",
                                  font=ctk.CTkFont(size=20, weight="bold"),
                                  fg_color="#202020",
                                  hover_color="#2b2b2b",
                                  width=250,
                                  height=32,
                                  command=calculate_date_difference)
    date_calc_btn.pack(anchor="n", pady=(2, 1))
    date_results_frame.pack(anchor="n", pady=(4, 0))
    date_error_label.pack(anchor="n", pady=(1, 0))
    date_divider = ctk.CTkFrame(date_lay,
                                height=2,
                                corner_radius=0,
                                fg_color=("#000000", "#996515"))
    date_divider.pack(fill="x", pady=(4, 5))

    basic_calc = ctk.CTkFrame(date_lay, fg_color="transparent")
    basic_calc.pack(anchor="n")
    basic_title = ctk.CTkLabel(basic_calc, text="Basic Calculator", text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=22, weight="bold"))
    basic_title.pack(anchor="n", pady=(0, 4))
    basic_display = ctk.CTkEntry(basic_calc, width=280, height=36, font=ctk.CTkFont(size=20), justify="right")
    basic_display.pack(anchor="n", pady=(0, 4))
    keypad = ctk.CTkFrame(basic_calc, fg_color="transparent")
    keypad.pack(anchor="n")

    def basic_button_press(value):
        if value == "C":
            basic_display.delete(0, "end")
            return
        if value == "=":
            expression = basic_display.get().strip()
            if not expression or not re.fullmatch(r"[0-9+*/().\- ]+", expression):
                basic_display.delete(0, "end")
                basic_display.insert(0, "Invalid input")
                return
            try:
                result = eval(expression, {"__builtins__": {}}, {})
                if not isinstance(result, (int, float)) or not math.isfinite(result):
                    raise ValueError
                basic_display.delete(0, "end")
                basic_display.insert(0, f"{result:g}")
            except (ArithmeticError, SyntaxError, ValueError):
                basic_display.delete(0, "end")
                basic_display.insert(0, "Error")
            return
        basic_display.insert("end", value)

    button_rows = (("7", "8", "9", "/"),
                   ("4", "5", "6", "*"),
                   ("1", "2", "3", "-"),
                   ("C", "0", ".", "+"),
                   ("(", ")", "=", ""))
    for row, values in enumerate(button_rows):
        for column, value in enumerate(values):
            if value:
                display_value = {"/": "/", "*": "x"}.get(value, value)
                ctk.CTkButton(keypad,
                              text=display_value,
                              text_color=("#000000", "#b18223"),
                              border_width=2,
                              border_color="#996515",
                              width=62,
                              height=34,
                              font=ctk.CTkFont(size=18, weight="bold"),
                              fg_color="#202020",
                              hover_color="#2b2b2b",
                              command=lambda pressed=value: basic_button_press(pressed)).grid(
                                  row=row, column=column, padx=2, pady=2)

    rate_inputs = ctk.CTkFrame(rate_lay, fg_color="transparent")
    rate_inputs.pack(fill="x")
    k_rate = ctk.CTkFrame(rate_inputs, fg_color="transparent")
    k_rate.pack(side="left", fill="both", expand=True)
    u_rate = ctk.CTkFrame(rate_inputs, fg_color="transparent")
    u_rate.pack(side="left", fill="both", expand=True)
    result_frame = ctk.CTkFrame(rate_lay, fg_color="transparent")
    result_frame.pack(fill="x", pady=(15, 0))
    k_title = ctk.CTkLabel(k_rate, text="Known Rate", text_color=("black", "#b18223"), font=ctk.CTkFont(size=32, weight="bold"))
    k_label1_1 = ctk.CTkLabel(k_rate,
                            text="Type Investment:", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    k_list1_1_wrap, k_list1_1 = bordered_optionmenu(k_rate,
                                values=var_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    k_label1_2 = ctk.CTkLabel(k_rate,
                            text="Interest Rate:", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    k_list1_2_wrap, k_list1_2 = bordered_optionmenu(k_rate,
                                values=rate_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    k_label1 = ctk.CTkLabel(k_rate,
                            text="Interest Rate (i)(%):", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold")) 
    k_entry1 = ctk.CTkEntry(k_rate, width=250, font=ctk.CTkFont(size=20)) 
    k_label2 = ctk.CTkLabel(k_rate,
                            text="Period (p):", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold")) 
    k_entry2 = ctk.CTkEntry(k_rate, width=250, font=ctk.CTkFont(size=20))
    k_label3 = ctk.CTkLabel(k_rate,
                            text="Year (n):", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold")) 
    k_entry3 = ctk.CTkEntry(k_rate, width=250, font=ctk.CTkFont(size=20)) 
    k_title.pack(anchor="n", pady=2)
    k_label1_1.pack(anchor="n", pady=2)
    k_list1_1_wrap.pack(anchor="n", pady=(0,10))
    k_label1_2.pack(anchor="n", pady=2)
    k_list1_2_wrap.pack(anchor="n", pady=(0,10))
    k_label1.pack(anchor="n", pady=(0, 2))
    k_entry1.pack(anchor="n", pady=(0, 10))
    k_label2.pack(anchor="n", pady=(0, 2))
    k_entry2.pack(anchor="n", pady=(0, 10))
    k_label3.pack(anchor="n", pady=(0, 2))
    k_entry3.pack(anchor="n", pady=(0, 10))
    u_title = ctk.CTkLabel(u_rate, text="Unknown Rate", text_color=("black", "#b18223"), font=ctk.CTkFont(size=32, weight="bold"))
    u_label1_1 = ctk.CTkLabel(u_rate,
                            text="Type Investment:", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    u_list1_1_wrap, u_list1_1 = bordered_optionmenu(u_rate,
                                values=var_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    u_label1_2 = ctk.CTkLabel(u_rate,
                            text="Interest Rate:", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    u_list1_2_wrap, u_list1_2 = bordered_optionmenu(u_rate,
                                values=rate_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    u_label2 = ctk.CTkLabel(u_rate,
                            text="Period (p):", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold")) 
    u_entry2 = ctk.CTkEntry(u_rate, width=250, font=ctk.CTkFont(size=20)) 
    u_label3 = ctk.CTkLabel(u_rate,
                            text="Year (n):", text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold")) 
    u_entry3 = ctk.CTkEntry(u_rate, width=250, font=ctk.CTkFont(size=20)) 
    
    u_title.pack(anchor="n", pady=2)
    u_label1_1.pack(anchor="n", pady=2)
    u_list1_1_wrap.pack(anchor="n", pady=(0,10))
    u_label1_2.pack(anchor="n", pady=2)
    u_list1_2_wrap.pack(anchor="n", pady=(0,10))
    u_label2.pack(anchor="n", pady=(0, 2))
    u_entry2.pack(anchor="n", pady=(0, 10))
    u_label3.pack(anchor="n", pady=(0, 2))
    u_entry3.pack(anchor="n", pady=(0, 20))
    
    r_title = ctk.CTkLabel(result_frame, text="Results", text_color=("black", "#b18223"), font=ctk.CTkFont(size=32, weight="bold"))
    r_title.pack(anchor="n", pady=2)
    result_labels = {}
    def create_result_field(key, label):
        frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        frame.pack(anchor="n", pady=3)
        title = ctk.CTkLabel(frame, text=label, text_color=("black", "#b18223"), font=ctk.CTkFont(size=18), anchor="w", width=180)
        title.pack(anchor="n")
        value = ctk.CTkLabel(frame, text="—", text_color=("black", "#b18223"), font=ctk.CTkFont(size=18), anchor="center", width=200)
        value.pack(anchor="n")
        bind_click_to_copy(value, decimals=6)
        result_labels[key] = value
    create_result_field("i_u", "Unknown Interest Rate:")

    def calculated():
        k_investment_type = k_list1_1.get()
        u_investment_type = u_list1_1.get()
        k_rate_type = k_list1_2.get()
        u_rate_type = u_list1_2.get()
        k_rate = float(k_entry1.get()) / 100
        k_period = float(k_entry2.get())
        u_period = float(u_entry2.get())
        k_year = float(k_entry3.get())
        u_year = float(u_entry3.get())
        if k_investment_type == "Compounded Interest":
            if k_rate_type == "Nominal":
                i_k = k_rate / k_period
            else:
                i_k = k_rate
            known = (1 + i_k)**(k_period * k_year)
        elif k_investment_type == "Simple Interest":
            i_k = k_rate
            known = (1 + (i_k * k_period * k_year))
        else:
            i_k = k_rate
            known = math.exp(k_year * i_k)

        if u_investment_type == "Compounded Interest":
            if u_rate_type == "Nominal":
                i_u = u_period * (((known)**(1 / (u_period * u_year))) - 1)
            else:
                i_u = ((known)**(1 / (u_period * u_year)) - 1)
        elif u_investment_type == "Simple Interest":
            i_u = (known - 1) / (u_year * u_period)
        else:
            i_u = math.log(known) / u_year
        display_map = {"i_u": (i_u, lambda v: f"{v*100:.4f}%")}
        for key, (val, fmt) in display_map.items():
                if val is not None:
                    result_labels[key].configure(text=fmt(val), text_color=("black", "#b18223"))
                    result_labels[key].raw_value = val
                else:
                    result_labels[key].configure(text="—", text_color=("black", "#b18223"))
                    result_labels[key].raw_value = None
        
    calc_btn = ctk.CTkButton(u_rate,
                            text="Calculate",
                            border_width=2,
                            border_color="#996515",
                            text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            width=250,
                            command=calculated)
    calc_btn.pack(anchor="n", pady=(22, 2))

def build_single_investment_page(page):
    var = ["FV", "PV", "i", "n", "p"]
    var_cont = ["FV", "PV", "δ", "n"]
    var_type = ["Compounded Interest", "Simple Interest", "Continuous Interest"]
    rate_type = ["Effective", "Nominal"]
    rate_type_cont = ["Continuous"]
    
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["Single_investment_large"],
                            text="", text_color=("#000000", "#b18223"),)
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Single Investment",
                                text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))

    tab = ctk.CTkTabview(page,
                        fg_color="transparent",
                        corner_radius=15,
                        segmented_button_fg_color="#202020",
                        segmented_button_selected_color="#2b2b2b",
                        segmented_button_selected_hover_color="#2b2b2b",
                        segmented_button_unselected_color="#202020",
                        text_color="#b18223")
    tab.pack(fill="both", expand=True, padx=0, pady=0)
    tab._segmented_button.configure(font=ctk.CTkFont(size=20),
                                    height=40)
    tab_1 = tab.add("Summary")
    tab_2 = tab.add("Graph")
    tab_3 = tab.add("Amortization")
    selected_solve_for = "PV"
    field_frames = {}
    entries = {}

    layout = ctk.CTkFrame(tab_1, fg_color="transparent")
    layout.pack(fill="both", expand=True)
    left = ctk.CTkFrame(layout, fg_color="transparent", width=270)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    sep1 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep1.pack(side="left", fill="y")
    middle = ctk.CTkFrame(layout, fg_color="transparent", width=550)
    middle.pack(side="left", fill="y")
    middle.pack_propagate(False)
    sep2 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep2.pack(side="left", fill="y")
    right = ctk.CTkFrame(layout, fg_color="transparent")
    right.pack(side="right", fill="y")

    result_title = ctk.CTkLabel(right,
                            text="Summary & Solutions",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    result_title.pack(anchor="n", pady=(0, 3))
    error_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont(size=16), text_color="red", wraplength=380)
    error_label.pack(anchor="n", pady=(0, 1))
    result_frame = ctk.CTkFrame(right, fg_color="transparent")
    result_frame.pack(anchor="n")
    chart_frame = ctk.CTkFrame(right, fg_color="transparent")
    chart_frame.pack(anchor="n", fill="both", expand=True)
    chart_canvas_holder = [None]
    result_labels = {}
    graph_title = ctk.CTkLabel(middle,
                            text="Graph",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    graph_title.pack(anchor="n", pady=(0, 3))
    graph_frame = ctk.CTkFrame(middle, fg_color="transparent")
    graph_frame.pack(fill="both", expand=True)
    middle_canvas_holder = [None]
    graph_placeholder = ctk.CTkLabel(graph_frame,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    graph_placeholder.pack(expand=True)

    def create_result_field(key, label):
        frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        frame.pack(anchor="w", pady=3)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        title = ctk.CTkLabel(frame, text=label, text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=18), anchor="w", width=180)
        title.grid(row=0, column=0, sticky="w")
        value = ctk.CTkLabel(frame, text="—", text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=18), anchor="e", width=200)
        value.grid(row=0, column=1, sticky="e")
        bind_click_to_copy(value, decimals=6)
        result_labels[key] = value
    create_result_field("interest_type", "Interest Type:")
    create_result_field("rate_type", "Rate Type:")
    create_result_field("i", "Rate:")
    create_result_field("PV", "Present Value:")
    create_result_field("FV", "Future Value:")
    create_result_field("n", "Years:")
    create_result_field("p", "Period:")
    create_result_field("np", "Compounding Periods:")
    create_result_field("interest_earned", "Interest Earned:")

    def get_active_fields():
        investment_type = list1_1.get()
        if investment_type == "Continuous Interest":
            return {"FV": "Future Value (FV)(Rand):",
                    "PV": "Present Value (PV)(Rand):",
                    "δ": "Interest Rate (δ)(%):",
                    "n": "Years (n):"}
        else:
            return {"PV": "Present Value (PV)(Rand):",
            "FV": "Future Value (FV)(Rand):",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}

    def create_field(parent, key, label_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(anchor="w")
        label = ctk.CTkLabel(frame,
                            text=label_text,
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", pady=(0, 2))
        entry = ctk.CTkEntry(frame, width=250, font=ctk.CTkFont(size=20))
        entry.pack(anchor="w", pady=(0, 10))
        field_frames[key] = frame
        entries[key] = entry

    def rebuild_fields():
        for frame in field_frames.values():
            frame.destroy()
        field_frames.clear()
        entries.clear()
        active_fields = get_active_fields()
        for key, label in active_fields.items():
            if key != selected_solve_for:
                create_field(frame1, key, label)

    def update_solve_for(choice):
        nonlocal selected_solve_for
        selected_solve_for = choice
        rebuild_fields()

    def update_rate_type(choice):
        if choice == "Nominal":
            list1_2.configure(values=["FV", "PV", "i", "n"])
            if list1_2.get() == "p":
                list1_2.set("FV")
                update_solve_for("FV")
        else:
            list1_2.configure(values=["FV", "PV", "i", "n", "p"])

    def update_rate_options(investment_type):
        if investment_type == "Simple Interest":
            list1_3.configure(values=["Simple Interest"])
            list1_3.set("Simple Interest")

    label1_2 = ctk.CTkLabel(left,
                            text="To solve for:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_2_wrap, list1_2 = bordered_optionmenu(left, values=var, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_solve_for)
    label1_3 = ctk.CTkLabel(left,
                            text="Interest Rate:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_3_wrap, list1_3 = bordered_optionmenu(left, values=rate_type, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16),
                                command=update_rate_type)
    
    def list1_2_change(choice):
        if choice == "Continuous Interest":
            nonlocal selected_solve_for
            list1_2.configure(values=var_cont, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type_cont, text_color=("black", "#b18223"))
            if selected_solve_for not in var_cont:
                selected_solve_for = "PV"
                list1_2.set("PV")
            list1_3.set(rate_type_cont[0])
        else:
            list1_2.configure(values=var, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type, text_color=("black", "#b18223"))
            if selected_solve_for not in var:
                selected_solve_for = "PV"
                list1_2.set("PV")
            list1_3.set(rate_type[0])
        rebuild_fields()

    label1_1 = ctk.CTkLabel(left,
                            text="Type Investment:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_1_wrap, list1_1 = bordered_optionmenu(left,
                                values=var_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                command=lambda choice: (list1_2_change(choice), list1_2.set("PV"), update_rate_options(choice)),
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_1.pack(anchor="w", pady=2)
    list1_1_wrap.pack(anchor="w", pady=(0,10))
    label1_2.pack(anchor="w", pady=2)
    list1_2_wrap.pack(anchor="w", pady=(0,10))
    label1_3.pack(anchor="w", pady=2)
    list1_3_wrap.pack(anchor="w", pady=(0,10))

    frame1 = ctk.CTkFrame(left, fg_color="transparent")
    frame1.pack(anchor="w", fill="x")
    fields = {"PV": "Present Value (PV)(Rand):",
            "FV": "Future Value (FV)(Rand):",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}
    list1_2.set("PV")
    selected_solve_for = "PV"
    rebuild_fields()

    def update_chart(pv, interest):
        if chart_canvas_holder[0] is not None:
            chart_canvas_holder[0].get_tk_widget().destroy()
            chart_canvas_holder[0] = None
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        fig = plt.Figure(figsize=(3.5, 3.5), facecolor=bg_color, edgecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_axis_off()
        sizes = [pv, interest]
        colors = ["#202020", "#996515"]
        wedges, texts, autotexts = ax.pie(sizes, colors=colors,
                            startangle=90, wedgeprops=None, autopct="%1.2f%%", pctdistance=0.5)
        legend = ["PV", "Interest"]
        legend = ax.legend(wedges, legend, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10, framealpha=0)
        legend_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pie_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        for text in legend.get_texts():
            text.set_color(legend_text_color)
            text.set_weight("bold")
        for text in texts:
            text.set_color(pie_text_color)
            text.set_fontsize(13)
        for autotext in autotexts:
            autotext.set_color(pie_text_color)
            autotext.set_fontsize(11)
            autotext.set_weight("bold")
        fig.patch.set_facecolor(bg_color)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0, bd=0)
        canvas.draw()
        widget.pack(fill="both", expand=True)
        chart_canvas_holder[0] = canvas
        plt.close(fig)

    def update_middle_graph(PV, FV, n , investment_type, rate_type, i=None, p=None, δ=None):
        for widget in graph_frame.winfo_children():
            widget.destroy()
        if middle_canvas_holder[0] is not None:
            middle_canvas_holder[0].get_tk_widget().destroy()
            middle_canvas_holder[0] = None
        graph_frame.pack_propagate(False)
        graph_frame.configure(width=550, height=400)
        steps = max(int(n * 100), 100)
        xs = [n * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if investment_type == "Simple Interest":
                ys.append(PV * (1 + i * x * p))
            elif investment_type == "Compounded Interest":
                if rate_type == "Nominal":
                    ys.append(PV * (1 + i / p) ** (x * p))
                else:
                    ys.append(PV * (1 + i) ** (x * p))
            else:
                ys.append(PV * math.exp(δ * x))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame.winfo_width()
        if pixel_width <= 1:
            pixel_width = 550
        fig_width_inches = (pixel_width - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, 4), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Years (n)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.2, bottom=0.20)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        middle_canvas_holder[0] = canvas
        plt.close(fig)
    layout2 = ctk.CTkFrame(tab_2, fg_color="transparent")
    layout2.pack(fill="both", expand=True)
    graph_frame2 = ctk.CTkFrame(layout2, fg_color="transparent")
    graph_frame2.pack(fill="both", expand=True)
    tab_2_canvas_holder = [None]
    tab2_placeholder = ctk.CTkLabel(graph_frame2,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    tab2_placeholder.pack(expand=True)
    def graph(PV, FV, n , investment_type, rate_type, i=None, p=None, δ=None):
        for widget in graph_frame2.winfo_children():
            widget.destroy()
        if tab_2_canvas_holder[0] is not None:
            tab_2_canvas_holder[0].get_tk_widget().destroy()
            tab_2_canvas_holder[0] = None
        steps = max(int(n * 100), 100)
        xs = [n * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if investment_type == "Simple Interest":
                ys.append(PV * (1 + i * x * p))
            elif investment_type == "Compounded Interest":
                if rate_type == "Nominal":
                    ys.append(PV * (1 + i / p) ** (x * p))
                else:
                    ys.append(PV * (1 + i) ** (x * p))
            else:
                ys.append(PV * math.exp(δ * x))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame2.winfo_width()
        pixel_height = graph_frame2.winfo_height()
        if pixel_width <= 1:
            pixel_width = 1200
        if pixel_height <= 1:
            pixel_height = 600
        fig_width_inches = (pixel_width - 20) / 100
        fig_height_inches = (pixel_height - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, fig_height_inches), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_title("Investment Growth Over Time", color=text_color, fontsize=14, fontweight="bold", pad=10)
        ax.grid(True, color=text_color, alpha=0.2, linestyle='--', linewidth=0.5)
        line, = ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Years (n)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.1)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        import numpy as np
        xdata = np.array(xs)
        ydata = np.array(ys)
        annot = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.4", fc=bg_color, ec="#202020", lw=1.5),
                            arrowprops=dict(arrowstyle="->", color="#202020"),
                            color=text_color, fontsize=10, zorder=10)
        annot.set_visible(False)
        last_idx = -1
        def on_hover(event):
            nonlocal last_idx
            if event.inaxes != ax or event.xdata is None:
                if annot.get_visible():
                    annot.set_visible(False)
                    canvas.draw_idle()
                return
            idx = np.searchsorted(xdata, event.xdata, side='left')
            if idx >= len(xdata):
                idx = len(xdata) - 1
            if idx > 0 and (event.xdata - xdata[idx-1]) < (xdata[idx] - event.xdata):
                idx -= 1
            if idx == last_idx and annot.get_visible():
                return
            last_idx = idx
            x_disp, y_disp = ax.transData.transform((xdata[idx], ydata[idx]))
            dist = ((event.x - x_disp)**2 + (event.y - y_disp)**2)**0.5
            if dist < 35:
                annot.xy = (xdata[idx], ydata[idx])
                annot.set_text(f"n = {xdata[idx]:.2f}\nFV = R {ydata[idx]:,.2f}")
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            canvas.draw_idle()
        canvas.mpl_connect("motion_notify_event", on_hover)
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        tab_2_canvas_holder[0] = canvas
        plt.close(fig)

    layout3 = ctk.CTkFrame(tab_3, fg_color="transparent")
    layout3.pack(fill="both", expand=True)
    style = ttk.Style()
    style.theme_use("default")
    current_mode = ctk.get_appearance_mode()
    bg_color = "#2B2B2B" if current_mode == "Dark" else "#DBDBDB"
    text_color = "#b18223" if current_mode == "Dark" else "black"
    header_bg = "#202020" if current_mode == "Dark" else "#F3F3F3"
    style.configure("Treeview", rowheight=35, borderwidth=0, font=("Arial", 14), background=bg_color,
                    foreground=text_color, fieldbackground=bg_color)
    style.map("Treeview", background=[("selected", "#202020")])
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"), borderwidth=0, relief="flat",
                    background=header_bg, foreground=text_color)
    style.map("Treeview.Heading", background=[("active", header_bg)])
    columns = ("Period", "Opening Balance", "Interest Earned", "Closing Balance")
    tree = ttk.Treeview(layout3, columns=columns, show="headings")
    column_alignments = {
        "Period": "center", 
        "Opening Balance": "center", 
        "Interest Earned": "center", 
        "Closing Balance": "center"}
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=column_alignments[col])
    def resize_columns_by_ratio(event):
        total_avail_width = event.width
        column_widths = {"Period": 1, 
                        "Opening Balance": 3, 
                        "Interest Earned": 3, 
                        "Closing Balance": 3}
        total_parts = sum(column_widths.values())
        for col, ratio in column_widths.items():
                calculated_width = int(total_avail_width * (ratio / total_parts))
                tree.column(col, width=calculated_width, stretch=False)
    tree.bind("<Configure>", resize_columns_by_ratio)
    scrollbar = ttk.Scrollbar(layout3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    def populate_table(PV, n, p, i, δ, investment_type, rate_type):
        tree.delete(*tree.get_children())
        if investment_type == "Continuous Interest":
            total_periods = int(math.ceil(n)) if n is not None else 0
        else:
            total_periods = int(math.ceil(n * p)) if n is not None and p is not None else 0
        current_balance = PV
        for k in range(1, total_periods + 1):
            if investment_type == "Simple Interest":
                closing_balance = PV * (1 + i * k)
            elif investment_type == "Compounded Interest":
                if rate_type == "Nominal":
                    closing_balance = current_balance * (1 + i / p)
                else:
                    closing_balance = current_balance * (1 + i)
            else:
                closing_balance = PV * math.exp(δ * k)
            if k == total_periods and investment_type != "Continuous Interest":
                exact_periods = n * p
                if k > exact_periods:
                    if investment_type == "Simple Interest":
                        closing_balance = PV * (1 + i * exact_periods)
                    elif investment_type == "Compounded Interest":
                        if rate_type == "Nominal":
                            closing_balance = PV * (1 + i / p)**exact_periods
                        else:
                            closing_balance = PV * (1 + i)**exact_periods
            if k == total_periods and investment_type == "Continuous Interest":
                exact_periods = n
                if k > exact_periods:
                    closing_balance = PV * math.exp(δ * exact_periods)
            interest = closing_balance - current_balance
            tree.insert("", "end", values=(k, 
                                            f"R {current_balance:,.2f}".replace(",", " "), 
                                            f"R {interest:,.2f}", 
                                            f"R {closing_balance:,.2f}".replace(",", " ")))
            current_balance = closing_balance
    
    def calculated():
        error_label.configure(text="", text_color=("#000000", "#b18223"),)
        investment_type = list1_1.get()
        rate_type = list1_3.get()
        solve_for = selected_solve_for
        values = {}
        for key, entry in entries.items():
            raw = entry.get().strip()
            if raw == "":
                values[key] = None
            else:
                try:
                    values[key] = float(raw)
                except ValueError:
                    print(f"Invalid input for {key}: {raw}")
                    return
        PV = values.get("PV")
        FV = values.get("FV")
        i = values.get("i")
        n = values.get("n")
        p = values.get("p")
        δ = values.get("δ")
        np_value = None
        interest_earned = None
        try:
            if i is not None:
                i = i / 100
            if δ is not None:
                δ = δ / 100
            if investment_type == "Simple Interest":
                if solve_for == "FV":
                    result = PV * (1 + i * n * p)
                    FV = result
                elif solve_for == "PV":
                    result = FV / (1 + i * n * p)
                    PV = result
                elif solve_for == "i":
                    result = (FV / PV - 1) / (n * p) * 100
                    i = result / 100
                elif solve_for == "n":
                    result = (FV / PV - 1) / (i * p)
                    n = result
                elif solve_for == "p":
                    result = (FV / PV - 1) / (i * n)
                    p = result
            elif investment_type == "Compounded Interest":
                if rate_type == "Nominal":
                    if solve_for == "FV":
                        result = PV * (1 + i / p)**(n * p)
                        FV = result
                    elif solve_for == "PV":
                        result = FV / (1 + i / p)**(n * p)
                        PV = result
                    elif solve_for == "n":
                        result = math.log(FV / PV) / (p * math.log(1 + i / p))
                        n = result
                    elif solve_for == "i":
                        result = p * ((FV / PV)**(1 / (n*p)) - 1) * 100
                        i = result / 100
                else:
                    if solve_for == "FV":
                        result = PV * (1 + i)**(n * p)
                        FV = result
                    elif solve_for == "PV":
                        result = FV / (1 + i)**(n * p)
                        PV = result
                    elif solve_for == "n":
                        result = math.log(FV / PV) / (p * math.log(1 + i))
                        n = result
                    elif solve_for == "i":
                        result = ((FV / PV)**(1 / (n*p)) - 1) * 100
                        i = result / 100
                    elif solve_for == "p":
                        result = math.log(FV / PV) / (n * math.log(1 + i))
                        p = result
            else:
                if solve_for == "FV":
                    result = PV * math.exp(δ * n)
                    FV = result
                elif solve_for == "PV":
                    result = FV / math.exp(δ * n)
                    PV = result
                elif solve_for == "δ":
                    result = math.log(FV / PV) / n * 100
                    δ = result / 100
                elif solve_for == "n":
                    result = math.log(FV / PV) / δ
                    n = result
            if n is not None and p is not None:
                np_value = n * p
            if FV is not None and PV is not None:
                interest_earned = FV - PV
            result_labels["interest_type"].configure(text=investment_type, text_color=("#000000", "#b18223"))
            result_labels["rate_type"].configure(text=rate_type, text_color=("#000000", "#b18223"))
            display_map = {"PV": (PV,  lambda v: f"R {v:,.2f}"),
                        "FV": (FV,  lambda v: f"R {v:,.2f}"),
                        "i": (i if i is not None else δ,   lambda v: f"{v*100:.4f}%"),
                        "n": (n,   lambda v: f"{v}"),
                        "p": (p,   lambda v: f"{v:.0f}"),
                        "np": (np_value, lambda v: f"{v:.0f}"),
                        "interest_earned": (interest_earned,  lambda v: f"R {v:,.2f}")}
            for key, (val, fmt) in display_map.items():
                if val is not None:
                    result_labels[key].configure(text=fmt(val), text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = val
                else:
                    result_labels[key].configure(text="—", text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = None
            if solve_for == "δ":
                result_labels["i"].configure(text=f"{result:.4f}%")
            elif solve_for == "i":
                result_labels[solve_for].configure(text=f"{result:.4f}%")
            elif solve_for == "n":
                result_labels[solve_for].configure(text=f"{result:.4f}")
            elif solve_for == "FV" or solve_for == "PV":
                result_labels[solve_for].configure(text=f"R {result:,.2f}")
            elif solve_for == "p" or solve_for == "np":
                result_labels[solve_for].configure(text=f"{result:.0f}")
            for key, label in result_labels.items():
                if key in ("interest_type", "rate_type"):
                    continue
                label.configure(font=ctk.CTkFont(size=18))
            solved_key = "i" if solve_for == "δ" else solve_for
            if solved_key in result_labels:
                result_labels[solved_key].configure(font=ctk.CTkFont(size=18, weight="bold"))
            if PV is not None and interest_earned is not None and interest_earned > 0:
                update_chart(PV, interest_earned)
            update_middle_graph(PV=PV, FV=FV, n=n, investment_type=investment_type,
                                rate_type=rate_type, i=i, p=p, δ=δ)
            graph(PV=PV, FV=FV, n=n, investment_type=investment_type,
                                rate_type=rate_type, i=i, p=p, δ=δ)
            populate_table(PV=PV, n=n, p=p, i=i, δ=δ, investment_type=investment_type, rate_type=rate_type)
        except ZeroDivisionError:
            error_label.configure(text="Error: Division with zero. Check inputs.")
        except ValueError as e:
            error_label.configure(text="Error: Invalid Calculation. Check inputs.")
        except Exception as e:
            error_label.configure(text=f"Error: {str(e)}")

    calc_btn = ctk.CTkButton(left,
                            text="Calculate",
                            border_width=2,
                            border_color="#996515",
                            text_color=("black", "#b18223"),
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            width=250,
                            command=calculated)
    calc_btn.pack(anchor="w", pady=(15, 10))
    
def build_annuity_page(page):
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["Annuity_large"],
                            text="", 
                            text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Annuity",
                                text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))
    tab = ctk.CTkTabview(page,
                        fg_color="transparent",
                        corner_radius=15,
                        segmented_button_fg_color="#202020",
                        segmented_button_selected_color="#2b2b2b",
                        segmented_button_selected_hover_color="#2b2b2b",
                        segmented_button_unselected_color="#202020",
                        text_color="#b18223")
    tab.pack(fill="both", expand=True, padx=0, pady=0)
    tab._segmented_button.configure(font=ctk.CTkFont(size=20), height=40)
    tab_1 = tab.add("Summary")
    tab_2 = tab.add("Graph")
    tab_3 = tab.add("Amortization")
    var = ["X", "FV", "PV", "i", "n", "p"]
    var_cont = ["X", "FV", "PV", "δ", "n"]
    var_type = ["Compounded Interest", "Continuous Interest"]
    rate_type = ["Effective", "Nominal"]
    rate_type_cont = ["Continuous"]
    payment_type = ["Arrears", "Advance"]
    known = ["FV", "PV"]
    selected_solve_for = "X"
    field_frames = {}
    entries = {}

    layout = ctk.CTkFrame(tab_1, fg_color="transparent")
    layout.pack(fill="both", expand=True)
    left = ctk.CTkFrame(layout, fg_color="transparent", width=270)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    sep1 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep1.pack(side="left", fill="y")
    middle = ctk.CTkFrame(layout, fg_color="transparent", width=550)
    middle.pack(side="left", fill="y")
    middle.pack_propagate(False)
    sep2 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep2.pack(side="left", fill="y")
    right = ctk.CTkFrame(layout, fg_color="transparent")
    right.pack(side="right", fill="y")

    result_title = ctk.CTkLabel(right,
                            text="Summary & Solutions",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    result_title.pack(anchor="n", pady=(0, 3))
    error_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont(size=16), text_color="red", wraplength=380)
    error_label.pack(anchor="n", pady=(0, 1))
    result_frame = ctk.CTkFrame(right, fg_color="transparent")
    result_frame.pack(anchor="n")
    chart_frame = ctk.CTkFrame(right, fg_color="transparent")
    chart_frame.pack(anchor="n", fill="both", expand=True)
    chart_canvas_holder = [None]
    result_labels = {}
    graph_title = ctk.CTkLabel(middle,
                            text="Graph",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    graph_title.pack(anchor="n", pady=(0, 3))
    graph_frame = ctk.CTkFrame(middle, fg_color="transparent")
    graph_frame.pack(fill="both", expand=True)
    middle_canvas_holder = [None]
    graph_placeholder = ctk.CTkLabel(graph_frame,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    graph_placeholder.pack(expand=True)

    def create_result_field(key, label):
        frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        frame.pack(anchor="w", pady=3)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        title = ctk.CTkLabel(frame, text=label,text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=18), anchor="w", width=180)
        title.grid(row=0, column=0, sticky="w")
        value = ctk.CTkLabel(frame, text="—",text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=18), anchor="e", width=200)
        value.grid(row=0, column=1, sticky="e")
        bind_click_to_copy(value, decimals=6)
        result_labels[key] = value
    create_result_field("interest_type", "Interest Type:")
    create_result_field("rate_type", "Rate Type:")
    create_result_field("i", "Rate:")
    create_result_field("PV", "Present Value:")
    create_result_field("FV", "Future Value:")
    create_result_field("X", "Payment:")
    create_result_field("total_payments", "Total Payments:")
    create_result_field("n", "Years:")
    create_result_field("p", "Period:")
    create_result_field("np", "Compounding Periods:")
    create_result_field("interest_earned", "Interest Earned:")

    def get_active_fields():
        investment_type = list1_1.get()
        if investment_type == "Continuous Interest":
            return {"X": "Payment (X)(Rand):",
                    "FV": "Future Value (FV)(Rand):",
                    "PV": "Present Value (PV)(Rand):",
                    "δ": "Interest Rate (δ)(%):",
                    "n": "Years (n):"}
        else:
            return {"X": "Payment (X)(Rand):",
            "PV": "Present Value (PV)(Rand):",
            "FV": "Future Value (FV)(Rand):",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}

    def create_field(parent, key, label_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(anchor="w")
        label = ctk.CTkLabel(frame,
                            text=label_text,
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", pady=(0, 1))
        entry = ctk.CTkEntry(frame, width=250, font=ctk.CTkFont(size=20))
        entry.pack(anchor="w", pady=(0, 3))
        field_frames[key] = frame
        entries[key] = entry

    def rebuild_fields():
        for frame in field_frames.values():
            frame.destroy()
        field_frames.clear()
        entries.clear()
        active_fields = get_active_fields()
        keys_to_skip = [selected_solve_for]
        if selected_solve_for == "FV":
            keys_to_skip.append("PV")
        elif selected_solve_for == "PV":
            keys_to_skip.append("FV")
        if selected_solve_for not in ("FV", "PV"):
            if known_selection == "FV":
                keys_to_skip.append("PV")
            elif known_selection == "PV":
                keys_to_skip.append("FV")
        for key, label in active_fields.items():
            if key not in keys_to_skip:
                create_field(frame1, key, label)
        arrange_fields()

    def update_solve_for(choice):
        nonlocal selected_solve_for
        selected_solve_for = choice
        if selected_solve_for in ("FV", "PV"):
            label1_5.pack_forget()
            list1_5_wrap.pack_forget()
        else:
            label1_5.pack(anchor="w", before=frame1)
            list1_5_wrap.pack(anchor="w", pady=(0, 2), before=frame1)
        rebuild_fields()

    def update_rate_type(choice):
        if choice == "Nominal":
            list1_2.configure(values=["X", "FV", "PV", "i", "n"])
            if list1_2.get() == "p":
                list1_2.set("X")
                update_solve_for("X")
        else:
            list1_2.configure(values=["X", "FV", "PV", "i", "n", "p"])
        rebuild_fields()

    known_selection = "FV" 
    def arrange_fields():
        for frame in field_frames.values():
            frame.pack_forget()
        active = get_active_fields()
        order = [k for k in active.keys() if k != selected_solve_for]
        for key in order:
            if key not in field_frames:
                continue
            if selected_solve_for == "FV" and key == "PV":
                continue
            if selected_solve_for == "PV" and key == "FV":
                continue
            if selected_solve_for not in ("FV", "PV"):
                if (key == "PV" and selected_solve_for not in ("FV", "PV") and known_selection == "FV"):
                    continue
                if (key == "FV" and selected_solve_for not in ("FV", "PV") and known_selection == "PV"):
                    continue
            field_frames[key].pack(anchor="w")

    def update_known(choice):
        nonlocal known_selection
        known_selection = choice
        arrange_fields()
        rebuild_fields()

    label1_4 = ctk.CTkLabel(left,
                            text="Payment Type:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_4_wrap, list1_4 = bordered_optionmenu(left, values=payment_type, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020",
                                button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_2 = ctk.CTkLabel(left,
                            text="To solve for:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_2_wrap, list1_2 = bordered_optionmenu(left, values=var, text_color=("black", "#b18223"),font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_solve_for)
    label1_3 = ctk.CTkLabel(left,
                            text="Interest Rate:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_3_wrap, list1_3 = bordered_optionmenu(left, values=rate_type, text_color=("black", "#b18223"),font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16),
                                command=update_rate_type)
    label1_5 = ctk.CTkLabel(left,
                            text="Known:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_5_wrap, list1_5 = bordered_optionmenu(left, values=known, text_color=("black", "#b18223"),font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_known)
    def list1_2_change(choice):
        if choice == "Continuous Interest":
            nonlocal selected_solve_for
            list1_2.configure(values=var_cont, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type_cont, text_color=("black", "#b18223"))
            if selected_solve_for not in var_cont:
                selected_solve_for = "X"
                list1_2.set("X")
            list1_3.set(rate_type_cont[0])
        else:
            list1_2.configure(values=var, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type, text_color=("black", "#b18223"))
            if selected_solve_for not in var:
                selected_solve_for = "X"
                list1_2.set("X")
            list1_3.set(rate_type[0])
        rebuild_fields()
    
    label1_4.pack(anchor="w")
    list1_4_wrap.pack(anchor="w", pady=(0,2))
    label1_1 = ctk.CTkLabel(left,
                            text="Type Investment:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_1_wrap, list1_1 = bordered_optionmenu(left,
                                values=var_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                command=lambda choice: (list1_2_change(choice), list1_2.set("X")),
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_1.pack(anchor="w")
    list1_1_wrap.pack(anchor="w", pady=(0,2))
    label1_2.pack(anchor="w")
    list1_2_wrap.pack(anchor="w", pady=(0,2))
    label1_3.pack(anchor="w")
    list1_3_wrap.pack(anchor="w", pady=(0,2))
    label1_5.pack(anchor="w")
    list1_5_wrap.pack(anchor="w", pady=(0,2))

    frame1 = ctk.CTkFrame(left, fg_color="transparent")
    frame1.pack(anchor="w", fill="x")
    fields = {"X": "Payment (X)(Rand):",
            "PV": "Present Value (PV)(Rand):",
            "FV": "Future Value (FV)(Rand):",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}
    list1_2.set("X")
    selected_solve_for = "X"
    rebuild_fields()

    def update_chart(PV, total_payments, interest):
        if chart_canvas_holder[0] is not None:
            chart_canvas_holder[0].get_tk_widget().destroy()
            chart_canvas_holder[0] = None
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        fig = plt.Figure(figsize=(3.5, 3.5), facecolor=bg_color, edgecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_axis_off()
        sizes = [total_payments, interest]
        legend = ["Payments", "Interest"]
        colors = ["#202020", "#996515"]
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=None, autopct="%1.2f%%", pctdistance=0.8)
        legend = ax.legend(wedges, legend, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10, framealpha=0)
        legend_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pie_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        for text in legend.get_texts():
            text.set_color(legend_text_color)
            text.set_weight("bold")
        for text in texts:
            text.set_color(pie_text_color)
            text.set_fontsize(13)
        for autotext in autotexts:
            autotext.set_color(pie_text_color)
            autotext.set_fontsize(11)
            autotext.set_weight("bold")
        fig.patch.set_facecolor(bg_color)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0, bd=0)
        canvas.draw()
        widget.pack(fill="both", expand=True)
        chart_canvas_holder[0] = canvas
        plt.close(fig)

    def ann_update_middle_graph(X, PV, FV, n , investment_type, rate_type, payment_type, i=None, p=None, δ=None):
        for widget in graph_frame.winfo_children():
            widget.destroy()
        if middle_canvas_holder[0] is not None:
            middle_canvas_holder[0].get_tk_widget().destroy()
            middle_canvas_holder[0] = None
        graph_frame.pack_propagate(False)
        graph_frame.configure(width=550, height=400)
        steps = max(int(n * 100), 100)
        xs = [n * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if investment_type == "Compounded Interest" and payment_type == "Arrears":
                if rate_type == "Nominal":
                    ys.append(X * (((1 + i / p) ** (x * p)) - 1) / (i / p))
                else:
                    ys.append(X * (((1 + i) ** (x * p)) - 1) / i)
            elif investment_type == "Compounded Interest" and payment_type == "Advance":
                if rate_type == "Nominal":
                    ys.append(X * (1+i/p) * (((1 + i / p) ** (x * p)) - 1) / (i / p))
                else:
                    ys.append(X * (1+i) * (((1 + i) ** (x * p)) - 1) / i)
            else:
                ys.append(X * ((math.exp(δ * x) - 1) / δ))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame.winfo_width()
        if pixel_width <= 1:
            pixel_width = 550
        fig_width_inches = (pixel_width - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, 4), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Years (n)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.2, bottom=0.20)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        middle_canvas_holder[0] = canvas
        plt.close(fig)
    
    layout2 = ctk.CTkFrame(tab_2, fg_color="transparent")
    layout2.pack(fill="both", expand=True)
    graph_frame2 = ctk.CTkFrame(layout2, fg_color="transparent")
    graph_frame2.pack(fill="both", expand=True)
    tab_2_canvas_holder = [None]
    tab2_placeholder = ctk.CTkLabel(graph_frame2,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    tab2_placeholder.pack(expand=True)
    def ann_graph(X, PV, FV, n , investment_type, rate_type, payment_type, i=None, p=None, δ=None):
        for widget in graph_frame2.winfo_children():
            widget.destroy()
        if tab_2_canvas_holder[0] is not None:
            tab_2_canvas_holder[0].get_tk_widget().destroy()
            tab_2_canvas_holder[0] = None
        steps = max(int(n * 100), 100)
        xs = [n * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if investment_type == "Compounded Interest" and payment_type == "Arrears":
                if rate_type == "Nominal":
                    ys.append(X * (((1 + i / p) ** (x * p)) - 1) / (i / p))
                else:
                    ys.append(X * (((1 + i) ** (x * p)) - 1) / i)
            elif investment_type == "Compounded Interest" and payment_type == "Advance":
                if rate_type == "Nominal":
                    ys.append(X * (1 + i/p) * ((((1 + i / p) ** (x * p)) - 1) / (i / p)))
                else:
                    ys.append(X * (1 + i) * ((((1 + i) ** (x * p)) - 1) / i))
            else:
                ys.append(X * ((math.exp(δ * x) - 1) / δ))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame2.winfo_width()
        pixel_height = graph_frame2.winfo_height()
        if pixel_width <= 1:
            pixel_width = 1200
        if pixel_height <= 1:
            pixel_height = 600
        fig_width_inches = (pixel_width - 20) / 100
        fig_height_inches = (pixel_height - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, fig_height_inches), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_title("Annuity Growth Over Time", color=text_color, fontsize=14, fontweight="bold", pad=10)
        ax.grid(True, color=text_color, alpha=0.2, linestyle='--', linewidth=0.5)
        line, = ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Years (n)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.1)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        import numpy as np
        xdata = np.array(xs)
        ydata = np.array(ys)
        annot = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.4", fc=bg_color, ec="#202020", lw=1.5),
                            arrowprops=dict(arrowstyle="->", color="#202020"),
                            color=text_color, fontsize=10, zorder=10)
        annot.set_visible(False)
        last_idx = -1
        def on_hover(event):
            nonlocal last_idx
            if event.inaxes != ax or event.xdata is None:
                if annot.get_visible():
                    annot.set_visible(False)
                    canvas.draw_idle()
                return
            idx = np.searchsorted(xdata, event.xdata, side='left')
            if idx >= len(xdata):
                idx = len(xdata) - 1
            if idx > 0 and (event.xdata - xdata[idx-1]) < (xdata[idx] - event.xdata):
                idx -= 1
            if idx == last_idx and annot.get_visible():
                return
            last_idx = idx
            x_disp, y_disp = ax.transData.transform((xdata[idx], ydata[idx]))
            dist = ((event.x - x_disp)**2 + (event.y - y_disp)**2)**0.5
            if dist < 35:
                annot.xy = (xdata[idx], ydata[idx])
                annot.set_text(f"n = {xdata[idx]:.2f}\nFV = R {ydata[idx]:,.2f}")
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            canvas.draw_idle()
        canvas.mpl_connect("motion_notify_event", on_hover)
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        tab_2_canvas_holder[0] = canvas
        plt.close(fig)

    layout3 = ctk.CTkFrame(tab_3, fg_color="transparent")
    layout3.pack(fill="both", expand=True)
    style = ttk.Style()
    style.theme_use("default")
    current_mode = ctk.get_appearance_mode()
    bg_color = "#2B2B2B" if current_mode == "Dark" else "#DBDBDB"
    text_color = "#b18223" if current_mode == "Dark" else "black"
    header_bg = "#202020" if current_mode == "Dark" else "#F3F3F3"
    style.configure("Treeview", rowheight=35, borderwidth=0, font=("Arial", 14), background=bg_color,
                    foreground=text_color, fieldbackground=bg_color)
    style.map("Treeview", background=[("selected", "#202020")])
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"), borderwidth=0, relief="flat",
                    background=header_bg, foreground=text_color)
    style.map("Treeview.Heading", background=[("active", header_bg)])
    columns = ("Period", "Opening Balance", "Payment", "Interest Earned", "Closing Balance")
    tree = ttk.Treeview(layout3, columns=columns, show="headings")
    column_alignments = {
        "Period": "center", 
        "Opening Balance": "center", 
        "Payment": "center",
        "Interest Earned": "center", 
        "Closing Balance": "center"}
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=column_alignments[col])
    def resize_columns_by_ratio(event):
        total_avail_width = event.width
        column_widths = {"Period": 1, 
                        "Opening Balance": 2.25,
                        "Payment": 2.25, 
                        "Interest Earned": 2.25, 
                        "Closing Balance": 2.25}
        total_parts = sum(column_widths.values())
        for col, ratio in column_widths.items():
                calculated_width = int(total_avail_width * (ratio / total_parts))
                tree.column(col, width=calculated_width, stretch=False)
    tree.bind("<Configure>", resize_columns_by_ratio)
    scrollbar = ttk.Scrollbar(layout3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    def ann_populate_table(X, PV, n, p, i, δ, investment_type, rate_type, payment_type):
        tree.delete(*tree.get_children())
        if investment_type == "Continuous Interest":
            total_periods = int(math.ceil(n)) if n is not None else 0
        else:
            total_periods = int(math.ceil(n * p)) if n is not None and p is not None else 0
        current_balance = PV
        if payment_type == "Advance":
            current_balance = 0.0
        for k in range(1, total_periods + 1):
            if investment_type == "Compounded Interest" and payment_type == "Arrears":
                if rate_type == "Nominal":
                    current_balance = X * (((1 + i / p)**((k-1)) - 1) / (i / p))
                    end_balance = X * (((1 + i / p)**((k)) - 1) / (i / p))
                    interest = current_balance * i/p
                else:
                    current_balance = X * (((1 + i)**((k-1)) - 1) / (i))
                    end_balance = X * (((1 + i)**((k)) - 1) / (i))
                    interest = current_balance * i
            elif investment_type == "Compounded Interest" and payment_type == "Advance":
                if rate_type == "Nominal":
                    current_balance += X
                    interest = current_balance * i/p
                    end_balance = current_balance + interest
                else:
                    current_balance += X
                    interest = current_balance * i
                    end_balance = current_balance + interest
            elif investment_type == "Continuous Interest" and payment_type == "Arrears":
                if rate_type == "Effective":
                    if k == 1:
                        current_balance = 0
                        interest = current_balance * i
                        end_balance = current_balance + X + interest
                    else:
                        current_balance = end_balance
                        interest = current_balance * i
                        end_balance = current_balance + X + interest
                elif rate_type == "Nominal":
                    if k == 1:
                        current_balance = 0
                        interest = current_balance * (i/p)
                        end_balance = current_balance + X + interest
                    else:
                        current_balance = end_balance
                        interest = current_balance * (i/p)
                        end_balance = current_balance + X + interest
                
            else:
                current_balance += X
                interest = X * (((math.exp(δ*k) * (1 - math.exp(-δ)))/δ) - 1)
                end_balance = X * ((math.exp(δ * (k-1)) - 1) / δ)
           
            payment = X
            tree.insert("", "end", values=(k, 
                                            f"R {current_balance:,.2f}".replace(",", " "),
                                            f"R {payment:,.2f}".replace(",", " "),
                                            f"R {interest:,.2f}".replace(",", " "),
                                            f"R {end_balance:,.2f}".replace(",", " ")))
            if payment_type == "Advance":
                current_balance = end_balance
    
    def ann_calculated():
        error_label.configure(text="", text_color=("#000000", "#b18223"))
        investment_type = list1_1.get()
        rate_type = list1_3.get()
        payment_type = list1_4.get()
        solve_for = selected_solve_for
        values = {}
        for key, entry in entries.items():
            raw = entry.get().strip()
            if raw == "":
                values[key] = None
            else:
                try:
                    values[key] = float(raw)
                except ValueError:
                    print(f"Invalid input for {key}: {raw}")
                    return
        X = values.get("X")
        PV = values.get("PV")
        FV = values.get("FV")
        i = values.get("i")
        n = values.get("n")
        p = values.get("p")
        δ = values.get("δ")
        np_value = None
        interest_earned = None
        try:
            if i is not None:
                i = i / 100
            if δ is not None:
                δ = δ / 100
            if investment_type == "Compounded Interest" and payment_type == "Arrears":
                if rate_type == "Nominal":
                    if solve_for == "FV":
                        result = X * (((1 + i / p)**(n*p) - 1) / (i / p))
                        FV = result
                    elif solve_for == "PV":
                        result = X * ((1 - (1 + i / p)**(-(n*p))) / (i / p))
                        PV = result
                    elif solve_for == "n" and FV is not None:
                        result = math.log((FV * (i / p) / X) + 1) / (p * math.log(1 + i / p))
                        n = result
                    elif solve_for == "n" and PV is not None:
                        result = math.log((-PV * (i / p) / X) + 1) / (-p * math.log(1 + i / p))
                        n = result
                    elif solve_for == "X" and FV is not None:
                        result = FV / ((((1 + i / p)**(n * p) - 1)) / (i / p))
                        X = result
                    elif solve_for == "X" and PV is not None:
                        result = PV / (((1 - (1 + i / p)**(-n * p))) / (i / p))
                        X = result
                    elif solve_for == "i" and FV is not None:
                        N = n * p
                        try:
                            a = 2 * (FV - X * N) / (X * N * (N - 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (((1 + a)**(n*p) - 1) / a) - FV) / (X * ((n*p) * a * (1 + a)**((n*p) - 1) - ((1 + a)**(n*p) - 1)) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                    elif solve_for == "i" and PV is not None:
                        N = n * p
                        try:
                            a = 2 * (X * n * p - PV) / (X * n * p * (n * p + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 - (1 + a)**(-n*p)) / a - PV) / (X * ((1 + a*n*p) * (1 + a)**(-n*p) - 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                else:
                    if solve_for == "FV":
                        result = X * (((1 + i)**(n*p) - 1) / (i))
                        FV = result
                    elif solve_for == "PV":
                        result = X * ((1 - (1 + i)**(-(n*p))) / (i))
                        PV = result
                    elif solve_for == "n" and FV is not None:
                        result = math.log((FV * (i) / X) + 1) / (p * math.log(1 + i))
                        n = result
                    elif solve_for == "n" and PV is not None:
                        result = math.log((-PV * (i) / X) + 1) / (-p * math.log(1 + i))
                        n = result
                    elif solve_for == "i" and FV is not None:
                        N = n * p
                        try:
                            a = 2 * (FV - X * N) / (X * N * (N - 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (((1 + a)**(n*p) - 1) / a) - FV) / (X * ((n*p) * a * (1 + a)**((n*p) - 1) - ((1 + a)**(n*p) - 1)) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a
                        result = a * 100     
                    elif solve_for == "i" and PV is not None:
                        N = n * p
                        try:
                            a = 2 * (X * n * p - PV) / (X * n * p * (n * p + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * ((1 - (1 + a)**(-n*p)) / a) - PV) / (X * ((1 + a*n*p) * (1 + a)**(-n*p) - 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a
                        result = a * 100       
                    elif solve_for == "X" and FV is not None:
                        result = FV / ((((1 + i)**(n * p) - 1)) / (i))
                        X = result
                    elif solve_for == "X" and PV is not None:
                        result = PV / (((1 - (1 + i)**(-n * p))) / (i))
                        X = result
                    elif solve_for == "p" and FV is not None:
                        result = math.log((FV * (i) / X) + 1) / (n * math.log(1 + i))
                        p = result
                    elif solve_for == "p" and PV is not None:
                        result = math.log((-PV * (i) / X) + 1) / (-n * math.log(1 + i))
                        p = result
            elif investment_type == "Compounded Interest" and payment_type == "Advance":
                if rate_type == "Nominal":
                    if solve_for == "FV":
                        result = X * (1 + i / p) * (((1 + i / p)**(n*p) - 1) / (i / p))
                        FV = result
                    elif solve_for == "PV":
                        result = X * (1 + i / p) * ((1 - (1 + i / p)**(-(n*p))) / (i / p))
                        PV = result
                    elif solve_for == "n" and FV is not None:
                        result = math.log((FV * (i / p) / (X * (1 + i / p))) + 1) / (p * math.log(1 + i / p))
                        n = result
                    elif solve_for == "n" and PV is not None:
                        result = math.log((-PV * (i / p) / (X * (1 + i / p))) + 1) / (-p * math.log(1 + i / p))
                        n = result
                    elif solve_for == "i" and FV is not None:
                        N = n * p
                        try:
                            a = 2 * (FV - X * N) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 + a) * ((1 + a)**(n*p) - 1) / a - FV) / (X * ((a * n * p - 1) * (1 + a)**(n*p) + 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                    elif solve_for == "i" and PV is not None:
                        N = n * p
                        try:
                            a = 2 * (X * N - PV) / (X * N * (N - 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 + a) * (1 - (1 + a)**(-n*p)) / a - PV) / (X * ((1 + a*n*p) * (1 + a)**(-n*p) - 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                    elif solve_for == "X" and FV is not None:
                        result = FV / ((1 + i / p) * ((((1 + i / p)**(n * p) - 1)) / (i / p)))
                        X = result
                    elif solve_for == "X" and PV is not None:
                        result = PV / ((1 + i / p) * (((1 - (1 + i / p)**(-n * p))) / (i / p)))
                        X = result
                else:
                    if solve_for == "FV":
                        result = X * (1 + i) * (((1 + i)**(n*p) - 1) / (i))
                        FV = result
                    elif solve_for == "PV":
                        result = X * (1 + i) * ((1 - (1 + i)**(-(n*p))) / (i))
                        PV = result
                    elif solve_for == "n" and FV is not None:
                        result = math.log((FV * (i) / (X * (1 + i))) + 1) / (p * math.log(1 + i))
                        n = result
                    elif solve_for == "n" and PV is not None:
                        result = math.log((-PV * (i) / (X * (1 + i))) + 1) / (-p * math.log(1 + i))
                        n = result
                    elif solve_for == "i" and FV is not None:
                        N = n * p
                        try:
                            a = 2 * (FV - X * N) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 + a) * ((1 + a)**(n*p) - 1) / a - FV) / (X * ((a * n * p - 1) * (1 + a)**(n*p) + 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a
                        result = a * 100
                    elif solve_for == "i" and PV is not None:
                        N = n * p
                        try:
                            a = 2 * (X * N - PV) / (X * N * (N - 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 + a) * (1 - (1 + a)**(-n*p)) / a - PV) / (X * ((1 + a*n*p) * (1 + a)**(-n*p) - 1) / a**2)
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a
                        result = a * 100
                    elif solve_for == "X" and FV is not None:
                        result = FV / ((1 + i) * ((((1 + i)**(n * p) - 1)) / (i)))
                        X = result
                    elif solve_for == "X" and PV is not None:
                        result = PV / ((1 + i) * (((1 - (1 + i)**(-n * p))) / (i)))
                        X = result
                    elif solve_for == "p" and FV is not None:
                        result = math.log((FV * (i) / X) + 1) / (n * math.log(1 + i))
                        p = result
                    elif solve_for == "p" and PV is not None:
                        result = math.log((-PV * (i) / X) + 1) / (-n * math.log(1 + i))
                        p = result
            else:
                if solve_for == "FV":
                    result = X * ((math.exp(δ * n) - 1) / δ)
                    FV = result
                elif solve_for == "PV":
                    result = X * ((1 - math.exp(-δ * n)) / δ)
                    PV = result
                elif solve_for == "δ" and FV is not None:
                        N = n
                        try:
                            a = 2 * (FV - X * N) / (X * N * N)
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (((math.exp(a*n)-1))/a) - FV) / ((X * (a * n * math.exp(a * n) - math.exp(a * n) + 1)) / (a**2))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        δ = a
                        result = a * 100
                elif solve_for == "δ" and PV is not None:
                        N = n
                        try:
                            a = 2 * (X * N - PV) / (X * N * N)
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * (1 - (math.exp(-a * n))) / a - PV) / (X * (a * n * (math.exp(-a * n)) + (math.exp(-a * n)) - 1) / (a ** 2))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        δ = a
                        result = a * 100
                elif solve_for == "n" and FV is not None:
                    result = math.log(((FV * δ) / X) + 1) / δ
                    n = result
                elif solve_for == "n" and PV is not None:
                    result = -math.log(1 - ((PV * δ) / X)) / δ
                    n = result
                elif solve_for == "X" and FV is not None:
                    result = FV / ((math.exp(δ * n) - 1) / δ)
                    X = result
                elif solve_for == "X" and PV is not None:
                    result = PV / ((1 - math.exp(-δ * n)) / δ)
                    X = result
                else:
                    print("ERROR")

            total_payments = 0
            if X is not None and n is not None:
                if investment_type == "Continuous Interest":
                    total_payments = X * n
                else:
                    total_payments = X * n * p
            if FV is not None and PV is None and total_payments is not None:
                interest_earned = FV - total_payments
            if n is not None and p is not None:
                np_value = n * p
            if FV is not None and PV is None:
                interest_earned = FV - total_payments
            result_labels["interest_type"].configure(text=investment_type, text_color=("#000000", "#b18223"))
            result_labels["rate_type"].configure(text=rate_type, text_color=("#000000", "#b18223"))
            display_map = {"PV": (PV if (solve_for == "PV" or (solve_for not in ("FV", "PV") and known_selection == "PV")) else None, lambda v: f"R {v:,.2f}"),
                        "FV": (FV if (solve_for == "FV" or (solve_for not in ("FV", "PV") and known_selection == "FV")) else None, lambda v: f"R {v:,.2f}"),
                        "X": (X,  lambda v: f"R {v:,.2f}"),
                        "i": (i if i is not None else δ,   lambda v: f"{v*100:.4f}%"),
                        "n": (n,   lambda v: f"{v}"),
                        "p": (p,   lambda v: f"{v:.0f}"),
                        "np": (np_value, lambda v: f"{v:.0f}"),
                        "total_payments": (total_payments if investment_type != "Continuous Interest" else None,  lambda v: f"R {v:,.2f}"),
                        "interest_earned": (interest_earned if investment_type != "Continuous Interest" else None,  lambda v: f"R {v:,.2f}")}
            for key, (val, fmt) in display_map.items():
                if val is not None:
                    result_labels[key].configure(text=fmt(val), text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = val
                else:
                    result_labels[key].configure(text="—", text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = None
            if solve_for == "δ":
                result_labels["i"].configure(text=f"{result:.4f}%")
            elif solve_for == "i":
                result_labels[solve_for].configure(text=f"{result:.4f}%")
            elif solve_for == "n":
                result_labels[solve_for].configure(text=f"{result:.4f}")
            elif solve_for == "FV" or solve_for == "PV" or solve_for == "X":
                result_labels[solve_for].configure(text=f"R {result:,.2f}")
            elif solve_for == "p" or solve_for == "np":
                result_labels[solve_for].configure(text=f"{result:.0f}")
            for key, label in result_labels.items():
                if key in ("interest_type", "rate_type"):
                    continue
                label.configure(font=ctk.CTkFont(size=18))
            solved_key = "i" if solve_for == "δ" else solve_for
            if solved_key in result_labels:
                result_labels[solved_key].configure(font=ctk.CTkFont(size=18, weight="bold"))
            graph_PV = PV
            if graph_PV is None and X is not None and n is not None:
                if investment_type == "Continuous Interest" and δ is not None:
                    graph_PV = X * (1 - math.exp(-δ * n)) / δ
                elif investment_type == "Compounded Interest" and FV is not None and i is not None and p is not None:
                    if rate_type == "Nominal":
                        graph_PV = FV / (1 + i / p) ** (n * p)
                    else:
                        graph_PV = FV / (1 + i) ** (n * p)
            if investment_type != "Continuous Interest":
                if graph_PV is not None and interest_earned is not None and interest_earned > 0:
                    update_chart(graph_PV, total_payments, interest_earned)
                else:
                    if chart_canvas_holder[0] is not None:
                        chart_canvas_holder[0].get_tk_widget().destroy()
                        chart_canvas_holder[0] = None
            else:
                if chart_canvas_holder[0] is not None:
                    chart_canvas_holder[0].get_tk_widget().destroy()
                    chart_canvas_holder[0] = None
            ann_update_middle_graph(X=X, PV=graph_PV, FV=FV, n=n, investment_type=investment_type,
                                rate_type=rate_type, payment_type=payment_type, i=i, p=p, δ=δ)
            ann_graph(X=X, PV=graph_PV, FV=FV, n=n, investment_type=investment_type,
                                rate_type=rate_type, payment_type=payment_type, i=i, p=p, δ=δ)
            ann_populate_table(X=X, PV=graph_PV, n=n, p=p, i=i, δ=δ, investment_type=investment_type, rate_type=rate_type, payment_type=payment_type)
        except ZeroDivisionError:
            error_label.configure(text="Error: Division with zero. Check inputs.")
        except ValueError as e:
            error_label.configure(text="Error: Invalid Calculation. Check inputs.")
        except Exception as e:
            error_label.configure(text=f"Error: {str(e)}")

    calc_btn = ctk.CTkButton(left,
                            text="Calculate",
                            text_color=("black", "#b18223"),
                            border_width=2,
                            border_color="#996515",
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            width=250,
                            command=ann_calculated)
    calc_btn.pack(anchor="w", pady=(10, 0))

def build_increasing_annuity_page(page):
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["Increasing_annuity_large"],
                            text="",
                            text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Increasing Annuity",
                                text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))
    tab = ctk.CTkTabview(page,
                        fg_color="transparent",
                        corner_radius=15,
                        segmented_button_fg_color="#202020",
                        segmented_button_selected_color="#2b2b2b",
                        segmented_button_selected_hover_color="#2b2b2b",
                        segmented_button_unselected_color="#202020",
                        text_color="#b18223")
    tab.pack(fill="both", expand=True, padx=0, pady=0)
    tab._segmented_button.configure(font=ctk.CTkFont(size=20), height=40)
    tab_1 = tab.add("Summary")
    tab_2 = tab.add("Graph")
    tab_3 = tab.add("Amortization")
    var = ["X", "FV", "PV"]
    rate_type = ["Effective", "Nominal"]
    payment_type = ["Arrears", "Advance"]
    known = ["FV", "PV"]
    selected_solve_for = "X"
    field_frames = {}
    entries = {}

    layout = ctk.CTkFrame(tab_1, fg_color="transparent")
    layout.pack(fill="both", expand=True)
    left = ctk.CTkScrollableFrame(layout, fg_color="transparent", width=270)
    left.pack(side="left", fill="both", expand=True)
    sep1 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep1.pack(side="left", fill="y")
    middle = ctk.CTkFrame(layout, fg_color="transparent", width=530)
    middle.pack(side="left", fill="y")
    middle.pack_propagate(False)
    sep2 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep2.pack(side="left", fill="y")
    right = ctk.CTkFrame(layout, fg_color="transparent")
    right.pack(side="right", fill="y")

    result_title = ctk.CTkLabel(right,
                            text="Summary & Solutions",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    result_title.pack(anchor="n", pady=(0, 1))
    error_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont(size=16), text_color="red", wraplength=380)
    error_label.pack(anchor="n", pady=(0, 1))
    result_frame = ctk.CTkFrame(right, fg_color="transparent")
    result_frame.pack(anchor="n", padx=(5,0))
    chart_frame = ctk.CTkFrame(right, fg_color="transparent")
    chart_frame.pack(anchor="n", fill="both", expand=True)
    chart_canvas_holder = [None]
    result_labels = {}
    graph_title = ctk.CTkLabel(middle,
                            text="Graph",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    graph_title.pack(anchor="n", pady=(0, 3))
    graph_frame = ctk.CTkFrame(middle, fg_color="transparent")
    graph_frame.pack(fill="both", expand=True)
    middle_canvas_holder = [None]
    graph_placeholder = ctk.CTkLabel(graph_frame,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    graph_placeholder.pack(expand=True)

    def create_result_field(key, label):
        frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        frame.pack(anchor="w", pady=2)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        title = ctk.CTkLabel(frame, text=label, text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=18), anchor="w", width=220)
        title.grid(row=0, column=0, sticky="w")
        value = ctk.CTkLabel(frame, text="—", text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=18), anchor="e", width=180)
        value.grid(row=0, column=1, sticky="e")
        bind_click_to_copy(value, decimals=6)
        result_labels[key] = value
    create_result_field("interest_type", "Interest Type:")
    create_result_field("rate_type", "Rate Type:")
    create_result_field("r", "Interest Rate:")
    create_result_field("j", "Increase Rate:")
    create_result_field("PV", "Present Value:")
    create_result_field("FV", "Future Value:")
    create_result_field("X", "Payment:")
    create_result_field("total_payments", "Total Payments:")
    create_result_field("total_interest", "Total Interest:")
    create_result_field("p", "Period:")
    create_result_field("k", "Payments per Level Group:")
    create_result_field("m", "Amount of Level Groups:")

    def get_active_fields():
        return {"X": "Payment (X)(Rand):",
        "PV": "Present Value (PV)(Rand):",
        "FV": "Future Value (FV)(Rand):",
        "r": "Interest Rate (r)(%):",
        "j": "Increase Rate (j)(%):",
        "k": "Payments per Group (k):",
        "m": "Amount of Groups (m):",
        "p": "Period (p):"}

    def create_field(parent, key, label_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(anchor="w")
        label = ctk.CTkLabel(frame,
                            text=label_text,text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", pady=(0, 1))
        entry = ctk.CTkEntry(frame, width=250, font=ctk.CTkFont(size=20))
        entry.pack(anchor="w", pady=(0, 3))
        field_frames[key] = frame
        entries[key] = entry

    def rebuild_fields():
        for frame in field_frames.values():
            frame.destroy()
        field_frames.clear()
        entries.clear()
        active_fields = get_active_fields()
        keys_to_skip = [selected_solve_for]
        if selected_solve_for == "FV":
            keys_to_skip.append("PV")
        elif selected_solve_for == "PV":
            keys_to_skip.append("FV")
        if selected_solve_for not in ("FV", "PV"):
            if known_selection == "FV":
                keys_to_skip.append("PV")
            elif known_selection == "PV":
                keys_to_skip.append("FV")
        for key, label in active_fields.items():
            if key not in keys_to_skip:
                create_field(frame1, key, label)
        arrange_fields()

    def update_solve_for(choice):
        nonlocal selected_solve_for
        selected_solve_for = choice
        if selected_solve_for in ("FV", "PV"):
            label1_5.pack_forget()
            list1_5_wrap.pack_forget()
        else:
            label1_5.pack(anchor="w", before=frame1)
            list1_5_wrap.pack(anchor="w", pady=(0, 2), before=frame1)
        rebuild_fields()

    def update_rate_type(choice):
        if choice == "Nominal":
            list1_2.configure(values=["X", "FV", "PV"])
            if list1_2.get() == "p":
                list1_2.set("X")
                update_solve_for("X")
        else:
            list1_2.configure(values=["X", "FV", "PV"])
        rebuild_fields()

    known_selection = "FV" 
    def arrange_fields():
        for frame in field_frames.values():
            frame.pack_forget()
        active = get_active_fields()
        order = [k for k in active.keys() if k != selected_solve_for]
        for key in order:
            if key not in field_frames:
                continue
            if selected_solve_for == "FV" and key == "PV":
                continue
            if selected_solve_for == "PV" and key == "FV":
                continue
            if selected_solve_for not in ("FV", "PV"):
                if (key == "PV" and selected_solve_for not in ("FV", "PV") and known_selection == "FV"):
                    continue
                if (key == "FV" and selected_solve_for not in ("FV", "PV") and known_selection == "PV"):
                    continue
            field_frames[key].pack(anchor="w")

    def update_known(choice):
        nonlocal known_selection
        known_selection = choice
        arrange_fields()
        rebuild_fields()

    label1_4 = ctk.CTkLabel(left,
                            text="Payment Type:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_4_wrap, list1_4 = bordered_optionmenu(left, values=payment_type, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_2 = ctk.CTkLabel(left,
                            text="To solve for:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_2_wrap, list1_2 = bordered_optionmenu(left, values=var, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_solve_for)
    label1_3 = ctk.CTkLabel(left,
                            text="Interest Rate:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_3_wrap, list1_3 = bordered_optionmenu(left, values=rate_type, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16),
                                command=update_rate_type)
    label1_5 = ctk.CTkLabel(left,
                            text="Known:",text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_5_wrap, list1_5 = bordered_optionmenu(left, values=known, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_known)
    def list1_2_change(choice):
        if choice == "Continuous Interest":
            nonlocal selected_solve_for
            list1_2.configure(values=var_cont, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type_cont, text_color=("black", "#b18223"))
            if selected_solve_for not in var_cont:
                selected_solve_for = "X"
                list1_2.set("X")
            list1_3.set(rate_type_cont[0])
        else:
            list1_2.configure(values=var, text_color=("black", "#b18223"))
            list1_3.configure(values=rate_type, text_color=("black", "#b18223"))
            if selected_solve_for not in var:
                selected_solve_for = "X"
                list1_2.set("X")
            list1_3.set(rate_type[0])
        rebuild_fields()
    
    label1_4.pack(anchor="w")
    list1_4_wrap.pack(anchor="w", pady=(0,2))
    label1_2.pack(anchor="w")
    list1_2_wrap.pack(anchor="w", pady=(0,2))
    label1_3.pack(anchor="w")
    list1_3_wrap.pack(anchor="w", pady=(0,2))
    label1_5.pack(anchor="w")
    list1_5_wrap.pack(anchor="w", pady=(0,2))

    frame1 = ctk.CTkFrame(left, fg_color="transparent")
    frame1.pack(anchor="w", fill="x")
    fields = {"X": "Payment (X)(Rand):",
            "PV": "Present Value (PV)(Rand):",
            "FV": "Future Value (FV)(Rand):",
            "r": "Interest Rate (r)(%):",
            "j": "Increase Rate (j)(%):",
            "k": "Payments per Group (k):",
            "m": "Amount of Groups (m):",
            "p": "Period (p):"}
    list1_2.set("X")
    selected_solve_for = "X"
    rebuild_fields()

    def update_chart(PV, total_payments, total_interest):
        if chart_canvas_holder[0] is not None:
            chart_canvas_holder[0].get_tk_widget().destroy()
            chart_canvas_holder[0] = None
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        fig = plt.Figure(figsize=(3.5, 3.5), facecolor=bg_color, edgecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_axis_off()
        fig.subplots_adjust(left=0.1, right=0.8, top=1, bottom=0.25)
        sizes = [total_payments, total_interest]
        legend = ["Payments", "Interest"]
        colors = ["#202020", "#996515"]
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=None, autopct="%1.2f%%", pctdistance=0.8, radius=0.75)
        legend = ax.legend(wedges, legend, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10, framealpha=0)
        legend_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pie_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        for text in legend.get_texts():
            text.set_color(legend_text_color)
            text.set_weight("bold")
        for text in texts:
            text.set_color(pie_text_color)
            text.set_fontsize(13)
        for autotext in autotexts:
            autotext.set_color(pie_text_color)
            autotext.set_fontsize(11)
            autotext.set_weight("bold")
        fig.patch.set_facecolor(bg_color)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0, bd=0)
        canvas.draw()
        widget.pack(fill="both", expand=True)
        chart_canvas_holder[0] = canvas
        plt.close(fig)

    def ann_update_middle_graph(X, PV, FV, r, j, k, m, p, investment_type, rate_type, payment_type):
        for widget in graph_frame.winfo_children():
            widget.destroy()
        if middle_canvas_holder[0] is not None:
            middle_canvas_holder[0].get_tk_widget().destroy()
            middle_canvas_holder[0] = None
        graph_frame.pack_propagate(False)
        graph_frame.configure(width=550, height=400)
        steps = max(int(m * 100), 100)
        xs = [m * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if payment_type == "Arrears":
                ys.append(X * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*x)) - ((1+j)**(x)))/((1+r)**(k) - (1+j))))   
            if payment_type == "Advance":
                ys.append(X * (1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*x)) - ((1+j)**(x)))/((1+r)**(k) - (1+j))))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame.winfo_width()
        if pixel_width <= 1:
            pixel_width = 550
        fig_width_inches = (pixel_width - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, 4), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Level Group (m)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.2, bottom=0.20)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        middle_canvas_holder[0] = canvas
        plt.close(fig)
    
    layout2 = ctk.CTkFrame(tab_2, fg_color="transparent")
    layout2.pack(fill="both", expand=True)
    graph_frame2 = ctk.CTkFrame(layout2, fg_color="transparent")
    graph_frame2.pack(fill="both", expand=True)
    tab_2_canvas_holder = [None]
    tab2_placeholder = ctk.CTkLabel(graph_frame2,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    tab2_placeholder.pack(expand=True)
    def ann_graph(X, PV, FV, r, j, k, m, p, investment_type, rate_type, payment_type):
        for widget in graph_frame2.winfo_children():
            widget.destroy()
        if tab_2_canvas_holder[0] is not None:
            tab_2_canvas_holder[0].get_tk_widget().destroy()
            tab_2_canvas_holder[0] = None
        steps = max(int(m * 100), 100)
        xs = [m * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if payment_type == "Arrears":
                ys.append(X * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*x)) - ((1+j)**(x)))/((1+r)**(k) - (1+j))))   
            if payment_type == "Advance":
                ys.append(X * (1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*x)) - ((1+j)**(x)))/((1+r)**(k) - (1+j))))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame2.winfo_width()
        pixel_height = graph_frame2.winfo_height()
        if pixel_width <= 1:
            pixel_width = 1200
        if pixel_height <= 1:
            pixel_height = 600
        fig_width_inches = (pixel_width - 20) / 100
        fig_height_inches = (pixel_height - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, fig_height_inches), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_title("Increasing Annuity Growth Over Time", color=text_color, fontsize=14, fontweight="bold", pad=10)
        ax.grid(True, color=text_color, alpha=0.2, linestyle='--', linewidth=0.5)
        line, = ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Level Groups (m)", color=text_color, fontsize=11)
        ax.set_ylabel("Future Value (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.1)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        import numpy as np
        xdata = np.array(xs)
        ydata = np.array(ys)
        annot = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.4", fc=bg_color, ec="#202020", lw=1.5),
                            arrowprops=dict(arrowstyle="->", color="#202020"),
                            color=text_color, fontsize=10, zorder=10)
        annot.set_visible(False)
        last_idx = -1
        def on_hover(event):
            nonlocal last_idx
            if event.inaxes != ax or event.xdata is None:
                if annot.get_visible():
                    annot.set_visible(False)
                    canvas.draw_idle()
                return
            idx = np.searchsorted(xdata, event.xdata, side='left')
            if idx >= len(xdata):
                idx = len(xdata) - 1
            if idx > 0 and (event.xdata - xdata[idx-1]) < (xdata[idx] - event.xdata):
                idx -= 1
            if idx == last_idx and annot.get_visible():
                return
            last_idx = idx
            x_disp, y_disp = ax.transData.transform((xdata[idx], ydata[idx]))
            dist = ((event.x - x_disp)**2 + (event.y - y_disp)**2)**0.5
            if dist < 35:
                annot.xy = (xdata[idx], ydata[idx])
                annot.set_text(f"m = {xdata[idx]:.2f}\nFV = R {ydata[idx]:,.2f}")
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            canvas.draw_idle()
        canvas.mpl_connect("motion_notify_event", on_hover)
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        tab_2_canvas_holder[0] = canvas
        plt.close(fig)

    layout3 = ctk.CTkFrame(tab_3, fg_color="transparent")
    layout3.pack(fill="both", expand=True)
    style = ttk.Style()
    style.theme_use("default")
    current_mode = ctk.get_appearance_mode()
    bg_color = "#2B2B2B" if current_mode == "Dark" else "#DBDBDB"
    text_color = "#b18223" if current_mode == "Dark" else "black"
    header_bg = "#202020" if current_mode == "Dark" else "#F3F3F3"
    style.configure("Treeview", rowheight=35, borderwidth=0, font=("Arial", 14), background=bg_color,
                    foreground=text_color, fieldbackground=bg_color)
    style.map("Treeview", background=[("selected", "#202020")])
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"), borderwidth=0, relief="flat",
                    background=header_bg, foreground=text_color)
    style.map("Treeview.Heading", background=[("active", header_bg)])
    columns = ("Period", "Opening Balance", "Payment", "Interest Earned", "Closing Balance")
    tree = ttk.Treeview(layout3, columns=columns, show="headings")
    column_alignments = {
        "Period": "center", 
        "Opening Balance": "center", 
        "Payment": "center",
        "Interest Earned": "center", 
        "Closing Balance": "center"}
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=column_alignments[col])
    def resize_columns_by_ratio(event):
        total_avail_width = event.width
        column_widths = {"Period": 1, 
                        "Opening Balance": 2.25,
                        "Payment": 2.25, 
                        "Interest Earned": 2.25, 
                        "Closing Balance": 2.25}
        total_parts = sum(column_widths.values())
        for col, ratio in column_widths.items():
                calculated_width = int(total_avail_width * (ratio / total_parts))
                tree.column(col, width=calculated_width, stretch=False)
    tree.bind("<Configure>", resize_columns_by_ratio)
    scrollbar = ttk.Scrollbar(layout3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    def ann_populate_table(X, PV, r, j, k, m, p, investment_type, rate_type, payment_type):
        tree.delete(*tree.get_children())
        if investment_type == "Compounded Interest":
            total_periods = int(math.ceil(m * k))
        i = 0
        total_m = int(math.ceil(m + 1))
        total_k = int(math.ceil(k + 1))
        
        current_balance = 0
        for z in range(1, total_m):
            for b in range(1, total_k):
                i += 1
                if payment_type == "Arrears":
                    payment = X * ((1 + j)**(z-1))
                    interest = r * current_balance
                    closing_balance = payment + current_balance + interest
                else:
                    payment = X * ((1 + j)**(z-1))
                    current_balance = current_balance + payment
                    interest = r * current_balance
                    closing_balance = current_balance + interest
            
                tree.insert("", "end", values=(i, 
                                            f"R {current_balance:,.2f}".replace(",", " "),
                                            f"R {payment:,.2f}".replace(",", " "),
                                            f"R {interest:,.2f}".replace(",", " "),
                                            f"R {closing_balance:,.2f}".replace(",", " ")))
               
                current_balance = closing_balance
    
    def ann_calculated():
        investment_type = "Compounded Interest"
        error_label.configure(text="", text_color=("#000000", "#b18223"))
        rate_type = list1_3.get()
        payment_type = list1_4.get()
        solve_for = selected_solve_for
        values = {}
        for key, entry in entries.items():
            raw = entry.get().strip()
            if raw == "":
                values[key] = None
            else:
                try:
                    values[key] = float(raw)
                except ValueError:
                    print(f"Invalid input for {key}: {raw}")
                    return
        X = values.get("X")
        PV = values.get("PV")
        FV = values.get("FV")
        r = values.get("r")
        j = values.get("j")
        m = values.get("m")
        k = values.get("k")
        p = values.get("p")
        np_value = None
        interest_earned = None
        if r is not None:
            r = r/100
        if j is not None:
            j = j/100
        try:
            r_map = r
            if payment_type == "Arrears":
                if rate_type == "Nominal":
                    r = r/p
                
                if solve_for == "FV":
                    result = X * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j)))
                    FV = result
                if solve_for == "PV":
                    result = X * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))) * ((1+r)**(-k*m))
                    PV = result
                if solve_for == "X" and FV is not None:
                    result = FV / (((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))))
                    X = result
                if solve_for == "X" and PV is not None:
                    result = PV / (((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))) * ((1+r)**(-k*m)))
                    X = result
            if payment_type == "Advance":
                if rate_type == "Nominal":
                    r = r/p
                if solve_for == "FV":
                    result = X * (1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j)))
                    FV = result
                if solve_for == "PV":
                    result = X * (1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))) * ((1+r)**(-k*m))
                    PV = result
                if solve_for == "X" and FV is not None:
                    result = FV / ((1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))))
                    X = result
                if solve_for == "X" and PV is not None:
                    result = PV / ((1+r) * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))) * ((1+r)**(-k*m)))
                    X = result
            total_payments = k * X * (((1+j)**(m) - 1)/j)
            total_interest = FV - total_payments
            
            if FV is not None and PV is None and total_payments is not None:
                interest_earned = FV - total_payments
            if p is not None:
                np_value = p
            if FV is not None and PV is None:
                interest_earned = FV - total_payments
            result_labels["rate_type"].configure(text=rate_type, text_color=("#000000", "#b18223"))
            result_labels["interest_type"].configure(text=investment_type, text_color=("#000000", "#b18223"))
            display_map = {"PV": (PV if (solve_for == "PV" or (solve_for not in ("FV", "PV") and known_selection == "PV")) else None, lambda v: f"R {v:,.2f}"),
                        "FV": (FV if (solve_for == "FV" or (solve_for not in ("FV", "PV") and known_selection == "FV")) else None, lambda v: f"R {v:,.2f}"),
                        "X": (X,  lambda v: f"R {v:,.2f}"),
                        "p": (p,   lambda v: f"{v:.0f}"),
                        "r": (r_map,   lambda v: f"{v*100:.4f}%"),
                        "j": (j,   lambda v: f"{v*100:.4f}%"),
                        "k": (k,   lambda v: f"{v:.0f}"),
                        "m": (m,   lambda v: f"{v:.0f}"),
                        "total_payments": (total_payments,   lambda v: f"R{v:,.2f}"),
                        "total_interest": (total_interest,   lambda v: f"R{v:,.2f}")}
            for key, (val, fmt) in display_map.items():
                if val is not None:
                    result_labels[key].configure(text=fmt(val), text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = val
                else:
                    result_labels[key].configure(text="—", text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = None
            
            if solve_for == "r" or solve_for == "j":
                result_labels[solve_for].configure(text=f"{result:.4f}%")
            elif solve_for == "m" or solve_for == "k":
                result_labels[solve_for].configure(text=f"{result:.4f}")
            elif solve_for == "FV" or solve_for == "PV" or solve_for == "X":
                result_labels[solve_for].configure(text=f"R {result:,.2f}")
            elif solve_for == "p":
                result_labels[solve_for].configure(text=f"{result:.0f}")
            for key, label in result_labels.items():
                if key in ("interest_type", "rate_type"):
                    continue
                label.configure(font=ctk.CTkFont(size=18))
            solved_key = solve_for 
            if solved_key in result_labels:
                result_labels[solved_key].configure(font=ctk.CTkFont(size=18, weight="bold"))
            graph_PV = PV
            if graph_PV is None and X is not None:
                if investment_type == "Compounded Interest" and FV is not None and r is not None and p is not None:
                    graph_PV = X * ((((1+r)**k) - 1)/r) * ((((1+r)**(k*m)) - ((1+j)**(m)))/((1+r)**(k) - (1+j))) * ((1+r)**(-k*m))
            if X is not None:
                if investment_type == "Compounded Interest":
                    update_chart(PV, total_payments, total_interest)
                else:
                    if chart_canvas_holder[0] is not None:
                        chart_canvas_holder[0].get_tk_widget().destroy()
                        chart_canvas_holder[0] = None
            else:
                if chart_canvas_holder[0] is not None:
                    chart_canvas_holder[0].get_tk_widget().destroy()
                    chart_canvas_holder[0] = None
            ann_update_middle_graph(X=X, PV=graph_PV, FV=FV, r=r, j=j, k=k, m=m, p=p, investment_type=investment_type,
                                rate_type=rate_type, payment_type=payment_type)
            ann_graph(X=X, PV=graph_PV, FV=FV, r=r, j=j, k=k, m=m, p=p, investment_type=investment_type,
                                rate_type=rate_type, payment_type=payment_type)
            ann_populate_table(X=X, PV=graph_PV, r=r, j=j, k=k, m=m, p=p, investment_type=investment_type, rate_type=rate_type, payment_type=payment_type)
        except ZeroDivisionError:
            error_label.configure(text="Error: Division with zero. Check inputs.")
        except ValueError as e:
            error_label.configure(text="Error: Invalid Calculation. Check inputs.")
        except Exception as e:
            error_label.configure(text=f"Error: {str(e)}")

    calc_btn = ctk.CTkButton(left,
                            text="Calculate",
                            text_color=("black", "#b18223"),
                            border_width=2,
                            border_color="#996515",
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            width=250,
                            command=ann_calculated)
    calc_btn.pack(anchor="w", pady=(10, 0))

def build_loan_page(page):
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["Loan_large"],
                            text="", text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="Loan",
                                text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))
    tab = ctk.CTkTabview(page,
                        fg_color="transparent",
                        corner_radius=15,
                        segmented_button_fg_color="#202020",
                        segmented_button_selected_color="#2b2b2b",
                        segmented_button_selected_hover_color="#2b2b2b",
                        segmented_button_unselected_color="#202020",
                        text_color="#b18223")
    tab.pack(fill="both", expand=True, padx=0, pady=0)
    tab._segmented_button.configure(font=ctk.CTkFont(size=20), height=40)
    tab_1 = tab.add("Summary")
    tab_2 = tab.add("Graph")
    tab_3 = tab.add("Amortization")
    var = ["X", "L", "i", "n", "p", "None"]
    var_type = ["Compounded Interest"]
    rate_type = ["Effective", "Nominal"]
    payment_type = ["Arrears", "Advance"]
    option_type = ["Years", "Payment"]
    selected_solve_for = "X"
    field_frames = {}
    entries = {}

    layout = ctk.CTkFrame(tab_1, fg_color="transparent")
    layout.pack(fill="both", expand=True)
    left = ctk.CTkFrame(layout, fg_color="transparent", width=270)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    sep1 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep1.pack(side="left", fill="y")
    middle = ctk.CTkFrame(layout, fg_color="transparent", width=550)
    middle.pack(side="left", fill="y")
    middle.pack_propagate(False)
    sep2 = ctk.CTkFrame(layout, width=2, fg_color=("#000000", "#996515"))
    sep2.pack(side="left", fill="y")
    right = ctk.CTkFrame(layout, fg_color="transparent")
    right.pack(side="right", fill="y")

    result_title = ctk.CTkLabel(right,
                            text="Summary & Solutions",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    result_title.pack(anchor="n", pady=(0, 2))
    error_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont(size=16), text_color="red", wraplength=380)
    error_label.pack(anchor="n", pady=(0, 1))
    result_frame = ctk.CTkFrame(right, fg_color="transparent")
    result_frame.pack(anchor="n")
    chart_frame = ctk.CTkFrame(right, fg_color="transparent")
    chart_frame.pack(anchor="n", fill="both", expand=True)
    chart_canvas_holder = [None]
    result_labels = {}
    graph_title = ctk.CTkLabel(middle,
                            text="Extra Calculations",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=28, weight="bold"))
    graph_title.pack(anchor="n", pady=(0, 3))
    graph_frame = ctk.CTkFrame(middle, fg_color="transparent")
    graph_frame.pack(fill="both", expand=True)
    middle_canvas_holder = [None]
    graph_placeholder = ctk.CTkLabel(graph_frame,
                                    text="Run a calculation to see other entries",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    graph_placeholder.pack(expand=True)

    def create_result_field(key, label):
        frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        frame.pack(anchor="w", pady=3)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        title = ctk.CTkLabel(frame, text=label, text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=18), anchor="w", width=180)
        title.grid(row=0, column=0, sticky="w")
        value = ctk.CTkLabel(frame, text="—", text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=18), anchor="e", width=200)
        value.grid(row=0, column=1, sticky="e")
        bind_click_to_copy(value, decimals=6)
        result_labels[key] = value
    create_result_field("interest_type", "Interest Type:")
    create_result_field("rate_type", "Rate Type:")
    create_result_field("i", "Rate:")
    create_result_field("L", "Loan Amount:")
    create_result_field("X", "Payment:")
    create_result_field("total_payments", "Total Payments:")
    create_result_field("small_payment", "Small Payment:")
    create_result_field("n", "Years:")
    create_result_field("p", "Period:")
    create_result_field("np", "Compounding Periods:")
    create_result_field("total_interest", "Interest Payed:")

    def get_active_fields():
        investment_type = list1_1.get()
        if investment_type == "Compounded Interest":
            return {"X": "Payment (X)(Rand):",
            "L": "Loan Amount (L)(Rand)",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}

    def create_field(parent, key, label_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(anchor="w")
        label = ctk.CTkLabel(frame,
                            text=label_text,
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", pady=(0, 1))
        entry = ctk.CTkEntry(frame, width=250, font=ctk.CTkFont(size=20))
        entry.pack(anchor="w", pady=(0, 3))
        field_frames[key] = frame
        entries[key] = entry

    def rebuild_fields():
        for frame in field_frames.values():
            frame.destroy()
        field_frames.clear()
        entries.clear()
        active_fields = get_active_fields()
        for key, label in active_fields.items():
            if key != selected_solve_for:
                create_field(frame1, key, label)
        arrange_fields()

    def update_solve_for(choice):
        nonlocal selected_solve_for
        selected_solve_for = choice
        rebuild_fields()

    def update_rate_type(choice):
        if choice == "Nominal":
            list1_2.configure(values=["X", "L", "i", "n"])
            if list1_2.get() == "p":
                list1_2.set("X")
                update_solve_for("X")
        else:
            list1_2.configure(values=["X", "L", "i", "n", "p"])
        rebuild_fields()

    known_selection = "FV" 
    def arrange_fields():
        for frame in field_frames.values():
            frame.pack_forget()
        active = get_active_fields()
        order = [k for k in active.keys() if k != selected_solve_for]
        for key in order:
            field_frames[key].pack(anchor="w")

    def update_known(choice):
        nonlocal known_selection
        known_selection = choice
        arrange_fields()
        rebuild_fields()

    label1_4 = ctk.CTkLabel(left,
                            text="Payment Type:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_4_wrap, list1_4 = bordered_optionmenu(left, values=payment_type, text_color=("black", "#b18223"), font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_2 = ctk.CTkLabel(left,
                            text="To solve for:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_2_wrap, list1_2 = bordered_optionmenu(left, values=var, text_color=("black", "#b18223"),font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16), command=update_solve_for)
    label1_3 = ctk.CTkLabel(left,
                            text="Interest Rate:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_3_wrap, list1_3 = bordered_optionmenu(left, values=rate_type, text_color=("black", "#b18223"),font=ctk.CTkFont(size=20),
                                width=250, fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16),
                                command=update_rate_type)

    label1_4.pack(anchor="w")
    list1_4_wrap.pack(anchor="w", pady=(0,2))
    label1_1 = ctk.CTkLabel(left,
                            text="Type Loan:",
                            text_color=("#000000", "#b18223"),
                            font=ctk.CTkFont(size=20, weight="bold"))
    list1_1_wrap, list1_1 = bordered_optionmenu(left,
                                values=var_type,
                                text_color=("black", "#b18223"),
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
    label1_1.pack(anchor="w")
    list1_1_wrap.pack(anchor="w", pady=(0,2))
    label1_2.pack(anchor="w")
    list1_2_wrap.pack(anchor="w", pady=(0,2))
    label1_3.pack(anchor="w")
    list1_3_wrap.pack(anchor="w", pady=(0,2))

    frame1 = ctk.CTkFrame(left, fg_color="transparent")
    frame1.pack(anchor="w", fill="x")
    fields = {"X": "Payment (X)(Rand):",
            "L": "Loan Amount (L)(Rand):",
            "i": "Interest Rate (i)(%):",
            "n": "Years (n):",
            "p": "Period (p):"}
    list1_2.set("X")
    selected_solve_for = "X"
    rebuild_fields()

    def l_update_chart(L, total_interest):
        if chart_canvas_holder[0] is not None:
            chart_canvas_holder[0].get_tk_widget().destroy()
            chart_canvas_holder[0] = None
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        fig = plt.Figure(figsize=(3.5, 3.5), facecolor=bg_color, edgecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_axis_off()
        sizes = [L, total_interest]
        legend = ["Loan Amount", "Interest"]
        colors = ["#202020", "#996515"]
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=None, autopct="%1.2f%%", pctdistance=0.8)
        legend = ax.legend(wedges, legend, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10, framealpha=0)
        legend_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pie_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        for text in legend.get_texts():
            text.set_color(legend_text_color)
            text.set_weight("bold")
        for text in texts:
            text.set_color(pie_text_color)
            text.set_fontsize(13)
        for autotext in autotexts:
            autotext.set_color(pie_text_color)
            autotext.set_fontsize(11)
            autotext.set_weight("bold")
        fig.patch.set_facecolor(bg_color)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0, bd=0)
        canvas.draw()
        widget.pack(fill="both", expand=True)
        chart_canvas_holder[0] = canvas
        plt.close(fig)

    def l_entry(np_value, X, L, n , investment_type, rate_type, payment_type, i=None, p=None):
        for widget in graph_frame.winfo_children():
            widget.destroy()
        if middle_canvas_holder[0] is not None:
            middle_canvas_holder[0].get_tk_widget().destroy()
            middle_canvas_holder[0] = None
        extra_frame = ctk.CTkFrame(graph_frame, fg_color = "transparent")
        extra_frame.pack(fill="both", padx=12, expand=True)
        extra_frame.pack_propagate(False)
        dropdown_frame1 = ctk.CTkFrame(extra_frame, fg_color="transparent", height=30)
        dropdown_frame1.pack(fill="x", pady=(0, 5))
        dropdown_frame1.pack_propagate(False)
        drop1_wrap, drop1 = bordered_optionmenu(dropdown_frame1, values=option_type,
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
        drop1_wrap.pack(side="left")
        drop2_wrap, drop2 = bordered_optionmenu(dropdown_frame1, values=option_type,
                                font=ctk.CTkFont(size=20),
                                width=250,
                                fg_color="#202020", button_color="#202020",
                                dropdown_font=ctk.CTkFont(size=16))
        drop2_wrap.pack(side="right")

        entry_frame1 = ctk.CTkFrame(extra_frame, fg_color="transparent", height=30)
        entry_frame1.pack(fill="x", pady=(0, 5))
        entry_frame1.pack_propagate(False)
        entry1 = ctk.CTkEntry(entry_frame1,
                                font=ctk.CTkFont(size=20),
                                width=250)
        entry1.pack(side="left")
        entry2 = ctk.CTkEntry(entry_frame1,
                                font=ctk.CTkFont(size=20),
                                width=250)
        entry2.pack(side="right")
        btn_frame1 = ctk.CTkFrame(extra_frame, fg_color="transparent", height=30)
        btn_frame1.pack(fill="x", pady=(0, 3))
        btn_frame1.pack_propagate(False)
        def extra_calc():
            np = np_value
            pay_year_type1 = drop1.get()
            pay_year_type2 = drop2.get()
            try:
                pay_year1 = float(entry1.get())
                pay_year2 = float(entry2.get())
            except:
                return
            if rate_type == "Nominal" and i is not None and p is not None:
                e_i = i/p
            else:
                e_i = i
            if pay_year_type1 == "Years" and p is not None:
                np_1 = pay_year1 * p
            else:
                np_1 = pay_year1
            if pay_year_type2 == "Years" and p is not None:
                np_2 = pay_year2 * p
            else:
                np_2 = pay_year2
            
            if payment_type == "Arrears":
                balance1 = (L * (1+e_i)**(np_1)) - X * (((1+e_i)**(np_1) - 1)/e_i)
                balance2 = (L * (1+e_i)**(np_2)) - X * (((1+e_i)**(np_2) - 1)/e_i)
                if np_1 == np:
                    total_payments1 = (np_1 * X) + (L*((1 + (e_i))**(np_1)) - X * (((1+e_i)**(np_1)-1)/(e_i)))*(1 + e_i)
                else:
                    total_payments1 = (np_1 * X)
                if np_2 == np:
                    total_payments2 = (np_2 * X) + (L*((1 + (e_i))**(np_2)) - X * (((1+e_i)**(np_2)-1)/(e_i)))*(1 + e_i)
                else:
                    total_payments2 = (np_2 * X)
                total_interest1 = (e_i * L - X) * (((1 + e_i)**(np_1) - 1)/e_i) + (np_1) * X
                total_interest2 = (e_i * L - X) * (((1 + e_i)**(np_2) - 1)/e_i) + (np_2) * X
                interest1 = (e_i * L - X) * (1 + e_i)**(np_1 - 1) + X
                interest2 = (e_i * L - X) * (1 + e_i)**(np_2 - 1) + X
                total_capital1 = np_1 * X - total_interest1
                total_capital2 = np_2 * X - total_interest2
                capital1 = (X - e_i * L)*((1 + e_i)**(np_1 - 1))
                capital2 = (X - e_i * L)*((1 + e_i)**(np_2 - 1))
                result_labels["balance1"].configure(text=f"R {balance1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["balance2"].configure(text=f"R {balance2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_payments1"].configure(text=f"R {total_payments1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_payments2"].configure(text=f"R {total_payments2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_interest1"].configure(text=f"R {total_interest1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_interest2"].configure(text=f"R {total_interest2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["interest1"].configure(text=f"R {interest1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["interest2"].configure(text=f"R {interest2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_capital1"].configure(text=f"R {total_capital1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_capital2"].configure(text=f"R {total_capital2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["capital1"].configure(text=f"R {capital1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["capital2"].configure(text=f"R {capital2:,.2f}",text_color=("#000000", "#b18223"))
            
            if payment_type == "Advance":
                balance1 = (L * (1+e_i)**(np_1)) - X * (1+e_i) * (((1+e_i)**(np_1) - 1)/e_i)
                balance2 = (L * (1+e_i)**(np_2)) - X * (1+e_i) * (((1+e_i)**(np_2) - 1)/e_i)
                if np_1 == np:
                    total_payments1 = (np_1 * X) + L*((1 + (e_i))**(np_1)) - (X * (1+e_i)) * (((1+e_i)**(np_1)-1)/(e_i))
                else:
                    total_payments1 = (np_1 * X)
                if np_2 == np:
                    total_payments2 = (np_2 * X) + L*((1 + (e_i))**(np_2)) - (X * (1+e_i)) * (((1+e_i)**(np_2)-1)/(e_i))
                else:
                    total_payments2 = (np_2 * X)
                total_interest1 = ((1+e_i)**(np_1) - 1)*((L/(1+e_i)) - X/e_i) + (np_1)*X - (e_i*L)/(1+e_i)
                total_interest2 = ((1+e_i)**(np_2) - 1)*((L/(1+e_i)) - X/e_i) + (np_2)*X - (e_i*L)/(1+e_i)
                if np_1 != 1:
                    interest1 = (e_i * L)*(1 + e_i)**(np_1 - 2) - X * (1 + e_i)**(np_1 - 1) + X
                else:
                    interest1 = 0
                if np_2 != 1:
                    interest2 = (e_i * L)*(1 + e_i)**(np_2 - 2) - X * (1 + e_i)**(np_2 - 1) + X
                else:
                    interest2 = 0
                total_capital1 = np_1 * X - total_interest1
                total_capital2 = np_2 * X - total_interest2
                capital1 = X - interest1
                capital2 = X - interest2
                result_labels["balance1"].configure(text=f"R {balance1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["balance2"].configure(text=f"R {balance2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_payments1"].configure(text=f"R {total_payments1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_payments2"].configure(text=f"R {total_payments2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_interest1"].configure(text=f"R {total_interest1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_interest2"].configure(text=f"R {total_interest2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["interest1"].configure(text=f"R {interest1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["interest2"].configure(text=f"R {interest2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_capital1"].configure(text=f"R {total_capital1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["total_capital2"].configure(text=f"R {total_capital2:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["capital1"].configure(text=f"R {capital1:,.2f}",text_color=("#000000", "#b18223"))
                result_labels["capital2"].configure(text=f"R {capital2:,.2f}",text_color=("#000000", "#b18223"))
            
            if total_interest1 > total_interest2:
                int_bet = total_interest1 - total_interest2
                result_labels["int_bet"].configure(text=f"R {int_bet:,.2f}",text_color=("#000000", "#b18223"))
            else:
                int_bet = total_interest2 - total_interest1
                result_labels["int_bet"].configure(text=f"R {int_bet:,.2f}",text_color=("#000000", "#b18223"))
            if total_capital1 > total_capital2:
                cap_bet = total_capital1 - total_capital2
                result_labels["cap_bet"].configure(text=f"R {cap_bet:,.2f}",text_color=("#000000", "#b18223"))
            else:
                cap_bet = total_capital2 - total_capital1
                result_labels["cap_bet"].configure(text=f"R {cap_bet:,.2f}",text_color=("#000000", "#b18223"))

        extra_calc_btn = ctk.CTkButton(btn_frame1,
                            text="Calculate",
                            text_color=("black", "#b18223"),
                            border_width=2,
                            border_color="#996515",
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            command=extra_calc)
        extra_calc_btn.pack(fill="x")
        results = ctk.CTkFrame(extra_frame, fg_color="transparent")
        results.pack(fill="x", expand=True, anchor="n")
        extra_result_frame3 = ctk.CTkFrame(extra_frame, fg_color="transparent")
        extra_result_frame3.pack(side="bottom", fill="x", expand=True)
        extra_result_frame1 = ctk.CTkFrame(results, fg_color="transparent")
        extra_result_frame1.pack(side="left", fill="x", padx=(0, 1), expand=True, anchor="n")
        def extra_result_field1(key, label):
            row_frame = ctk.CTkFrame(extra_result_frame1, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            title = ctk.CTkLabel(row_frame, text=label,text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(anchor="center")
            value = ctk.CTkLabel(row_frame, text="—",text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=14))
            value.pack(anchor="center")
            result_labels[key] = value
        extra_result_frame2 = ctk.CTkFrame(results, fg_color="transparent")
        extra_result_frame2.pack(side="right", fill="x", padx=(1, 0), expand=True, anchor="n")
        def extra_result_field2(key, label):
            row_frame = ctk.CTkFrame(extra_result_frame2, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            title = ctk.CTkLabel(row_frame, text=label,text_color=("#000000", "#b18223"), font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(anchor="center")
            value = ctk.CTkLabel(row_frame, text="—", text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=14))
            value.pack(anchor="center")
            result_labels[key] = value
        
        def extra_result_field3(key, label):
            row_frame = ctk.CTkFrame(extra_result_frame3, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            title = ctk.CTkLabel(row_frame, text=label, text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(anchor="center")
            value = ctk.CTkLabel(row_frame, text="—", text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=14))
            value.pack(anchor="center")
            result_labels[key] = value
        
        extra_result_field1("balance1", "Balance after:")
        extra_result_field2("balance2", "Balance after:")
        extra_result_field1("total_payments1", "Total payments after:")
        extra_result_field2("total_payments2", "Total payments after:")
        extra_result_field1("total_interest1", "Total interest after:")
        extra_result_field2("total_interest2", "Total interest after:")
        extra_result_field1("interest1", "Interest after:")
        extra_result_field2("interest2", "Interest after:")
        extra_result_field1("total_capital1", "Total capital after:")
        extra_result_field2("total_capital2", "Total capital after:")
        extra_result_field1("capital1", "Capital after:")
        extra_result_field2("capital2", "Capital after:")
        extra_result_field3("int_bet", "Interest Paid between:")
        extra_result_field3("cap_bet", "Capital Paid between:")
        
    layout2 = ctk.CTkFrame(tab_2, fg_color="transparent")
    layout2.pack(fill="both", expand=True)
    graph_frame2 = ctk.CTkFrame(layout2, fg_color="transparent")
    graph_frame2.pack(fill="both", expand=True)
    tab_2_canvas_holder = [None]
    tab2_placeholder = ctk.CTkLabel(graph_frame2,
                                    text="Run a calculation to see the graph",
                                    font=ctk.CTkFont(size=16),
                                    text_color="gray")
    tab2_placeholder.pack(expand=True)
    def l_graph(X, L, n , investment_type, rate_type, payment_type, i=None, p=None):
        for widget in graph_frame2.winfo_children():
            widget.destroy()
        if tab_2_canvas_holder[0] is not None:
            tab_2_canvas_holder[0].get_tk_widget().destroy()
            tab_2_canvas_holder[0] = None
        steps = max(int(n * 100), 100)
        xs = [n * t / steps for t in range(steps + 1)]
        ys = []
        for x in xs:
            if investment_type == "Compounded Interest":
                if payment_type == "Arrears":
                    if rate_type == "Effective":
                        ys.append((L * (1 + i)**(x*p)) - X * (((1+i)**(x*p) - 1)/i))
                    else:
                        ys.append((L * (1 + i/p)**(x*p)) - X * (((1+i/p)**(x*p) - 1)/(i/p)))
                if payment_type == "Advance":
                    if rate_type == "Effective":
                        ys.append((L * (1 + i)**(x*p)) - X * (1+i) * (((1+i)**(x*p) - 1)/i))
                    else:
                        ys.append((L * (1 + i/p)**(x*p)) - X * (1+i/p) * (((1+i/p)**(x*p) - 1)/(i/p)))
        bg_color = container.cget("fg_color")
        if isinstance(bg_color, tuple):
            bg_color = bg_color[1 if ctk.get_appearance_mode() == "Dark" else 0]
        text_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        pixel_width = graph_frame2.winfo_width()
        pixel_height = graph_frame2.winfo_height()
        if pixel_width <= 1:
            pixel_width = 1200
        if pixel_height <= 1:
            pixel_height = 600
        fig_width_inches = (pixel_width - 20) / 100
        fig_height_inches = (pixel_height - 20) / 100
        fig = plt.Figure(figsize=(fig_width_inches, fig_height_inches), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_title("Loan Balance Over Time", color=text_color, fontsize=14, fontweight="bold", pad=10)
        ax.grid(True, color=text_color, alpha=0.2, linestyle='--', linewidth=0.5)
        line, = ax.plot(xs, ys, color=("#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"), linewidth=2)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        ax.set_xlabel("Years (n)", color=text_color, fontsize=11)
        ax.set_ylabel("Balance (R)", color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.yaxis.get_major_formatter().set_useMathText(True)
        ax.yaxis.get_offset_text().set_color(text_color)
        fig.subplots_adjust(left=0.1)
        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        canvas.draw()
        import numpy as np
        xdata = np.array(xs)
        ydata = np.array(ys)
        annot = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.4", fc=bg_color, ec="#202020", lw=1.5),
                            arrowprops=dict(arrowstyle="->", color="#202020"),
                            color=text_color, fontsize=10, zorder=10)
        annot.set_visible(False)
        last_idx = -1
        def on_hover(event):
            nonlocal last_idx
            if event.inaxes != ax or event.xdata is None:
                if annot.get_visible():
                    annot.set_visible(False)
                    canvas.draw_idle()
                return
            idx = np.searchsorted(xdata, event.xdata, side='left')
            if idx >= len(xdata):
                idx = len(xdata) - 1
            if idx > 0 and (event.xdata - xdata[idx-1]) < (xdata[idx] - event.xdata):
                idx -= 1
            if idx == last_idx and annot.get_visible():
                return
            last_idx = idx
            x_disp, y_disp = ax.transData.transform((xdata[idx], ydata[idx]))
            dist = ((event.x - x_disp)**2 + (event.y - y_disp)**2)**0.5
            if dist < 35:
                annot.xy = (xdata[idx], ydata[idx])
                annot.set_text(f"n = {xdata[idx]:.2f}\nFV = R {ydata[idx]:,.2f}")
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            canvas.draw_idle()
        canvas.mpl_connect("motion_notify_event", on_hover)
        widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        tab_2_canvas_holder[0] = canvas
        plt.close(fig)

    layout3 = ctk.CTkFrame(tab_3, fg_color="transparent")
    layout3.pack(fill="both", expand=True)
    style = ttk.Style()
    style.theme_use("default")
    current_mode = ctk.get_appearance_mode()
    bg_color = "#2B2B2B" if current_mode == "Dark" else "#DBDBDB"
    text_color = "#b18223" if current_mode == "Dark" else "black"
    header_bg = "#202020" if current_mode == "Dark" else "#F3F3F3"
    style.configure("Treeview", rowheight=35, borderwidth=0, font=("Arial", 14), background=bg_color,
                    foreground=text_color, fieldbackground=bg_color)
    style.map("Treeview", background=[("selected", "#202020")])
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"), borderwidth=0, relief="flat",
                    background=header_bg, foreground=text_color)
    style.map("Treeview.Heading", background=[("active", header_bg)])
    columns = ("Period", "Opening Balance", "Payment", "Interest", "Capital", "Closing Balance")
    tree = ttk.Treeview(layout3, columns=columns, show="headings")
    column_alignments = {
        "Period": "center", 
        "Opening Balance": "center", 
        "Payment": "center",
        "Interest": "center",
        "Capital": "center", 
        "Closing Balance": "center"}
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=column_alignments[col])
    def resize_columns_by_ratio(event):
        total_avail_width = event.width
        column_widths = {"Period": 1, 
                        "Opening Balance": 1.8,
                        "Payment": 1.8, 
                        "Interest": 1.8,
                        "Capital": 1.8,
                        "Closing Balance": 1.8}
        total_parts = sum(column_widths.values())
        for col, ratio in column_widths.items():
                calculated_width = int(total_avail_width * (ratio / total_parts))
                tree.column(col, width=calculated_width, stretch=False)
    tree.bind("<Configure>", resize_columns_by_ratio)
    scrollbar = ttk.Scrollbar(layout3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    def l_populate_table(X, L, n, p, i, investment_type, rate_type, payment_type, small_payment):
        tree.delete(*tree.get_children())
        if investment_type == "Continuous Interest":
            total_periods = int(math.ceil(n)) if n is not None else 0
        else:
            total_periods = int(math.ceil(n * p)) if n is not None and p is not None else 0
            new_total_periods = total_periods + 1
        for k in range(1, new_total_periods):
            if k == total_periods:
                pay = small_payment
            else:
                 pay =  X
            if payment_type == "Arrears":
                if rate_type == "Nominal":
                    bal_start = (L * (1 + (i/p))**(k-1)) - X * (((1+(i/p))**(k-1) - 1)/(i/p))
                    inter = bal_start * (i/p)
                    cap = pay - inter
                    bal_end = (L * (1 + (i/p))**(k)) - X * (((1+(i/p))**(k) - 1)/(i/p))
                if rate_type == "Effective":
                    bal_start = (L * (1 + i)**(k-1)) - X * (((1+i)**(k-1) - 1)/i)
                    inter = bal_start * i
                    cap = pay - inter
                    bal_end = (L * (1 + i)**(k)) - X * (((1+i)**(k) - 1)/i)
                if pay>=bal_start and k == total_periods:
                    bal_end = 0
            else: 
                if rate_type == "Nominal":
                    if k != total_periods:
                        bal_start = (L * (1 + (i/p))**(k-1)) - X * (1 + (i/p)) * (((1+(i/p))**(k-1) - 1)/(i/p)) - X
                    if k == 1:
                        inter = 0
                        cap = pay
                    else:
                        inter = bal_start_new * (i/p)
                        cap = pay - inter
                    bal_start_new = bal_start
                    bal_end = (L * (1 + (i/p))**(k)) - X * (1 + (i/p)) * (((1+(i/p))**(k) - 1)/(i/p))
                    if pay>=bal_end and k == total_periods:
                        bal_start = 0
                        bal_end = 0
                if rate_type == "Effective":
                    if k != total_periods:
                        bal_start = (L * (1 + i)**(k-1)) - X * (1 + (i)) * (((1+i)**(k-1) - 1)/i) - X
                    if k == 1:
                        inter = 0
                        cap = pay
                    else:
                        inter = bal_start_new * (i)
                        cap = pay - inter
                    bal_start_new = bal_start
                    bal_end = (L * (1 + (i))**(k)) - X * (1 + (i)) * (((1+(i))**(k) - 1)/(i))
                    if pay>=bal_end and k == total_periods:
                        bal_start = 0
                        bal_end = 0
                    

            tree.insert("", "end", values=(k,
                                            f"R {bal_start:,.2f}".replace(",", " "),
                                            f"R {pay:,.2f}".replace(",", " "),
                                            f"R {inter:,.2f}".replace(",", " "),
                                            f"R {cap:,.2f}".replace(",", " "),
                                            f"R {bal_end:,.2f}".replace(",", " ")))
    
    def l_calculated():
        error_label.configure(text="", text_color=("#000000", "#b18223"))
        investment_type = list1_1.get()
        rate_type = list1_3.get()
        payment_type = list1_4.get()
        solve_for = selected_solve_for
        values = {}
        for key, entry in entries.items():
            raw = entry.get().strip()
            if raw == "":
                values[key] = None
            else:
                try:
                    values[key] = float(raw)
                except ValueError:
                    print(f"Invalid input for {key}: {raw}")
                    return
        X = values.get("X")
        L = values.get("L")
        i = values.get("i")
        n = values.get("n")
        p = values.get("p")
        δ = values.get("δ")
        np_value = None
        interest_payed = None
        try:
            if i is not None:
                i = i / 100
            if investment_type == "Compounded Interest" and payment_type == "Arrears":
                if rate_type == "Nominal":
                    if solve_for == "L":
                        result = X * ((1 - (1 + i/p)**(-n*p))/(i/p))
                        L = result
                    elif solve_for == "X":
                        result = L / ((1 - (1 + i/p)**(-n*p))/(i/p))
                        X = result
                    elif solve_for == "n":
                        result = math.log(1 - ((L * (i/p))/X)) / (-p*math.log(1 + (i/p)))
                        n = result
                    elif solve_for == "i":
                        N = n * p
                        try:
                            a = 2 * (X * N - L) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * ((1 - (1 + a) ** (-N)) / a) - L) / (X * (N * a * (1 + a) ** (-N - 1) - 1 + (1 + a) ** (-N)) / (a * a))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                    a_np = math.ceil(n*p) - 1
                    total_payments = (a_np * X) + (L*((1 + (i/p))**(a_np)) - X * (((1+i/p)**(a_np)-1)/(i/p)))*(1 + i/p)
                    small_payment =  (L*((1 + (i/p))**(a_np)) - X * (((1+i/p)**(a_np)-1)/(i/p)))*(1 + i/p)
                    total_interest = ((i/p)*L - X) * (((1 + (i/p))**(a_np + 1) - 1)/(i/p)) + (a_np + 1)*X
                elif rate_type == "Effective":
                    if solve_for == "L":
                        result = X * ((1 - (1 + i)**(-n*p))/(i))
                        L = result
                    elif solve_for == "X":
                        result = L / ((1 - (1 + i)**(-n*p))/(i))
                        X = result
                    elif solve_for == "n":
                        result = math.log(1 - ((L * (i))/X)) / (-p*math.log(1 + (i)))
                        n = result
                    elif solve_for == "p":
                        result = math.log(1 - ((L * (i))/X)) / (-n*math.log(1 + (i)))
                        p = result
                    elif solve_for == "i":
                        N = n * p
                        try:
                            a = 2 * (X * N - L) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for q in range(1, 2001):
                            result = a - (X * ((1 - (1 + a) ** (-N)) / a) - L) / (X * (N * a * (1 + a) ** (-N - 1) - 1 + (1 + a) ** (-N)) / (a * a))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a
                        result = a * 100
                    a_np = math.ceil(n*p) - 1
                    total_payments = (a_np * X) + (L*((1 + (i))**(a_np)) - X * (((1+i)**(a_np)-1)/(i)))*(1 + i)
                    small_payment =  (L*((1 + (i))**(a_np)) - X * (((1+i)**(a_np)-1)/(i)))*(1 + i)
                    total_interest = (i*L - X) * (((1 + i)**(a_np + 1) - 1)/i) + (a_np + 1)*X 
            if investment_type == "Compounded Interest" and payment_type == "Advance":
                if rate_type == "Nominal":
                    if solve_for == "L":
                        result = X * (1 + (i / p)) * (1 - (1 + (i / p))**(-n*p)) / (i / p)
                        L = result
                    elif solve_for == "X":
                        result = L / ((1 + (i / p)) * (1 - (1 + (i / p))**(-n*p)) / (i / p))
                        X = result
                    elif solve_for == "n":
                        result = -math.log(1 - (L * (i / p)) / (X * (1 + (i / p)))) / (p * math.log(1 + (i / p)))
                        n = result
                    elif solve_for == "i":
                        N = n * p
                        try:
                            a = 2 * (X * N - L) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for _ in range(2000):
                            result = a - (X * (1 + a) * (1 - (1 + a)**(-N)) / a - L) / (X * (-1 + (1 + a)**(-N) * (N * (1 + a) - (N - 1))) / (a * a))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        i = a * p
                        result = a * 100 * p
                    a_np = math.ceil(n*p) - 1
                    total_payments = (a_np * X) + L*((1 + (i/p))**(a_np)) - (X * (1+i/p)) * (((1+i/p)**(a_np)-1)/(i/p))
                    small_payment = L*((1 + (i/p))**(a_np)) - (X * (1+i/p)) * (((1+i/p)**(a_np)-1)/(i/p))
                    total_interest = ((1+(i/p))**(a_np + 1) - 1)*((L/(1+(i/p))) - X/(i/p)) + (a_np + 1)*X - ((i/p)*L)/(1+(i/p))
                elif rate_type == "Effective":
                    if solve_for == "L":
                        result = X * (1 + i) * (1 - (1 + i)**(-n*p)) / i
                        L = result
                    elif solve_for == "X":
                        result = L / ((1 + i) * (1 - (1 + i)**(-n*p)) / i)
                        X = result
                    elif solve_for == "n":
                        result = -math.log(1 - (L * i) / (X * (1 + i))) / (p * math.log(1 + i))
                        n = result
                    elif solve_for == "p":
                        result = -math.log(1 - (L * i) / (X * (1 + i))) / (n * math.log(1 + i))
                        p = result
                    elif solve_for == "i":
                        N = n * p
                        try:
                            a = 2 * (X * N - L) / (X * N * (N + 1))
                            if a <= 0:
                                a = 0.01
                        except:
                            a = 0.05
                        for _ in range(2000):
                            result = a - (X * (1 + a) * (1 - (1 + a)**(-N)) / a - L) / (X * (-1 + (1 + a)**(-N) * (N * (1 + a) - (N - 1))) / (a * a))
                            if abs(result - a) < 1e-8:
                                a = result
                                break
                            a = result
                        result = a * 100
                    a_np = math.ceil(n*p) - 1
                    total_payments = (a_np * X) + L*((1 + (i))**(a_np)) - (X * (1+i)) * (((1+i)**(a_np)-1)/(i))
                    small_payment = L*((1 + (i))**(a_np)) - (X * (1+i)) * (((1+i)**(a_np)-1)/(i)) 
                    total_interest = ((1+i)**(a_np+1) - 1)*((L/(1+i)) - X/i) + (a_np+1)*X - (i*L)/(1+i)
            interest_payed = 0
            np_value = math.ceil(n * p)
            result_labels["interest_type"].configure(text=investment_type, text_color=("#000000", "#b18223"))
            result_labels["rate_type"].configure(text=rate_type, text_color=("#000000", "#b18223"))
            display_map = {"L": (L,  lambda v: f"R {v:,.2f}"),
                        "X": (X,  lambda v: f"R {v:,.2f}"),
                        "i": (i if i is not None else δ,   lambda v: f"{v*100:.4f}%"),
                        "n": (n,   lambda v: f"{v}"),
                        "p": (p,   lambda v: f"{v:.0f}"),
                        "np": (np_value, lambda v: f"{v:.0f}"),
                        "total_payments": (total_payments, lambda v: f"R {v:,.2f}"),
                        "small_payment": (small_payment, lambda v: f"R {v:,.2f}"),
                        "total_interest": (total_interest, lambda v: f"R {v:,.2f}")}
                        
            for key, (val, fmt) in display_map.items():
                if val is not None:
                    result_labels[key].configure(text=fmt(val), text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = val
                else:
                    result_labels[key].configure(text="—", text_color=("#000000", "#b18223"))
                    result_labels[key].raw_value = None
            if solve_for == "i":
                result_labels[solve_for].configure(text=f"{result:.4f}%", text_color=("#000000", "#b18223"))
            elif solve_for == "n":
                result_labels[solve_for].configure(text=f"{result:.4f}", text_color=("#000000", "#b18223"))
            elif solve_for == "L" or solve_for == "X":
                result_labels[solve_for].configure(text=f"R {result:,.2f}", text_color=("#000000", "#b18223"))
            elif solve_for == "p" or solve_for == "np":
                result_labels[solve_for].configure(text=f"{result:.0f}", text_color=("#000000", "#b18223"))
            for key, label in result_labels.items():
                if key in ("interest_type", "rate_type"):
                    continue
                label.configure(font=ctk.CTkFont(size=18))
            solved_key = solve_for
            if solved_key in result_labels:
                result_labels[solved_key].configure(font=ctk.CTkFont(size=18, weight="bold"))
            
            if L is not None and X is not None and n is not None:
                if investment_type == "Compounded Interest" and L is not None and i is not None and p is not None:
                    l_update_chart(L, total_interest)
                else:
                    if chart_canvas_holder[0] is not None:
                        chart_canvas_holder[0].get_tk_widget().destroy()
                        chart_canvas_holder[0] = None
            else:
                if chart_canvas_holder[0] is not None:
                    chart_canvas_holder[0].get_tk_widget().destroy()
                    chart_canvas_holder[0] = None
            l_entry(np_value=np_value, X=X, L=L, n=n, investment_type=investment_type,
                                rate_type=rate_type,payment_type=payment_type, i=i, p=p)
            l_graph(X=X, L=L, n=n, investment_type=investment_type,
                                rate_type=rate_type, payment_type=payment_type, i=i, p=p)
            l_populate_table(X=X, L=L, n=n, p=p, i=i, investment_type=investment_type, rate_type=rate_type, payment_type=payment_type, small_payment=small_payment)
        except ZeroDivisionError:
            error_label.configure(text="Error: Division with zero. Check inputs.")
        except ValueError as e:
            error_label.configure(text="Error: Invalid Calculation. Check inputs.")
        except Exception as e:
            error_label.configure(text=f"Error: {str(e)}")

    calc_btn = ctk.CTkButton(left,
                            text="Calculate",
                            text_color=("black", "#b18223"),
                            border_width=2,
                            border_color="#996515",
                            font=ctk.CTkFont(size=24, weight="bold"),
                            fg_color="#202020",
                            hover_color="#2b2b2b",
                            width=250,
                            command=l_calculated)
    calc_btn.pack(anchor="w", pady=(10, 0))

def build_about_page(page):
    title_frame = ctk.CTkFrame(page, fg_color="transparent")
    title_frame.pack(pady=(10, 5))
    main_icon = ctk.CTkLabel(title_frame,
                            image = icons["About_large"],
                            text="", text_color=("#000000", "#b18223"))
    main_icon.pack(side="left", padx=10)
    main_title = ctk.CTkLabel(title_frame,
                                text="About", text_color=("#000000", "#b18223"),
                                font=ctk.CTkFont(size=45))
    main_title.pack(side="left")
    line = ctk.CTkFrame(page,
                        height=2,
                        fg_color=("#000000", "#996515"))
    line.pack(fill="x", padx=20, pady=(10, 0))
    layout = ctk.CTkFrame(page, fg_color="transparent")
    layout.pack(fill="both", expand=True)
    layout4 = ctk.CTkFrame(layout, fg_color="transparent")
    layout4.pack(fill="both", expand=True)
    layout4.pack_propagate(False)
    scroll = ctk.CTkScrollableFrame(layout4, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=20, pady=10)
    def add_definition(parent, symbol, formal, plain):
        card = ctk.CTkFrame(parent, fg_color=("#CBCBCB", "#3a3a3a"), corner_radius=10)
        card.pack(fill="x", pady=6)
        ctk.CTkLabel(card, text=symbol, text_color=("#000000", "#b18223"),
                    font=ctk.CTkFont(size=22, weight="bold"),
                    anchor="w").pack(anchor="w", padx=15, pady=(10, 2))
        if "\\" in formal or "_" in formal or "^" in formal:
            try:
                latex_str = f"${formal}$"
                text_color = "#b18223" if ctk.get_appearance_mode() == "Dark" else "#996515"

                probe_fig = plt.Figure(figsize=(20, 3), dpi=100, facecolor='none')
                probe_text = probe_fig.text(0, 0, latex_str, fontsize=18, color=text_color)
                probe_canvas = FigureCanvasTkAgg(probe_fig, master=None)
                probe_canvas.draw()
                bbox = probe_text.get_window_extent(renderer=probe_canvas.get_renderer())
                plt.close(probe_fig)

                padding_w, padding_h = 20, 10
                width_in = max((bbox.width + padding_w) / 100, 0.3)
                height_in = max((bbox.height + padding_h) / 100, 0.3)

                fig = plt.Figure(figsize=(width_in, height_in), dpi=100, facecolor='none')
                fig.text(0, 0, latex_str, fontsize=18, color=text_color,
                         verticalalignment="bottom", horizontalalignment="left")
                canvas = FigureCanvasTkAgg(fig, master=None)
                canvas.draw()
                rgba = canvas.buffer_rgba()
                img = Image.frombuffer("RGBA", canvas.get_width_height(), rgba, "raw", "RGBA", 0, 1)
                plt.close(fig)
                w, h = canvas.get_width_height()
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
                math_label = ctk.CTkLabel(card, image=ctk_img, text="", text_color=("#000000", "#b18223"))
                math_label.pack(anchor="w", padx=15, pady=(0, 4))
            except Exception as e:
                ctk.CTkLabel(card, text=formal, text_color=("#000000", "#b18223"),font=ctk.CTkFont(size=18)).pack(anchor="w", padx=15, pady=(0, 4))
        else:
            ctk.CTkLabel(card, text=formal, text_color=("#000000", "#b18223"),
                        font=ctk.CTkFont(size=18),
                        anchor="w", wraplength=1100, justify="left").pack(anchor="w", padx=15, pady=(0, 4))
        ctk.CTkLabel(card, text=plain, text_color=("#000000", "#b18223"),
                    font=ctk.CTkFont(size=16), 
                    anchor="w", wraplength=1100, justify="left").pack(anchor="w", padx=15, pady=(0, 10))
    add_definition(scroll,
        "Simple Interest - Single Investment",
        r"FV = PV(1 + i \cdot np)",
        "Interest is calculated using the original investment amount only.")
    add_definition(scroll,
        "Compounded Interest - Single Investment",
        r"FV = PV \left(1 + \frac{i^{(p)}}{p}\right)^{np}",
        "Interest is calculated using the sum of the original investment amount and the interest earned during the previous period.")
    add_definition(scroll,
        "Continuous Interest - Single Investment",
        r"FV = PV e^{\delta n}",
        "Compounded interest where the number of compoundings are infinite.")
    add_definition(scroll,
        "Future Value - FV",
        "The sum of the original cash flow and all the interest additions made during the investment period.",
        "How much your money will be worth later.")
    add_definition(scroll,
        "Present Value - PV",
        "The once off amount that needs to be invested at the beginning of the investment period to accumulate to the amount at the end of the investment period",
        "How much a future amount is worth today.")
    add_definition(scroll,
        "Interest Rate - i",
        "The profit earned on a savings account or investment",
        "Can be Simple, Effective, Nominal or Continuous. For this app, all rates, except continuous, use 'i' as notation")
    add_definition(scroll,
        "Simple Interest Rate",
        r"\text{Notation: } i",
        "Interest only on the original deposit",)
    add_definition(scroll,
        "Effective Interest Rate",
        r"Notation: \frac{i^{(p)}}{p}",
        "Compounded Interest of each period")
    add_definition(scroll,
        "Nominal Interest Rate",
        r"Notation: {i^{(p)}}",
        "Compounded Interest in one year")
    add_definition(scroll,
        "Continuous Interest Rate",
        r"\text{Notation: } {\delta}",
        "Force of Interest, compounded infinitely")
    add_definition(scroll,
        "Period - p",
        "How many times interest is applied per year",
        "Examples: 12 for monthly or 4 for quarterly")
    add_definition(scroll,
        "Years - n",
        "Total amount of time",
        "")
    add_definition(scroll,
        "Effective Annual Rate from Nominal Rate",
        r"i = \left(1 + \frac{i^{(p)}}{p}\right)^{p} - 1",
        "Converts a nominal interest rate, compounded p times a year, into the equivalent effective annual rate.")
    add_definition(scroll,
        "Annuity (level)",
        "A series of equal payments made at regular time intervals.",
        "Examples: monthly savings deposits, regular loan repayments.")
    add_definition(scroll,
        "Annuity Certain",
        "Payment is made at the end of every period (in arrears).",
        "The most common type of annuity.")
    add_definition(scroll,
        "Annuity Due",
        "Payment is made at the beginning of every period (in advance).",
        "")
    add_definition(scroll,
        "Future Value of an Annuity Certain",
        r"FV = X \cdot \frac{\left(1 + \frac{i^{(p)}}{p}\right)^{np} - 1}{\frac{i^{(p)}}{p}}",
        "The accumulated amount in the account after all the regular payments (X) were made, at the end of every period, and interest added.")
    add_definition(scroll,
        "Present Value of an Annuity Certain",
        r"PV = X \cdot \frac{1 - \left(1 + \frac{i^{(p)}}{p}\right)^{-np}}{\frac{i^{(p)}}{p}}",
        "The single amount that should be invested today to lead to the same accumulated amount as the regular payments (X).")
    add_definition(scroll,
        "Future Value of an Annuity Due",
        r"FV = \frac{X\left(1 + \frac{i^{(p)}}{p}\right)\left[\left(1 + \frac{i^{(p)}}{p}\right)^{np} - 1\right]}{\frac{i^{(p)}}{p}}",
        "The accumulated amount in the account after all the regular payments (X) were made, at the beginning of every period, and interest added.")
    add_definition(scroll,
        "Payment - X",
        "The amount paid at the regular time intervals.",
        "")
    add_definition(scroll,
        "Loan",
        "A single amount that gains interest. Interest is paid because somebody else's money is used.",
        "")
    add_definition(scroll,
        "Loan Repayments",
        "The payments on a loan are a series (annuity) and every payment earns interest over time.",
        "")
    add_definition(scroll,
        "Loan Equation - Future Value",
        r"L(1+i)^{n} = \frac{X\left[(1+i)^{n} - 1\right]}{i}",
        "The accumulated value of the loan must equal the accumulated value of all the repayments (X) for the loan to be paid off.")
    add_definition(scroll,
        "Loan Equation - Present Value",
        r"L = \frac{X\left[1 - (1+i)^{-n}\right]}{i}",
        "Determines the loan amount (L), given the repayment amount (X), for a loan repaid in arrears.")
    add_definition(scroll,
        "Loan Equation - Repayments in Advance",
        r"L(1+i)^{n} = \frac{X(1+i)\left[(1+i)^{n} - 1\right]}{i}",
        "Used when repayments (X) are made at the beginning of every period instead of the end.")
    add_definition(scroll,
        "Interest Component",
        "Fee charged for the use of somebody else's money.",
        "The portion of a repayment that covers the cost of borrowing.")
    add_definition(scroll,
        "Capital Component",
        "Additional amount paid beyond the interest payment made.",
        "The portion of a repayment that reduces the outstanding loan balance.")
    add_definition(scroll,
        "Balance (Outstanding Loan Balance)",
        "The outstanding balance on a loan at any time t is the difference between the future value of the loan and the future value of the repayments made up to that time.",
        "")
    add_definition(scroll,
        "Balance at Time n - Arrears",
        r"B_{t=n} = L(1+i)^{n} - X\frac{(1+i)^{n} - 1}{i}",
        "The remaining amount owed on a loan repaid in arrears, after n repayments.")
    add_definition(scroll,
        "Balance at Time n - Advance",
        r"B_{t=n} = L(1+i)^{n} - X(1+i)\frac{(1+i)^{n} - 1}{i}",
        "The remaining amount owed on a loan repaid in advance, after n repayments.")
    add_definition(scroll,
        "Total Interest Paid",
        r"S^{(R)} = \left(iL - X\right)\frac{(1+i)^{n} - 1}{i} + nX",
        "The sum of all interest components paid over the full term of the loan.")
    add_definition(scroll,
        "Total Capital Paid",
        r"S_n^{(K)} = (X - Li)(1+i)^{n-1}",
        "The sum of all capital components paid over the full term of the loan.")
    add_definition(scroll,
        "Last Payment",
        "Balance at the start of the last period, multiplied by (1 + periodic interest rate of last period).",
        "Used when the final repayment differs from the regular instalment amount, to fully settle the loan.")
    add_definition(scroll,
        "Force of Interest (Continuous Interest Rate)",
        r"\delta = \ln(1+i)",
        "The interest rate when the number of compounding periods becomes infinitely large and the rate per period becomes infinitely small.")
    add_definition(scroll,
        "Relationship Between Interest Rates",
        r"(1+i) = \left(1 + \frac{i^{(p)}}{p}\right)^{p} = e^{\delta}",
        "Shows how the effective, nominal, and continuous interest rates relate to and can be converted into one another.")
    add_definition(scroll,
        "Future Value - Continuous Annuity",
        r"FV = \frac{X\left[e^{\delta n} - 1\right]}{\delta}",
        "The accumulated amount when payments (X) are made continuously throughout each year, under a continuous interest rate.")
    add_definition(scroll,
        "Present Value - Continuous Annuity",
        r"PV = \frac{X\left[1 - e^{-\delta n}\right]}{\delta}",
        "The single amount today that is equivalent to a continuous series of payments (X), under a continuous interest rate.")
    add_definition(scroll,
        "Increasing Annuity",
        "A series of payments made at regular time intervals where the payment amount grows over time instead of staying level.",
        "Examples: retirement contributions that rise with your salary, or savings that increase with inflation each year.")
    add_definition(scroll,
        "j - Growth Rate",
        "The percentage by which each payment (or each group of payments) increases relative to the previous one.",
        "Not to be confused with the interest rate i, which is what the payments earn once invested.")
    add_definition(scroll,
        "FV - Increasing Annuity, Every Payment Increases (Arrears)",
        r"FV = \frac{X\left[(1+r)^{np} - (1+j)^{np}\right]}{r - j}",
        "Accumulated amount when every single payment (paid at the end of each period) is j% larger than the one before it.")
    add_definition(scroll,
        "FV - Increasing Annuity, Every Payment Increases (Advance)",
        r"FV = \frac{X(1+r)\left[(1+r)^{np} - (1+j)^{np}\right]}{r - j}",
        "Same as the arrears version, but payments are made at the start of each period instead of the end.")
    add_definition(scroll,
        "r - Effective Period Rate",
        r"r = \frac{i^{(p)}}{p}",
        "The interest rate actually earned per payment period, used in the increasing annuity formulas.")
    add_definition(scroll,
        "FV - Increasing Annuity, Every k Payments Increase (Arrears)",
        r"FV = X \cdot \frac{(1+r)^{k}-1}{r} \times \frac{(1+r)^{km}-(1+j)^{m}}{(1+r)^{k}-(1+j)}",
        "Accumulated amount when payments stay level for a group of k periods, then step up by j% for the next group, repeated m times.")
    add_definition(scroll,
        "FV - Increasing Annuity, Every k Payments Increase (Advance)",
        r"FV = X(1+r) \cdot \frac{(1+r)^{k}-1}{r} \times \frac{(1+r)^{km}-(1+j)^{m}}{(1+r)^{k}-(1+j)}",
        "Same as the k-period arrears version, but each payment is made at the start of its period instead of the end.")
    add_definition(scroll,
        "k - Level Period Length",
        "The number of payments that stay the same amount before the next increase is applied.",
        "Example: k = 12 if payments are monthly but only increase once a year.")
    add_definition(scroll,
        "m - Number of Increase Groups",
        "The number of times the payment level changes over the full term, including the first, unincreased group.",
        "Example: a payment that starts level and increases 3 times has m = 4 groups in total.")
    add_definition(scroll,
        "Special Case - No Increase",
        "Setting k = np and j = 0 in the k-period increasing annuity formula reduces it back to the standard level annuity formula.",
        "Confirms the increasing annuity formula is a generalisation of the ordinary annuity formula.")
    add_definition(scroll,
        "Special Case - Every Payment Increases",
        "Setting k = 1 in the k-period increasing annuity formula reduces it to the every-payment-increasing formula.",
        "Confirms the k-period formula also generalises the every-payment-increasing case.")

if __name__=="__main__":
    ctk.set_appearance_mode("dark")
    mode = ctk.get_appearance_mode()
    def get_display_scale():
        try:
            ctypes.windll.user32.SetProcessDPIAware()
            dpi = ctypes.windll.user32.GetDpiForSystem()
            dpi_scale = dpi / 96
            phys_w = ctypes.windll.user32.GetSystemMetrics(0)
            phys_h = ctypes.windll.user32.GetSystemMetrics(1)
            return dpi_scale, phys_w, phys_h
        except Exception:
            return 1.0, 1920, 1080
    current_scale, current_w, current_h = get_display_scale()
    ref_w = 1920
    ref_h = 1080
    dpi_scale = 1.25 / current_scale
    res_correction = min(current_w / ref_w, current_h / ref_h)
    res_correction = max(0.55, min(res_correction, 1.5))
    scale = dpi_scale * res_correction
    ctk.set_widget_scaling(scale)
    app = ctk.CTk()

    app.title("Kin Calculator")
    def on_closing():
        os._exit(0)
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.after(250, lambda: app.iconbitmap(resource_path("Icons/Sidebar.ico")))
    app.geometry("800x450")
    app.after(0, lambda: app.state('zoomed'))

    loading_frame = ctk.CTkFrame(app, fg_color=("#DBDBDB", "#2B2B2B"))
    loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    loading_frame.lift()

    loading_logo_image = ctk.CTkImage(
        light_image=Image.open(resource_path("Icons/Sidebar.png")).convert("RGBA"),
        dark_image=Image.open(resource_path("Icons/Sidebar.png")).convert("RGBA"),
        size=(90, 90),
    )
    loading_logo = ctk.CTkLabel(loading_frame, text="", image=loading_logo_image)
    loading_logo.place(relx=0.5, rely=0.36, anchor="center")

    loading_label = ctk.CTkLabel(
        loading_frame,
        text="Kin Calculator",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=("#000000", "#b18223"),
    )
    loading_label.place(relx=0.5, rely=0.46, anchor="center")

    status_label = ctk.CTkLabel(
        loading_frame,
        text="Starting...",
        font=ctk.CTkFont(size=14),
        text_color=("#000000", "#b18223"),
    )
    status_label.place(relx=0.5, rely=0.52, anchor="center")

    progress_bar = ctk.CTkProgressBar(
        loading_frame,
        width=320,
        progress_color=("#996515", "#b18223"),
    )
    progress_bar.place(relx=0.5, rely=0.57, anchor="center")
    progress_bar.set(0)

    loading_steps = []
    app_state = {}

    def add_step(text, fn):
        loading_steps.append((text, fn))

    def step_load_icons():
        global icons
        icons = load_icons()
        app_state["icons"] = icons

    def step_skeleton():
        global container
        container, app_state["sidebar"] = skeleton(mode)
        app_state["container"] = container

    def step_make_pages():
        global home_page, rate_page, single_investment_page, annuity_page
        global increasing_annuity_page, loan_page, settings_page, about_page, date_page
        container = app_state["container"]
        home_page = ctk.CTkFrame(container)
        rate_page = ctk.CTkFrame(container)
        single_investment_page = ctk.CTkFrame(container)
        annuity_page = ctk.CTkFrame(container)
        increasing_annuity_page = ctk.CTkFrame(container)
        loan_page = ctk.CTkFrame(container)
        settings_page = ctk.CTkFrame(container)
        about_page = ctk.CTkFrame(container)
        date_page = ctk.CTkFrame(container)
        app_state["home_page"] = home_page
        app_state["rate_page"] = rate_page
        app_state["single_investment_page"] = single_investment_page
        app_state["annuity_page"] = annuity_page
        app_state["increasing_annuity_page"] = increasing_annuity_page
        app_state["loan_page"] = loan_page
        app_state["settings_page"] = settings_page
        app_state["about_page"] = about_page
        app_state["date_page"] = date_page
        for key in ("home_page", "rate_page", "single_investment_page",
                    "annuity_page", "increasing_annuity_page",
                    "loan_page", "about_page"):
            app_state[key].place(relx=0, rely=0, relwidth=1, relheight=1)
        loading_frame.lift()

    def step_build_home():
        build_home_page(app_state["home_page"])

    def step_build_rate():
        build_rate_page(app_state["rate_page"])

    def step_build_single_investment():
        build_single_investment_page(app_state["single_investment_page"])

    def step_build_annuity():
        build_annuity_page(app_state["annuity_page"])

    def step_build_increasing_annuity():
        build_increasing_annuity_page(app_state["increasing_annuity_page"])

    def step_build_loan():
        build_loan_page(app_state["loan_page"])

    def step_build_about():
        build_about_page(app_state["about_page"])

    def step_finalize():
        app_state["home_page"].tkraise()
        buttons(app_state["icons"], app_state["container"], app_state["sidebar"],
                mode, app_state["home_page"], app_state["rate_page"])

    def step_reveal():
        loading_frame.destroy()

    add_step("Loading icons...", step_load_icons)
    add_step("Building layout...", step_skeleton)
    add_step("Preparing pages...", step_make_pages)
    add_step("Building home page...", step_build_home)
    add_step("Building rate and date tools...", step_build_rate)
    add_step("Building single investment page...", step_build_single_investment)
    add_step("Building annuity page...", step_build_annuity)
    add_step("Building increasing annuity page...", step_build_increasing_annuity)
    add_step("Building loan page...", step_build_loan)
    add_step("Building about page...", step_build_about)
    add_step("Finishing up...", step_finalize)
    add_step("Done", step_reveal)

    total_steps = len(loading_steps)

    def run_next_step(index=0):
        if index >= total_steps:
            return
        text, fn = loading_steps[index]
        status_label.configure(text=text)
        loading_frame.update_idletasks()
        fn()
        is_last_step = (index == total_steps - 1)
        if not is_last_step:
            loading_frame.lift()
            progress_bar.set((index + 1) / total_steps)
            loading_frame.update_idletasks()
            app.after(1, lambda: run_next_step(index + 1))

    app.update_idletasks()
    app.update()

    app.after(1, run_next_step)

    app.mainloop()