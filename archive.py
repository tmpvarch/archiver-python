from collections import Counter

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

def build_huffman_tree(char_freq):
    queue = [(freq, Node(char, freq)) for char, freq in char_freq.items()]
    while len(queue) > 1:
        queue.sort(key=lambda x: x[0])  # Use a custom sorting function
        freq1, node1 = queue.pop(0)
        freq2, node2 = queue.pop(0)
        queue.append((freq1+freq2, Node(None, freq1+freq2, node1, node2)))
    _, root = queue[0]
    return root

def generate_huffman_codes(root, code=''):
    if root is None:
        return {}
    if root.char is not None:
        return {root.char: code}
    codes = {}
    codes.update(generate_huffman_codes(root.left, code + '0'))
    codes.update(generate_huffman_codes(root.right, code + '1'))
    return codes

def encode_huffman(codes, text):
    return ''.join(codes[char] for char in text if char in codes)

def decode_huffman(root, encoded_text):
    decoded_text = ''
    node = root
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        elif bit == '1':
            node = node.right
        if node and node.char is not None:
            decoded_text += str(chr(node.char))  # Convert node.char to a string
            node = root
    return decoded_text

def main():
    with open('file.txt', 'rb') as f:
        data = f.read()
    char_freq = Counter(data)
    root = build_huffman_tree(char_freq)
    codes = generate_huffman_codes(root)
    encoded_text = encode_huffman(codes, data)
    decoded_text = decode_huffman(root, encoded_text)
    with open('encoded_file.txt', 'wb') as f:
        f.write(encoded_text.encode())
        print('File has been encoded and saved as encoded_file.txt')
    with open('decoded_file.txt', 'wb') as f:
        f.write(decoded_text.encode())
        print('File has been decoded and saved as decoded_file.txt')


if __name__ == "__main__":
    main()