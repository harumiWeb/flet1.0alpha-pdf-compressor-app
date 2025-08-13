# GhostFlet PDF Compressor

This application is a demo app created to explore changes in version `1.0` of the Python application framework [Flet](https://flet.dev/).

It serves as a user-friendly **PDF conversion tool** that bundles [GhostScript](https://www.ghostscript.com/index.html) and the `PyMuPDF` library internally.

The app is released under the [AGPL-3.0 License](https://www.gnu.org/licenses/agpl-3.0.html), so please review the license before use.

## Features

- Easy to use: Compress, extract pages, and merge `PDF` files with just a few clicks.
- Fast performance: Powered by `GhostScript`, enabling high-speed processing.
- Intuitive UI: Simple and user-friendly interface based on Material Design via the `Flet` framework.

## Screenshot

<img width="1584" height="889" alt="Image" src="https://github.com/user-attachments/assets/9a349a9a-11a8-4561-a22d-b68abebf963c" />

## Installation

- Install via installer:

  [Windows 64-bit Installer](https://github.com/harumiWeb/flet1.0alpha-pdf-compressor-app/releases)

- Build the application manually:

## How to Use

1. Select the `PDF` file you want to convert using the `Select Files` button.
2. Choose the image quality from the `Image Quality` dropdown.
3. Specify the output pages in detail using the `Page Select` option.
4. Click the `Compress` button to start processing.
5. Save the converted files via the `Save Zip` button under the `Compressed Files` tab.

## Development

### 1. Clone this repository

```bash
git clone https://github.com/harumiWeb/flet1.0alpha-pdf-compressor-app.git
cd flet1.0alpha-pdf-compressor-app
```

### 2. Set up the environment

- Using `requirements.txt`:

  ```bash
  pip install -r requirements.txt
  ```

- Using `uv`:

  ```bash
  uv sync
  ```

### 3. Start the development server

```bash
  .venv/Scripts/activate
  flet run
```

### 4. Build the application

```bash
  python dev/build.py
```

## LICENSE

### GNU Affero General Public License v3.0

This software bundles Ghostscript and PyMuPDF internally and is released under the GNU Affero General Public License Version 3 (AGPL-3.0).  
All code and binaries included in this application are permitted for use and redistribution under the terms of AGPL-3.0.

#### Copyright Notice

Copyright © 2025 harumiWeb  
This software incorporates Ghostscript and PyMuPDF, developed by Artifex Software, Inc.  
The copyright notice and license for Ghostscript are as follows.

#### License Terms

This program is free software: you can redistribute it and/or modify it  
under the terms of the GNU Affero General Public License Version 3  
as published by the Free Software Foundation.  
This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the license for more details.  
You should have received a copy of the GNU Affero General Public License along with this program.  
If not, you can obtain it from the following URL:  
[https://www.gnu.org/licenses/agpl-3.0.txt](https://www.gnu.org/licenses/agpl-3.0.txt)

See the [LICENSE](./LICENSE.txt) file for details.

## Developer

- Developer: harumiWeb
- Email: [halpost](https://www.halpost.tech/contact)
- GitHub: [harumiWeb](https://github.com/harumiWeb)
- X: [@HarumiWebDesign](https://x.com/HarumiWebDesign)
