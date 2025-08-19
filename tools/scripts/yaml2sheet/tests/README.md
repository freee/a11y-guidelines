# yaml2sheet テストスイート

このディレクトリには、yaml2sheetプロジェクトの包括的なテストスイートが含まれています。

## テスト構造

```
tests/
├── conftest.py                    # pytest設定とフィクスチャ
├── unit/                          # ユニットテスト
│   ├── test_config_loader.py      # 設定ローダーのテスト
│   ├── test_auth.py               # 認証管理のテスト
│   └── test_yaml2sheet_main.py    # メイン機能のテスト
├── integration/                   # 統合テスト（今後追加予定）
├── fixtures/                      # テストデータ
│   ├── config/                    # 設定ファイルのサンプル
│   ├── yaml_data/                 # YAMLデータのサンプル
│   └── expected_outputs/          # 期待される出力データ
└── mocks/                         # モックオブジェクト
```

## テスト実行方法

### 全テストの実行
```bash
cd tools/scripts/yaml2sheet
pytest
```

### 特定のテストファイルの実行
```bash
pytest tests/unit/test_config_loader.py
```

### 特定のテストクラスの実行
```bash
pytest tests/unit/test_config_loader.py::TestApplicationConfig
```

### 特定のテストメソッドの実行
```bash
pytest tests/unit/test_config_loader.py::TestApplicationConfig::test_default_values
```

### カバレッジレポート付きで実行
```bash
pytest --cov=yaml2sheet --cov-report=html
```

### 詳細出力で実行
```bash
pytest -v -s
```

## テストマーカー

テストには以下のマーカーが設定されています：

- `@pytest.mark.unit`: ユニットテスト
- `@pytest.mark.integration`: 統合テスト
- `@pytest.mark.slow`: 実行時間の長いテスト
- `@pytest.mark.auth`: 認証関連のテスト
- `@pytest.mark.config`: 設定関連のテスト
- `@pytest.mark.sheet`: シート生成関連のテスト

特定のマーカーのテストのみ実行：
```bash
pytest -m unit
pytest -m "not slow"
```

## テストの特徴

### 既存実装の保護
- 現在の実装の全ての機能をテスト
- リファクタリング時の回帰テストとして機能
- 既存の動作を変更せずにテスト

### 包括的なカバレッジ
- 正常系・異常系の両方をテスト
- エラーハンドリングの全パターンをテスト
- 設定の全組み合わせをテスト

### モック戦略
- 外部依存（Google API、ファイルシステム）をモック
- freee_a11y_glライブラリをモック
- 環境変数の影響を排除

## フィクスチャ

### 設定関連
- `sample_config_data`: サンプル設定データ
- `sample_yaml_config_file`: YAML設定ファイル
- `sample_toml_config_file`: TOML設定ファイル
- `sample_ini_config_file`: INI設定ファイル

### 認証関連
- `mock_credentials`: Google API認証情報のモック
- `mock_google_auth`: Google認証フローのモック
- `mock_google_service`: Google Sheets APIサービスのモック

### データ関連
- `sample_yaml_data`: freee_a11y_gl出力データのサンプル
- `sample_check_with_subchecks`: サブチェック付きチェックデータ

### 環境関連
- `temp_dir`: 一時ディレクトリ
- `clean_environment`: 環境変数のクリーンアップ

## 開発時の注意点

### テスト追加時
1. 適切なマーカーを設定
2. 既存のフィクスチャを活用
3. モックを適切に使用
4. テスト名は機能を明確に表現

### 実装変更時
1. 関連するテストを更新
2. 新しい機能にはテストを追加
3. 既存テストが失敗しないことを確認
4. カバレッジが低下しないことを確認

## トラブルシューティング

### よくある問題

#### インポートエラー
```bash
# yaml2sheetモジュールが見つからない場合
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

#### 環境変数の影響
```bash
# 環境変数をクリアしてテスト実行
env -i pytest
```

#### モックが効かない
- パッチのパスが正しいか確認
- インポート順序を確認
- フィクスチャのスコープを確認

### デバッグ方法

#### テスト内でのデバッグ
```python
import pdb; pdb.set_trace()  # ブレークポイント設定
```

#### 詳細ログ出力
```bash
pytest -v -s --log-cli-level=DEBUG
```

#### 失敗したテストのみ再実行
```bash
pytest --lf  # last failed
pytest --ff  # failed first
```

## 継続的インテグレーション

このテストスイートは以下の環境で動作することを想定：

- Python 3.8+
- pytest 6.0+
- 必要な依存関係（requirements-dev.txt参照）

CI/CDパイプラインでの実行例：
```bash
pip install -r requirements-dev.txt
pytest --cov=yaml2sheet --cov-report=xml --junitxml=test-results.xml
