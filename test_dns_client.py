# test client for the dns server

import socket
import struct

def create_dns_query(domain, transaction_id=0xAABB):
    packet = bytearray()
    packet.extend(struct.pack('>H', transaction_id))
    packet.extend([0x01, 0x00])
    packet.extend([0x00, 0x01])
    packet.extend([0x00, 0x00])
    packet.extend([0x00, 0x00])
    packet.extend([0x00, 0x00])

    for label in domain.split('.'):
        packet.append(len(label))
        packet.extend(label.encode('utf-8'))
    packet.append(0)

    packet.extend([0x00, 0x10])
    packet.extend([0x00, 0x01])

    return bytes(packet)

def parse_dns_response(data):
    trans_id = struct.unpack('>H', data[0:2])[0]
    num_answers = struct.unpack('>H', data[6:8])[0]

    print(f"Transaction ID: 0x{trans_id:04x}")
    print(f"Number of answers: {num_answers}")

    if num_answers == 0:
        return "No answers"

    for i in range(len(data) - 20):
        if data[i:i+2] == b'\xC0\x0C' and data[i+2:i+4] == b'\x00\x10':
            txt_start = i + 12
            txt_length = data[txt_start]
            txt_data = data[txt_start + 1:txt_start + 1 + txt_length].decode('utf-8')
            return txt_data

    return "Could not parse TXT record"

def query_dns(domain, server='127.0.0.1', port=5454):
    print(f"\n{'='*60}")
    print(f"Querying: {domain}")
    print(f"Server: {server}:{port}")
    print('='*60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    try:
        query = create_dns_query(domain)
        print(f"\nSending query ({len(query)} bytes)...")

        sock.sendto(query, (server, port))

        print("Waiting for response...")
        response, addr = sock.recvfrom(512)
        print(f"✓ Received response ({len(response)} bytes)")

        print("\nParsing response:")
        answer = parse_dns_response(response)

        print(f"\n{'='*60}")
        print("ANSWER:")
        print(f"  {answer}")
        print('='*60)

    except socket.timeout:
        print("ERROR: Query timed out")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    query_dns('google.com')
    query_dns('example.com')
    query_dns('test.rule110.com')
