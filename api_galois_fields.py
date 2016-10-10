def hamming_weight(x):
   '''Numbers is delivered at input in the binary system: a = 0b00001101'''
   weight = 0
   while x > 0:
      weight += x & 1
      x >>= 1
   return weight

def cl_mult(x, y):
   '''Bitwise carry-less multiplication on integers'''
   z = 0
   i = 0
   while (y >> i) > 0:
      if y & (1 << i):
         z ^= x << i
      i += 1

def bit_length(n):
   '''Compute the position of the most significant bit (1) of an integer. Equivalent to int.bit_length()'''
   bits = 0
   while n >> bits: bits += 1
   return bits

def cl_div(dividend, divisor=None):
   '''Bitwise carry-less long division on integers and returns the remainder'''
   # Compute the position of the most significant bit for each integers
   dl1 = bit_length(dividend)
   dl2 = bit_length(divisor)
   # If the dividend is smaller than the divisor, just exit
   if dl1 < dl2:
      return dividend
   # Else, align the most significant 1 of the divisor to the most significant 1 of the dividend (by shifting the divisor)
   for i in range(dl1 - dl2, -1, -1):
      # Check that the dividend is divisible (useless for the first iteration but important for the next ones)
      if dividend & (1 << i + dl2 - 1):
         # If divisible, then shift the divisor to align the most significant bits and XOR (carry-less subtraction)
         dividend ^= divisor << i
   return dividend

def gf_mult(x, y, prim=0):
   '''Multiplication in Galois Fields by using the standard carry-less multiplication + modular reduction
   using an irreducible prime polynomial'''
    # Multiply the gf numbers
   result = cl_mult(x, y)
   # Then do a modular reduction (ie, remainder from the division) with an irreducible primitive polynomial so that it stays inside GF bounds
   if prim > 0:
      result = cl_div(result, prim)

   return result