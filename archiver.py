from collections import Counter

class Tree:
    # Инициализация узла древа: символ, код символа, левая и правая ветви древа
    def __init__(self, char, code=0, left=None, right=None):
        self.char = char
        self.code = code
        self.left = left
        self.right = right

    # Возвращает сам объект для итератора
    def __iter__(self):
        return self

    # Вовзращает текстовое представление объекта/сущности в определенном формате
    # Пример: Tree(None, 11, Tree(None, 4, Tree(None, 2, None, None))
    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format \
            (self.__class__.__name__, self.char, self.code, self.left, self.right)


# Генерация текстового файла
def write_file(filename: str, data):
    with open(filename + '.txt', 'wb') as f:
        f.write(data)
        print('Данные были сохранены в файл', filename + '.txt')

# Чтение файла для динамического исполнения содержимового в файле
# Пример: eval("2 + 2") -> Вывод: 4
def eval_read_file(filename):
    with open(filename, 'r') as f:
        return eval(f.read())

# Постройка древа Хаффмана
def build_huffman_tree(frequencies):
    tree = None
    queue = [(code, Tree(char, code)) for char, code in frequencies.items()]
    while len(queue) > 1:
        queue.sort(key=lambda x: x[0])
        code1, node1 = queue.pop(0)
        code2, node2 = queue.pop(0)
        queue.append((code1 + code2, Tree(None, code1 + code2, node1, node2)))
        _, tree = queue[0]
    write_file('tree', str(tree).encode())
    return tree

# Сопоставление двоичного кода и символов
def get_codes(tree, code=''):
    if tree is None:
        return {}
    if tree.char is not None:
        return {tree.char: code}
    codes = {}
    codes.update(get_codes(tree.left, code + '0'))
    codes.update(get_codes(tree.right, code + '1'))
    return codes

# Функция кодирования данных
def encode_file(codes, data):
    encoded_data = ''.join(codes[char] for char in data if char in codes)
    write_file('encoded_file', encoded_data.encode())

# Функция декодирования данных
def decode_file(tree, encoded_data):
    encoded_data = str(encoded_data)
    decoded_data = ''
    node = tree
    for bit in encoded_data:
        if bit == '0':
            node = node.left
        elif bit == '1':
            node = node.right
        if node and node.char is not None:
            decoded_data += str(chr(node.char))
            node = tree
    write_file('decoded_file', decoded_data.encode())

# Функция input() с проверкой
def check_input(key, message=''):
    if key == 'ENTRY':
        while True:
            action = input('Выберите действие:\n1 - архивировать\n2 - разархивировать\nq - закрыть программу\nВвод: ')
            if action not in ['1', '2', 'q']:
                print('Неверное действие, попробуйте еще раз\n')
            else:
                return action
    if key == 'FILE':
        while True:
            try:
                file = input(message)
                # проверяем на ошибку
                open(file)
            except FileNotFoundError:
                print('Файл не найден, повторие ввод\n')
            else:
                return file

# Основной код программы
def main():
    while True:
        option = check_input('ENTRY')
        if option == '1':
            source_file = check_input('FILE', 'Введите название файла, который вы хотите архивировать: ')
            with open(source_file, 'rb') as f:
                data = f.read()
            # Функция Counter(), импортированная из модуля collections,
            # помогает считать частоту символов
            frequencies = Counter(data)
            huffman_tree = build_huffman_tree(frequencies)
            codes = get_codes(huffman_tree)
            encode_file(codes, data)
        if option == '2':
            encoded_file = check_input('FILE', 'Введите назваине файла, который вы хотите разархивировать: ')
            tree_file = check_input('FILE', 'Введите название файла с древом Хаффмана: ')
            decode_file(eval_read_file(tree_file), eval_read_file(encoded_file))
        if option == 'q':
            exit()
        print('\n')


if __name__ == "__main__":
    main()