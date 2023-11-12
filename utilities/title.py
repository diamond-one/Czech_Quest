class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_title_art():
    title = """
 ██████╗███████╗███████╗ ██████╗██╗  ██╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔════╝╚══███╔╝██╔════╝██╔════╝██║  ██║    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
██║       ███╔╝ █████╗  ██║     ███████║    ██║   ██║██║   ██║█████╗  ███████╗   ██║   
██║      ███╔╝  ██╔══╝  ██║     ██╔══██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
╚██████╗███████╗███████╗╚██████╗██║  ██║    ╚██████╔╝╚██████╔╝███████╗███████║   ██║   
 ╚═════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
    """

    # Replace characters in the title with corresponding colors
   #  title = title.replace('█', Colors.RED + '█' + Colors.RESET)
    title = title.replace('╗', Colors.BLUE + '╗' + Colors.RESET)
    title = title.replace('╝', Colors.BLUE + '╝' + Colors.RESET)
    title = title.replace('═', Colors.RED + '═' + Colors.RESET)
    title = title.replace('╚', Colors.RED + '╚' + Colors.RESET)
    title = title.replace(' ', Colors.BLUE + ' ' + Colors.RESET)
    title = title.replace('║', Colors.BLUE + '║' + Colors.RESET) 
    title = title.replace('╔', Colors.BLUE + '╔' + Colors.RESET)

    print(title)


#Currently not printing correctly (not showing in terminal)

# def print_flag_art():
#     print(Colors.BLUE + '█'  + Colors.RESET + Colors.WHITE + '█' * 85 + Colors.RESET)
#     print(Colors.BLUE + '█' * 2 + Colors.RESET + Colors.WHITE + '█' * 84 + Colors.RESET)
#     print(Colors.BLUE + '█' * 2 + Colors.RESET + Colors.RED + '█' * 84 + Colors.RESET)
#     print(Colors.BLUE + '█' + Colors.RESET + Colors.RED + '█' * 85 + Colors.RESET)

# # To call the function and print the flag art

def print_flag_art():
    print(Colors.BLUE + '█' *8 + Colors.RESET + Colors.WHITE + '█' * 78 + Colors.RESET)
    print(Colors.BLUE + '█' *8 + Colors.RESET + Colors.RED + '█' * 78 + Colors.RESET)

