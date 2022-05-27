#!/usr/bin/env python3
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

from sys import argv

binfile = argv[1]

file=open(binfile,"rb")
while word:=file.read(4) :
    print("{:02x}{:02x}{:02x}{:02x}".format(word[3],word[2],word[1],word[0]))

