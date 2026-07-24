#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import math
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_NOMOUSE"] = "1"

import pygame

pygame.init()
pygame.joystick.init()
pygame.mouse.set_visible(False)

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

pygame.display.set_caption("Ruffle Launcher")

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BG_TOP = (18, 18, 28)
BG_BOTTOM = (10, 10, 16)
PANEL = (28, 28, 40)
PANEL_LIGHT = (36, 36, 52)
ACCENT = (124, 108, 255)
CYAN = (86, 226, 255)
TEXT_MAIN = (235, 235, 245)
TEXT_DIM = (135, 138, 160)
TEXT_ERROR = (255, 110, 110)

def load_font(names, size, bold=False):
    for name in names:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            continue
    return pygame.font.Font(None, size)

FONT_STACK = ["segoeui", "sfprodisplay", "helvetica", "dejavusans", "arial"]
font_title = load_font(FONT_STACK, 34, bold=True)
font_subtitle = load_font(FONT_STACK, 15, bold=False)
font_item = load_font(FONT_STACK, 21, bold=True)
font_small = load_font(FONT_STACK, 15, bold=True)
font_badge = load_font(FONT_STACK, 14, bold=True)

GAMES_DIR = "games"
KEYMAP_DIR = "keymap"
if not os.path.exists(GAMES_DIR):
    os.makedirs(GAMES_DIR)
if not os.path.exists(KEYMAP_DIR):
    os.makedirs(KEYMAP_DIR)

games = sorted([f for f in os.listdir(GAMES_DIR) if f.endswith('.swf')])
selected_index = 0
scroll_y = 0
MAX_VISIBLE = 5

BUTTON_ORDER = ["A", "B", "X", "Y", "L", "R", "L2", "R2", "Start", "Select", "L3", "R3"]

KEY_OPTIONS = (
    [chr(c) for c in range(ord('A'), ord('Z') + 1)] +
    [f"Num{n}" for n in range(10)] +
    ["Up", "Down", "Left", "Right"] +
    ["Space", "Return", "Escape", "Tab", "Backspace"] +
    [f"F{n}" for n in range(1, 13)] +
    ["Delete", "Insert", "Home", "End", "PageUp", "PageDown"]
)

BTN_B = 0
BTN_A = 1
BTN_X = 2
BTN_Y = 3
BTN_L = 4
BTN_R = 5
BTN_L2 = 6
BTN_R2 = 7
BTN_DPUP = 8
BTN_DPDOWN = 9
BTN_DPLEFT = 10
BTN_DPRIGHT = 11
BTN_SELECT = 12
BTN_START = 13
BTN_L3 = 14
BTN_R3 = 15

mode = "MENU"
remap_game = None
remap_button_idx = 0
remap_key_idx = {}
remap_confirmed = {}

clock = pygame.time.Clock()
running = True
anim_scroll = 0.0
pulse_t = 0.0

def draw_vertical_gradient(surface, rect, top_color, bottom_color):
    x, y, w, h = rect
    if h <= 0:
        return
    for i in range(h):
        ratio = i / h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def rounded_rect(surface, rect, color, radius=12, width=0):
    try:
        pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)
    except TypeError:
        pygame.draw.rect(surface, color, rect, width)

def rounded_rect_shadow(surface, rect, radius=12, offset=4, alpha=90):
    shadow_surf = pygame.Surface((rect[2] + offset * 2, rect[3] + offset * 2), pygame.SRCALPHA)
    shadow_rect = (offset, offset, rect[2], rect[3])
    try:
        pygame.draw.rect(shadow_surf, (0, 0, 0, alpha), shadow_rect, border_radius=radius)
    except TypeError:
        pygame.draw.rect(shadow_surf, (0, 0, 0, alpha), shadow_rect)
    surface.blit(shadow_surf, (rect[0] - offset, rect[1] - offset + 3))

def lerp(a, b, t):
    return a + (b - a) * t

bg_surface = pygame.Surface((WIDTH, HEIGHT))
draw_vertical_gradient(bg_surface, (0, 0, WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)

def cfg_path_for(swf_name):
    base = os.path.splitext(swf_name)[0]
    return os.path.join(KEYMAP_DIR, f"{base}.cfg")

def load_existing_keymap(swf_name):
    result = {btn: 0 for btn in BUTTON_ORDER}
    path = cfg_path_for(swf_name)
    
    # Swap mapping: convert CFG keys back to UI buttons
    swap_map = {"A": "B", "B": "A", "X": "Y", "Y": "X"}
    
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Convert the loaded key back to its UI equivalent
                    ui_btn = swap_map.get(key, key)
                    
                    if ui_btn in result and val in KEY_OPTIONS:
                        result[ui_btn] = KEY_OPTIONS.index(val)
        except OSError:
            pass
    return result

def save_keymap(swf_name, key_idx_map):
    path = cfg_path_for(swf_name)
    
    # Swap mapping: convert UI buttons to CFG keys
    swap_map = {"A": "B", "B": "A", "X": "Y", "Y": "X"}
    
    with open(path, "w") as f:
        f.write(f"# Keymap for {swf_name} (generated by launcher.py)\n\n")
        for btn in BUTTON_ORDER:
            # Map the UI button to its swapped counterpart for the CFG file
            cfg_btn = swap_map.get(btn, btn)
            f.write(f"{cfg_btn}={KEY_OPTIONS[key_idx_map[btn]]}\n")

def enter_remap_mode(swf_name):
    global mode, remap_game, remap_button_idx, remap_key_idx, remap_confirmed
    remap_game = swf_name
    remap_button_idx = 0
    remap_key_idx = load_existing_keymap(swf_name)
    remap_confirmed = {btn: False for btn in BUTTON_ORDER}
    mode = "REMAP"

def exit_remap_mode(save):
    global mode
    if save:
        save_keymap(remap_game, remap_key_idx)
    mode = "MENU"

def launch_game(game_name):
    with open("/tmp/ruffle_selected.txt", "w") as f:
        f.write(game_name)
    pygame.quit()
    sys.exit(0)

def draw_menu():
    screen.blit(bg_surface, (0, 0))

    header_surf = pygame.Surface((WIDTH, 82), pygame.SRCALPHA)
    draw_vertical_gradient(header_surf, (0, 0, WIDTH, 82), (26, 24, 42), (18, 18, 28))
    screen.blit(header_surf, (0, 0))

    title_surf = font_title.render("Ruffle", True, TEXT_MAIN)
    screen.blit(title_surf, (28, 14))

    subtitle_surf = font_subtitle.render("SWF GAME LAUNCHER", True, TEXT_DIM)
    screen.blit(subtitle_surf, (30, 52))

    pygame.draw.line(screen, ACCENT, (28, 76), (28 + title_surf.get_width() + 10, 76), 3)

    count_text = f"{len(games)} JUEGO" + ("S" if len(games) != 1 else "")
    badge_surf = font_badge.render(count_text, True, TEXT_MAIN)
    badge_w = badge_surf.get_width() + 24
    badge_rect = pygame.Rect(WIDTH - badge_w - 24, 26, badge_w, 30)
    rounded_rect(screen, badge_rect, PANEL_LIGHT, radius=15)
    rounded_rect(screen, badge_rect, ACCENT, radius=15, width=1)
    screen.blit(badge_surf, (badge_rect.x + 12, badge_rect.y + 6))

    list_top = 100
    item_h = 62
    item_gap = 10
    list_area_x = 24
    list_area_w = WIDTH - 48

    if not games:
        error_panel = pygame.Rect(list_area_x, list_top, list_area_w, 90)
        rounded_rect_shadow(screen, error_panel, radius=16)
        rounded_rect(screen, error_panel, PANEL, radius=16)
        msg1 = font_item.render("Sin juegos disponibles", True, TEXT_ERROR)
        msg2 = font_subtitle.render("Coloca archivos .swf en la carpeta /games", True, TEXT_DIM)
        screen.blit(msg1, (error_panel.x + 20, error_panel.y + 18))
        screen.blit(msg2, (error_panel.x + 20, error_panel.y + 52))
    else:
        for i in range(MAX_VISIBLE + 1):
            list_index = int(anim_scroll) + i
            if list_index >= len(games) or list_index < 0:
                continue

            frac_offset = anim_scroll - int(anim_scroll)
            y = list_top + (i - frac_offset) * (item_h + item_gap)

            if y > HEIGHT - 60 or y < list_top - item_h:
                continue

            swf = games[list_index]
            clean_name = swf.replace(".swf", "").replace("_", " ")
            is_selected = (list_index == selected_index)

            card_rect = pygame.Rect(list_area_x, int(y), list_area_w, item_h)

            if is_selected:
                rounded_rect_shadow(screen, card_rect, radius=16, offset=5, alpha=110)
                card_surf = pygame.Surface((card_rect.w, card_rect.h), pygame.SRCALPHA)
                draw_vertical_gradient(card_surf, (0, 0, card_rect.w, card_rect.h), (58, 48, 130), (40, 34, 96))
                screen.blit(card_surf, card_rect.topleft)
                rounded_rect(screen, card_rect, ACCENT, radius=16, width=2)

                bar_h = card_rect.h - 16
                bar_rect = pygame.Rect(card_rect.x + 6, card_rect.y + 8, 5, bar_h)
                pulse = int(180 + 60 * math.sin(pulse_t * 4))
                rounded_rect(screen, bar_rect, (min(255, CYAN[0]), min(255, CYAN[1]), min(255, CYAN[2])), radius=3)

                name_color = TEXT_MAIN
                play_cx = card_rect.right - 34
                play_cy = card_rect.centery
                pygame.draw.polygon(screen, CYAN, [(play_cx - 6, play_cy - 9), (play_cx - 6, play_cy + 9), (play_cx + 9, play_cy)])
            else:
                rounded_rect(screen, card_rect, PANEL, radius=16)
                name_color = TEXT_DIM

            text_surf = font_item.render(clean_name, True, name_color)
            text_y = card_rect.y + (card_rect.h - text_surf.get_height()) // 2
            screen.blit(text_surf, (card_rect.x + 26, text_y))

    if len(games) > MAX_VISIBLE:
        track_x = WIDTH - 10
        track_y = list_top
        track_h = MAX_VISIBLE * (item_h + item_gap) - item_gap
        rounded_rect(screen, (track_x, track_y, 4, track_h), PANEL_LIGHT, radius=2)
        thumb_h = max(24, track_h * (MAX_VISIBLE / len(games)))
        thumb_ratio = anim_scroll / max(1, (len(games) - MAX_VISIBLE))
        thumb_y = track_y + (track_h - thumb_h) * min(1.0, max(0.0, thumb_ratio))
        rounded_rect(screen, (track_x, int(thumb_y), 4, int(thumb_h)), ACCENT, radius=2)

    footer_h = 42
    footer_rect = pygame.Rect(0, HEIGHT - footer_h, WIDTH, footer_h)
    footer_surf = pygame.Surface((WIDTH, footer_h), pygame.SRCALPHA)
    footer_surf.fill((16, 16, 24, 210))
    screen.blit(footer_surf, footer_rect.topleft)
    pygame.draw.line(screen, PANEL_LIGHT, (0, HEIGHT - footer_h), (WIDTH, HEIGHT - footer_h), 1)

    def draw_button_hint(x, label, text, color):
        r = 12
        cx, cy = x, HEIGHT - footer_h // 2
        pygame.draw.circle(screen, color, (cx, cy), r)
        label_surf = font_badge.render(label, True, (20, 20, 28))
        screen.blit(label_surf, (cx - label_surf.get_width() // 2, cy - label_surf.get_height() // 2))
        text_surf = font_small.render(text, True, TEXT_DIM)
        screen.blit(text_surf, (cx + r + 8, cy - text_surf.get_height() // 2))
        return cx + r + 8 + text_surf.get_width()

    next_x = draw_button_hint(30, "A", "Select", CYAN)
    next_x = draw_button_hint(next_x + 30, "Y", "Edit Keymap", ACCENT)
    draw_button_hint(next_x + 30, "B", "Exit", (255, 130, 130))

def draw_remap():
    screen.blit(bg_surface, (0, 0))

    header_surf = pygame.Surface((WIDTH, 82), pygame.SRCALPHA)
    draw_vertical_gradient(header_surf, (0, 0, WIDTH, 82), (26, 24, 42), (18, 18, 28))
    screen.blit(header_surf, (0, 0))

    title_surf = font_title.render("Keymap Editor", True, TEXT_MAIN)
    screen.blit(title_surf, (28, 14))

    clean_name = remap_game.replace(".swf", "").replace("_", " ")
    subtitle_surf = font_subtitle.render(clean_name, True, ACCENT)
    screen.blit(subtitle_surf, (30, 52))

    pygame.draw.line(screen, ACCENT, (28, 76), (28 + title_surf.get_width() + 10, 76), 3)

    list_top = 100
    card_h = 44
    item_gap = 10
    col_gap = 12
    list_area_x = 24
    list_area_w = WIDTH - 48
    col_w = (list_area_w - col_gap) // 2

    for i, btn in enumerate(BUTTON_ORDER):
        row = i // 2
        col = i % 2
        x = list_area_x + col * (col_w + col_gap)
        y = list_top + row * (card_h + item_gap)

        card_rect = pygame.Rect(x, y, col_w, card_h)
        is_current = (i == remap_button_idx)

        if is_current:
            rounded_rect_shadow(screen, card_rect, radius=12, offset=4, alpha=100)
            card_surf = pygame.Surface((card_rect.w, card_rect.h), pygame.SRCALPHA)
            draw_vertical_gradient(card_surf, (0, 0, card_rect.w, card_rect.h), (58, 48, 130), (40, 34, 96))
            screen.blit(card_surf, card_rect.topleft)
            rounded_rect(screen, card_rect, ACCENT, radius=12, width=2)

            bar_h = card_rect.h - 12
            bar_rect = pygame.Rect(card_rect.x + 5, card_rect.y + 6, 4, bar_h)
            pulse = int(180 + 60 * math.sin(pulse_t * 4))
            rounded_rect(screen, bar_rect, (min(255, CYAN[0]), min(255, CYAN[1]), min(255, CYAN[2])), radius=2)

            name_color = TEXT_MAIN
            key_color = CYAN
        else:
            rounded_rect(screen, card_rect, PANEL, radius=12)
            if remap_confirmed.get(btn, False):
                name_color = TEXT_DIM
                key_color = TEXT_DIM
            else:
                name_color = (80, 82, 100)
                key_color = (80, 82, 100)

        btn_text = font_item.render(btn, True, name_color)
        key_text = font_item.render(KEY_OPTIONS[remap_key_idx[btn]], True, key_color)

        screen.blit(btn_text, (card_rect.x + 18, card_rect.y + (card_h - btn_text.get_height()) // 2))
        screen.blit(key_text, (card_rect.right - key_text.get_width() - 18, card_rect.y + (card_h - key_text.get_height()) // 2))

    footer_h = 42
    footer_rect = pygame.Rect(0, HEIGHT - footer_h, WIDTH, footer_h)
    footer_surf = pygame.Surface((WIDTH, footer_h), pygame.SRCALPHA)
    footer_surf.fill((16, 16, 24, 210))
    screen.blit(footer_surf, footer_rect.topleft)
    pygame.draw.line(screen, PANEL_LIGHT, (0, HEIGHT - footer_h), (WIDTH, HEIGHT - footer_h), 1)

    lr_surf = font_badge.render("<- / ->", True, TEXT_MAIN)
    pill_w = lr_surf.get_width() + 20
    pill_rect = pygame.Rect(30, HEIGHT - footer_h // 2 - 12, pill_w, 24)
    rounded_rect(screen, pill_rect, PANEL_LIGHT, radius=12)
    screen.blit(lr_surf, (pill_rect.x + 10, pill_rect.y + 5))

    lr_text = font_small.render("Change key", True, TEXT_DIM)
    screen.blit(lr_text, (pill_rect.right + 10, HEIGHT - footer_h // 2 - lr_text.get_height() // 2))

    def draw_button_hint(x, label, text, color):
        r = 12
        cx, cy = x, HEIGHT - footer_h // 2
        pygame.draw.circle(screen, color, (cx, cy), r)
        label_surf = font_badge.render(label, True, (20, 20, 28))
        screen.blit(label_surf, (cx - label_surf.get_width() // 2, cy - label_surf.get_height() // 2))
        text_surf = font_small.render(text, True, TEXT_DIM)
        screen.blit(text_surf, (cx + r + 8, cy - text_surf.get_height() // 2))
        return cx + r + 8 + text_surf.get_width()

    next_x = draw_button_hint(pill_rect.right + 10 + lr_text.get_width() + 30, "A", "Confirm", CYAN)
    draw_button_hint(next_x + 30, "B", "Back", (255, 130, 130))

while running:
    dt = clock.tick(60) / 1000.0
    pulse_t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if mode == "MENU":
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == BTN_DPUP:
                    selected_index = max(0, selected_index - 1)
                elif event.button == BTN_DPDOWN:
                    if games:
                        selected_index = min(len(games) - 1, selected_index + 1)
                elif event.button == BTN_A:
                    if games:
                        launch_game(games[selected_index])
                elif event.button == BTN_Y:
                    if games:
                        enter_remap_mode(games[selected_index])
                elif event.button == BTN_B or event.button == BTN_START:
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    if games:
                        selected_index = min(len(games) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    if games:
                        launch_game(games[selected_index])
                elif event.key == pygame.K_TAB:
                    if games:
                        enter_remap_mode(games[selected_index])
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        else:
            btn_name = BUTTON_ORDER[remap_button_idx]

            def cycle_key(direction):
                remap_key_idx[btn_name] = (remap_key_idx[btn_name] + direction) % len(KEY_OPTIONS)

            def confirm_and_advance():
                global remap_button_idx
                remap_confirmed[btn_name] = True
                if remap_button_idx < len(BUTTON_ORDER) - 1:
                    remap_button_idx += 1
                else:
                    exit_remap_mode(save=True)

            def go_back():
                global remap_button_idx
                if remap_button_idx > 0:
                    remap_button_idx -= 1
                else:
                    exit_remap_mode(save=False)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == BTN_DPLEFT:
                    cycle_key(-1)
                elif event.button == BTN_DPRIGHT:
                    cycle_key(1)
                elif event.button == BTN_A:
                    confirm_and_advance()
                elif event.button == BTN_B:
                    go_back()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cycle_key(-1)
                elif event.key == pygame.K_RIGHT:
                    cycle_key(1)
                elif event.key == pygame.K_RETURN:
                    confirm_and_advance()
                elif event.key == pygame.K_ESCAPE:
                    go_back()

    if mode == "MENU":
        if selected_index < scroll_y:
            scroll_y = selected_index
        elif selected_index >= scroll_y + MAX_VISIBLE:
            scroll_y = selected_index - MAX_VISIBLE + 1

    if mode == "MENU":
        anim_scroll = lerp(anim_scroll, scroll_y, min(1.0, dt * 12))

    if mode == "MENU":
        draw_menu()
    else:
        draw_remap()

    pygame.display.flip()

pygame.quit()
sys.exit(0)