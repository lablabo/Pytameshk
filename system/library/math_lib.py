import random

class controller:

    def __init__(self, register):
        pass

    def generate_prime(self, N=10**8, bases=range(2,20000)):
        p = 1
        while any(pow(base, p-1, p) != 1 for base in bases):
            p = random.SystemRandom().randrange(N)
        return p

    def multiplicative_inverse(self, modulus, value):
        # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        x, lastx = 0, 1
        a, b = modulus, value
        while b:
            a, q, b = b, a // b, a % b
            x, lastx = lastx - q * x, x
        result = (1 - lastx * modulus) // value
        return result + modulus if result < 0 else result

    def public_private_keys(self, N = 2**64):
        '''Generate public and private keys from primes up to N.

            >>> pubkey, privkey = keygen(2**64)
            >>> msg = 123456789012345
            >>> coded = pow(msg, 65537, pubkey)
            >>> plain = pow(coded, privkey, pubkey)
            >>> assert msg == plain

        '''
        # http://en.wikipedia.org/wiki/RSA
        prime1 = self.generate_prime(N)
        prime2 = self.generate_prime(N)
        totient = (prime1 - 1) * (prime2 - 1)
        return prime1 * prime2, self.multiplicative_inverse(totient, 65537)
