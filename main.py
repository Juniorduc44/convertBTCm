from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.clock import Clock
from blockchain import exchangerates as ex
from kivy.core.window import Window
import ssl
import certifi
import logging
from kivy.properties import ListProperty

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Set default dark theme color
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# Configure SSL context
ssl._create_default_https_context = ssl._create_unverified_context

def hex_to_rgba(hex_str):
    """Convert hex color (e.g. 'f9a420') to RGBA tuple."""
    try:
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            return (r, g, b, 1)
        elif len(hex_str) == 8:
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            a = int(hex_str[6:8], 16) / 255.0
            return (r, g, b, a)
        else:
            raise ValueError('Hex color must be 6 or 8 characters')
    except Exception as e:
        logging.error(f"Invalid hex color '{hex_str}': {str(e)}")
        return (1, 1, 1, 1)

class BitcoinConverterApp(App):
    theme_bg = ListProperty([0.1, 0.1, 0.1, 1])
    theme_accent = ListProperty([0.98, 0.64, 0.13, 1])
    theme_button = ListProperty([0, 0.3, 0.6, 1])
    theme_button_text = ListProperty([1, 1, 1, 1])
    theme_input_bg = ListProperty([0.2, 0.2, 0.2, 1])
    theme_input_text = ListProperty([1, 1, 1, 1])
    theme_label = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_usd_to_btc = True
        self.btc_price = 0

    def build(self):
        self.root = Builder.load_file('main.kv')
        self.update_price(0)  # Fetch price immediately
        Clock.schedule_interval(self.update_price, 60)
        return self.root

    def update_price(self, dt):
        try:
            ticker = ex.get_ticker()
            self.btc_price = ticker["USD"].p15min
            self.root.ids.price_label.text = f'${self.btc_price:,.2f}'
            self.clear_error()
        except Exception as e:
            logging.error(f"Error fetching price: {str(e)}")
            self.root.ids.price_label.text = 'Error updating price'
            self.set_error(f"Price update failed: {str(e)}")

    def toggle_mode(self, is_active):
        try:
            self.is_usd_to_btc = not is_active
            if self.is_usd_to_btc:
                self.root.ids.mode_label.text = "USD → BTC"
                self.root.ids.amount_input.hint_text = "Enter USD Amount"
                self.root.ids.satoshi_checkbox.disabled = True
                self.root.ids.satoshi_checkbox.active = False
            else:
                self.root.ids.mode_label.text = "BTC → USD"
                self.root.ids.amount_input.hint_text = "Enter BTC Amount"
                self.root.ids.satoshi_checkbox.disabled = False
            self.clear()
            self.clear_error()
        except Exception as e:
            logging.error(f"Error toggling mode: {str(e)}")
            self.set_error(f"Mode toggle failed: {str(e)}")

    def convert(self):
        try:
            amount_str = self.root.ids.amount_input.text
            if not amount_str:
                self.set_error("Please enter an amount.")
                return
            amount = float(amount_str)
            if amount <= 0:
                self.set_error("Please enter a positive number.")
                return
            if self.btc_price <= 0:
                self.set_error("BTC price unavailable.")
                return
            if self.is_usd_to_btc:
                btc_amount = amount / self.btc_price
                satoshis = int(btc_amount * 100_000_000)
                self.root.ids.result_label.text = f"{btc_amount:.8f} BTC\n({satoshis:,} satoshis)"
            else:
                if self.root.ids.satoshi_checkbox.active:
                    amount = amount / 100_000_000  # Convert satoshis to BTC
                usd_amount = amount * self.btc_price
                self.root.ids.result_label.text = f"${usd_amount:,.2f}"
                if usd_amount < 0.01:
                    self.root.ids.result_label.text += f"\n(${usd_amount:.8f})"
            self.clear_error()
        except ValueError:
            self.set_error("Please enter a valid number.")
        except Exception as e:
            logging.error(f"Error during conversion: {str(e)}")
            self.set_error(f"Conversion failed: {str(e)}")

    def clear(self):
        try:
            self.root.ids.amount_input.text = ''
            self.root.ids.result_label.text = ''
            self.clear_error()
        except Exception as e:
            logging.error(f"Error clearing fields: {str(e)}")
            self.set_error(f"Clear failed: {str(e)}")

    def set_error(self, msg):
        self.root.ids.error_label.text = msg

    def clear_error(self):
        self.root.ids.error_label.text = ''

    def set_theme(self, main_color, accent_color, button_color=None, button_text=None, input_bg=None, input_text=None, label_color=None):
        try:
            self.theme_bg = main_color
            self.theme_accent = accent_color
            self.theme_button = button_color or [0, 0.3, 0.6, 1]
            self.theme_button_text = button_text or [1, 1, 1, 1]
            self.theme_input_bg = input_bg or [0.2, 0.2, 0.2, 1]
            self.theme_input_text = input_text or [1, 1, 1, 1]
            self.theme_label = label_color or [1, 1, 1, 1]
            if self.root:
                self.root.ids.price_label.color = self.theme_accent
        except Exception as e:
            logging.error(f"Error setting theme: {str(e)}")
            self.set_error(f"Theme change failed: {str(e)}")

    def select_theme(self, theme_name):
        try:
            if theme_name == 'default':
                self.set_theme((0.1, 0.1, 0.1, 1), (0.98, 0.64, 0.13, 1))
            elif theme_name == 'retro':
                self.set_theme((0.98, 0.64, 0.13, 1), (0.1, 0.1, 0.1, 1))
            elif theme_name == 'nineties':
                self.set_theme((0.2, 0.2, 0.7, 1), (1, 1, 0.2, 1))
            elif theme_name == 'hacker':
                self.set_theme((0.1, 0.1, 0.1, 1), (0.2, 1, 0.2, 1))
            else:
                self.set_error('Unknown theme')
        except Exception as e:
            logging.error(f"Error selecting theme: {str(e)}")
            self.set_error(f"Theme selection failed: {str(e)}")

    def apply_custom_theme(self):
        try:
            main_hex = self.root.ids.main_color_input.text.strip()
            sub_hex = self.root.ids.sub_color_input.text.strip()
            if not main_hex or not sub_hex:
                self.set_error('Please enter both main and sub color hex values.')
                return
            main_color = hex_to_rgba(main_hex)
            sub_color = hex_to_rgba(sub_hex)
            self.set_theme(main_color, sub_color)
        except Exception as e:
            logging.error(f"Error applying custom theme: {str(e)}")
            self.set_error(f"Custom theme failed: {str(e)}")

if __name__ == '__main__':
    BitcoinConverterApp().run()