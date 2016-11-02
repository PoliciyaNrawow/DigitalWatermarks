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


def gf_poly_scale(p,x):
    '''Multiplies a polynomial by a scalar.'''
    r = [0] * len(p)
    for i in range(0, len(p)):
        r[i] = gf_mul(p[i], x)
    return r

def gf_poly_add(p,q):
    '''Polynomial additional'''
    r = [0] * max(len(p),len(q))
    for i in range(0,len(p)):
        r[i+len(r)-len(p)] = p[i]
    for i in range(0,len(q)):
        r[i+len(r)-len(q)] ^= q[i]
    return r

def gf_poly_mul(p,q):
    '''Multiply two polynomials, inside Galois Field'''
    # Pre-allocate the result array
    r = [0] * (len(p)+len(q)-1)
    # Compute the polynomial multiplication (just like the outer product of two vectors,
    # we multiply each coefficients of p with all coefficients of q)
    for j in range(0, len(q)):
        for i in range(0, len(p)):
            r[i+j] ^= gf_mul(p[i], q[j]) # equivalent to: r[i + j] = gf_add(r[i+j], gf_mul(p[i], q[j]))
                                                         # -- you can see it's your usual polynomial multiplication
    return r

def gf_poly_eval(poly, x):
    '''Evaluates a polynomial in GF(2^p) given the value for x. This is based on Horner's scheme for maximum efficiency.'''
    y = poly[0]
    for i in range(1, len(poly)):
        y = gf_mul(y, x) ^ poly[i]
    return y

gf_exp = [0] * 512
gf_log = [0] * 256

def init_tables(prim=0x11d):
    '''Precompute the logarithm and anti-log tables for faster computation later, using the provided primitive polynomial.'''
    # prim is the primitive (binary) polynomial. Since it's a polynomial in the binary sense,
    # it's only in fact a single galois field value between 0 and 255, and not a list of gf values.
    global gf_exp, gf_log
    gf_exp = [0] * 512 # anti-log (exponential) table
    gf_log = [0] * 256 # log table
    # For each possible value in the galois field 2^8, we will pre-compute the logarithm and anti-logarithm (exponential) of this value
    x = 1
    for i in range(0, 255):
        gf_exp[i] = x # compute anti-log for this value and store it in a table
        gf_log[x] = i # compute log at the same time
        x = gf_mult_noLUT(x, 2, prim)

        # If you use only generator==2 or a power of 2, you can use the following which is faster than gf_mult_noLUT():
        #x <<= 1 # multiply by 2 (change 1 by another number y to multiply by a power of 2^y)
        #if x & 0x100: # similar to x >= 256, but a lot faster (because 0x100 == 256)
            #x ^= prim # substract the primary polynomial to the current value (instead of 255, so that we get a unique set made of coprime numbers), this is the core of the tables generation

    # Optimization: double the size of the anti-log table so that we don't need to mod 255 to
    # stay inside the bounds (because we will mainly use this table for the multiplication of two GF numbers, no more).
    for i in range(255, 512):
        gf_exp[i] = gf_exp[i - 255]
    return [gf_log, gf_exp]

def gf_mul(x,y):
    if x==0 or y==0:
        return 0
    return gf_exp[gf_log[x] + gf_log[y]] # should be gf_exp[(gf_log[x]+gf_log[y])%255] if gf_exp wasn't oversized

def gf_div(x,y):
    if y==0:
        raise ZeroDivisionError()
    if x==0:
        return 0
    return gf_exp[(gf_log[x] + 255 - gf_log[y]) % 255]

def gf_pow(x, power):
    return gf_exp[(gf_log[x] * power) % 255]

def gf_inverse(x):
    return gf_exp[255 - gf_log[x]] # gf_inverse(x) == gf_div(1, x)



