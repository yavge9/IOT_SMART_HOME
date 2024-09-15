## Color params:
color_red = "#FF0000"
color_green = "#008000"
color_orange = "#FFA500"
color_yellow = "#FFFF00"
color_gray = "#808080"
color_navy_blue = "#00274d"

def change_btn_color(color):
    return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 4px;
                padding: 1px 15px;
                border: 1px solid {color};
                font-size: 12px;
            }}
        """