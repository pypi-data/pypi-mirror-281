import base64
import os

from thinkup_cli.form.code_gen.code_gen_form import get_code_gen_menu_form
from thinkup_cli.form.code_gen.create_new_screen import create_new_screen
from thinkup_cli.form.code_gen.create_new_module import create_new_module
from thinkup_cli.entities.app import App
from thinkup_cli.utils.ui_menu import UIMenu, UIMenuOptions
from thinkup_cli.utils.singleton import singleton
from thinkup_cli.utils.ui import UI


@singleton
class Menu:

    @staticmethod
    def code_gen_menu():
        working_directory = os.getcwd()
        UI().clear()
        UI().pheader(f"ANDROID CODE GENERATION")
        UI().pline()
        UI().ptext(f"│  Working directory:")
        UI().ptext(f"│  {working_directory}")
        if (not os.path.exists("settings.gradle.kts")):
            UI().ptext('│  <y>WARNING:</y> This doesn\'t seem to be the right directory.')
        UI().pline()
        UI().ptext('<g>Options</g>')

        result = get_code_gen_menu_form()
        print(result)
        if result == -1:
            return

        if result == "SCREEN":
            create_new_screen()
        else:
            create_new_module()

    # MAIN MENU ------------------------------------
    def main_menu(self):
        options = [
            ("1", f"Android Code Generation", self.code_gen_menu),
        ]

        menu = UIMenuOptions(
            type="main_menu",
            top=f"<y>ThinkUp CLI</y> │ <gray>{App().version}</gray>",
            options=options
        )

        UIMenu().print_menu(menu)
