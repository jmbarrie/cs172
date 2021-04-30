class TermInfo: 
    def __init__(self, files):
        self.term_index_file = files[0]
        self.term_info_file = files[1]
        self.term_info = {}

    def create_term_info_dict(self):
        with open('./data/term_index.txt', 'r') as f:
            offset = f.tell()
            for line in iter(f.readline, ''):
                line_list = line.strip().split('\t')
                total_frequency = len(line_list) - 1
                doc_set = set()
                for item in line_list[1:]:
                    doc_set.add(item.split(':')[0])

                self.term_info[line_list[0]] = [offset, total_frequency, len(doc_set)]
                offset = f.tell()

        self.write_term_info_file()

    def write_term_info_file(self):
        with open(self.term_info_file, 'w') as f:
            for k, v, in self.term_info.items():
                f.write(f'%s\t%s\t%s\t%s\n' % (k, v[0], v[1], v[2]))
        