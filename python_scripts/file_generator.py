import random
import sys
import os

class Generator:
    def __init__(self):
        self.RANDOM_CONTENT_SIZE = 40
        self.COMMON_CONTENT_SIZE = 2000
        self.ROOT_FILE_NAME = ""
        self.COMMON_CONTENT = ""

    def generate_random_content(self):
        size=random.randint(0,self.RANDOM_CONTENT_SIZE)
        print(size)
        str_random = ""
        for num in range(size):
            str_random += " "+str(random.randint(0, sys.maxsize))+","
        return str_random

    def generate_common_content(self):
        str_common = ""
        for num in range(self.COMMON_CONTENT_SIZE):
            str_common += " " + str(random.randint(0, sys.maxsize)) + ","
        return str_common


if __name__ == "__main__":
    NUMBER_OF_FILES = 20
    str_common = Generator().generate_common_content()

    for num in range(NUMBER_OF_FILES):
        f1 = open(os.getcwd() + "\\data\\file" + str(num)+".txt", "w", encoding='utf-8')
        str_random_prefix = Generator().generate_random_content()
        str_random_suffix = Generator().generate_common_content()
        print(str_random_prefix + str_common + str_random_suffix)
        f1.write(str_random_prefix + str_common + str_random_suffix)
        f1.close()
