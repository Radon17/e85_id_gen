import sys

def print_help():
    print("e85_id_gen utility")
    print("Usage:")
    print("  e85_id_gen           # interactive mode")
    print("  e85_id_gen -g        # generate ROM file (interactive)")
    print("  e85_id_gen -c FILE   # check and decode ROM file")
    print("  e85_id_gen -h        # show this help")
    print("\nInteractive mode lets you generate or check ROM files.")

def interleave_zeros(arr):
    out = bytearray()
    for b in arr:
        out.append(b)
        out.append(0x00)
    return out

def deinterleave_zeros(arr):
    return arr[::2]

def calculate_checksum(data_bytes):
    a = 0xFFFF
    words_count = len(data_bytes) // 2
    for i in range(words_count):
        b = data_bytes[2*i] | (data_bytes[2*i + 1] << 8)
        a ^= b
        a = ((a << 1) | (a >> 15)) & 0xFFFF
    return a

def press_enter():
    input("Press Enter to exit...")

FOOTER = bytes.fromhex('00FF55AAFF00AF50')

def generator_flow():
    print("Elektronika MS0585 and DEC PRO ID Number Generator")
    print("")
    while True:
        serial = input("Please enter the serial number (1 to 12 digits): ").strip()
        if serial.isdigit() and 1 <= len(serial) <= 12:
            break
        print("Invalid input. Enter from 1 to 12 digits.")
    xhomer_mode = input("File for Xhomer emulator? (Y/N): ").strip().lower()
    interleave = xhomer_mode == 'y'
    num_str = serial.zfill(12)
    bcd = bytearray((int(num_str[i]) << 4 | int(num_str[i+1])) for i in range(0, 12, 2))[::-1]
    chk = calculate_checksum(bcd)
    chk_bytes = chk.to_bytes(2, "little")
    if interleave:
        bcd = interleave_zeros(bcd)
        chk_bytes = interleave_zeros(chk_bytes)
    sequence = bcd + chk_bytes
    full_bytes = sequence * 3
    footer = FOOTER
    if interleave:
        footer = interleave_zeros(footer)
    final_bytes = full_bytes + footer
    print("\nResulting HEX dump:")
    print(' '.join(f'{b:02X}' for b in final_bytes))
    print(f"Checksum: {chk} (0x{chk:04X})\n")
    if interleave:
        out_name = "id.rom"
        print("Output file name set to 'id.rom' for Xhomer emulator.")
    else:
        while True:
            out_name = input("Enter output filename: ").strip()
            if out_name:
                break
    with open(out_name, 'wb') as f:
        f.write(final_bytes)
    if interleave:
        print(f"\nFile '{out_name}' successfully written.")
        print("Place 'id.rom' in your Xhomer emulator directory.")
    else:
        print(f"\nFile '{out_name}' successfully written.")
        print("You may now proceed to burn this image to the K155RE3 chip.")

def checker_flow(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Failed to open file: {e}\n")
        return
    interleave = all(data[i] == 0 for i in range(1, len(data), 2))
    mode = "Xhomer" if interleave else "E85"
    expected_footer = FOOTER if not interleave else interleave_zeros(FOOTER)
    footer = data[-len(expected_footer):]
    footer_to_show = footer if not interleave else deinterleave_zeros(footer)
    footer_status = "OK" if footer == expected_footer else "INVALID"
    body = data[:-len(expected_footer)]
    seq_len = len(body) // 3
    chunk = body[:seq_len]
    if interleave:
        chunk = deinterleave_zeros(chunk)
    bcd_vals = chunk[:-2]
    crc_bytes = chunk[-2:]
    bcd_vals_rev = bcd_vals[::-1]
    serial_dec = ''.join(f"{b >> 4}{b & 0xF}" for b in bcd_vals_rev)
    crc_expected = calculate_checksum(bcd_vals)
    crc_real = int.from_bytes(crc_bytes, "little")
    crc_status = "OK" if crc_expected == crc_real else "INVALID"
    print("\nROM file analysis:")
    print(f"  Mode: {mode}")
    print(f"  ID: {serial_dec}")
    print(f"  Checksum in ROM: {crc_real} (0x{crc_real:04X})")
    print(f"  Calculated CRC:  {crc_expected} (0x{crc_expected:04X})  [{crc_status}]")
    print(f"  Footer: {footer_to_show.hex().upper()} [{footer_status}]\n")
    if crc_status == "OK" and footer_status == "OK":
        print("File is valid.")
    else:
        print("File integrity or format may be broken!")

### main logic
if len(sys.argv) == 1:
    # Диалоговый режим по умолчанию
    print("e85_id_gen - interactive mode\n")
    print("Choose operation:\n"
          "  [G] Generate new ROM file\n"
          "  [C] Check and decode existing ROM file\n"
          "  [H] Help\n")
    while True:
        choice = input("Enter mode (G/C/H): ").strip().lower()
        if choice in ['g', 'c', 'h']:
            break
        print("Invalid choice. Please type G, C or H.")

    if choice == 'g':
        generator_flow()
        press_enter()
    elif choice == 'c':
        fname = input("Enter ROM filename to check: ").strip()
        checker_flow(fname)
        press_enter()
    elif choice == 'h':
        print_help()
        press_enter()
else:
    arg = sys.argv[1]
    if arg == '-g':
        generator_flow()
    elif arg == '-c':
        if len(sys.argv) < 3:
            print("Specify filename for checking!\n")
            print_help()
            sys.exit(1)
        checker_flow(sys.argv[2])
    elif arg == '-h':
        print_help()
    else:
        print_help()
        sys.exit(1)