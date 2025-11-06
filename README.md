
# e85_id_gen

**Elektronika MS0585 and DEC PRO ID ROM Generator and Checker**

Utility for generating and analyzing ID ROM files for DEC PRO and it's soviet clone Elektronika 85.

---

## Features

- Interactive mode and command-line support
- Generates ROM files with user-defined serial numbers (1–12 digits, leading zeros kept)
- Supports plain and Xhomer emulator (interleaved) formats
- Triplicates core data block, appends special 8-byte footer
- checksum (hardware-compatible algorithm)
- Checks/analyzes ROM files, autodetects format, validates content
- Checks format's signature footer
- Friendly for burning into К155РЕ3 chip or using with Xhomer

---

## Usage

### Interactive Mode (by default)

```sh
python e85_id_gen.py
```

### Command Line Options

- `-g`&emsp;&emsp;Generate ROM file (interactive)
- `-c FILE`&emsp;Check and decode existing ROM file
- `-h`&emsp;&emsp;Show help

---

### Generate new ROM file

```sh
python e85_id_gen.py -g
```

* You will be prompted for:
  - Serial number (1–12 digits, zeros allowed)
  - Xhomer emulator format (Y/N)
  - Output file name (`id.rom` used for Xhomer automatically)

---

### Check / Decode ROM file

```sh
python e85_id_gen.py -c myrom.bin
```
* Auto-detects format (plain/Xhomer)
* Shows serial number (all 12 digits), checksum, validates CRC, and shows footer correctness

---

### Show Help

```sh
python e85_id_gen.py -h
```

---

## File Structure

- **BCD ID:** 12 digits (leading zeros preserved), stored as 6 BCD bytes (little-endian order)
- **Checksum (2 bytes):** Calculated from BCD bytes (little-endian; see PDP-11-compatible rotate-XOR algorithm)
- **(Xhomer mode)**: each data byte (including checksum) is interleaved with 0x00
- **Block repeated 3 times**
- **Footer:** 8 bytes:  
  - Always `00FF55AAFF00AF50` (also interleaved if Xhomer)
- **Total file size:**  
  - E85: 32 bytes  
  - Xhomer: 64 bytes

---

## Example Session

**Interactive:**

```sh
python e85_id_gen.py
```
```
e85_id_gen - interactive mode

Choose operation:
  [G] Generate new ROM file
  [C] Check and decode existing ROM file
  [H] Help

Enter mode (G/C/H): g
Elektronika MS0585 and DEC PRO ID Number Generator

Please enter the serial number (1 to 12 digits): 0004711
File for Xhomer emulator? (Y/N): n
Enter output filename: myrom.bin

Resulting HEX dump:
15 47 00 00 00 00 00 00 00 00 00 00 62 12 ... 00FF55AAFF00AF50
Checksum: 47074 (0xB802)

File 'myrom.bin' successfully written.
You may now proceed to burn this image to the K155RE3 chip.
Press Enter to exit...
```

---

**Check/Decode existing file:**

```sh
python e85_id_gen.py -c id.rom
```
```
ROM file analysis:
  Mode: Xhomer
  ID: 000000004711
  Checksum in ROM: 47074 (0xB802)
  Calculated CRC:  47074 (0xB802)  [OK]
  Footer: 00FF55AAFF00AF50 [OK]
File is valid.
```

---

## Compatibility / Burning

- Use Xhomer-format files directly with the emulator.
- For real MS0585/DEC hardware, burn with your programmer to the К155РЕ3 chip.

---

## Building & Running

- **No build required**
- Needs **Python 3** (no extra modules).
- Run as described above.

---

## License

MIT License. Use, modify, and share freely.

---

## Authors

For retrocomputing, DEC, and PDP-11 enthusiasts everywhere.  
Issues and pull requests welcome!

---

**Enjoy emulation and real hardware fun!**
