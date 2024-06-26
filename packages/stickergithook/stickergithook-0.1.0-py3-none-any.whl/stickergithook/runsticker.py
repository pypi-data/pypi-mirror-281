#!/usr/bin/env python3

import os, random

if len(os.listdir("./.git/hooks/current")) == 0:
    if len(os.listdir("./.git/hooks/todo/")) == 0:
        os.rename("./.git/hooks/todo/", "./.git/hooks/temp")
        os.rename("./.git/hooks/done/", "./.git/hooks/todo/")
        os.rename("./.git/hooks/temp", "./.git/hooks/done/")
    f = random.choice(os.listdir("./.git/hooks/todo/"))
    os.rename("./.git/hooks/todo//" + f , "./.git/hooks/current/0.txt")

# commit_msg_filepath = sys.argv[1]
count = int(os.listdir("./.git/hooks/current")[0].split('.')[0]) + 1
with open("./.git/hooks/current" + os.listdir("./.git/hooks/current")[0], "r") as f:
    temp =""
    lines = f.readlines()
    for x in range(count):
        temp += lines[x]
    print(temp)
    # with open(commit_msg_filepath, 'w') as send:
    #     send.write(temp)
    if count == len(lines):
        os.rename("./.git/hooks/current/" + str(count - 1) + ".txt" , "./.git/hooks/done/"+ str(len(os.listdir("./.git/hooks/done/")))+".txt")
    else:
        os.rename("./.git/hooks/current/" + str(count - 1)+ ".txt" , "./.git/hooks/current/" + str(count)+ ".txt")