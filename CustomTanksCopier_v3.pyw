"""
Custom Tanks Copier v3
Author: Ton
Python version: 3.11.3 (lower is also probably fine)

CAUTION!
This script CAN delete your precious custom tanks if you're not careful enough!
"""

import re
import configparser as cp  # 💀
import os
import copy
import shutil
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Logic:
    def __init__(self):
        self.SETTINGS_FILE_PATH = "settings.txt"
        self.SETTINGS_COMMENTS = "# For the inheritors, go to the next lines\n# and also indent every time you want to\n# include another level.\n"

        self.load_variables()

    def load_variables(self):
        self.raw_settings = {}
        self.settings = {}
        self.source_file_path = ""

        self.custom_tanks = []
        self.custom_tanks_names = []

        self.load_settings()
        try:
            self.source_file_path = self.settings["source"]
            self.inheritors_file_paths = self.settings["inheritors"]
            self.search_word = self.settings["search_word"]
            self.load_custom_tanks(self.source_file_path, self.search_word)
            self.load_custom_tanks_names()
        except Exception as e:
            # Don't care + didn't ask + ratio
            pass

    def log(self, function, *args, **kwargs):
        result = function(*args, **kwargs)
        # TODO: is it really a good idea to reload every single time?
        self.load_variables()
        return f"[{datetime.now().strftime('%H-%M-%S')}]{function.__name__}: {'SUCCESS' if result == True else f'FAIL -> {result}'}"

    def fileExists(self, filepath: str):
        return os.path.isfile(filepath)

    def create_backup(self):
        backup_dir = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        try:
            file_paths = [self.settings["source"]] + self.settings["inheritors"]

            os.makedirs(backup_dir)
            for file_path in file_paths:
                shutil.copy(file_path, backup_dir)

            return True
        except Exception as e:
            return e

    def create_default_settings(self):
        configParser = cp.ConfigParser(allow_no_value=True)
        configParser.add_section("SETTINGS")
        configParser.set("SETTINGS", self.SETTINGS_COMMENTS)
        configParser.set("SETTINGS", "directory", "%%userprofile%%\\.tanks\\levels\\")
        configParser.set("SETTINGS", "file_extension", ".tanks")
        configParser.set("SETTINGS", "search_word", "tanks")
        configParser.set("SETTINGS", "source", "NAME_LEVEL_TO_BE_COPIED_FROM")
        configParser.set(
            "SETTINGS",
            "inheritors",
            "LEVEL_TO_BE_COPIED_TO\nANOTHER_LEVEL_TO_BE_COPIED_TO\nANOTHER_LEVEL_TO_BE_COPIED_TO",
        )

        try:
            with open(self.SETTINGS_FILE_PATH, "w") as configfile:
                configParser.write(configfile)

            return True
        except Exception as e:
            return e

    def save_settings(self, settings: dict):
        configParser = cp.ConfigParser(allow_no_value=True)
        configParser.add_section("SETTINGS")
        configParser.set("SETTINGS", self.SETTINGS_COMMENTS)

        for key in settings.keys():
            configParser.set("SETTINGS", key, settings[key].replace("%", "%%"))

        try:
            with open(self.SETTINGS_FILE_PATH, "w") as configfile:
                configParser.write(configfile)
            return True
        except Exception as e:
            return e

    def load_settings(self):
        configParser = cp.ConfigParser()

        try:
            configParser.read(self.SETTINGS_FILE_PATH)
            raw_settings = dict(configParser.items("SETTINGS"))

            settings = copy.deepcopy(raw_settings)
            settings["directory"] = os.path.expandvars(settings["directory"])
            settings["source"] = (
                settings["directory"] + settings["source"] + settings["file_extension"]
            )
            settings["inheritors"] = [
                settings["directory"] + inheritor_file_name + settings["file_extension"]
                for inheritor_file_name in settings["inheritors"].strip().split("\n")
            ]

            self.raw_settings = raw_settings
            self.settings = settings

            return True
        except Exception as e:
            return e

    def load_custom_tanks(self, file_path: str, search_word: str):
        custom_tanks = []
        try:
            with open(file_path, "r") as file:
                found_tanks = False

                for line in file:
                    line = line.strip()

                    if found_tanks:
                        custom_tanks.append(line)

                    if line == search_word and not found_tanks:
                        found_tanks = True

            self.custom_tanks = custom_tanks

            return True
        except Exception as e:
            return e

    def load_custom_tanks_names(self):
        custom_tanks_names = []
        pattern = re.compile(r"name=([^;]+);")

        for i in range(len(self.custom_tanks)):
            matches = pattern.findall(self.custom_tanks[i])
            if len(matches) == 1:
                custom_tanks_names.append(matches[0])
            else:
                custom_tanks_names.append(f"{matches[-1]} -> {', '.join(matches[:-1])}")

        self.custom_tanks_names = custom_tanks_names

    def overwrite_custom_tanks(self, file_path: str, custom_tanks, search_word: str):
        found_tanks = False
        updated_lines = []

        try:
            assert self.fileExists(file_path) == True, FileNotFoundError
            with open(file_path, "r") as file:
                for line in file:
                    if found_tanks:
                        continue

                    line = line.strip()

                    if line == search_word:
                        found_tanks = True
                        updated_lines.append(line)
                        updated_lines.extend(custom_tanks)
                    else:
                        updated_lines.append(line)

            if not found_tanks:
                updated_lines.append("tanks")
                updated_lines.extend(custom_tanks)

            updated_lines = [line + "\n" for line in updated_lines]

            with open(file_path, "w") as file:
                file.writelines(updated_lines)

            return True
        except Exception as e:
            return e

    def overwrite_multiple_custom_tanks(
        self, file_paths, custom_tanks, search_word: str
    ):
        try:
            for file_path in file_paths:
                assert self.fileExists(file_path) == True, FileNotFoundError
                self.overwrite_custom_tanks(file_path, custom_tanks, search_word)
            return True
        except Exception as e:
            return e


class App(tk.Tk):
    def __init__(self, title, size):
        # Setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.call("tk", "scaling", self.winfo_fpixels("1i") / 72.0)

        # Widgets
        self.build_widgets()

        if not logic.fileExists(logic.SETTINGS_FILE_PATH):
            self.operations_widget.create_default_settings()
            self.rebuild_settings_widget()

        # Run
        self.mainloop()

    def load_widgets(self):
        self.tanks_widget.reload_str_display_swap_mode()
        self.tanks_widget.reload_ListBox()
        self.settings_widget.reload_settings()

    def build_widgets(self):
        self.tanks_widget = TanksWidget(self)
        self.settings_widget = SettingsWidget(self)
        self.log_widget = LogWidget(self)
        self.operations_widget = OperationsWidget(self)

    def rebuild_settings_widget(self):
        self.settings_widget = SettingsWidget(self)


class TanksWidget(ttk.Frame):
    def __init__(self, parent: App):
        # Setup
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=0.35, relheight=1)

        # Vars
        self.bool_swap_mode = tk.BooleanVar(value=False)
        self.str_display_swap_mode = tk.StringVar()
        self.reload_str_display_swap_mode()
        self.int_num_tanks = tk.IntVar(value=0)

        # Widgets
        self.create_LabelFrame(self).pack(side="top", fill="x")
        self.create_ListFrame(self).pack(side="bottom", fill="both", expand=True)

    def create_LabelFrame(self, parent):
        frame = ttk.LabelFrame(parent, text="Custom Tanks")
        frame.columnconfigure(0, weight=3, uniform="a")
        frame.columnconfigure((1, 2), weight=1, uniform="a")
        frame.columnconfigure(3, weight=3, uniform="a")

        ttk.Label(frame, text="Number of tanks:").grid(row=0, column=0, sticky="nsew")
        ttk.Label(frame, textvariable=self.int_num_tanks).grid(
            row=0, column=1, sticky="nsew"
        )

        ttk.Label(frame, text="Swap mode:").grid(row=1, column=0, sticky="nsew")
        ttk.Label(frame, textvariable=self.str_display_swap_mode).grid(
            row=1, column=1, sticky="nsew"
        )
        ttk.Checkbutton(
            frame,
            text="",
            variable=self.bool_swap_mode,
            command=lambda: self.reload_str_display_swap_mode(),
        ).grid(row=1, column=2, sticky="nsew")
        ttk.Label(
            frame,
            text="Press S to enable swap mode, use up and down arrow keys to swap.",
            wraplength=120,
            justify="left",
        ).grid(row=1, column=3, sticky="nsew")

        ttk.Button(
            frame, text="Undo changes", command=lambda: self.reload_ListBox()
        ).grid(row=2, column=0, sticky="nsew")

        return frame

    def create_ListFrame(self, parent):
        frame = ttk.Frame(parent)
        self.list_box = tk.Listbox(frame)
        x_scrollbar = ttk.Scrollbar(
            frame, orient="horizontal", command=self.list_box.xview
        )
        y_scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.list_box.yview
        )
        self.list_box.configure(
            xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set
        )

        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar.pack(side="right", fill="y")
        self.list_box.pack(side="left", fill="both", expand=True)

        self.list_box.bind("<Up>", lambda event: self.swap_elements(event))
        self.list_box.bind("<Down>", lambda event: self.swap_elements(event))
        self.list_box.bind(
            "<s>",
            lambda event: [
                self.bool_swap_mode.set(not self.bool_swap_mode.get()),
                self.reload_str_display_swap_mode(),
            ],
        )

        self.reload_ListBox()

        return frame

    def reload_str_display_swap_mode(self):
        self.str_display_swap_mode.set("On" if self.bool_swap_mode.get() else "Off")

    def reload_ListBox(self):
        self.list_box.delete(0, tk.END)
        for num, name in enumerate(logic.custom_tanks_names, start=1):
            self.list_box.insert(tk.END, f"{num}. {name}")

    def swap_elements(self, event):
        if not self.bool_swap_mode.get():
            return

        selected_index = self.list_box.curselection()
        for i in range(self.list_box.size()):
            self.list_box.itemconfig(i, {"bg": "white"})

        if selected_index:
            selected_index = selected_index[0]

            if event.keysym == "Up":
                if selected_index > 0:
                    text = self.list_box.get(selected_index)
                    self.list_box.delete(selected_index)
                    self.list_box.insert(selected_index - 1, text)
                    self.list_box.selection_set(selected_index - 1)
                    self.list_box.activate(selected_index)

            elif event.keysym == "Down":
                if selected_index < self.list_box.size() - 1:
                    text = self.list_box.get(selected_index)
                    self.list_box.delete(selected_index)
                    self.list_box.insert(selected_index + 1, text)
                    self.list_box.selection_set(selected_index + 1)
                    self.list_box.activate(selected_index)

        self.list_box.itemconfig(selected_index, {"bg": "grey"})

    def get_ListBoxContents(self):
        return [item.split(". ", 1)[1] for item in self.list_box.get(0, tk.END)]


class SettingsWidget(ttk.Frame):
    def __init__(self, parent: App):
        # Setup
        super().__init__(parent)
        self.place(relx=0.35, rely=0, relwidth=0.35, relheight=1.0)

        # Vars
        self.text_boxes = {}

        # Widgets
        self.createSettingsFrame(self).pack(side="bottom", fill="both", expand=True)

    def reload_settings(self):
        for k, widget in self.settings_entries.items():
            text_value = logic.raw_settings[k]
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, text_value)
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, text_value.strip())

    def createSettingsFrame(self, parent):
        frame = ttk.LabelFrame(parent, text="Settings")
        ttk.Button(
            frame, text="Undo changes", command=lambda: self.reload_settings()
        ).pack(side="bottom")
        self.create_LabeledEntryFrame(frame).pack(
            side="bottom", fill="both", expand=True
        )

        return frame

    def create_LabeledEntryFrame(self, parent):
        frame = ttk.Frame(parent)
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=3, uniform="a")

        self.settings_entries = {}
        for i, (k, v) in enumerate(logic.raw_settings.items()):
            ttk.Label(frame, text=k).grid(row=i, column=0, sticky="nw")

            amount_values = len([item for item in v.split("\n")])
            if amount_values == 1:
                self.settings_entries[k] = ttk.Entry(frame)
                self.settings_entries[k].grid(row=i, column=1, sticky="nsew")
            else:
                self.create_TextEntryFrame(frame, k).grid(
                    row=i, column=1, sticky="nsew"
                )
                # Weird fix
                frame.rowconfigure(i, weight=1, uniform="a")

        self.reload_settings()

        return frame

    def create_TextEntryFrame(self, parent, k):
        frame = ttk.Frame(parent)
        text_box = tk.Text(frame, wrap="none")

        x_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=text_box.xview)
        y_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_box.yview)
        text_box.configure(
            xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set
        )

        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar.pack(side="right", fill="y")
        text_box.pack(side="top", fill="both", expand=True)

        self.settings_entries[k] = text_box

        return frame

    def get_settings_entries_contents(self):
        settings_contents = {}
        for k, widget in self.settings_entries.items():
            if isinstance(widget, ttk.Entry):
                settings_contents[k] = widget.get()
            elif isinstance(widget, tk.Text):
                settings_contents[k] = "\n" + widget.get("1.0", tk.END)
        return settings_contents


class LogWidget(ttk.Frame):
    def __init__(self, parent: App):
        # Setup
        super().__init__(parent)
        self.place(relx=0.7, rely=0, relwidth=0.3, relheight=0.7)

        # Vars
        self.log_contents = tk.StringVar()

        # Widgets
        ttk.Label(self, text="Log").pack(side="top")
        self.create_TextFrame(self).pack(side="bottom", fill="both", expand=True)

    def create_TextFrame(self, parent):
        frame = ttk.Frame(parent)
        self.text_box = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED)

        y_scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.text_box.yview
        )
        self.text_box.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)

        return frame

    def add_log_message(self, string):
        self.text_box.configure(state=tk.NORMAL)

        self.log_contents.set(self.log_contents.get() + ">" + string + "\n")
        self.reload_log()

        self.text_box.configure(state=tk.DISABLED)

    def reload_log(self):
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.INSERT, self.log_contents.get())


class OperationsWidget(ttk.Frame):
    def __init__(self, parent: App):
        # Setup
        super().__init__(parent)
        self.place(relx=0.7, rely=0.7, relwidth=0.3, relheight=0.3)

        # Vars
        self.parent = parent

        # Widgets
        self.create_LabelFrame(self).pack(side="left", fill="both", expand=True)

    def create_LabelFrame(self, parent):
        frame = ttk.LabelFrame(parent, text="File Operations")

        ttk.Button(
            frame, text="Create backup", command=lambda: self.create_backup()
        ).grid(row=0, column=0, sticky="nsw")
        ttk.Button(
            frame,
            text="Create default settings",
            command=lambda: self.create_default_settings(),
        ).grid(row=1, column=0, sticky="nsw")
        ttk.Button(
            frame, text="Save settings", command=lambda: self.save_settings()
        ).grid(row=2, column=0, sticky="nsw")
        ttk.Button(
            frame, text="Save reorder", command=lambda: self.save_reorder()
        ).grid(row=3, column=0, sticky="nsw")
        ttk.Button(
            frame, text="Sync custom tanks", command=lambda: self.sync_tanks()
        ).grid(row=4, column=0, sticky="nsw")

        return frame

    def message_box(self, title, question):
        return messagebox.askquestion(title, question) == "yes"

    def create_backup(self):
        self.parent.log_widget.add_log_message(logic.log(logic.create_backup))

    def create_default_settings(self):
        if logic.fileExists(logic.SETTINGS_FILE_PATH):
            if not self.message_box(
                "Existing settings found",
                "Do you want to overwrite the existing settings?",
            ):
                return

        self.parent.log_widget.add_log_message(logic.log(logic.create_default_settings))
        self.parent.load_widgets()

    def save_settings(self):
        if logic.fileExists(logic.SETTINGS_FILE_PATH):
            if not self.message_box(
                "Existing settings found",
                "Do you want to overwrite the existing settings?",
            ):
                return

        self.parent.log_widget.add_log_message(
            logic.log(
                logic.save_settings,
                self.parent.settings_widget.get_settings_entries_contents(),
            )
        )
        self.parent.load_widgets()

    def save_reorder(self):
        if not self.message_box(
            "Apply new order", "Do you want to modify the source file?"
        ):
            return

		# Would prefer if this was handled in Logic()
        combined_tanks_lists = list(zip(logic.custom_tanks_names, logic.custom_tanks))
        sorted_combined_tanks_lists = sorted(
            combined_tanks_lists,
            key=lambda x: self.parent.tanks_widget.get_ListBoxContents().index(x[0]),
        )

        # Kinda hacky way to avoid exceptions,
        # ideally handle this entirely in Logic()
        if sorted_combined_tanks_lists:
            _, reordered_custom_tanks = zip(*sorted_combined_tanks_lists)
        else:
            reordered_custom_tanks = ""

        self.parent.log_widget.add_log_message(
            logic.log(
                logic.overwrite_custom_tanks,
                logic.source_file_path,
                reordered_custom_tanks,
                logic.search_word,
            )
        )
        self.parent.load_widgets()

    def sync_tanks(self):
        if not self.message_box(
            "Sync custom tanks", "Do you want to overwrite all the inheriting files?"
        ):
            return

        self.parent.log_widget.add_log_message(
            logic.log(
                logic.overwrite_multiple_custom_tanks,
                logic.inheritors_file_paths,
                logic.custom_tanks,
                logic.search_word,
            )
        )


if __name__ == "__main__":
    logic = Logic()
    App("Custom Tanks Copier v3", (1200, 600))
