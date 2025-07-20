# Bitcoin Converter Mobile App

A sleek, production-ready mobile application for converting between Bitcoin (BTC), Satoshis, and US Dollars (USD). Built with [Kivy](https://kivy.org/) for cross-platform compatibility and optimized for Android deployment.

**Current Version:** v3.0.0

## Features
- **Live Bitcoin Price:** Real-time BTC/USD price fetched from the blockchain.com API.
- **Tabbed Interface:** Modern, user-friendly navigation with tabs for Conversion, Info, and Themes.
- **Bidirectional Conversion:** Instantly convert between USD and BTC, with Satoshi support.
- **Info Page:** Learn about Bitcoin, Satoshis, and Fiat currencies in a clear, scrollable format.
- **Theming:** Choose from Default, Retro, 90s, Neo Hacker, or set your own custom color themes.
- **Dark Mode UI:** Modern, dark-themed interface with customizable accent colors.
- **Touch-Optimized:** Large buttons and inputs for mobile usability.
- **Satoshi Toggle:** Convert BTC to USD or input Satoshis directly.
- **Clear & Convert Actions:** Simple controls for fast calculations.
- **Robust Error Handling:** Extensive try/except and logging for easy troubleshooting.
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
- **Info Tab:** Read about Bitcoin, Satoshis, and Fiat currencies.
- **Themes Tab:** Instantly switch between color themes or enter your own hex codes for a custom look.
- **Clear:** Resets the input and result fields.

## Theming
- Choose from built-in themes: Default, Retro, 90s, Neo Hacker.
- Enter custom hex color codes for main and sub themes (e.g., `f9a420`).
- Theme changes are applied instantly across the app.

## Troubleshooting
- All major actions are wrapped in try/except blocks with error messages displayed in the app.
- Check the terminal/log output for detailed error logs if something goes wrong.
- If the Bitcoin price fails to update, ensure you have an internet connection.

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
