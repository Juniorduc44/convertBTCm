# Bitcoin Converter Mobile App

A sleek, production-ready mobile application for converting between Bitcoin (BTC), Satoshis, and US Dollars (USD). Built with [Kivy](https://kivy.org/) for cross-platform compatibility and optimized for Android deployment.

## Features
- **Live Bitcoin Price:** Real-time BTC/USD price fetched from the blockchain.com API.
- **Bidirectional Conversion:** Instantly convert between USD and BTC, with Satoshi support.
- **Dark Mode UI:** Modern, dark-themed interface for comfortable use.
- **Touch-Optimized:** Large buttons and inputs for mobile usability.
- **Satoshi Toggle:** Convert BTC to USD or input Satoshis directly.
- **Clear & Convert Actions:** Simple controls for fast calculations.
- **Android Ready:** Configured for Android deployment via Buildozer.

## Screenshots
*Coming soon: UI overhaul and screenshots!*

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/convertBTCm.git
cd convertBTCm
```

### 2. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application (Desktop Preview)
```bash
python main.py
```

### 5. Build for Android (Optional)
Ensure you have [Buildozer](https://github.com/kivy/buildozer) and Android SDK/NDK set up.
```bash
buildozer -v android debug
```
The APK will be generated in the `bin/` directory.

## Usage
- **USD → BTC:** Enter a USD amount, tap Convert to see the equivalent in BTC and Satoshis.
- **BTC → USD:** Toggle the switch, enter BTC or Satoshis, tap Convert to see the USD value.
- **Clear:** Resets the input and result fields.

## Requirements
- Python 3.7+
- See `requirements.txt` for all dependencies
- For Android: JDK, Android SDK/NDK, Buildozer

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License. See [LICENSE](LICENSE) for details.

---
*This project is under active development. UI/UX improvements and new features coming soon!*
