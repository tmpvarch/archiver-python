from collections import Counter

class Node:
    def __init__(self, char, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __iter__(self):
        return self

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(self.__class__.__name__, self.char, self.freq, self.left, self.right)


def generate_file(name: str, content):
    with open(name + '.txt', 'wb') as f:
        f.write(content)
        print('File has been encoded and saved as', name + '.txt')

def build_huffman_tree(char_freq):
    queue = [(freq, Node(char, freq)) for char, freq in char_freq.items()]
    while len(queue) > 1:
        with open('roots.txt', 'wb') as f:
            queue.sort(key=lambda x: x[0])  # Use a custom sorting function
            freq1, node1 = queue.pop(0)
            freq2, node2 = queue.pop(0)
            queue.append((freq1+freq2, Node(None, freq1+freq2, node1, node2)))
            _, root = queue[0]
            f.write(str(root).encode())
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
    string = ''.join(codes[char] for char in text if char in codes)
    generate_file('encoded_file', string.encode())

def read_nodes(file):
    with open(file, 'r') as f:
        return eval(f.read())

def read_encoded_file(file):
    with open(file, 'r') as f:
        return f.read()

def decode_huffman(root, encoded_text):
    encoded_text = encoded_text
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
    generate_file('decoded_file', decoded_text.encode())

def main():
    with open('file.txt', 'rb') as f:
        data = f.read()
    char_freq = Counter(data)
    root = build_huffman_tree(char_freq)
    codes = generate_huffman_codes(root)
    encode_huffman(codes, data)
    decode_huffman(read_nodes('roots.txt'), read_encoded_file('encoded_file.txt'))


if __name__ == "__main__":
    main()