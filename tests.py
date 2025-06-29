from functions import *

# testing fme
def fme_sample(a, n, b):
    result = 1
    square = a
    binary_n = dec_to_bin(n)
    print("result = ({} * {}) % {}".format(result, square, b))
    for digit in reversed(binary_n):
        if digit == 1:
            result = (result * square) % b
            print("{} = ({} * {}) % {}".format(result, result, square, b))
        square = (square * square) % b
    return result

test1 = fme_sample(105, 7, 100)
print(" ")
test2 = fme_sample(105, 7, 128)

# code break
def factorize(n):
    for i in range(2, n - 1):
        if n % i == 0:
            return i
    return False

def code_break(n, e, cipher):
    p = factorize(n)
    q = n // p
    d = find_priv_key_d(e, p, q)
    decoded_txt = decode(n, d, cipher)
    return decoded_txt

# sample 1
p, q = generate_prime()
e, n = find_pub_key_e(p, q)
print(e, n)
message1 = "I don't speak, I operate a machine called language. It creaks and groans, but is mine own."
cipher_text1 = encode(n, e, message1)
print(cipher_text1)
codebreak = code_break(n, e, cipher_text1)
print(codebreak)

#sample 2
p, q = generate_prime()
e, n = find_pub_key_e(p, q)
print(e, n)
message2 = "The vision of time is broad, but when you pass through it, time becomes a narrow door."
cipher_text2 = encode(n, e, message2)
print(cipher_text2)
# Testing factorize() function
codebreak = code_break(n, e, cipher_text2)
print(codebreak)

# sample 3
p, q = generate_prime()
e, n = find_pub_key_e(p, q)
print(e, n)
message3 = "To see eternity was to be exposed to eternity's whims, oppressed by endless dimensions."
cipher_text3 = encode(n, e, message3)
print(cipher_text3)
codebreak = code_break(n, e, cipher_text3)
print(codebreak)