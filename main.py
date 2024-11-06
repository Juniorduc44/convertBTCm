from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from blockchain import exchangerates as ex
from kivy.clock import Clock
from functools import partial
import certifi
import ssl
import urllib3
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# Configure SSL context
ssl._create_default_https_context = ssl._create_unverified_context

class BitcoinConverterApp(App):
    def build(self):
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Initialize BTC price
        self.btc_price = 0
        self.is_usd_to_btc = True
        
        # Bitcoin price display (at the top)
        self.price_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        self.price_label = Label(
            text='Loading Bitcoin Price...',
            font_size=dp(24),
            color=get_color_from_hex('#FFFFFF')
        )
        self.price_layout.add_widget(self.price_label)
        self.main_layout.add_widget(self.price_layout)
        
        # Satoshi info
        self.main_layout.add_widget(Label(
            text='1 satoshi = 0.00000001 BTC',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30)
        ))
        
        # Conversion mode switch
        switch_layout = BoxLayout(size_hint_y=None, height=dp(50))
        self.mode_label = Label(
            text='USD → BTC',
            font_size=dp(18),
            size_hint_x=0.7
        )
        self.mode_switch = Switch(size_hint_x=0.3)
        self.mode_switch.bind(active=self.toggle_conversion_mode)
        switch_layout.add_widget(self.mode_label)
        switch_layout.add_widget(self.mode_switch)
        self.main_layout.add_widget(switch_layout)
        
        # Input area
        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
        self.amount_input = TextInput(
            multiline=False,
            hint_text='Enter Amount',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        
        # Satoshi checkbox
        checkbox_layout = BoxLayout(size_hint_y=None, height=dp(40))
        self.satoshi_checkbox = CheckBox(
            disabled=True,
            size_hint_x=None,
            width=dp(40)
        )
        checkbox_label = Label(
            text='Satoshi',
            font_size=dp(16)
        )
        checkbox_layout.add_widget(self.satoshi_checkbox)
        checkbox_layout.add_widget(checkbox_label)
        
        input_layout.add_widget(self.amount_input)
        input_layout.add_widget(checkbox_layout)
        self.main_layout.add_widget(input_layout)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        convert_button = Button(
            text='Convert',
            font_size=dp(18),
            background_color=get_color_from_hex('#2196F3')
        )
        clear_button = Button(
            text='Clear',
            font_size=dp(18),
            background_color=get_color_from_hex('#757575')
        )
        convert_button.bind(on_press=self.convert)
        clear_button.bind(on_press=self.delete_result)
        button_layout.add_widget(convert_button)
        button_layout.add_widget(clear_button)
        self.main_layout.add_widget(button_layout)
        
        # Result labels
        results_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        self.result_label = Label(
            text='',
            font_size=dp(24),
            color=get_color_from_hex('#4CAF50')
        )
        self.satoshi_result_label = Label(
            text='',
            font_size=dp(18)
        )
        self.micro_amount_label = Label(
            text='',
            font_size=dp(16)
        )
        results_layout.add_widget(self.result_label)
        results_layout.add_widget(self.satoshi_result_label)
        results_layout.add_widget(self.micro_amount_label)
        self.main_layout.add_widget(results_layout)
        
        # Initial price fetch
        self.update_price(None)
        
        # Schedule regular price updates
        Clock.schedule_interval(self.update_price, 60)
        
        return self.main_layout
    
    def update_price(self, dt):
        try:
            ticker = ex.get_ticker()
            self.btc_price = ticker["USD"].p15min
            self.price_label.text = f'Bitcoin: ${self.btc_price:,.2f}'
            self.price_label.color = get_color_from_hex('#4CAF50')  # Green for success
        except Exception as e:
            print(f"Error fetching price: {str(e)}")
            self.btc_price = 0
            self.price_label.text = 'Error fetching Bitcoin price'
            self.price_label.color = get_color_from_hex('#F44336')  # Red for error
    
    def toggle_conversion_mode(self, instance, value):
        self.is_usd_to_btc = not value
        if self.is_usd_to_btc:
            self.mode_label.text = "USD → BTC"
            self.amount_input.hint_text = "Enter USD Amount"
            self.satoshi_checkbox.disabled = True
            self.satoshi_checkbox.active = False
        else:
            self.mode_label.text = "BTC → USD"
            self.amount_input.hint_text = "Enter BTC Amount"
            self.satoshi_checkbox.disabled = False
        self.delete_result(None)
    
    def format_usd_amount(self, amount):
        if amount < 0.01:
            return f"${amount:.8f}"
        return f"${amount:,.2f}"
    
    def convert(self, instance):
        if self.btc_price == 0:
            self.result_label.text = "Please wait for price update"
            self.result_label.color = get_color_from_hex('#FFC107')  # Yellow for warning
            return
            
        try:
            entry_value = self.amount_input.text.strip()
            if not entry_value:
                self.result_label.text = "Please enter an amount"
                self.result_label.color = get_color_from_hex('#F44336')
                return
                
            # Handle satoshi input
            if not self.is_usd_to_btc and self.satoshi_checkbox.active:
                amount = float(entry_value) / 100000000  # Convert satoshis to BTC
            else:
                amount = float(entry_value)
            
            if amount < 0:
                self.result_label.text = "Please enter a positive number"
                self.result_label.color = get_color_from_hex('#F44336')
                return
                
            if self.is_usd_to_btc:
                # Convert USD to BTC
                btc_amount = amount / self.btc_price
                satoshis = int(btc_amount * 100000000)
                
                self.result_label.text = f"{btc_amount:.8f} BTC"
                self.result_label.color = get_color_from_hex('#4CAF50')
                self.satoshi_result_label.text = f"{satoshis:,} satoshis"
                self.micro_amount_label.text = ""
                
            else:
                # Convert BTC to USD
                usd_amount = amount * self.btc_price
                formatted_usd = self.format_usd_amount(usd_amount)
                
                self.result_label.text = formatted_usd
                self.result_label.color = get_color_from_hex('#4CAF50')
                
                if usd_amount < 0.01:
                    self.satoshi_result_label.text = "Less than 1¢ (USD)"
                    micro_usd = usd_amount * 1000000
                    self.micro_amount_label.text = f"({micro_usd:.6f} millionths of a dollar)"
                else:
                    self.satoshi_result_label.text = ""
                    self.micro_amount_label.text = ""
                
        except ValueError:
            self.result_label.text = "Please enter a valid number"
            self.result_label.color = get_color_from_hex('#F44336')
            self.satoshi_result_label.text = ""
            self.micro_amount_label.text = ""
    
    def delete_result(self, instance):
        self.result_label.text = ""
        self.satoshi_result_label.text = ""
        self.micro_amount_label.text = ""
        self.amount_input.text = ""

if __name__ == '__main__':
    BitcoinConverterApp().run()