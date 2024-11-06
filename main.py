import ssl
import certifi
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
import urllib3

# Create a custom SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Configure urllib3 to use the custom SSL context
urllib3.connection_pools = {}
urllib3.connection_from_url = lambda url, **kw: urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
).connection_from_url(url, **kw)

class BitcoinConverterApp(App):
    def build(self):
        try:
            # Get initial Bitcoin price with error handling
            try:
                ticker = ex.get_ticker()
                self.btc_price = ticker["USD"].p15min
            except Exception as e:
                print(f"Error fetching Bitcoin price: {str(e)}")
                self.btc_price = 0
            
            self.is_usd_to_btc = True
            
            # Main layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            # Bitcoin price label
            self.price_label = Label(
                text=f'Bitcoin\n${self.btc_price:,.2f}' if self.btc_price else 'Error fetching price',
                size_hint_y=None,
                height=100
            )
            layout.add_widget(self.price_label)
            
            # Rest of your UI code remains the same
            layout.add_widget(Label(
                text='1 satoshi = 0.00000001 BTC',
                size_hint_y=None,
                height=30
            ))
            
            # Mode switch layout
            switch_layout = BoxLayout(
                size_hint_y=None,
                height=50
            )
            self.mode_label = Label(text='USD → BTC')
            self.mode_switch = Switch(active=False)
            self.mode_switch.bind(active=self.toggle_conversion_mode)
            switch_layout.add_widget(self.mode_label)
            switch_layout.add_widget(self.mode_switch)
            layout.add_widget(switch_layout)
            
            # Input layout
            input_layout = BoxLayout(
                size_hint_y=None,
                height=50
            )
            self.amount_input = TextInput(
                multiline=False,
                hint_text='Enter Amount'
            )
            self.satoshi_checkbox = CheckBox(disabled=True)
            self.satoshi_label = Label(text='Satoshi')
            
            input_layout.add_widget(self.amount_input)
            input_layout.add_widget(self.satoshi_checkbox)
            input_layout.add_widget(self.satoshi_label)
            layout.add_widget(input_layout)
            
            # Buttons
            button_layout = BoxLayout(
                size_hint_y=None,
                height=50
            )
            convert_button = Button(text='Convert')
            convert_button.bind(on_press=self.convert)
            clear_button = Button(text='Clear')
            clear_button.bind(on_press=self.delete_result)
            
            button_layout.add_widget(convert_button)
            button_layout.add_widget(clear_button)
            layout.add_widget(button_layout)
            
            # Result labels
            self.result_label = Label(text='')
            self.satoshi_result_label = Label(text='')
            self.micro_amount_label = Label(text='')
            
            layout.add_widget(self.result_label)
            layout.add_widget(self.satoshi_result_label)
            layout.add_widget(self.micro_amount_label)
            
            # Schedule price updates
            Clock.schedule_interval(self.update_price, 60)  # Update price every minute
            
            return layout
        except Exception as e:
            print(f"Error in build: {str(e)}")
            return Label(text=f"Error: {str(e)}")
    
    def update_price(self, dt):
        try:
            ticker = ex.get_ticker()
            self.btc_price = ticker["USD"].p15min
            self.price_label.text = f'Bitcoin\n${self.btc_price:,.2f}'
        except Exception as e:
            print(f"Error updating price: {str(e)}")
            self.price_label.text = 'Error updating price'
    
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
        entry_value = self.amount_input.text.strip()
        
        try:
            # Handle satoshi input
            if not self.is_usd_to_btc and self.satoshi_checkbox.active:
                amount = float(entry_value) / 100000000  # Convert satoshis to BTC
            else:
                amount = float(entry_value)
            
            if amount < 0:
                self.result_label.text = "Please enter a positive number"
                self.result_label.color = (1, 0, 0, 1)  # Red
                return
                
            if self.is_usd_to_btc:
                # Convert USD to BTC
                btc_amount = amount / self.btc_price
                satoshis = int(btc_amount * 100000000)
                
                self.result_label.text = f"{btc_amount:.8f} BTC"
                self.result_label.color = (0, 1, 0, 1)  # Green
                self.satoshi_result_label.text = f"{satoshis:,} satoshis"
                self.satoshi_result_label.color = (0, 1, 0, 1)
                self.micro_amount_label.text = ""
                
            else:
                # Convert BTC to USD
                usd_amount = amount * self.btc_price
                formatted_usd = self.format_usd_amount(usd_amount)
                
                self.result_label.text = formatted_usd
                self.result_label.color = (0, 1, 0, 1)
                
                if usd_amount < 0.01:
                    self.satoshi_result_label.text = "Less than 1¢ (USD)"
                    self.satoshi_result_label.color = (1, 0.65, 0, 1)  # Orange
                    micro_usd = usd_amount * 1000000
                    self.micro_amount_label.text = f"(Approximately {micro_usd:.6f} millionths of a dollar)"
                    self.micro_amount_label.color = (1, 0.65, 0, 1)
                else:
                    self.satoshi_result_label.text = ""
                    self.micro_amount_label.text = ""
                
                if amount < 0.00001:
                    satoshis = int(amount * 100000000)
                    self.satoshi_result_label.text = f"Input was approximately {satoshis} satoshi(s)"
                    self.satoshi_result_label.color = (0, 1, 0, 1)
                
        except ValueError:
            self.result_label.text = "Please enter a valid number"
            self.result_label.color = (1, 0, 0, 1)
            self.satoshi_result_label.text = ""
            self.micro_amount_label.text = ""
        except Exception as e:
            print(f"Error in convert: {str(e)}")
            self.result_label.text = f"Error: {str(e)}"
            self.result_label.color = (1, 0, 0, 1)
    
    def delete_result(self, instance):
        self.result_label.text = ""
        self.satoshi_result_label.text = ""
        self.micro_amount_label.text = ""
        self.amount_input.text = ""

if __name__ == '__main__':
    BitcoinConverterApp().run()