class Colors:
    BLACK = "\033[0;30m"
    YELLOW_BG = "\033[0;103m"
    CYAN_BG = "\033[30;103m"
    YELLOW = "\033[1;93m"
    BLACK_ON_YELLOW = "\033[30;103m"
    RESET = "\033[0m"
    BOLD_WHITE = "\033[1;97m"
    GRAY = "\033[90m"

def fmt_dollars(x_in: str | int) -> str:
    x = int(x_in)
    return f"{Colors.YELLOW}{"" if x >= 0 else "-"}${abs(x)}{Colors.RESET}"

# def fmt_dollars(x_in: str | int) -> str:
#     x = int(x_in)
#     return f"{Colors.BLACK_ON_YELLOW}{"" if x >= 0 else "-"}${abs(x)}{Colors.RESET}"

def fmt_bold(x_in: str) -> str:
    return f"{Colors.BOLD_WHITE}{x_in}{Colors.RESET}"

def fmt_highlight(x_in: str) -> str:
    return f"{Colors.CYAN_BG}{x_in}{Colors.RESET}"

def fmt_black(x_in: str) -> str:
    return f"{Colors.GRAY}{x_in}{Colors.RESET}"