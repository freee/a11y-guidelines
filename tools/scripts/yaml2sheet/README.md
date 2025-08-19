# yaml2sheet

YAMLファイルからGoogle Sheetsチェックリストを生成するPythonツールです。freee アクセシビリティ・ガイドラインのチェックリストを自動的にGoogleスプレッドシートに展開します。

## 主な機能

- **YAMLからGoogle Sheetsへの変換**: freee_a11y_glライブラリで処理されたYAMLデータを構造化されたGoogle Sheetsチェックリストに変換
- **OAuth認証**: Google Sheets APIとの安全な連携
- **柔軟な設定管理**: YAML形式の設定ファイルによる詳細なカスタマイズ
- **複数スプレッドシート対応**: 開発時確認用と公開用のスプレッドシートを明示的に切り替えて出力可能
- **多言語対応**: 日本語・英語のチェックリスト生成

## インストール

### 前提条件

- Python 3.8以上
- Google Cloud Platformアカウント
- Google Sheets APIの有効化

### パッケージのインストール

```bash
pip install tools/scripts/yaml2sheet
```

### 依存関係

- `google-api-python-client>=2.0.0`: Google Sheets API連携
- `google-auth-oauthlib>=1.0.0`: OAuth認証
- `tools/lib/freee_a11y_gl>=0.2.2`: YAMLデータ処理

## セットアップ

### 1. Google Cloud Platform設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Google Sheets APIを有効化
3. OAuth 2.0認証情報を作成し、`credentials.json`としてダウンロード

### 2. 設定ファイルの作成

デフォルト設定ファイルを生成：

```bash
yaml2sheet --create-config
```

設定ファイルの標準のパスは、`~/.cconfig/freee_a11y_gl/yaml2sheet.yaml`です。

または手動で`yaml2sheet.yaml`を作成：

```yaml
# yaml2sheet.yaml
---
credentials_path: credentials.json
token_path: token.json
development_spreadsheet_id: your-dev-spreadsheet-id-here
production_spreadsheet_id: your-prod-spreadsheet-id-here
sheet_editor_email: email@example.com
log_level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
basedir: /path/to/a11y-guidelines  # ガイドラインプロジェクトのルートディレクトリ
base_url: https://a11y-guidelines.freee.co.jp  # ガイドラインのベースURL
version_info_cell: A27  # バージョン情報を書き込む1枚目のシートのセル番地
```

### 3. Googleスプレッドシートの準備

1. Googleスプレッドシートで新しいスプレッドシートを作成
2. スプレッドシートのIDを設定ファイルに記録
3. 必要に応じて共有設定を調整

## 使用方法

### 基本的な使用方法

```bash
# 開発用スプレッドシートに出力
yaml2sheet

# 公開用スプレッドシートに出力
yaml2sheet --production

# 設定ファイルを指定
yaml2sheet -c /path/to/config.yaml

# スプレッドシートを初期化（既存シートを削除）
yaml2sheet --init

# 詳細ログ出力
yaml2sheet --verbose
```

### コマンドラインオプション

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--create-config` | - | デフォルト設定ファイルを作成して終了 |
| `--config` | `-c` | 設定ファイルのパス（YAML形式のみ） |
| `--init` | - | スプレッドシートを初期化（警告：既存シートを削除） |
| `--production` | `-p` | 公開用のスプレッドシートを使用 |
| `--basedir` | `-b` | ガイドライン・プロジェクトのルートディレクトリ |
| `--url` | - | ドキュメントのベースURL |
| `--verbose` | `-v` | 詳細ログ出力（設定ファイルのログレベルを上書き） |
| `--help` | `-h` | ヘルプメッセージを表示 |

### Pythonモジュールとして実行

```bash
# モジュールとして実行
python -m yaml2sheet

# 設定ファイルを指定
python -m yaml2sheet -c config.yaml
```

## 設定ファイル詳細

### 設定ファイルの検索順序

1. `-c`オプション指定時：
   - 絶対パス：そのまま使用
   - 相対パス：カレントディレクトリから検索

2. `-c`オプション未指定時：
   - `${HOME}/.config/freee_a11y_gl/yaml2sheet.{yaml,yml}`
   - `./yaml2sheet.{yaml,yml}`

### 設定項目

#### 必須設定

| 項目 | 説明 | 例 |
|------|------|-----|
| `development_spreadsheet_id` | 開発用のスプレッドシートID | `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` |
| `production_spreadsheet_id` | 公開用のスプレッドシートID | `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` |
| `sheet_editor_email` | 保護範囲の編集権限を持つGoogleアカウント | `user@example.com` |

#### オプション設定

| 項目 | デフォルト値 | 説明 |
|------|-------------|------|
| `credentials_path` | `credentials.json` | Google認証情報ファイルのパス |
| `token_path` | `token.json` | Googleトークンファイルのパス |
| `log_level` | `INFO` | ログレベル（DEBUG/INFO/WARNING/ERROR/CRITICAL） |
| `basedir` | カレントディレクトリ | ガイドラインプロジェクトのルートディレクトリ |
| `base_url` | `https://a11y-guidelines.freee.co.jp` | ドキュメントのベースURL |
| `version_info_cell` | `A27` | バージョン情報を書き込むセル番地 |

## 開発・テスト

### テストの実行

```bash
# 全テストの実行
pytest

# カバレッジレポート付き
pytest --cov=yaml2sheet --cov-report=html

# 特定のテストのみ
pytest tests/unit/test_config_loader.py
```

### 開発環境のセットアップ

```bash
# 開発用依存関係のインストール
pip install -r requirements-dev.txt

# パッケージを開発モードでインストール
pip install -e .
```
