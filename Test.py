import math

def find_m(a, b, x):
    # factorize A and B into their prime factors
    factors_a = prime_factors(a)
    factors_b = prime_factors(b)
    
    # find the intersection of the prime factors of A and B
    common_factors = set(factors_a).intersection(set(factors_b))
    m = 1
    
    # multiply the common factors together to get a potential value of M
    for factor in common_factors:
        m *= factor
    
    # find the GCD of the potential M and X
    gcd = math.gcd(m, x)
    
    if gcd != 1:
        # there is no solution for M
        return None
    
    # check if the potential M satisfies the equation
    if (a * b) % m == x:
        # found the correct value of M
        return m
    
    # continue searching for other potential values of M
    for factor in factors_a:
        if factor not in common_factors:
            m *= factor
            gcd = math.gcd(m, x)
            if gcd != 1:
                # there is no solution for M
                return None
            if (a * b) % m == x:
                # found the correct value of M
                return m
    
    # no solution found
    return None
    
def prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

a = 115792089237316195423570985008687907852837564279074904382605163141518161494336
b = 40360748372915677739060455046407153445907911874643188801639465548522
x = 55066263021366149949932944254155024514247492615142308993872983365411851378577

m = find_m(a, b, x)
if m is None:
    print("No solution found")
else:
    print("M =", m)