def get_file_name(dir, i, folder_size):
    i = i%folder_size + 1
    string = dir+"0"*(4-len(str(i)))+str(i)+".png"
    return string

for i in range(0,110,10):
    print(get_file_name("tutorial",i, 90))