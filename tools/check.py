import os
import configparser


def file_walk(walk_path):
    for filepath, dirnames, filenames in os.walk(walk_path):
        for filename in filenames:
            target = os.path.join(filepath, filename)
            if os.path.getsize(target) == 0:
                print("\ndelete file: ", target)
                os.remove(target)
            else:
                print("\roperate on ", target, end="", flush=True)


def main():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    file_walk(config.get("Network", "Data"))


if __name__ == '__main__':
    main()
