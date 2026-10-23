import json
import os

import flet as ft

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
ASSETS_DIR = os.path.join(BASE, "assets")

# Flet version-er shathe milie ney
Btn = getattr(ft, "Button", None) or ft.ElevatedButton
try:
    import flet_audio as fta
    AudioCls = fta.Audio
except Exception:
    AudioCls = getattr(ft, "Audio", None)

SECTIONS = [
    ("alphabet", "рзз. ржмрж░рзНржгржорж╛рж▓рж╛"),
    ("words", "рзи. рж╢ржмрзНржж"),
    ("sentences", "рзй. ржмрж╛ржХрзНржп"),
    ("reading", "рзк. ржкржбрж╝рж╛ (Reading)"),
]


def load_languages():
    langs = {}
    for fname in sorted(os.listdir(DATA_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname), encoding="utf-8") as fh:
                langs[fname[:-5]] = json.load(fh)
    return langs


def main(page: ft.Page):
    page.title = "ржнрж╛рж╖рж╛ рж╢рж┐ржХрзНрж╖рж╛"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
    langs = load_languages()
    state = {"audio": None}

    def play(code, item):
        rel = item.get("audio")
        if not rel or AudioCls is None:
            return
        if not os.path.exists(os.path.join(ASSETS_DIR, "audio", rel)):
            return
        if state["audio"] in page.overlay:
            page.overlay.remove(state["audio"])
        a = AudioCls(src="audio/" + rel, autoplay=True)
        state["audio"] = a
        page.overlay.append(a)
        page.update()

    def has_audio(item):
        rel = item.get("audio")
        return bool(rel) and os.path.exists(os.path.join(ASSETS_DIR, "audio", rel))

    def item_card(code, item, big=48):
        rows = [
            ft.Text(item["text"], size=big, text_align=ft.TextAlign.CENTER),
            ft.Text("ржЙржЪрзНржЪрж╛рж░ржг: " + item["roman"], size=22, text_align=ft.TextAlign.CENTER),
            ft.Text("ржЕрж░рзНрже: " + item["meaning"], size=20, text_align=ft.TextAlign.CENTER),
        ]
        if has_audio(item):
            rows.append(Btn("ЁЯФК рж╢рзБржирзЛ", on_click=lambda e: play(code, item)))
        return ft.Container(
            content=ft.Column(rows, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=20,
            border=ft.border.all(1, "#999999"),
            border_radius=12,
        )

    def show_home():
        page.clean()
        page.add(ft.Text("ржнрж╛рж╖рж╛ рж╢рж┐ржХрзНрж╖рж╛", size=32, weight=ft.FontWeight.BOLD))
        page.add(ft.Text("ржХрзЛржи ржнрж╛рж╖рж╛ рж╢рж┐ржЦрждрзЗ ржЪрж╛ржУ?", size=18))
        for code, d in langs.items():
            label = f'{d["native"]}  ({d["name_bn"]})'
            page.add(Btn(label, on_click=lambda e, c=code: show_language(c)))

    def show_language(code):
        d = langs[code]
        page.clean()
        page.add(Btn("тЖР ржлрж┐рж░рзЗ ржпрж╛ржУ", on_click=lambda e: show_home()))
        page.add(ft.Text(f'{d["native"]} - {d["name_bn"]}', size=28, weight=ft.FontWeight.BOLD))
        for key, title in SECTIONS:
            if d.get(key):
                if key == "reading":
                    page.add(Btn(title, on_click=lambda e: show_reading(code)))
                else:
                    page.add(Btn(title, on_click=lambda e, k=key, t=title: show_cards(code, k, t)))

    def show_cards(code, key, title):
        items = langs[code][key]
        pos = {"i": 0}

        def render():
            page.clean()
            page.add(Btn("тЖР ржлрж┐рж░рзЗ ржпрж╛ржУ", on_click=lambda e: show_language(code)))
            page.add(ft.Text(title, size=22, weight=ft.FontWeight.BOLD))
            page.add(ft.Text(f'{pos["i"] + 1} / {len(items)}'))
            big = 90 if key == "alphabet" else 48
            page.add(item_card(code, items[pos["i"]], big))
            page.add(ft.Row([
                Btn("тЧА ржЖржЧрзЗрж░", on_click=lambda e: step(-1)),
                Btn("ржкрж░рзЗрж░ тЦ╢", on_click=lambda e: step(1)),
            ], alignment=ft.MainAxisAlignment.CENTER))

        def step(n):
            pos["i"] = (pos["i"] + n) % len(items)
            render()

        render()

    def show_reading(code):
        d = langs[code]
        page.clean()
        page.add(Btn("тЖР ржлрж┐рж░рзЗ ржпрж╛ржУ", on_click=lambda e: show_language(code)))
        page.add(ft.Text("ржкржбрж╝рж╛рж░ ржЕржирзБрж╢рзАрж▓ржи", size=22, weight=ft.FontWeight.BOLD))
        for item in d["reading"]:
            page.add(item_card(code, item, 34))

    show_home()


if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main, assets_dir="assets")
    else:
        ft.app(target=main, assets_dir="assets")
