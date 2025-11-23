import kivy
kivy.require('2.0.0') # Replace with your current kivy version if necessary

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

import numpy as np
import math

# Define the screens in the Kivy App
class MainScreen(Screen):
    pass

class QuadraticScreen(Screen):
    def solve_quadratic(self):
        try:
            # Get values from TextInputs using their IDs defined in Kv language
            a = float(self.ids.input_a.text)
            b = float(self.ids.input_b.text)
            c = float(self.ids.input_c.text)

            if a == 0:
                self.show_popup("Error", "If 'a' is 0, this is not a quadratic equation.")
                return

            delta = b**2 - 4*a*c
            result_text = ""

            if delta > 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                result_text = f"Two real solutions:\nx1 = {x1:.4f}\nx2 = {x2:.4f}"
            elif delta == 0:
                x = -b / (2*a)
                result_text = f"One real solution:\nx = {x:.4f}"
            else:
                real_part = -b / (2*a)
                imag_part = math.sqrt(abs(delta)) / (2*a)
                result_text = f"Complex solutions:\nx1 = {real_part:.4f} + {imag_part:.4f}i\nx2 = {real_part:.4f} - {imag_part:.4f}i"
            
            self.show_popup("Quadratic Results", result_text)

        except ValueError:
            self.show_popup("Invalid Input", "Please enter valid numerical coefficients (a, b, c).")

    def show_popup(self, title, text):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=text))
        close_button = Button(text="Close", size_hint_y=None, height=44)
        content.add_widget(close_button)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()


class SimultaneousScreen(Screen):
    def solve_simultaneous(self):
        try:
            # Get values from TextInputs using their IDs defined in Kv language
            inputs = self.ids
            # Define the matrix of coefficients (A)
            A = np.array([
                [float(inputs.e11.text), float(inputs.e12.text), float(inputs.e13.text)],
                [float(inputs.e21.text), float(inputs.e22.text), float(inputs.e23.text)],
                [float(inputs.e31.text), float(inputs.e32.text), float(inputs.e33.text)]
            ])

            # Define the array of constants (B)
            B = np.array([
                float(inputs.e1b.text),
                float(inputs.e2b.text),
                float(inputs.e3b.text)
            ])

            X = np.linalg.solve(A, B)
            # Format the solutions nicely
            result_text = f"Solutions (I1, I2, I3):\nI1 = {X[0]:.4f}\nI2 = {X[1]:.4f}\nI3 = {X[2]:.4f}"
            self.show_popup("Simultaneous Equation Results", result_text)

        except ValueError:
            self.show_popup("Invalid Input", "Ensure all 12 fields have valid numbers.")
        except np.linalg.LinAlgError:
            self.show_popup("No Unique Solution", "The system has no unique solution.")
        except Exception as e:
            # You can log the error if needed, but the popup handles user feedback
            # self.show_popup("An Error Occurred", str(e))
            pass
            
    def show_popup(self, title, text):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=text))
        close_button = Button(text="Close", size_hint_y=None, height=44)
        content.add_widget(close_button)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()


# Create the Screen Manager
screen_manager = ScreenManager()


# --- Kivy Language Definition (Kv) ---
kv_string = """
ScreenManager:
    MainScreen:
    QuadraticScreen:
    SimultaneousScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: "Physics Solver Menu"
            font_size: '24sp'
        Button:
            text: "Solve Quadratic Equations"
            on_press: app.root.current = 'quadratic'
        Button:
            text: "Solve Simultaneous Equations"
            on_press: app.root.current = 'simultaneous'

<QuadraticScreen>:
    name: 'quadratic'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            text: "Solve ax² + bx + c = 0"
            font_size: '20sp'
            size_hint_y: None
            height: 40
        GridLayout:
            cols: 2
            spacing: 10
            size_hint_y: None
            height: 150
            Label:
                text: "Coefficient a:"
            TextInput:
                id: input_a
                input_type: 'number'
                multiline: False
            Label:
                text: "Coefficient b:"
            TextInput:
                id: input_b
                input_type: 'number'
                multiline: False
            Label:
                text: "Coefficient c:"
            TextInput:
                id: input_c
                input_type: 'number'
                multiline: False

        Button:
            text: "Calculate Solutions"
            size_hint_y: None
            height: 50
            on_press: root.solve_quadratic()

        Button:
            text: "Back to Main Menu"
            size_hint_y: None
            height: 40
            on_press: app.root.current = 'main'

<SimultaneousScreen>:
    name: 'simultaneous'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: "Solve 3-Variable Linear System"
            font_size: '20sp'
            size_hint_y: None
            height: 40
        ScrollView:
            GridLayout:
                cols: 6
                spacing: 5
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 40
                Label:
                    text: ""
                Label:
                    text: "I1"
                Label:
                    text: "I2"
                Label:
                    text: "I3"
                Label:
                    text: "="
                Label:
                    text: "Const"
                
                # Row 1
                Label:
                    text: "Eq 1:"
                TextInput:
                    id: e11
                    input_type: 'number'
                TextInput:
                    id: e12
                    input_type: 'number'
                TextInput:
                    id: e13
                    input_type: 'number'
                Label:
                    text: ""
                TextInput:
                    id: e1b
                    input_type: 'number'
                
                # Row 2
                Label:
                    text: "Eq 2:"
                TextInput:
                    id: e21
                    input_type: 'number'
                TextInput:
                    id: e22
                    input_type: 'number'
                TextInput:
                    id: e23
                    input_type: 'number'
                Label:
                    text: ""
                TextInput:
                    id: e2b
                    input_type: 'number'
                
                # Row 3
                Label:
                    text: "Eq 3:"
                TextInput:
                    id: e31
                    input_type: 'number'
                TextInput:
                    id: e32
                    input_type: 'number'
                TextInput:
                    id: e33
                    input_type: 'number'
                Label:
                    text: ""
                TextInput:
                    id: e3b
                    input_type: 'number'

        Button:
            text: "Calculate Solutions"
            size_hint_y: None
            height: 50
            on_press: root.solve_simultaneous()

        Button:
            text: "Back to Main Menu"
            size_hint_y: None
            height: 40
            on_press: app.root.current = 'main'
"""

# Load the Kv language string into the Kivy builder
Builder.load_string(kv_string)


class PhysicsSolverApp(App):
    def build(self):
        # Add screens to the screen manager
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(QuadraticScreen(name='quadratic'))
        screen_manager.add_widget(SimultaneousScreen(name='simultaneous'))
        return screen_manager


if __name__ == '__main__':
    PhysicsSolverApp().run()