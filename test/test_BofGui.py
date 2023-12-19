import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import Mock
from tkinter import Tk
from bofpy.BofGui import (  
    Bof_Gui_SplashScreen, 
    Bof_Gui_Text_Console, 
    Bof_Gui_Text_Scroll, 
    Bof_Gui_Html_Console
) 

class TestBofGuiSplashScreen(unittest.TestCase):
    def test_splash_screen_creation(self):
        # Mocking the Tkinter root window
        root = Tk()
        root.withdraw()

        # Creating a Bof_Gui_SplashScreen instance
        splash_screen = Bof_Gui_SplashScreen("./test/colorbar.png", "Loading...", 30, ("Arial", 12), "black")

        # Asserting that the Tkinter Toplevel window was created
        self.assertIsNotNone(splash_screen.splash_screen)

        # Closing the splash screen
        splash_screen.close()

        # Asserting that the root window is not destroyed
        #self.assertFalse(root.destroyed)

    def test_add_text(self):
        # Creating a Bof_Gui_SplashScreen instance
        splash_screen = Bof_Gui_SplashScreen("./test/colorbar.png", "Loading...", 30, ("Arial", 12), "black")

        # Adding text to the splash screen
        splash_screen.add_text(0, 0, "V1.0.2", ("Arial", 12), "black")

        # Closing the splash screen
        splash_screen.close()


class TestBofGuiTextConsole(unittest.TestCase):
    def test_clear(self):
        # Creating a Bof_Gui_Text_Console instance
        text_console = Bof_Gui_Text_Console(Tk(), 8, 4, "black", 12)

        # Clearing the text console
        text_console.clear("white")

        # Asserting that the text console is cleared
        #self.assertEqual(text_console.gui_text_console.get("1.0", "end-1c"), " " * 80 + "\n" * 10)
        expected_content = (" " * 8 + "\n") * 4
        a=text_console.gui_text_console.get("1.0", "end-1c")
        self.assertEqual(text_console.gui_text_console.get("1.0", "end-1c"), expected_content)

    def test_print_at(self):
        # Creating a Bof_Gui_Text_Console instance
        text_console = Bof_Gui_Text_Console(Tk(), 80, 10, "black", 12)

        # Printing text at a specific position
        result = text_console.print_at(2, 5, "red", "yellow", "Hello")

        # Asserting that the text is printed at the correct position
        self.assertTrue(result)
        self.assertEqual(text_console.gui_text_console.get("3.5", "3.10"), "Hello")


class TestBofGuiTextScroll(unittest.TestCase):
    def test_clear(self):
        # Creating a Bof_Gui_Text_Scroll instance
        text_scroll = Bof_Gui_Text_Scroll(Tk(), 80, 10, 5, 12, "", True)

        # Clearing the text scroll
        text_scroll.clear()

        # Asserting that the text scroll is cleared
        self.assertEqual(text_scroll.gui_text_terminal.size(), 0)

    def test_add_line(self):
        # Creating a Bof_Gui_Text_Scroll instance
        text_scroll = Bof_Gui_Text_Scroll(Tk(), 80, 10, 5, 12, "", True)

        # Adding a line to the text scroll
        result = text_scroll.add_line("red", "yellow", "Hello")

        # Asserting that the line is added to the text scroll
        self.assertTrue(result)
        self.assertEqual(text_scroll.gui_text_terminal.get(0), "0001 Hello")


class TestBofGuiHtmlConsole(unittest.TestCase):
    def test_render(self):
        # Creating a Bof_Gui_Html_Console instance
        html_console = Bof_Gui_Html_Console(Tk())

        # Rendering HTML content
        html_content = "<html><body><h1>Hello, World!</h1></body></html>"
        html_console.render(html_content)

        # Asserting that the HTML content is rendered
        #self.assertEqual(html_console.gui_html_console.get_html(), html_content)
        self.assertEqual(html_console.gui_html_console.get("1.0", "end-1c"), "Hello, World!")

if __name__ == "__main__":
    unittest.main()
