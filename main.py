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

# Set dark theme colors
Window.clearcolor = (0.2, 0.2, 0.2, 1)

# Kivy UI layout
KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    
    canvas.before:
        Color:
            rgba: 0.25, 0.25, 0.25, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        id: title_label
        text: 'Bitcoin'
        font_size: '24sp'
        size_hint_y: None
        height: '40dp'
    
    Label:
        id: price_label
        text: 'Loading...'
        font_size: '28sp'
        size_hint_y: None
        height: '40dp'
    
    Label:
        text: '1 satoshi = 0.00000001 BTC'
        font_size: '16sp'
        size_hint_y: None
        height: '40dp'
    
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        
        Label:
            id: mode_label
            text: 'USD → BTC'
            size_hint_x: 0.4
        
        Switch:
            id: mode_switch
            size_hint_x: 0.6
            on_active: app.toggle_mode(self.active)
    
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        
        TextInput:
            id: amount_input
            hint_text: 'Enter Amount'
            multiline: False
            size_hint_x: 0.7
            font_size: '18sp'
        
        CheckBox:
            id: satoshi_checkbox
            size_hint_x: 0.15
            disabled: True
        
        Label:
            text: 'Satoshi'
            size_hint_x: 0.15
    
    Button:
        text: 'Convert'
        size_hint_y: None
        height: '40dp'
        background_color: 0.2, 0.6, 0.9, 1
        on_press: app.convert()
    
    Button:
        text: 'Clear'
        size_hint_y: None
        height: '40dp'
        background_color: 0.2, 0.6, 0.9, 1
        on_press: app.clear()
    
    Label:
        id: result_label
        text: ''
        font_size: '20sp'
        size_hint_y: None
        height: '60dp'
'''

class BitcoinConverterApp(App):
    def build(self):
        Window.size = (300, 500)
        Window.minimum_width = 300
        Window.minimum_height = 500
        self.is_usd_to_btc = True
        self.btc_price = 0
        
        # Load the UI
        self.root = Builder.load_string(KV)
        
        # Schedule the first price update
        Clock.schedule_once(self.update_price, 0)
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