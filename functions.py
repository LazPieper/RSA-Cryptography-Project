def dec_to_bin(n):
    # make sure that n is a positive integer
    assert n >= 0, "Error: n is not greater than or equal to 0."
    # creating an empty list that will acquire each binary digit as we iterate through the number to reach the digit corresponding with 2^0
    binary = []
    # did this to not have to go through any loops should the number simply be 0
    if n == 0:
        binary.append(n)
    while n > 0:
        # doing n mod 2 each iteration to confirm whether the power of 2 of that particular iteration exists in the decimal
        r = n % 2
        # the insert function allows us to place the variable in a specific spot and through each iteration 
        # we'll need to add r to the front of the list the binary number is in order
        binary.insert(0, r)
        # I divide n by 2 here to ensure we continue onto the next iteration and update n appropriately and to avoid an infinite loop
        n = n // 2
    return binary

def fme(a, n, b):
    result = 1
    square = a
    binary_n = dec_to_bin(n)
    # I kept the previous function as a list so it can be used to iterate through each bit for FME
    # I apply the reversed function so the iteration can begin with the lowest bit
    for digit in reversed(binary_n):
        if digit == 1:
            result = (result * square) % b
        square = (square * square) % b
    return result

def gcd(m, n):
    while n > 0:
        # we know that m == m mod n, so we compute that to find the remainder r.
        r = m % n
        '''
        after establishing the remainder, we replace m with n (so that there lies the bigger number that we must reduce) and n to r
        reduces the problem to a smaller pair of numbers while maintaining the same gcd
        '''
        m = n
        n = r
    # once we reach 0, the while loop will terminate and we'll be left with the gcd as m and n as 0
    # so we return m
    return m

def eea(m, n):
    # ensuring that we have m as the greater integer so we are able to distinguish between m and m mod n
    if m < n:
        m, n = n, m
    # ensure we have positive integers for m and n, and stop the function with an error message should that not be the case
    if m < 0 or n < 0:
        raise ValueError("Error: Please input positive integers.")
    # set initial s1, t1 for m and s2, t2 for n
    s1, t1 = 1, 0
    s2, t2 = 0, 1
    while n > 0:
        # calculate quotient and remainder
        # can't use gcd function in this case since we're going to need to iterate through each remainder for the linear equations
        # finding the quotient of m and n and using // to ensure it's an integer (leaving out the remainder) and solving that on its own (r)
        q = m // n
        r = m - q * n
        # m, n to be updated to each iteration of m mod n (r) and shift n to take m and n to take r, so m remains greater
        m, n = n, r
        # to reflect updates to the coefficients and use these variables to update s1 and s2 for each iteration
        s = s1 - q * s2
        t = t1 - q * t2
        s1, t1 = s2, t2
        s2, t2 = s, t
    return m, (s1, t1)

# using brute force primality test p and q since we're not yet dealing with larger numbers
def is_prime(a):
    if a >= 2:
        for i in range(2, a):
            if a % i == 0:
                return False
        return True

'''
ascii defines printable values between 32-126, so n must be greater than 126 for our encryption to work in the encode() and decode() 
functions, because if n is less than any of the ascii values for a letter (as it will be converted in convert_text() and convert_num() 
functions) then the first FME modulo operation will reduce the value before encryption could happen, giving us a different ascii value. 
But if n is greater than 126, then any integer between 32-126 mod n, would come out as the integer itself since it's smaller than n 
which would be accurately tied to the right ascii value
'''
def generate_prime():
    # importing the random module and using its choice function to pick one random integer
    from random import randint
    # creating a loop that will generate a random integer and test its primality, and we'll exit the loop once we hit a prime number
    while True:
        # begin the range at 13 since 13 is the lowest prime number that both p and q can be to have a product over 126
        p = randint(13, 100)
        if is_prime(p):
            break
    while True:
        q = randint(13, 100)
        if is_prime(q):
            break
    return p, q

def find_pub_key_e(p, q):
    n = p * q
    x = (p - 1) * (q - 1) 
    # made an empty list to place all possible e so the function can choose a random one later on
    possible_e = []
    # e can be various numbers so long as it is relatively prime to x 
    # so I set the range from 2 to 10000 (can't be 0 or 1 because nothing would get encrypted)
    for num in range(2, 10000):
        if gcd(x, num) == 1:
            possible_e.append(num)
    # importing the random module and using its choice function to pick one random integer from the list of e's and setting as e
    from random import choice
    e = choice(possible_e)
    return (e, n)

def find_priv_key_d(e, p, q):
    n = p * q
    x = (p - 1) * (q - 1)
    e_mod_x = eea(e, x)
    # here I'm separating (s, t) from the output of EEA in order to set d to s
    bezout = e_mod_x[1]
    # whichever of the two between s, t that is the modular inverse of e, will be assigned to d
    if (e * bezout[0]) % x == 1:
        d = bezout[0]
    elif (e * bezout[1]) % x == 1:
        d = bezout[1]
    else:
        raise ValueError("Neither coefficient is the modular inverse of e.")
    if d < 0:
        d += x
    return d

def convert_text(string):
    integer_list = []
    for char in string:
        integer_list.append(ord(char))
    return integer_list

def convert_num(lst):
    string = ""
    for integer in lst:
        string += chr(integer)
    return string

def encode(n, e, message):
    cipher_text = []
    ascii_msg = convert_text(message)
    for integer in ascii_msg:
        # using the fme() function to more quickly compute the encryption method C = M^e mod n
        encryption = fme(integer, e, n)
        cipher_text.append(encryption)
    return cipher_text

def decode(n, d, cipher_text):
    # set up an empty list that will take in decoded integers and will be used in the convert_num() function to create the message
    decoded_msg = []
    for integer in cipher_text:
        # using the fme() function to more quickly go compute the decryption method M = C^d mod n
        decryption = fme(integer, d, n)
        decoded_msg.append(decryption)
    # once decoded_msg has each of the decoded integers, the program converts the list into a string
    message = convert_num(decoded_msg)
    return message