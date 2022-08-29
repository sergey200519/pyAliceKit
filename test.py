a = ["button1", "button2"]
b = ["button3", "button4", "button5", "button6", "button7"]
def view_buttons(buttons):
        first_buttons = buttons[0]
        last_buttons = buttons[1]
        for item in first_buttons:
            print("_" * 40)
            print(item)
        print("_" * 40)
        last_buttons_text1 = ""
        last_buttons_text2 = ""
        last_buttons_text3 = ""
        for item in last_buttons:
            n = len(item)
            last_buttons_text1 += " " + "_" * (n + 2) + " "
            last_buttons_text2 += f" |{item}| "
            last_buttons_text3 += " " + "‾" * (n + 2) + " "
        print(last_buttons_text1)
        print(last_buttons_text2)
        print(last_buttons_text3)
view_buttons([a, b])




















#
