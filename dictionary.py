import hashlib
import secrets  # For secrets.token_hex(8)


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
                for hash_value in common_hashes:
                    print(
                        f"  - Hash: {hash_value}, Password: {my_passwords[hash_value]}"
                    )
            else:
                print("[FAILED] No common hashed passwords found.")

            if unique_hashes:
                print("[INFO] Unique hashed passwords in your file:")
                for hash_value in unique_hashes:
                    print(
                        f"  - Hash: {hash_value}, Password: {my_passwords[hash_value]}"
                    )
            else:
                print("[INFO] No unique hashed passwords in your file.")

            return common_hashes, unique_hashes
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return None, None


######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
def pbkdf_hash(word, salt, loop):
    return hashlib.pbkdf2_hmac(
        "sha256", str.encode(word.strip()), str.encode(salt.strip()), loop
    ).hex()


def dictionary_attack_pbkd(target_hash, dictionary_file, salt, loop):
    """Perform a dictionary attack to find the password matching the hash."""
    try:
        with open(
            dictionary_file, "r", encoding="latin-1"
        ) as file:  # latin-1 handles special characters in rockyou.txt
            for word in file:
                hashed_word = pbkdf_hash(word, salt, loop)
                if hashed_word == target_hash:
                    print(f"[SUCCESS] Password found: {word.strip()}")
                    return word
        print("[FAILED] Password not found in dictionary.")
        return None
    except FileNotFoundError:
        print(f"[ERROR] Dictionary file '{dictionary_file}' not found.")
        return None


def Loop_attack_md5(my_file_origin, dictionary_file_origin):
    try:
        with open(my_file_origin, "r", encoding="latin-1") as my_file:
            for i, line in enumerate(my_file):
                ans = dictionary_attack(line.strip(), dictionary_file_origin)
                if ans != None:
                    print(f"Find at index: {i}")
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return None, None


def Loop_attack_pbkd(my_file_origin, dictionary_file_origin, loop):
    try:
        with open(my_file_origin, "r", encoding="latin-1") as my_file:
            for i, line in enumerate(my_file):
                ans = dictionary_attack_pbkd(
                    line[:64], dictionary_file_origin, line[65:], loop
                )
                if ans != None:
                    print(f"Find at index: {i}")
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return None, None


def create_md5_hash_file(original_file, goal_file):
    try:
        with open(original_file, "r", encoding="latin-1") as original, open(
            goal_file, "w", encoding="latin-1"
        ) as goal:
            firt_line = True
            for line in original:
                if firt_line == False:
                    goal.write("\n")
                goal.write(md5_hash(line.strip()))
                firt_line = False
    except FileNotFoundError as e:
        print("f[ERROR] File not found: {e}")
        return None, None


def create_pbkd_file(original_file, goal_file, loop):
    try:
        with open(original_file, "r", encoding="latin-1") as original, open(
            goal_file, "w", encoding="latin-1"
        ) as goal:
            firt_line = True
            for line in original:
                if firt_line == False:
                    goal.write("\n")
                random_string = secrets.token_hex(8)
                goal.write(pbkdf_hash(line, random_string, loop))
                goal.write("|")
                goal.write(random_string)
                firt_line = False
            dummy = 1
    except FileNotFoundError as e:
        print("f[ERROR] File not found: {e}")
        return None, None


# Sample usage
if __name__ == "__main__":
    # Target hash to crack (hash of 'password123' as an example)
    print("###Example of a dictionary attack on 1 hash - md5###")
    target_password = "1234"
    target_hash = md5_hash(target_password)
    print(f"Target Hash: {target_hash}")

    # Path to the rockyou.txt file
    # dictionary_file = "/Users/ben/Documents/GitHub/Dictionary-Attack-on-Password-Hashing/rockyou.txt"  # Update with your file path
    dictionary_file = "rockyou.txt"
    # Run the dictionary attack
    found_password = dictionary_attack(target_hash, dictionary_file)

    # if found_password:
    # print(f"The cracked password is: {found_password}")
    # else:
    # print("No matching password found.")

    # Path to your password file
    # my_password_file = "/Users/ben/Documents/GitHub/Dictionary-Attack-on-Password-Hashing/pass.txt"  # Update with your file path
    my_password_file = "pass.txt"
    # Compare passwords in your file with rockyou.txt
    compare_files(my_password_file, dictionary_file)
    ###################################################################
    print("###Example of a dictionary attack on list of hashes - md5###")
    db1 = "db1_md5.txt"
    create_md5_hash_file(my_password_file, db1)

    Loop_attack_md5(db1, dictionary_file)

    print("###Example of a dictionary attack on 1 hash - pbkdf###")
    target_password = "1234"
    salt = "salt"
    target_hash = pbkdf_hash(target_password, salt, 1)
    print(f"Target Hash: {target_hash}")
    found_password = dictionary_attack_pbkd(target_hash, dictionary_file, salt, 1)

    print("###Example of a dictionary attack on list of hashes - pbkdf###")
    db2 = "db2_pbkdf.txt"
    create_pbkd_file(my_password_file, db2, 1)
    Loop_attack_pbkd(db2, dictionary_file, 1)
