import hashlib


def md5_hash(word):
    """Generate the MD5 hash of a word."""
    return hashlib.md5(word.encode()).hexdigest()


def dictionary_attack(target_hash, dictionary_file):
    """Perform a dictionary attack to find the password matching the hash."""
    try:
        with open(
            dictionary_file, "r", encoding="latin-1"
        ) as file:  # latin-1 handles special characters in rockyou.txt
            for word in file:
                word = word.strip()  # Remove whitespace and newlines
                hashed_word = md5_hash(word)
                if hashed_word == target_hash:
                    print(f"[SUCCESS] Password found: {word}")
                    return word
        print("[FAILED] Password not found in dictionary.")
        return None
    except FileNotFoundError:
        print(f"[ERROR] Dictionary file '{dictionary_file}' not found.")
        return None


def compare_files(my_file, dictionary_file):
    """Compare hashed passwords and their plaintext equivalents."""
    try:
        with open(my_file, "r", encoding="latin-1") as my_file, open(
            dictionary_file, "r", encoding="latin-1"
        ) as dict_file:
            my_passwords = {md5_hash(line.strip()): line.strip() for line in my_file}
            dict_passwords = {
                md5_hash(line.strip()): line.strip() for line in dict_file
            }

            common_hashes = my_passwords.keys() & dict_passwords.keys()
            unique_hashes = my_passwords.keys() - dict_passwords.keys()

            if common_hashes:
                print("[SUCCESS] Common hashed passwords found:")
                for hash_val in common_hashes:
                    print(f"  - Hash: {hash_val}, Password: {my_passwords[hash_val]}")
            else:
                print("[FAILED] No common hashed passwords found.")

            if unique_hashes:
                print("[INFO] Unique hashed passwords in your file:")
                for hash_val in unique_hashes:
                    print(f"  - Hash: {hash_val}, Password: {my_passwords[hash_val]}")
            else:
                print("[INFO] No unique hashed passwords in your file.")

            return common_hashes, unique_hashes
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return None, None


# Sample usage
if __name__ == "__main__":
    # Target hash to crack (hash of 'password123' as an example)
    target_password = "hiiii"
    target_hash = md5_hash(target_password)
    print(f"Target Hash: {target_hash}")

    # Path to the rockyou.txt file
    dictionary_file = (
        "E:/study/sem 5/Cryptography/rockyou.txt"  # Update with your file path
    )

    # Run the dictionary attack
    found_password = dictionary_attack(target_hash, dictionary_file)

    if found_password:
        print(f"The cracked password is: {found_password}")
    else:
        print("No matching password found.")

    # Path to your password file
    my_password_file = (
        "E:/study/sem 5/Cryptography/pass.txt"  # Update with your file path
    )

    # Compare passwords in your file with rockyou.txt
    compare_files(my_password_file, dictionary_file)
