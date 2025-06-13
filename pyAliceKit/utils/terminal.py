import os
import sys
from typing import Optional

def print_start_welcome() -> None:
    print(r"""
    ____        ___    ___           __ __ _ __ 
   / __ \__  __/   |  / (_)_______  / //_/(_) /_
  / /_/ / / / / /| | / / / ___/ _ \/ ,<  / / __/
 / ____/ /_/ / ___ |/ / / /__/  __/ /| |/ / /_  
/_/    \__, /_/  |_/_/_/\___/\___/_/ |_/_/\__/  
      /____/  
                        Welcome to PyAliceKit!
        """)


def clear_terminal() -> None:
    platforms: dict[str, str] = {
        "linux": "clear",
        "linux2": "clear",
        "darwin": "clear",
        "win32": "cls"
    }
    command: str | None = platforms.get(sys.platform)
    if command:
        os.system(command)


def print_log(
    log_text: str,
    time: str,
    text_color: Optional[str] = None,
    bg_color: Optional[str] = None
) -> None:
    colors: dict[str, int] = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "purple": 5,
        "magenta": 5,  # alias
        "cyan": 6,
        "turquoise": 6,  # alias
        "white": 7,
        "gray": 8,
        "light_red": 9,
        "light_green": 10,
        "light_yellow": 11,
        "light_blue": 12,
        "light_purple": 13,
        "light_cyan": 14,
        "light_white": 15
    }

    def color_code(name: Optional[str], is_bg: bool = False) -> str:
        if name is None:
            return ""
        name = name.lower()
        if name not in colors:
            return ""
        base = 48 if is_bg else 38
        return f"\033[{base};5;{colors[name]}m"

    color_start: str = f"{color_code(text_color)}{color_code(bg_color, is_bg=True)}"
    color_end: str = "\033[0m" if color_start else ""

    print(f"{color_start}{time}  -->  {log_text}{color_end}")