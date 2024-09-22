def parse_data(binary_data):
    decoded_strings = []
    current_string = b""
    for byte in binary_data:
        if byte == 0:
            if current_string:
                try:
                    decoded_strings.append(current_string.decode("utf-8"))
                except UnicodeDecodeError:
                    pass
                current_string = b""
        else:
            current_string += bytes([byte])
    strings = [s[1:] for s in decoded_strings]
    filtered_strings = [s for s in strings if s != '']
    return filtered_strings