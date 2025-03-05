import shutil
import time
import sys
import re
import wcwidth

from utils import fmt_dollars as d, fmt_bold as b, fmt_highlight as h, fmt_black

ESCAPE_TOP_LEFT = "\033[H"
ESCAPE_RIGHT = "\033[C"
ESCAPE_UP = "\033[1A"
ESCAPE_CLEAR = "\033[H\033[J"
ESCAPE_ERASE_SCROLLBACK = "\033[H\033[2J\033[3J"
ESCAPE_HIDE_CURSOR = "\033[?25l"
ESCAPE_SHOW_CURSOR = "\033[?25h"

# ⚒⌂🏠 ☐☑ ❌✅ ✘✔
RAW_STRING = "\033[31m■\033[0m"
PRODUCT_STRING = "\033[34m▲\033[0m"
FACTORY_STRING = "\033[90m⚒\033[0m"

def visible_width(s: str):
    # Remove ANSI escape sequences (color codes, cursor moves, etc.)
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    clean_str = ansi_escape.sub('', s)
    
    return sum(wcwidth.wcwidth(c) for c in clean_str)

def put_cursor_at(x: int, y: int):
    # print(f"{ESCAPE_TOP_LEFT}\033[{x-1}C\033[{y-1}B", end="")
    print(f"\033[{y};{x}H", end="")
    sys.stdout.flush()

if __name__ == "__main__":
    width, height = shutil.get_terminal_size()

    print(ESCAPE_ERASE_SCROLLBACK, end="")
    print(ESCAPE_HIDE_CURSOR, end="")
    sys.stdout.flush()
    
    
    
    string_buys = f"{b("Bank")} has {RAW_STRING*4} (min. {d(500)} each)"
    string_sells = f"{b("Bank")} sells {PRODUCT_STRING*2} (max. {d(5500)} each)"
    string_i_buy = f"I {b("buy")} __ {RAW_STRING} for ____ each."
    string_i_sell = f"I {b("sell")} __ {PRODUCT_STRING} for ____ each."
    # max_row_visible_width = max(visible_width(string_buys), visible_width(string_sells))

    put_cursor_at(2, 15)
    print(string_buys, end="")
    put_cursor_at(2, 16)
    print(string_i_buy, end="")
    
    col2_start = width - max(visible_width(string_sells), visible_width(string_i_sell))
    put_cursor_at(col2_start, 15)
    print(string_sells, end="")
    put_cursor_at(col2_start, 16)
    print(string_i_sell, end="")


    """ Draw top left corner """
    put_cursor_at(2, 2)
    print(h(" Month 3 "))
    put_cursor_at(2, 4)
    print(f"{b("Lex")} has {d(10000)} {RAW_STRING*4} {PRODUCT_STRING*2} {FACTORY_STRING*2}")
    put_cursor_at(2, 5)
    print(f"{b("Jool")} has {d(6541)} {RAW_STRING*6} {PRODUCT_STRING*6} {FACTORY_STRING*5}\033[90m245\033[0m")
    put_cursor_at(2, 6)
    print(f"{b("God")} has {d(513)} {RAW_STRING*1} {PRODUCT_STRING*1} {FACTORY_STRING*2}\033[90m1\033[0m    {h(" ⚠ WARNING! ")}")

    put_cursor_at(1, 8)
    print(fmt_black("=" * width))

    put_cursor_at(2, 10)
    print(f"I {b("produce")} __/3 {PRODUCT_STRING} using...")

    put_cursor_at(2, 12)
    print(f"{b("Order")} a {FACTORY_STRING} for {d(2500)} now, and {d(2500)} 1 month before constuction finish ✘", end="")

    put_cursor_at(2, height - 3)
    print(f"Money {b("left")}")
    put_cursor_at(2, height - 2)
    print(f"Best case {d(3500)}")
    put_cursor_at(2, height - 1)
    print(f"{b("Worst")} case {d(-1700)}")

    put_cursor_at(30, height - 3)
    print(f"{RAW_STRING} storage cost = {d(300)}")
    put_cursor_at(30, height - 2)
    print(f"{PRODUCT_STRING} storage cost = {d(500)}")
    put_cursor_at(30, height - 1)
    print(f"{FACTORY_STRING} maintenance cost = {d(1000)}")

    put_cursor_at(width-7, height - 1)
    print(h(" READY "))

    print(ESCAPE_TOP_LEFT, end="")
    sys.stdout.flush()
    time.sleep(50.0)
    print(ESCAPE_SHOW_CURSOR, end="", flush=True)   