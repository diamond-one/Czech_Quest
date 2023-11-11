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

