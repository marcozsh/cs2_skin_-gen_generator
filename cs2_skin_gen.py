import requests
import json
import pyperclip as clipboard
import sqlite3
from datetime import datetime
from flet_contrib.color_picker import ColorPicker

import flet as ft

URL = "https://api.cs2inspects.com/getGenCode?url="


class DataBase:
    def __init__(self, db_name="cs2_skin_gen.db"):
        self.db_name = db_name
    
    def check_bd(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE settings(id integer primary key, color varchar(100), date_time varchar(250))")
        except Exception as e:
            print(e)
        return conn


    def save_settings(self,BD,color):
        try:
            cur = BD.cursor()
            cur.execute("INSERT INTO settings (id, color, date_time) VALUES (1, ?, ?  )", [color, datetime.now()])
            BD.commit()
        except Exception as e:
            print(e)
    

    def update_settings(self, BD, color):
        try:
            cur = BD.cursor()
            data = self.read_settings(BD)
            if len(data) == 0:
                self.save_settings(BD, color)
            else:
                cur.execute("UPDATE settings set color = ? WHERE id = 1", [color])
                BD.commit()
        except Exception as e:
            print(e)
            
    def read_settings(self, BD):
        data = []
        try:
            cur = BD.cursor()
            cur.execute("SELECT color, date_time FROM settings WHERE id = 1")
            data = cur.fetchall()
        except Exception as e:
            print(e)
        return data


def main(page: ft.Page):
    
    data_base = DataBase()
    color_settings = data_base.read_settings(data_base.check_bd())
    app_color = "#FF0000" if len(color_settings) == 0 else color_settings[0][0]

    def open_dialog(txt, title="ALERT!"):
        dialog.title = ft.Text(title)
        dialog.content = ft.Text(txt)
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog( modal= True
                            ,actions=[
                                ft.TextButton("OK", on_click=close_dialog)
                            ], actions_alignment=ft.alignment.center)
    
    def snack_bar(text):
        return ft.SnackBar(ft.Text(
                        spans=[ 
                                ft.TextSpan(text, 
                                                style=ft.TextStyle(color=ft.colors.WHITE))
                                        ],), 
                                bgcolor=ft.colors.BACKGROUND,)

    def copy_to_clipboard(text, item_name = ""):
        if "!g" in text:
            clipboard.copy(text)
            page.snack_bar = snack_bar(f"Code !gen for \"{item_name}\" copied")
            page.snack_bar.open = True
            page.update()

    def gen_code(e):
        if len(skin_link.value.strip()) == 0:
            open_dialog("Please provide a CS2 link preview", "WARNING")
            return

        if "csgo_econ_action_preview" not in skin_link.value.strip():
            open_dialog("CS2 Link preview not valid", "WARNING")
            return
        gen_code_request = requests.get(f"{URL}{skin_link.value.strip()}")
        gen_code_json = json.loads(gen_code_request.text)

        table_rows= ft.DataRow(
                cells=[
                    ft.DataCell( ft.Text(gen_code_json["genCodeDetail"]["Item_ID"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Skin_FullName"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Float"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Pattern_ID"])),
                    ft.DataCell(ft.Text(gen_code_json["genCode"])),
                ],on_select_changed=lambda e :copy_to_clipboard(gen_code_json["genCode"], gen_code_json["genCodeDetail"]["Skin_FullName"])
            )
        temp_data_table.rows.insert(0,table_rows)
        clear_list_button.visible = True
        skin_link.value = ""
        page.update()
    
    def clear_table(e):
        temp_data_table.rows.clear()
        clear_list_button.visible = False
        page.update()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter":
            gen_code(e)

    def set_app_theme():
        color = color_picker.color
        config_table.border = ft.border.all(2, color)
        search_button_config.color = color
        set_color_button.color = color
        t.divider_color = color
        t.indicator_color = color
        t.label_color = color
        app_bar.bgcolor = color

        page.update()
    
    def save_settings(e):
        db= data_base.check_bd()
        color = color_picker.color
        config_table.border = ft.border.all(2, color)
        search_button_config.color = color
        set_color_button.color = color
        temp_data_table.border = ft.border.all(2, color)
        skin_link.border_color = color
        search_button.color = color
        clear_list_button.color = color
        t.divider_color = color
        t.indicator_color = color
        t.label_color = color
        app_bar.bgcolor = color
        data_base.update_settings(db,color)
        db.close()
        page.snack_bar = snack_bar("Color Saved!")
        page.snack_bar.open = True
        page.update()

    data_base.check_bd()

    color_picker = ColorPicker(on_change_color_picker=set_app_theme,color=app_color)

    set_color_button = ft.ElevatedButton(text="Change Color", on_click=save_settings, color=app_color)

    clear_list_button = ft.ElevatedButton(text="Clear list", color=app_color, visible= False, on_click=clear_table, animate_offset=1000)

    app_bar = ft.AppBar(title=ft.Text("CS2 !GEN CODE GENERATOR"), 
                        bgcolor=app_color,
                        actions=[])
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    page.window_maximizable = False
    #page.window_always_on_top = True
    page.window_width = 900 
    page.window_height = 1000
    page.theme = ft.Theme(font_family="Hack")

    page.on_keyboard_event = on_keyboard

    skin_link = ft.TextField(label="Inspect link",label_style=ft.TextStyle(size=20, color=ft.colors.WHITE), value="", text_align=ft.TextAlign.CENTER, 
                            width=page.width, border_color=app_color)
    search_button = ft.ElevatedButton(text="Generate !gen code", on_click=gen_code, color=app_color, data=0)
    search_button_config = ft.ElevatedButton(text="Generate !gen code", color=app_color, data=0)

    config_table = ft.DataTable(
        show_bottom_border=True,
        border=ft.border.all(2, app_color),
        border_radius=10,
        heading_text_style=ft.TextStyle(size=15),
        data_text_style=ft.TextStyle(size=15),
        columns=[
            ft.DataColumn(ft.Text("Item ID")),
            ft.DataColumn(ft.Text("Skin Name")),
            ft.DataColumn(ft.Text("Float")),
        ],rows=[ft.DataRow(cells=[
            ft.DataCell(ft.Text("519")),
            ft.DataCell(ft.Text("★ Ursus Knife")),
            ft.DataCell(ft.Text("0.08758267015218735")),
        ])]
    )
    
    temp_data_table = ft.DataTable(
        show_bottom_border=True,
        border=ft.border.all(2, app_color),
        border_radius=10,
        data_row_height=100,
        data_text_style=ft.TextStyle(size=12),
        columns=[
            ft.DataColumn(ft.Text("Item ID")),
            ft.DataColumn(ft.Text("Skin Name")),
            ft.DataColumn(ft.Text("Float")),
            ft.DataColumn(ft.Text("Pattern")),
            ft.DataColumn(ft.Text("!Gen code")),
        ],rows=[]
        ,width=page.width-420
    )
    cv = ft.Column([temp_data_table],scroll=True)
    rv = ft.Row([cv],scroll=True,expand=1,vertical_alignment=ft.CrossAxisAlignment.START)

    row = ft.Column([
        skin_link,
    ], alignment=ft.MainAxisAlignment.CENTER)

    row2 = ft.Row(
        [
        search_button,
        clear_list_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    container = ft.Container(content=row2, alignment=ft.alignment.center)

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        divider_color=ft.colors.BACKGROUND,
        indicator_color=app_color,
        label_color=app_color,
        tabs=[
            ft.Tab(
                text="Generator",
                icon=ft.icons.SEARCH,
                content=ft.Container(
                    content= ft.Column([
                        row,
                        container, 
                        rv
                    ]),
                    margin=10,
                )
            ),
            ft.Tab(
                text="Settings",
                icon=ft.icons.SETTINGS,
                content=ft.Container(
                    content= ft.Row([
                        ft.Column([
                            color_picker,
                            set_color_button
                        ]),
                        ft.Column([
                            config_table,
                            search_button_config
                        ]),
                    ]),
                    margin=10,
                )
            ),
        ],
        expand=1,
    )
    page.add(app_bar,t)


if __name__=='__main__':
    ft.app(target=main, view=ft.FLET_APP)

