# GhostFlet PDF Compressor

このアプリケーションは Python のアプリケーション作成フレームワークである [Flet](https://flet.dev/) のバージョン`1.0`での変更を理解するために作成したデモアプリです。

内部に [GhostScript](https://www.ghostscript.com/index.html) と`PyMuPDF`ライブラリを組み込んだユーザーフレンドリーな**PDF 変換アプリケーション**としてお使いいただけます。

[AGPL-3.0 ライセンス](https://www.gnu.org/licenses/agpl-3.0.html) の元で作成しているので、ライセンスを読んでお使いください。

## 特徴

- 簡単操作: 数クリックで`PDF`ファイルの圧縮・ページの切り出し・結合などができます。
- 高速: `GhostScript`によって動作しているので非常に高速な処理が可能です。
- 直感的な UI: `Flet`フレームワークのマテリアルデザインによるシンプルで使いやすいインターフェース

## スクリーンショット

<img width="1584" height="889" alt="Image" src="https://github.com/user-attachments/assets/9a349a9a-11a8-4561-a22d-b68abebf963c" />

## インストール

- インストーラーによるインストール

  [Windows64bit インストーラー](https://github.com/harumiWeb/flet1.0alpha-pdf-compressor-app/releases)

- 自身でアプリケーションをビルドする方法

## 使用方法

1. `Select Files`ボタンから変換したい`PDF`ファイルを選択します。
2. `Image Quality`から`PDF`ファイル内の画像の画質を選択します。
3. `Page Select`から出力するページの細かい指定ができます。
4. `Compress`ボタンで処理を開始します。
5. `Compressed Files`タブの`Save Zip`ボタンから変換後のファイルを保存します。

## 開発

1. 環境のセットアップ

- `requirements.txt`から作成する方法

  ```bash
  pip install -r requirements.txt
  ```

- `uv`を使う方法

  ```bash
  uv sync
  ```

2. 開発サーバーの起動

```bash
  .venv/Scripts/activate
  flet run
```

3. アプリケーションのビルド

```bash
  python dev/build.py
```

## ライセンス

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

## 開発者

- 開発者: harumiWeb
- メール: [halpost](https://www.halpost.tech/contact)
- GitHub: [harumiWeb](https://github.com/harumiWeb)
- X: [@HarumiWebDesign](https://x.com/HarumiWebDesign)