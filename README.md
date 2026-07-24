<p align="center"> <img width="2752" height="1021" alt="Ruffle for R36S" src="https://github.com/user-attachments/assets/c34824ff-e633-4a0e-9aea-f8ab5638ebd2" /> </p> <h1 align="center">Ruffle for R36S (DarkOS)</h1> <p align="center"> Run Adobe Flash games on the R36S using the official Ruffle ARM64 build. </p> <p align="center"> ⚠️ Experimental • Community Project • Hardware Accelerated </p>


> **Disclaimer**
> 
> This is an unofficial community project and is **not affiliated** with the Ruffle, PortMaster, or DarkOS projects.

---

# Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Choose Your Launch Method](#choose-your-launch-method)
    - [Option A — Menu Launcher (recommended for many games)](#option-a--menu-launcher-recommended-for-many-games)
    - [Option B — Template Launcher (one script per game)](#option-b--template-launcher-one-script-per-game)
- [File Cleanup Guide](#file-cleanup-guide)
- [Folder Structure](#folder-structure)
- [Controller Profiles](#controller-profiles)
- [Known Issues](#known-issues)
- [Copyright](#copyright)
- [Credits](#credits)
- [License](#license)

---

# Overview

This project adapts the official **Ruffle ARM64 Linux build** so it can run on the **R36S** with **DarkOS**.

The objective is simple:

Bring Adobe Flash games to the R36S while keeping installation and game management as easy as possible.

This repository contains:

- a menu-based launcher (optional)
- a per-game launcher template (optional)
- the Ruffle engine and required files
- example keymap/controller configs
- documentation

Flash games (**.swf**) are **NOT included**.

> **Recent change:** the engine now runs noticeably faster and the graphical glitches previously caused by mouse input are gone. As a trade-off, some games may occasionally show minor in-game graphical bugs. See [Known Issues](#known-issues).

---

# Features

✔ Hardware accelerated rendering

✔ Uses the official Ruffle ARM64 build

✔ Faster performance than previous versions

✔ Two launch methods to fit your needs: a graphical menu **or** a lightweight per-game script

✔ Per-game controller profiles

✔ **Built-in Keymap Editor (exclusive to the Menu Launcher)**

✔ DarkOS compatible

---

# Requirements

- R36S
- DarkOS
- PortMaster
  
>**Note:** PortMaster itself isn't actually required to run these games — the scripts don't depend on it. The `/roms/ports/` folder is used simply because EmulationStation scans it natively and can launch any `.sh` script placed there directly as a game.

---

# Installation

## 1. Download this repository

Copy the repository contents into:

```text
/roms/ports/

```

## 2. Place the Ruffle binary

Make sure the compiled Ruffle binary (`rufflesa`) is inside:

```text
/roms/ports/ruffleEngine/

```

## 3. Choose your launch method

This is where the two options diverge — see below.

---

# Choose Your Launch Method

There are **two ways** to launch your games. You don't need both — pick the one that fits you and, per the [cleanup guide](https://www.google.com/search?q=%23file-cleanup-guide), delete the files you don't need.

## Option A — Menu Launcher

A graphical, gamepad-navigable menu (built with Pygame) that lists every `.swf` file inside `ruffleEngine/games/`, **allows you to map your controls directly from the interface**, and lets you pick one to launch. Best if you have several games and want a single entry point in EmulationStation.

**Requires:** Pygame installed on the system (one-time setup).

### Setup

1. Run `install_pygame.sh` once to install Pygame on your DarkOS system.
2. Copy your `.swf` files into:
```text
ruffleEngine/games/

```


3. Launch `ruffle-interface.sh` from EmulationStation. It opens the menu (`launcher.py`), lets you pick a game with the D-Pad, map your keys if needed, and launches it through Ruffle.

### Files this option needs

* `install_pygame.sh` (only until Pygame is installed — see cleanup guide)
* `ruffle-interface.sh`
* `ruffleEngine/launcher.py`
* `ruffleEngine/rufflesa`
* `ruffleEngine/games/*.swf`

---

## Option B — Template Launcher (one script per game)

A simple, self-contained shell script per game — no Pygame, no menu, no extra dependencies. Best if you only have one or a few games, or if you don't want a menu at all.

### Setup

1. Copy your `.swf` file into:
```text
ruffleEngine/games/

```


2. Copy `launcher-template.sh`, rename it to your game's name (e.g. `DadNMe.sh`), and place the copy in `/roms/ports/`.
3. Edit only this variable inside the copied script:
```bash
SWF_FILE="dadnme.swf"

```


4. Repeat steps 1–3 for every additional game (one script per game).
5. Launch each game directly from EmulationStation — every game gets its own entry.

### Files this option needs

* `launcher-template.sh` (one renamed copy per game)
* `ruffleEngine/rufflesa`
* `ruffleEngine/games/*.swf`

If you choose this option, you do **not** need Pygame, the menu, or the installer at all.

---

# File Cleanup Guide

Since your setup only needs one of the two launch methods, here's what can be safely deleted and when:

| File | Safe to delete when… |
| --- | --- |
| `install_pygame.sh` | Right after Pygame has finished installing successfully — regardless of which option you choose long-term, once it has run once you no longer need it. |
| `ruffle-interface.sh` | You've chosen **Option B** (Template Launcher) and don't want the menu. |
| `ruffleEngine/launcher.py` | You've chosen **Option B** (Template Launcher). |
| `launcher-template.sh` | You've chosen **Option A** (Menu Launcher) and won't be creating individual per-game scripts. |

In short:

* **Going with the menu (Option A)?** Delete `launcher-template.sh` once you've confirmed the menu works. Keep `install_pygame.sh` only until Pygame is installed, then delete it too.
* **Going with per-game scripts (Option B)?** Delete `install_pygame.sh`, `ruffle-interface.sh`, and `ruffleEngine/launcher.py` — none of them are needed.

---

# Folder Structure

```text
/roms/ports/
│
│   install_pygame.sh        (Option A only — delete after Pygame install)
│   launcher-template.sh     (Option B only — one renamed copy per game)
│   LICENSE
│   README.md
│   ruffle-interface.sh      (Option A only)
│
└───ruffleEngine
    │   launcher.py          (Option A only)
    │   rufflesa
    │
    ├───games
    │       game.swf
    │
    └───keymap
            game.cfg

```

---

# Controller Profiles

Controller mapping works on two levels:

1. A base SDL gamepad config embedded in the launcher scripts (`SDL_GAMECONTROLLERCONFIG`), which normalizes the physical controller so it's recognized cleanly by the engine.
2. A **per-game keymap file** that maps each button to a keyboard key, since every Flash game expects different keys.

## Per-game keymap files

Keymap files live inside:

```text
ruffleEngine/keymap/

```

### How to configure keys

**Method 1: Using the Menu Launcher (Recommended)**
If you are using Option A, you can simply highlight your game in the menu and press **Y** to open the built-in **Keymap Editor**. You can assign the keys directly from the interface, and the `.cfg` file will be generated and saved automatically.

**Method 2: Manual Creation**
If you are using Option B (or prefer editing files manually):

1. Copy the template `game.cfg`.
2. Rename the copy to match your game's filename exactly (e.g. `mario.cfg`).
3. Open it and, after each `=`, type the keyboard key that button should send. For example:
```properties
A=Return
B=Escape

```



### Buttons you can map

* **Face buttons:** `A`, `B`, `X`, `Y`
* **Shoulders/triggers:** `L`, `R`, `L2`, `R2`
* **System/joystick:** `Start`, `Select`, `L3`, `R3`

> **Note on the R36S:** the physical face buttons don't match their labels 1:1 — physical B behaves as `A`, physical A as `B`, physical X as `Y`, and physical Y as `X`. (The built-in Keymap Editor handles this swap visually for you). Test in-game before finalizing your mapping.

### Supported keyboard key names

* Letters: `A`, `B`, `C` … `Z`
* Numbers: `Num0`, `Num1` … `Num9`
* Arrows: `Up`, `Down`, `Left`, `Right`
* Actions: `Space`, `Return` (Enter key), `Escape`, `Tab`, `Backspace`
* Special: `F1`–`F12`, `Delete`, `Insert`, `Home`, `End`, `PageUp`, `PageDown`

### ⚠️ Important: don't leave buttons blank

If you leave a button's value empty or delete its line entirely, the engine will **not** disable that button. Instead it falls back to its hardcoded default profile, which may assign it an unrelated key (like `J` or `U`) without warning.

If you want a button to do nothing, explicitly assign it to a key the game doesn't use (e.g. `Num9`, `V`, or `M`) instead of leaving it blank.

### Native system shortcuts (always active, not configurable)

These are hardcoded into the engine and work regardless of what's in your `.cfg` file:

* **Exit game:** hold `Select` and press `Start`.
* **Mouse mode:** hold `Select` and press `X` — the D-Pad moves the cursor and `Y` acts as left click. Press `Select + X` again to turn it off.
* **WASD mode:** hold `Select` and press `A` — switches the D-Pad to send `W`/`A`/`S`/`D` keys instead.

The included `game.cfg` is only a template with empty values — always customize it per game.

---

# Known Issues

This project is still experimental.

Current known issues include:

* Some games may show minor in-game graphical glitches (a trade-off introduced by the recent performance improvements).
* Some games may still have lower performance depending on complexity.
* Controller profiles must be configured manually per game (unless using the Menu Launcher's built-in editor).

---

# Copyright

This repository **does not include Flash games**.

Users must provide their own legally obtained `.swf` files.

Ruffle is developed by the Ruffle project and licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) or the [MIT License](https://opensource.org/licenses/MIT), at the licensor's option.

The `rufflesa` binary included in `ruffleEngine/` is used **as-is, unmodified**: it was compiled for the R36S by [lcdyk0517 / arkos4clone](https://github.com/lcdyk0517/arkos4clone) (MIT licensed), itself built on top of [aweigit / ruffle-miyooflip](https://github.com/aweigit/ruffle-miyooflip). No source code from either project was changed or recompiled here.

This repository's own contribution is limited to the launcher scripts (`launcher-template.sh`, `ruffle-interface.sh`, `launcher.py`, `install_pygame.sh`) and documentation needed to run that binary on the R36S — it does not modify or redistribute Ruffle's source code.

---

# Credits

Ruffle for R36S (DarkOS) is built on the shoulders of giants within the retro-handheld and open-source communities. This project would not be possible without the incredible work of the following developers and teams:

* **[aweigit / ruffle-miyooflip](https://github.com/aweigit/ruffle-miyooflip):** developed the original Ruffle build optimized for handhelds like the Miyoo Flip. Their documentation was used as a reference to understand how the binary handles controller/keyboard input — no code from this project was copied into this repo.
* **[lcdyk0517 / arkos4clone](https://github.com/lcdyk0517/arkos4clone):** compiled the `rufflesa` binary for the R36S (based on aweigit's build), released under the MIT License. This repository uses that binary exactly as distributed, with no modifications or recompilation.
* **The [Ruffle](https://ruffle.rs/) Project:** the brilliant developers writing the Rust-based Flash Player emulator, keeping an entire era of internet history alive and playable.

A significant part of the research and debugging process was **AI-assisted**. AI was used to analyze logs, investigate graphics issues, and explore possible solutions. Every working configuration was ultimately tested and validated manually on real hardware.

---

# License

See the LICENSE file for details.