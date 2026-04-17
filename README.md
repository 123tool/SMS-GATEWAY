## 🚀 SMS GATEWAY

SMS Broadcasting Tool coded for professional developers and marketing needs.

## ✨ Features
- **Multi-Threading**: Send thousands of messages in seconds using parallel processing.
- **Multi-Provider**: Supports Twilio and Vonage (Nexmo) with easy expansion.
- **Auto-Logging**: Success and failure logs are automatically saved to the `results/` folder.
- **Smart Directory**: Automatically manages data and config folders.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/123tool/SMS-GATEWAY.git]
   cd SMS-GATEWAY

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Setup Data**
​Create a folder named data.
​Add phone.txt (List of phone numbers with country code, e.g., +62812...).
​Add message.txt (The text you want to send).

4. **Run the tool**
```bash
python main.py

