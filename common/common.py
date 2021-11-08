ENV = "dev"


def prt_dev(string, *args):
    if(ENV == "dev"):
        tmp_str = ""
        for x, arg in enumerate(args):
            if x != len(args):
                tmp_str += " " + str(arg)
            else:
                tmp_str += str(arg)

        print(f"{Colors.BOLD}{Colors.OKBLUE}DEV: {Colors.ENDC}{string}{tmp_str}")


class Colors:
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    WARNING = "\033[93m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
