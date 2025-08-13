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

### 1. リポジトリのクローン

```bash
git clone https://github.com/harumiWeb/flet1.0alpha-pdf-compressor-app.git
cd flet1.0alpha-pdf-compressor-app
```

### 2. 環境のセットアップ

- `requirements.txt`から作成する方法

  ```bash
  pip install -r requirements.txt
  ```

- `uv`を使う方法

  ```bash
  uv sync
  ```

### 3. 開発サーバーの起動

```bash
  .venv/Scripts/activate
  flet run
```

### 4. アプリケーションのビルド

```bash
  python dev/build.py
```

## ライセンス

### GNU Affero General Public License v3.0

このソフトウェアは，内部で Ghostscript と PyMuPDF をバンドルしており，GNU Affero General Public License Version 3（AGPL-3.0）の下で公開されています。  
以下，このアプリケーションに含まれるすべてのコードとバイナリは AGPL-3.0 の条件に従って利用および再配布が許可されます。

当アプリケーション内に組み込んでいる`GhostScript`やライブラリとして使用している`PyMuPDF`のソースコードに対しては一切のソースコード改変を行っていません。

#### 著作権表示

Copyright © 2025 harumiWeb  
このソフトウェアは，Artifex Software, Inc. により開発された Ghostscript と PyMuPDF を内部に組み込んでいます。  
Ghostscript の著作権表示とライセンスは以下のとおりです。

#### ライセンス条項

このプログラムはフリーソフトウェアです。あなたはこれを再配布および／または改変することができます。  
ただし，Free Software Foundation によって公表された GNU Affero General Public License Version 3 の条項に従うものとします。  
このプログラムは有用であることを願って配布されますが，いかなる保証もありません。商品適格性や特定目的適合性についての黙示の保証も含め，一切責任を負いません。詳しくは本ライセンスをご覧ください。  
You should have received a copy of the GNU Affero General Public License along with this program.  
もし添付されていない場合は，次の URL から入手してください：  
[https://www.gnu.org/licenses/agpl-3.0.txt](https://www.gnu.org/licenses/agpl-3.0.txt)

See the [LICENSE](./LICENSE.txt) file for details.

## 開発者

- 開発者: harumiWeb
- メール: [halpost](https://www.halpost.tech/contact)
- GitHub: [harumiWeb](https://github.com/harumiWeb)
- X: [@HarumiWebDesign](https://x.com/HarumiWebDesign)