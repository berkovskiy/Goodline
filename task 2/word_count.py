import os

os.path.abspath(__file__)

iin_file = open("strings.txt", "r", encoding="utf8")
word = 0
lines = iin_file.readlines()[0]#Подсчет слов в первой строке
print(lines)
space = 'out'