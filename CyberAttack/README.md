# Network Intrusion Detection with LSTM (CICIDS2017)

An LSTM-based deep learning model for multi-class network intrusion detection, trained on the [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) dataset. The model classifies network flow records into benign traffic and several attack categories (DoS, Web Attack, PortScan, etc.) using short sequences of consecutive flow records as input.

## Dataset

This project uses the CICIDS2017 dataset (CSV/flow-based version, ISCX format), which contains labeled network traffic captured over five days, covering benign traffic and a range of attack scenarios.

The following CSV files are expected in the working directory:

- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

> The raw CSVs are not included in this repo due to size. Download them from the [official CIC IDS2017 page](https://www.unb.ca/cic/datasets/ids-2017.html) and place them in the project root (or update the `files` list in `model.py` with the correct paths).

### Label consolidation

To reduce class sparsity, related attack subtypes are merged into broader categories:

| Original label(s) | Merged into |
|---|---|
| DoS Hulk, DoS GoldenEye, DoS slowloris, DoS Slowhttptest, DDoS | `DoS` |
| Web Attack – Brute Force, Web Attack – XSS, Web Attack – Sql Injection | `Web Attack` |

Rows labeled `Heartbleed` are dropped due to extremely low sample count.

## Preprocessing pipeline

1. Load and concatenate all six CSVs, stripping whitespace from column names.
2. Drop duplicate rows.
3. Replace infinite values with `NaN` and drop resulting missing rows.
4. Apply label consolidation (above).
5. Stratified split into train / validation / test sets (70% / 15% / 15%).
6. Encode labels with `LabelEncoder`.
7. Scale features with `StandardScaler` (fit on train only).
8. Compute class weights (`sqrt` of the "balanced" weighting) to counter class imbalance in the loss function.
9. Build overlapping sequences of consecutive flow records (`seq_len=6`, stride 1) via a sliding window, so the model sees short temporal context rather than single flows in isolation.

## Model architecture

A single-layer LSTM followed by a linear classification head:

```
Input: (batch, seq_len=6, features=78)
  -> LSTM(input_size=78, hidden_size=70, num_layers=1, batch_first=True)
  -> take output at last timestep
  -> Linear(70 -> 7)  # 7 output classes
```

- **Loss:** Cross-entropy with class weights
- **Optimizer:** Adam, lr=0.001
- **Batch size:** 3050
- **Epochs:** 10
- **Device:** CUDA if available, else CPU

## Requirements

```
pandas
numpy
scikit-learn
torch
joblib
```

Install with:

```bash
pip install pandas numpy scikit-learn torch joblib
```

## Usage

1. Place the six CICIDS2017 CSV files in the project root.
2. Run the training script:

```bash
python model.py
```

This will:
- Preprocess the data and build sequences
- Train the LSTM for 10 epochs, printing per-epoch training/validation loss
- Evaluate on the held-out test set and print accuracy plus a full classification report
- Save the trained model and preprocessing objects:
  - `lstm_model.pth` — model weights (`state_dict`)
  - `scaler.pkl` — fitted `StandardScaler`
  - `encoder.pkl` — fitted `LabelEncoder`

## Loading the saved model for inference

```python
import torch
import joblib
from model import cyber 

model = cyber()
model.load_state_dict(torch.load("lstm_model.pth"))
model.eval()

scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")
```
