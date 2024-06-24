
class TermiX:
    @staticmethod
    def run(obj, method_name):
        if hasattr(obj, method_name) and callable(getattr(obj, method_name)):
            method = getattr(obj, method_name)
            method()
        else:
            print(f"Oops, Unknown action {method_name}!")
            exit()
