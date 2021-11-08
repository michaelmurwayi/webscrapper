ENV = "dev"


def prt_dev(string):
    if(ENV == "dev"):
        print(f"{Colors.BOLD}{Colors.OKBLUE}DEV:{Colors.ENDC}{string}")


class Colors:
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    WARNING = "\033[93m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
