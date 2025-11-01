# DNS server that computes Rule 110 cellular automaton
# Because someone had to ask "can DNS be Turing complete?"
# Spoiler: maybe? but maybe not

import socket
import struct
import hashlib

RULE_110 = {
    "111": "0", "110": "1", "101": "1", "100": "0",
    "011": "1", "010": "1", "001": "1", "000": "0"
}

def hash_to_initial_state(domain, width=60):
    h = hashlib.md5(domain.encode()).hexdigest()
    binary = bin(int(h[:8], 16))[2:].zfill(32)
    padding = (width - len(binary)) // 2
    return '0' * padding + binary + '0' * (width - padding - len(binary))

def rule110_step(state):
    padded = '0' + state + '0'
    return ''.join(RULE_110[padded[i:i+3]] for i in range(len(state)))

def compute_rule110(domain, generations=10):
    state = hash_to_initial_state(domain)
    result = []
    for gen in range(generations):
        visual = state.replace('0', ' ').replace('1', '█')
        result.append(f"Gen {gen:2d}: {visual}")
        state = rule110_step(state)
    return '\n'.join(result)

def parse_query(data):
    transaction_id = struct.unpack('>H', data[0:2])[0]
    position = 12
    domain = ""
    while data[position] != 0:
        length = data[position]
        position += 1
        label = data[position:position+length].decode('utf-8')
        domain += label + '.'
        position += length
    return domain[:-1] if domain else "", transaction_id

def build_response(query_data, answer):
    response = bytearray()
    response.extend(query_data[0:2])
    response.extend([0x81, 0x80])
    response.extend([0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])

    position = 12
    while query_data[position] != 0:
        length = query_data[position]
        if (length & 0xC0) == 0xC0:
            position += 2
            break
        position += length + 1
    if query_data[position] == 0:
        position += 1
    position += 4
    response.extend(query_data[12:position])

    response.extend([0xC0, 0x0C, 0x00, 0x10, 0x00, 0x01])
    response.extend([0x00, 0x00, 0x00, 0x3C])

    answer_bytes = answer.encode('utf-8')
    chunks = [answer_bytes[i:i+255] for i in range(0, len(answer_bytes), 255)]
    data_length = sum(len(chunk) + 1 for chunk in chunks)
    response.extend(struct.pack('>H', data_length))

    for chunk in chunks:
        response.append(len(chunk))
        response.extend(chunk)

    return bytes(response)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5454))

    print("DNS + Rule 110 server running on port 5454")
    print("Query any domain to see Rule 110 computation!")
    print("Example: dig @localhost -p 5454 example.com TXT\n")

    try:
        while True:
            data, address = sock.recvfrom(512)
            domain, _ = parse_query(data)
            computation = compute_rule110(domain, generations=5)
            response = build_response(data, computation)
            sock.sendto(response, address)

            print(f"Query: {domain}")
            print(computation)
            print("-" * 70)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        sock.close()

if __name__ == '__main__':
    main()