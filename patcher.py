# IPS patching tool written by Wil Steadman

# More info about IPS format available below:
# https://zerosoft.zophar.net/ips.php

import sys
import os.path

def apply_patch(patch, to_patch, output, verbose=False):
    with open(patch, "rb") as patch, open(to_patch, "rb") as to_patch, open(output, "wb") as output:
        output.write(to_patch.read())  # Preserves original binary file

        # Applies the patch

        if patch.read(5) != b"PATCH":   # Each IPS file begins with PATCH
            print("[X] Invalid header")
            return

        if verbose:
            print("[+] Valid header found")

        while True:
            offset = int.from_bytes(patch.read(3), byteorder="big")  # Where to write in the binary file

            if offset == 4542278:   # 0x454F46, or EOF
                if verbose:
                    print("[+] Patching complete")
                return

            size = int.from_bytes(patch.read(2), byteorder="big")    # Size of the overwrite block

            if not size:   # Zero size signals an RLE patch
                rle_size = int.from_bytes(patch.read(2), byteorder="big")    # Repetition of byte
                rle_byte = patch.read(1)    # Byte to be repeated

                output.seek(offset) # Moves to specified position

                for i in range(rle_size):
                    output.write(rle_byte)

                if verbose:
                    print("[*] Wrote RLE patch of length {} to offset {}".format(
                        size,
                        hex(offset)
                    ))

            else:   # Normal patch routine
                payload = patch.read(size)

                output.seek(offset)
                output.write(payload)

                if verbose:
                    print("[*] Wrote patch of length {} to offset {}".format(
                        size,
                        hex(offset)
                    ))

# Commandline logic

if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage: {} [-vh] <patch> <file> <output>".format(sys.argv[0]))

    else:
        assert (os.path.isfile(sys.argv[1]) is True), "Patch file doesn't exist"
        assert (os.path.isfile(sys.argv[2]) is True), "Binary file doesn't exist"

        verbose = ("-v" in sys.argv) or ("--verbose" in sys.argv)

        apply_patch(sys.argv[1], sys.argv[2], sys.argv[3], verbose=verbose)
