from reedsolomon import *


"""
Инициализируем декодер, nsym = n-k - число корректирующих символов. Код рида-соломона
 является МДР-кодом, а значит он лежит на границе Синглтона d = n - k + 1 = nsym + 1.
Это значит, что мы можем гарантированно исправлять nsym/2 ошибок
"""
nsym = 10
rs = RSCodec(nsym)

a = rs.encode(b'petuh')
'''>>> bytearray(b'petuh\xf1+\x04W\xb63\xaa\xab\xa9\xb7')'''
b = rs.encode([1,2,3,4])
'''>>> bytearray(b'\x01\x02\x03\x04,\x9d\x1c+=\xf8h\xfa\x98M')'''

'''b[0] = 1
   b[1] = 2
    ...

   '''

'''Декодер выдает нам байт-массивы в 16-ричной системе счисления'''

a = bytearray(b"mamka\xb2\'\xbeJKJQ\xc5\x90")

'''внесли пять ошибок petuh -> mamka'''



a = rs.encode ([1,1,1,1,1,1,0,0,0,0])
a[0] = 3
a[1] = 2
a[2] = 4
a[3] = 3
a[4] = 3
a[5] = 3

b = rs.decode(a)

print(b)





