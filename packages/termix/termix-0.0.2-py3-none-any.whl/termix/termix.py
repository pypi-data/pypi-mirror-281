
class Termix:
    @staticmethod
    def run(obj, args):
        method_name = args[0]
        if hasattr(obj, method_name) and callable(getattr(obj, method_name)):
            method = getattr(obj, method_name)
            method(args[1:])
        else:
            print(f"Oops, Unknown action {method_name}!")
            exit()
