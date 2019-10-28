import random
import sys
import os

COMMON_CONTENT_SIZE_RANGE = 200
RANDOM_CONTENT_SIZE_RANGE = 50
MAX_FILES_IN_CLUSTER = 20
NUMBER_OF_CLUSTERS = 30

def create_file(file_name, file_type, content ):
    print("writing file "+file_name)
    f1 = open(os.getcwd() + "/dataset/"+file_name + file_type, "w", encoding='utf-8')
    print(content)
    f1.write(content)
    f1.close()


def generate_common_content(common_content_Size):
    str_common = ""
    for num in range(common_content_Size):
        str_common += " " + str(random.randint(0, sys.maxsize)) + ","
    return str_common


def generate_file_metadata(common_size, prefix_size, postfix_size, cluster_num):
    return "[ commonSize=" + str(common_size) + ", prefixSize=" + str(prefix_size) + ", postfixSize=" + str(postfix_size) + ", totalUncommonSize=" + str((postfix_size + prefix_size)) + ", totalSize=" + str((prefix_size + prefix_size + common_size)) + ", cluster=" + str(cluster_num) + " ]";



def create_file_cluster(cluster_num, cluster_size):

    common_content_size = random.randint(0,COMMON_CONTENT_SIZE_RANGE)
    common_content = generate_common_content(common_content_size);
    for num in range(1, cluster_size+1):
        prefix_content_size = random.randint(0, RANDOM_CONTENT_SIZE_RANGE);
        postfix_content_size = random.randint(0, RANDOM_CONTENT_SIZE_RANGE);
        random_prefix_content = generate_common_content(prefix_content_size);
        random_suffix_content = generate_common_content(postfix_content_size);
        content = random_prefix_content + common_content + random_suffix_content;
        create_file(str(cluster_num) + "_" + str(num), ".txt", content);
        metadata = generate_file_metadata(common_content_size, prefix_content_size, postfix_content_size, cluster_num);
        create_file(str(cluster_num) + "_" + str(num), ".properties", metadata);






if __name__ == "__main__":
    print("started file generation")
    for num in range(1, NUMBER_OF_CLUSTERS+1):
        number_of_files_in_cluster = random.randint(1, MAX_FILES_IN_CLUSTER)
        create_file_cluster(num,number_of_files_in_cluster)

    print("completed")