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
