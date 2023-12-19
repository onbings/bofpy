import tkinter as tk
import tkhtmlview
import datetime 
import sys

def Bof_Gui_CenterWindow(root, wnd, width:int=0, height:int=0):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if ((width==0) or (height==0)):
        width = wnd.winfo_width()
        height = wnd.winfo_height()    
    x = int((screen_width - width)/2)
    y = int((screen_height - height)/2)
    #root.geometry(f"+{x}+{y}")
    wnd.geometry(f"{width}x{height}+{x}+{y}")
    wnd.update()
    return x,y


class Bof_Gui_SplashScreen:
    def __init__(self, image_file: str, label_text: str, label_height: int, label_font: str, label_fore_color: str) -> None:
        self.root = tk.Tk()
        self.root.withdraw()
        if sys.platform.startswith('win'):
            self.splash_screen = tk.Toplevel(background="SystemButtonFace")
        else:
            self.splash_screen = tk.Toplevel()  # background="SystemButtonFace")

        self.splash_screen.overrideredirect(True)
        picture = tk.PhotoImage(file=image_file)
        logo = tk.Label(self.splash_screen, image=picture)
        logo.grid(row=0, column=0, padx=0, pady=0)

        self.label = tk.Label(self.splash_screen, text=label_text, compound="center", font=label_font, foreground=label_fore_color)
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="")
        width = picture.width()+4
        height = picture.height()+label_height
        x, y = Bof_Gui_CenterWindow(self.root, self.splash_screen, width, height)
        #self.splash_screen.geometry(f"{width}x{height}+{x}+{y}")
        #self.splash_screen.update()

    def add_text(self, x: int, y: int, text: str, font: str, fore_color: str) -> None:
        self.label.config(text="V1.0.2")

    def close(self):
        # self.root.deiconify()
        self.root.destroy()
        self.splash_screen = None  # .destroy()


class Bof_Gui_Text_Console(tk.Frame):
    def __init__(self, parent, console_width: int, console_height: int, foreground: str, font_size: int) -> None:
        super().__init__(parent)
        self.console_width = console_width
        self.console_height = console_height
        self.gui_text_console = tk.Text(self, wrap="char", width=self.console_width, height=self.console_height, font=("Courier", font_size))
        self.gui_text_console.pack(expand=True, fill="both")
        self.clear(foreground)

    def clear(self, background: str) -> None:        
        self.gui_text_console["state"] = "normal"
        self.gui_text_console.config(bg=background)
        self.gui_text_console.delete("1.0", "end")
        empty_line = (" " * self.console_width) + "\n"
        for i in range(self.console_height):
            self.gui_text_console.insert(f"{i+1}.0", empty_line)
        self.gui_text_console["state"] = "disabled"

    def print_at(self, line: int, col: int, foreground: str, background: str, text: str) -> bool:
        rts = False
        text_len = len(text)
        if (line >= 0) and (line <= (self.console_height-1)) and (col >= 0) and (col <= (self.console_width-1)) and ((col + text_len-1) <= (self.console_width-1)):
            self.gui_text_console.tag_configure(f"conf_{line}.{col}", foreground=foreground, background=background)
            self.gui_text_console["state"] = "normal"
            self.gui_text_console.delete(f"{line+1}.{col}", f"{line+1}.{col+text_len}")
            self.gui_text_console.insert(f"{line+1}.{col}", text, f"conf_{line}.{col}")
            self.gui_text_console["state"] = "disabled"
            rts = True
        return rts


class Bof_Gui_Text_Scroll(tk.Frame):
    def __init__(self, parent, terminal_width: int, terminal_height: int, terminal_history_line: int, font_size: int, show_now_format:str, show_line_num:bool) -> None:
        super().__init__(parent)
        self.terminal_width = terminal_width
        self.terminal_history_line = terminal_history_line
        self.show_line_num = show_line_num
        self.line_num = 0
        self.show_now_format=show_now_format
        
        self.gui_text_terminal = tk.Listbox(self, width=terminal_width, height=terminal_height, font=("Courier", font_size))
        self.gui_text_terminal.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.gui_text_terminal.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.gui_text_terminal.config(yscrollcommand=scrollbar.set)

        self.clear()
        # TODO add an optional line counter

    def clear(self) -> None:
        self.gui_text_terminal.delete(0, tk.END)

    def add_line(self, foreground: str, background: str, text: str) -> bool:
        rts = False
        text_len = len(text)
        #if text_len <= self.terminal_width:
        if self.gui_text_terminal.size() >= self.terminal_history_line:
            self.gui_text_terminal.delete(0)
        if self.show_line_num:
            self.line_num = self.line_num + 1
            text = f"{self.line_num:04} " + text 
        if self.show_now_format!="":
            text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + text
        self.gui_text_terminal.insert(tk.END, text[:self.terminal_width])
        self.gui_text_terminal.itemconfig(tk.END, {'fg': foreground, 'bg': background})
        self.gui_text_terminal.yview_moveto("1.0")
        rts = True
        return rts


class Bof_Gui_Html_Console():
    def __init__(self, parent) -> None:
        # super().__init__(parent)
        self.gui_html_console = tkhtmlview.HTMLScrolledText(parent)  # HTMLScrolledText(parent)
        self.gui_html_console.pack(expand=True, fill="both")

    def render(self, html: str) -> None:
        self.gui_html_console.set_html(html)
