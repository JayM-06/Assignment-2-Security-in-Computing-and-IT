import os

# Making sure the file path is able to work on all os
BASE = os.path.dirname(os.path.abspath(__file__))

# Ensure the keys directory exists
keys_dir = os.path.join(BASE, 'keys')
os.makedirs(keys_dir, exist_ok=True)

def is_prime(n):
    if n < 2:
        return False
    
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
        
    return True

while True:
    try:
        p = int(input("Enter a prime number (5 or more digits): "))
        
        if len(str(p)) < 5:
            print("Error: The number must have at least 5 digits.")    
        elif not is_prime(p):
            print("Error: The number is not prime.")
        else:
            print("Valid prime number:", p)
            break

    except ValueError:
        print("Error: Please enter a whole number.")

while True:
    try:
        q = int(input("Enter prime number q (5 or more digits): "))

        if len(str(q)) < 5:
            print("Number must have at least 5 digits.")
        elif not is_prime(q):
            print("Number is not prime.")
        elif q == p:
            print("q must be different from p.")
        else:
            break

    except ValueError:
        print("Please enter a whole number.")


print("p =", p)
print("q =", q)

n = p * q
ntotient = (p-1)*(q-1)

# Put these up with is_prime(), outside any loop
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# ... after computing n and ntotient:
print("n =", n)
print("phi(n) =", ntotient)

def is_valid_e(e, ntotient):
    return 1 < e < ntotient and gcd(e, ntotient) == 1

while True:
    try:
        e = int(input("Please enter a valid e: "))

        if is_valid_e(e, ntotient):
            print("Valid e:", e, "with gcd(e, phi(n)) = 1")
            break
        else:
            print("Invalid e. It must satisfy 1 < e < phi(n) and gcd(e, phi(n)) = 1.")

    except ValueError:
        print("Please enter a whole number.")

        
def mod_inverse(e, ntotient):
    return pow(e, -1, ntotient)

d = mod_inverse(e, ntotient)

print("Check: (e * d) mod phi(n) =", (e * d) % ntotient)   # must print 1


while True:
    try:
        user_input_msg = int(input("Enter valid student ID: "))

        if len(str(user_input_msg)) != 7:
            print("Student ID must have 7 digits.")
        else:
            break

    except ValueError:
        print("Please enter a whole number.")

print("Ciphertext = ", pow (user_input_msg, e, n))