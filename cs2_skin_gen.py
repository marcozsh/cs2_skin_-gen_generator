import requests
#import sys, signal
import json
import pyperclip as clipboard
from time import sleep

import flet as ft

URL = "https://api.cs2inspects.com/getGenCode?url="

"""
def def_handler(sig, frame):
    print("\n\n[!] Saliendo...[!]\n")
    sys.exit(1)
# Ctrl+C
signal.signal(signal.SIGINT, def_handler)
"""




def main(page: ft.Page):

    def copy_to_clipboard(text):
        clipboard.copy(text)

    def gen_code(e):

        if len(skin_link.value.strip()) == 0:
            open_dialog("Please provide a CS2 link preview", "WARNING")
            return

        if "csgo_econ_action_preview" not in skin_link.value.strip():
            open_dialog("CS2 Link preview not valid", "WARNING")
            return
        gen_code_request = requests.get(f"{URL}{skin_link.value.strip()}")
        gen_code_json = json.loads(gen_code_request.text)
        #print(gen_code_json)
        table_rows= ft.DataRow(
                cells=[
                    ft.DataCell( ft.Text(gen_code_json["genCodeDetail"]["Item_ID"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Skin_FullName"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Float"])),
                    ft.DataCell(ft.Text(gen_code_json["genCodeDetail"]["Pattern_ID"])),
                    ft.DataCell(ft.Text(gen_code_json["genCode"])),
                ],on_select_changed=lambda e :open_dialog(gen_code_json["genCode"])
            )
        temp_data_table.rows.append(table_rows)
        skin_link.value = ""
        page.update()
    
    def open_dialog(txt, title="GEN CODE COPIED"):
        dialog.title = ft.Text(title)
        dialog.content = ft.Text(txt)
        if "!gen" in txt:
            copy_to_clipboard(txt)
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

    app_bar = ft.AppBar(title=ft.Text("CS2 SKIN GENERATOR"), bgcolor=ft.colors.RED,
                        actions=[])
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    page.window_maximizable = False
    #page.window_always_on_top = True
    page.window_width = 900 
    page.window_height = 1000

    skin_link = ft.TextField(label="Inspect link", value="", text_align=ft.TextAlign.CENTER, 
                            width=page.width, border_color=ft.colors.RED)
    search_button = ft.ElevatedButton(text="Generate !gen code", on_click=gen_code, color=ft.colors.RED, data=0)

    temp_data_table = ft.DataTable(
        show_bottom_border=True,
        border=ft.border.all(2, "red"),
        border_radius=10,
        data_row_height=70,
        columns=[
            ft.DataColumn(ft.Text("Item ID")),
            ft.DataColumn(ft.Text("Skin Name")),
            ft.DataColumn(ft.Text("Float")),
            ft.DataColumn(ft.Text("Pattern")),
            ft.DataColumn(ft.Text("!Gen code")),
        ],rows=[]
        ,width=page.width-400
    )

    row = ft.Column([
        skin_link,
    ], alignment=ft.MainAxisAlignment.CENTER)

    row2 = ft.Column([
        search_button
    ],alignment=ft.MainAxisAlignment.CENTER)
    
                

    container = ft.Container(content=row2, alignment=ft.alignment.center)

    cv = ft.Column([temp_data_table],scroll=True)
    rv = ft.Row([cv],scroll=True,expand=1,vertical_alignment=ft.CrossAxisAlignment.START)

    page.add(app_bar, row,container, rv)


ft.app(target=main, assets_dir="assets", view=ft.FLET_APP)

