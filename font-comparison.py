import json
import sys
from textwrap import dedent
from tkinter import Entry, Frame, StringVar, Text, Tk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

from jsonschema import ValidationError, validate


def loadConfig() -> dict:
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
        validateConfig(data)
        return data
    except FileNotFoundError:
        clean_json = {
            "default_font1": "Arial",
            "default_font2": "Calibri",
            "font_size1": 11,
            "font_size2": 11,
        }
        with open("config.json", "w+") as file:
            json.dump(clean_json, file, indent=4)
        sys.exit("config.json is missing! A clean config.json has been generated.")


def validateConfig(config: dict):
    schema = {
        "type": "object",
        "properties": {
            "default_font1": {"type": "string"},
            "default_font2": {"type": "string"},
            "font_size1": {"type": "number"},
            "font_size2": {"type": "number"},
        },
        "required": ["default_font1", "default_font2", "font_size1", "font_size2"],
    }
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        print(e)
        sys.exit(1)


def initWindow() -> Tk:
    window = Tk()
    window.title("Simple Font Comparison Tool")
    window.geometry("1000x500")
    window.resizable(0, 0)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    return window


def initTextField() -> Text:
    entry = Text(width=100, height=10, wrap="word")
    entry.insert("end", defaultText)
    entry.grid(row=0, column=0, columnspan=2, pady=15)
    entry.bind("<KeyRelease>", lambda *args: updatePreviewBoth())
    return entry


def initPreview(col: int, defaultFont: tuple[str, int]) -> Text:
    frame = Frame(width=480, height=250)
    frame.grid_propagate(False)
    frame.grid(row=2, column=col)

    preview = ScrolledText(frame, wrap="word", font=defaultFont)
    preview.insert("end", defaultText)
    preview.config(state="disabled")
    preview.grid()
    return preview


def initFontEntry(col: int, defaultFont: str, preview: Text) -> StringVar:
    font = StringVar(value=defaultFont)
    font.trace_add("write", lambda *args: updatePreview(font, preview))

    fontEntry = Entry(textvariable=font, font=("Segoe UI", 11))
    fontEntry.grid(row=1, column=col, pady=10)
    return font


def updatePreview(fontvar: StringVar, preview: ScrolledText):
    newText = textField.get("1.0", "end")
    font = Font(family=fontvar.get(), size=11)

    preview.config(font=font)
    preview.config(state="normal")
    preview.delete("1.0", "end")
    preview.insert("end", newText)
    preview.config(state="disabled")


def updatePreviewBoth():
    updatePreview(font1, preview1)
    updatePreview(font2, preview2)


if __name__ == "__main__":
    config = loadConfig()
    window = initWindow()

    defaultText = dedent(
        """\
        The quick brown fox jumps over the lazy dog.
        Sphinx of black quartz, judge my vow.
        The five boxing wizards jump quickly.

        !#$%&'()*+,-./0123456789:;<=>?@
        ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{|}~
        ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïð"""
    )

    defaultFont1 = (config["default_font1"], config["font_size1"])
    defaultFont2 = (config["default_font2"], config["font_size2"])

    textField = initTextField()
    preview1 = initPreview(0, defaultFont1)
    font1 = initFontEntry(0, defaultFont1[0], preview1)
    preview2 = initPreview(1, defaultFont2)
    font2 = initFontEntry(1, defaultFont2[0], preview2)

    window.mainloop()
