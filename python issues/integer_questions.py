#задача 1
print(11 * 2 ** 2 - 13 / 4 + 7)
# issue 2
import sys
a = sys.getsizeof (3**9090001) / (1024*1024)
# issue 3
def pos_add(c, d):
   return abs(c + d)
a = input("Vvedite a: ")
b = input("Vvedite b: ")
x = pos_add(int(a), int(b))
print(x)

