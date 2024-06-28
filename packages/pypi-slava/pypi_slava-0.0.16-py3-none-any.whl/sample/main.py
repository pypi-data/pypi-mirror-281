if __name__ == "__main__" and __package__ is None:
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    __package__ = "sample"


from sample.functions import say_my_name

def main():
    print("main function is executed")
    say_my_name()

if __name__ == "__main__":
    main()