<p align="center">
  <img width="2752" height="1021" alt="Ruffle for R36S" src="https://github.com/user-attachments/assets/c34824ff-e633-4a0e-9aea-f8ab5638ebd2" />

</p>

<h1 align="center">Ruffle for R36S (DarkOS)</h1>

<p align="center">
Run Adobe Flash games on the R36S using the official Ruffle ARM64 build.
</p>

<p align="center">
⚠️ Experimental • Community Project • Hardware Accelerated
</p>

---

> **Disclaimer**
>
> This is an unofficial community project and is **not affiliated** with the Ruffle, PortMaster, or DarkOS projects.

---

# Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Folder Structure](#folder-structure)
- [Adding Games](#adding-games)
- [Controller Profiles](#controller-profiles)
- [Known Issues](#known-issues)
- [Copyright](#copyright)
- [Credits](#credits)

---

# Overview

This project adapts the official **Ruffle ARM64 Linux build** so it can run on the **R36S** with **DarkOS**.

The objective is simple:

Bring Adobe Flash games to the R36S while keeping installation and game management as easy as possible.

This repository contains:

- launcher scripts
- required runtime libraries
- example controller profiles
- documentation
- launcher templates

Flash games (**.swf**) are **NOT included**.

---

# Features

✔ Hardware accelerated rendering

✔ Uses the official Ruffle ARM64 build

✔ Per-game controller profiles (.gptk)

✔ Simple launcher template

✔ DarkOS compatible

---

# Requirements

- R36S
- DarkOS
- PortMaster
- Official Linux ARM64 build of Ruffle

---

# Installation

## 1. Download this repository.

Copy the repository contents into:

```text
/roms/ports/
```

---

## 2. Download Ruffle

Download the latest **Linux ARM64** build from the official Ruffle website.

Rename the executable to:

```text
ruffle
```

Place it here:

```text
/roms/ports/ruffleEngine/
```

After doing so, your folder should look like this:

```text
/roms/ports/

├── launcher-template.sh
└── ruffleEngine/
    ├── ruffle
    ├── libssl.so.1.1
    ├── libcrypto.so.1.1
    ├── ...
    └── games/
```

That's it.

---

# Quick Start

Create a folder for your game.

Example:

```text
ruffleEngine/games/DadNMe/
```

Copy your Flash game:

```text
dadnme.swf
```

Copy or create:

```text
controls.gptk
```

Copy:

```text
launcher-template.sh
```

Rename it and paste it in roms/ports:

```text
DadNMe.sh
```

Edit only these variables:

```bash
GAME_FOLDER="DadNMe"

SWF_FILE="dadnme.swf"

CONTROL_PROFILE="controls.gptk"
```

Launch the game from **EmulationStation**.

---

# Folder Structure

```text
/roms/ports/

├── DadNMe.sh
├── FancyPants.sh
├── HappyWheels.sh
│
└── ruffleEngine/
    │
    ├── ruffle
    ├── libssl.so.1.1
    ├── libcrypto.so.1.1
    ├── ...
    │
    └── games/
        │
        ├── DadNMe/
        │   ├── dadnme.swf
        │   └── controls.gptk
        │
        ├── FancyPants/
        │   ├── fancypants.swf
        │   └── controls.gptk
        │
        └── HappyWheels/
            ├── happywheels.swf
            └── controls.gptk
```

---

# Adding Games

Adding a game only requires four steps.

1. Create a folder inside:

```text
ruffleEngine/games/
```

2. Copy your Flash game (.swf).

3. Create a `controls.gptk` profile.

4. Copy `launcher-template.sh`, rename it, and edit:

```bash
GAME_FOLDER=""

SWF_FILE=""

CONTROL_PROFILE=""
```

Every Flash game uses different keyboard controls.

Because of this, every game requires its own `.gptk` profile.

---

# Controller Profiles

Controller mapping is handled through **gptokeyb**.

Each game needs its own:

```text
controls.gptk
```

The included profile is only an example.

You will likely need to customize it depending on the game.

---

# Known Issues

This project is still experimental.

Current known issues include:

- Mouse movement causes screen flickering.
- Some games have low performance.
- Controller profiles must be configured manually.

---

# Copyright

This repository **does not include Flash games**.

Users must provide their own legally obtained `.swf` files.

Ruffle is developed by the Ruffle project.

This repository only provides the integration necessary to run Ruffle on the R36S.

---

# Credits

This project would not have been possible without:

- ❤️ The Ruffle developers
- ❤️ The PortMaster team
- ❤️ The DarkOS developers

A significant part of the research and debugging process was **AI-assisted**.

AI was used to analyze logs, investigate graphics issues, and explore possible solutions.

Every working configuration was ultimately tested and validated manually on real hardware.

---

# License

See the LICENSE file for details.
