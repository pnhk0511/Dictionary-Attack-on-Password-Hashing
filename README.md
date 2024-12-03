# Dictionary-Attack-on-Password-Hashing-

Original https://github.com/pnhk0511/Dictionary-Attack-on-Password-Hashing

Change log:

03/12/2024
+Add pbkdf_hash and return hash value\
+Add dictionary_attack_pbkd: Recieve hash value, loop through dictionary to find similar hash.\
+Add Loop_attack_md5: Loop through file contains hashes, and individual run "dictionary_attack" (md5-attack).\
+Add Loop_attack_pbkd: Loop through file contains hashes, and individual run "dictionary_attack_pbkd".\
+Add create_md5_hash_file: create a file that simulate that of a database, in this example hacker has already know about the database.
file will contains many line, each line has a hash value (md5).\
+Add create_pbkd_file: The description is similar to create_md5_hash_file, only different is file format
file will contains many lines, each line has the format "hash"|"salt"