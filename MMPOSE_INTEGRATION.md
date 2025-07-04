# MMPose水滴付与データ拡張 - 統合ガイド

## 🎯 概要

このガイドは、ROLE_python3の水滴生成機能をMMPoseのRTMPose学習パイプラインに統合する方法を説明します。

## 📁 ファイル構成

```
ROLE_python3/
├── mmpose_integration/                    # MMPose統合モジュール
│   ├── __init__.py
│   └── raindrop_transform.py             # カスタムTransform実装
├── raindrop/                             # 水滴生成ライブラリ
│   ├── dropgenerator.py
│   └── config.py
└── rtmpose-m_8xb64-210e_mpii-256x256.py  # 修正済み設定ファイル
```

## 🚀 使用方法

### 1. ファイル配置

元のMMPose設定ファイルの場所:
```
/home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py
```

### 2. ROLE_python3を適切な場所に配置

MMPoseからアクセスできる場所にROLE_python3を配置します：

**方法A: シンボリックリンク (推奨)**
```bash
cd /home/usami/mmpose
ln -s /home/usami/ROLE/ROLE_python3 ./role_python3
```

**方法B: 環境変数でPythonパスを追加**
```bash
export PYTHONPATH="/home/usami/ROLE/ROLE_python3:$PYTHONPATH"
```

### 3. 修正済み設定ファイルをコピー

```bash
# 元のファイルをバックアップ
cp /home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py \
   /home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py.backup

# 修正版をコピー
cp /home/usami/ROLE/ROLE_python3/rtmpose-m_8xb64-210e_mpii-256x256.py \
   /home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py
```

### 4. MMPose設定ファイルのインポートパス修正

`/home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py`
のインポートパスを環境に合わせて修正：

```python
# Custom imports for raindrop augmentation
custom_imports = dict(
    imports=['role_python3.mmpose_integration.raindrop_transform'],  # パスを調整
    allow_failed_imports=False)
```

## 📊 水滴付与の動作

### Stage 1 (最初の180エポック)
- **水滴付与**: 40%の確率で適用
- **水滴設定**: 
  - 水滴数: 5-15個
  - 半径: 15-25ピクセル
  - 形状: default, round, oval, teardrop
  - エッジ暗化: 25%

### Stage 2 (最後の30エポック)
- **水滴付与**: なし（通常のファインチューニング）

## 🔧 学習実行

### 通常の学習コマンド
```bash
cd /home/usami/mmpose

# 学習実行
python tools/train.py configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py

# 分散学習の場合
bash tools/dist_train.sh configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py 8
```

### 設定の確認
```bash
# 設定ファイルの構文チェック
python tools/misc/print_config.py configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py
```

## ⚙️ パラメータ調整

### 水滴付与確率の調整

```python
# rtmpose-m_8xb64-210e_mpii-256x256.py 内で調整
dict(type='RaindropAugmentationStage1', probability=0.3),  # 30%に下げる
dict(type='RaindropAugmentationStage1', probability=0.5),  # 50%に上げる
```

### カスタム水滴設定

```python
# より強い水滴効果
dict(type='RaindropAugmentation', 
     probability=0.4,
     raindrop_config={
         'maxR': 30,
         'minR': 20,
         'maxDrops': 20,
         'minDrops': 10,
         'edge_darkratio': 0.3
     })
```

## 🐛 トラブルシューティング

### 1. インポートエラー
```
ModuleNotFoundError: No module named 'mmpose_integration'
```

**解決策**:
- PYTHONPATHの設定を確認
- シンボリックリンクの作成を確認
- custom_importsのパスを確認

### 2. 水滴生成エラー
```
Warning: Raindrop augmentation failed: [Errno 2] No such file or directory
```

**解決策**:
- 一時ディレクトリ`/tmp`の書き込み権限を確認
- ディスク容量を確認

### 3. 学習が遅い
水滴付与により学習が遅くなった場合：

```python
# 確率を下げる
dict(type='RaindropAugmentationStage1', probability=0.2),

# または一時的に無効化
# dict(type='RaindropAugmentationStage1', probability=0.4),
```

## 📈 効果測定

### 学習ログの確認
```bash
# ログから水滴適用状況を確認
tail -f work_dirs/rtmpose-m_8xb64-210e_mpii-256x256/[timestamp].log | grep -i raindrop
```

### 推論での効果確認
```python
# 雨天画像での推論テスト
python demo/topdown_demo_with_mmdet.py \
    demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person.py \
    https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth \
    configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py \
    work_dirs/rtmpose-m_8xb64-210e_mpii-256x256/best_PCK_epoch_210.pth \
    --input rainy_test_image.jpg \
    --output-root vis_results/
```

## 📊 期待される効果

- **雨天精度向上**: PCK@0.5で+2-5%の改善を期待
- **ロバスト性**: 悪天候での安定した推定
- **汎化性能**: 未知環境での適応能力向上

## ⚠️ 注意事項

1. **Stage 1のみ適用**: Stage 2では水滴付与を行わない
2. **確率的適用**: 全ての画像に適用するわけではない
3. **計算コスト**: 水滴生成により若干の処理時間増加
4. **一時ファイル**: 十分なディスク容量が必要

---

## 🔄 元の設定に戻す方法

```bash
# バックアップから復元
cp /home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py.backup \
   /home/usami/mmpose/configs/body_2d_keypoint/rtmpose/mpii/rtmpose-m_8xb64-210e_mpii-256x256.py
```