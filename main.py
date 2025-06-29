from functions import *

def main():
    # giving the user the option of either encrypting or decrypting by using the input() function
    instruction = input("Enter 'E' to encrypt or 'D' to decrypt.")
    # this if statement checks to see if the user requested to encrypt by setting the condition to equaling "E" or "e"
    if instruction == "E" or instruction == "e":
        # requires the user to input their message and saves to the variable txt taht will be used for encoding
        txt = input("Please enter your message.")
        p, q = generate_prime()
        e, n = find_pub_key_e(p, q)
        d = find_priv_key_d(e, p, q)
        cipher = encode(n, e, txt)
        # these print statements are meant for the user to hold onto their public and private keys in order to decrypt later
        print("Encrypted message: " + str(cipher))
        print("Your public key: e = " + str(e) + " n = " + str(n))
        print(" Your private key: d = " + str(d))
    # this if statement checks to see if the user requested to decrypt by setting the condition to equaling "D" or "d"   
    elif instruction == "D" or instruction == "d":
        # the user then has to input d, n, and their encoded message so that the decoding function can be used, which they
        # received when encrypting their message
        d = int(input("Please provide your private key, d."))
        n = int(input("Please provide n."))
        cipher = input("Please enter encrypted message with commas and no brackets.")
        # because the user input a string for their cipher and we can't convert it into an integer list with the int() function
        # we need to iterate and split each integer and place them into a list to use for the decode function
        cipher_lst = []
        for num in cipher.split(","):
            cipher_lst.append(int(num))
        txt = decode(n, d, cipher_lst)
        print("Decrypted message: " + txt)
    # added a ValueError in case the user fails to follow the input instructions at the beginning
    else:
        raise ValueError("Must enter 'E' or 'D'")

# use for when importing the file containing the main() function
if __name__ == "__main__":
    main()