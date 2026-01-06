# Intro to AI HW2 - Optimization Algorithms Simulation

這是一個模擬不同優化演算法（Optimization Algorithms）在 2D 地形上尋找全域最大值（最高 GPA）的專案。透過視覺化與路徑紀錄，觀察不同演算法在隨機生成的崎嶇地形上的搜尋表現。

## 專案結構

此專案包含以下主要檔案：

- **`main.py`**: 專案的進入點。負責生成隨機地形（Loss Function）、初始化起始點、執行各個優化演算法，並呼叫視覺化模組儲存結果。
- **`landscape.py`**: 負責生成隨機的 2D 地形。地形由多個高斯分佈的圓形凸起（bumps）組成，模擬多峰值的搜尋空間。
- **`algo1.py`**: 實作 **Hill Climbing**（爬山演算法）。
- **`algo2.py`**: 實作 **Simulated Annealing**（模擬退火演算法）。
- **`algo3.py`**: 實作 **Ultimate Algorithm**（進階搜尋演算法），結合了動態步長與隨機探索策略。
- **`algo_example.py`**: 提供基本的 **Random Search**（隨機搜尋）作為對照範例。
- **`visuals.py`**: 負責繪製地形與演算法的搜尋過程，並輸出為 GIF 動畫。

## 環境需求

請確保您的 Python 環境已安裝以下套件：

- `numpy`
- `matplotlib`
- `scipy` (用於 `visuals.py` 中的圖像處理)

您可以透過 pip 安裝這些依賴：

```bash
pip install numpy matplotlib scipy
```

## 如何執行

在終端機中執行 `main.py` 即可開始模擬：

```bash
python main.py
```

程式執行過程中會針對不同的情境（單一太空船、多艘太空船）與不同的演算法進行模擬。

## 演算法說明

本專案實作了三種主要的優化策略：

1.  **Hill Climbing (`algo1.py`)**:
    -   **策略**: 貪婪策略（Greedy）。從當前位置檢查周圍 8 個鄰居，若有鄰居的 GPA 比當前高，則移動至該鄰居。
    -   **特性**: 容易陷入局部最優解（Local Optima），不保證能找到全域最大值。

2.  **Simulated Annealing (`algo2.py`)**:
    -   **策略**: 模擬金屬退火過程。除了接受更好的移動外，也有一定機率接受較差的移動（由溫度 `temp` 與差異 `delta` 決定），以跳脫局部最優解。
    -   **特性**: 具有全域搜尋能力，隨著溫度降低，行為會逐漸趨近於爬山演算法。

3.  **Ultimate Algorithm (`algo3.py`)**:
    -   **策略**: 結合多種策略的進階演算法。包含：
        -   **動態步長**: 初期步長較大以利探索，後期步長縮小以利精確定位。
        -   **隨機擾動**: 在移動中加入微小隨機性。
        -   **隨機跳躍**: 以小機率進行較長距離的跳躍，防止受困。
    -   **特性**: 旨在平衡「探索（Exploration）」與「開發（Exploitation）」，以在多艘太空船的情境下達到最佳的搜尋效率。

## 輸出檔案說明

程式執行完畢後，將會在目錄下產生以下檔案：

### 路徑紀錄 (.txt)
紀錄了演算法在每一步的座標與評分：
- `result1.txt`: Hill Climbing 的搜尋路徑。
- `result2.txt`: Simulated Annealing 的搜尋路徑。
- `result3.txt`: Ultimate Algorithm 的搜尋路徑。
- `example_1.txt`, `example_10.txt`: 範例 Random Search 的搜尋路徑。

### 視覺化動畫 (.gif)
動態展示演算法在地形上的移動過程（UFO 代表搜尋點，星星代表全域最高點）：
- `optimizer1.gif`: Hill Climbing 視覺化。
- `optimizer2.gif`: Simulated Annealing 視覺化。
- `optimizer3.gif`: Ultimate Algorithm 視覺化。
- `optimizer_example_1.gif`, `optimizer_example_10.gif`: Random Search 視覺化。

