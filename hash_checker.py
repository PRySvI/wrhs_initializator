import hashlib
import os

import csv

all_hashes = dict()
valid_hashes = dict()


def load_hashes():
    try:
        with open('hashes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                all_hashes[row['filename']] = row['hash']
    except:
        pass


load_hashes()


def verify_and_get_hash(filename: str):
    print(f'\t verify hash: of {filename}')
    last_hash = load_last_file_hash(filename)
    new_file_hash = calc_file_hash(filename)
    if last_hash is not None and last_hash == new_file_hash:
        raise Exception(
            f'file: ${filename} is not updated!!! You use already used csv \t change your ${filename} or remove hashes.csv')
    valid_hashes[filename] = new_file_hash


def load_last_file_hash(filename: str):
    try:
        hashValue = all_hashes[filename]
    except KeyError as e:
        hashValue = None
    return hashValue


def calc_file_hash(filename: str):
    hashValue = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    return hashValue


def write_hashes():
    with open('hashes.csv', 'w', newline='') as csvfile:
        fieldnames = ['filename', 'hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename, hash_row in valid_hashes.items():
            writer.writerow({'filename': filename, 'hash': hash_row})
