from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from blockchain import exchangerates as ex
from kivy.core.text import LabelBase
import ssl
import certifi

# Set dark theme colors
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Darker background

# Configure SSL context
ssl._create_default_https_context = ssl._create_unverified_context

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: '20dp'
    spacing: '15dp'
    canvas.before:
        Color:
            rgba: 0.15, 0.15, 0.15, 1  # Slightly lighter than background
        Rectangle:
            pos: self.pos
            size: self.size

    # Title Section
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '120dp'
        
        Label:
            id: title_label
            text: 'Bitcoin'
            font_size: '28sp'
            bold: True
            size_hint_y: None
            height: '40dp'
            color: 1, 1, 1, 1
        
        Label:
            id: price_label
            text: 'Loading...'
            font_size: '32sp'
            bold: True
            size_hint_y: None
            height: '40dp'
            color: 1, 1, 1, 1
        
        Label:
            text: '1 satoshi = 0.00000001 BTC'
            font_size: '16sp'
            size_hint_y: None
            height: '40dp'
            color: 0.7, 0.7, 0.7, 1

    # Conversion Mode Section
    BoxLayout:
        size_hint_y: None
        height: '50dp'
        spacing: '10dp'
        
        BoxLayout:
            size_hint_x: 0.7
            Label:
                id: mode_label
                text: 'USD → BTC'
                font_size: '20sp'
                color: 1, 1, 1, 1
                
        Switch:
            id: mode_switch
            size_hint_x: 0.3
            on_active: app.toggle_mode(self.active)

    # Input Section
    BoxLayout:
        size_hint_y: None
        height: '50dp'
        spacing: '10dp'
        
        TextInput:
            id: amount_input
            hint_text: 'Enter Amount'
            multiline: False
            size_hint_x: 0.8
            font_size: '18sp'
            background_color: 0.2, 0.2, 0.2, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.5, 0.5, 0.5, 1
            padding: '10dp', '10dp'
            
        BoxLayout:
            size_hint_x: 0.2
            CheckBox:
                id: satoshi_checkbox
                disabled: True
            Label:
                text: 'Sats'
                font_size: '14sp'
                color: 0.7, 0.7, 0.7, 1

    # Buttons Section
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '100dp'
        spacing: '10dp'
        
        Button:
            text: 'Convert'
            size_hint_y: None
            height: '45dp'
            background_color: 0, 0.3, 0.6, 1  # Dark blue
            background_normal: ''
            font_size: '18sp'
            on_press: app.convert()
            canvas.before:
                Color:
                    rgba: self.background_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [23]  # This creates rounded corners
            
        Button:
            text: 'Clear'
            size_hint_y: None
            height: '45dp'
            background_color: 0, 0.3, 0.6, 1  # Dark blue
            background_normal: ''
            font_size: '18sp'
            on_press: app.clear()
            canvas.before:
                Color:
                    rgba: self.background_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [23]  # This creates rounded corners

    # Result Section
    Label:
        id: result_label
        text: ''
        font_size: '24sp'
        color: 0.2, 0.8, 0.2, 1  # Green color for results
        size_hint_y: 0.4
'''

class BitcoinConverterApp(App):
    def build(self):
        self.is_usd_to_btc = True
        self.btc_price = 0      
        # Load the UI
        self.root = Builder.load_string(KV)        
        # Schedule the first price update
        Clock.schedule_once(self.update_price, 1)
        # Schedule regular price updates every 60 seconds
        Clock.schedule_interval(self.update_price, 60)
        
        return self.root
    
    def update_price(self, dt):
        try:
            ticker = ex.get_ticker()
            self.btc_price = ticker["USD"].p15min
            self.root.ids.price_label.text = f'${self.btc_price:,.2f}'
        except Exception as e:
            print(f"Error fetching price: {str(e)}")
            self.root.ids.price_label.text = 'Error updating price'
    
    def toggle_mode(self, is_active):
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
    
    def convert(self):
        try:
            amount = float(self.root.ids.amount_input.text)
            if amount <= 0:
                self.root.ids.result_label.text = "Please enter a positive number"
                return
            
            if self.is_usd_to_btc:
                # Convert USD to BTC
                btc_amount = amount / self.btc_price
                satoshis = int(btc_amount * 100000000)
                self.root.ids.result_label.text = f"{btc_amount:.8f} BTC\n({satoshis:,} satoshis)"
            else:
                # Convert BTC to USD
                if self.root.ids.satoshi_checkbox.active:
                    amount = amount / 100000000  # Convert satoshis to BTC
                usd_amount = amount * self.btc_price
                self.root.ids.result_label.text = f"${usd_amount:,.2f}"
                
                if usd_amount < 0.01:
                    self.root.ids.result_label.text += f"\n(${usd_amount:.8f})"
        
        except ValueError:
            self.root.ids.result_label.text = "Please enter a valid number"
        except Exception as e:
            self.root.ids.result_label.text = f"Error: {str(e)}"
    
    def clear(self):
        self.root.ids.amount_input.text = ''
        self.root.ids.result_label.text = ''

if __name__ == '__main__':
    BitcoinConverterApp().run()