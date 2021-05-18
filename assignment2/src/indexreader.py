import re
from nltk.stem import PorterStemmer

class IndexReader:
    def __init__(self, args):
        self.arguments = args
        self.term_index = {}
        self.intermediate_data = {}

    def print_args(self):
        print(self.arguments)

    def run_command(self, output=True):
        self._read_term_index_file()
        self.process_intermediate_data()

    def _read_term_index_file(self):
        with open('data/term_index.txt', 'r') as f:
            lines = f.readlines()

        for line in lines:
            split_line = line.replace('\n', '').split('\t')
            self.term_index[split_line[0]] = split_line[1:]

    def process_intermediate_data(self):
        # TODO: Create a way for assignment 2 to query for complex results e.g. multiple things
        '''
        Process:
            1. Get the term_id, store it
            2. Use the term_id to get the doc_ids for the entire corpus
            2. Do a --doc and --term query for EACH document to compute the cosine similarity

            {
                "query": [word, term_id, [doc1, ... , docn]]
            }
        '''

        for key, values in self.arguments.items():
            for term in values:
                term_id = self._get_id('data/termids.txt', term)
                self.intermediate_data.setdefault(key, []).append([term, term_id])

        for key, query_term_list in self.intermediate_data.items():
            query_doc_ids = set()
            for i in range(len(query_term_list)):
                doc_ids_list = self._get_doc_ids(query_term_list[i][1])
                query_doc_ids.update(doc_ids_list)
                self.intermediate_data[key][i].append(doc_ids_list)
            self.intermediate_data[key].append(list(query_doc_ids))

    def _get_doc_frequencies(self):
        pass

    def _get_doc_ids(self, term_id):
        term_doc_ids = []
        for term in self.term_index[term_id]:
            doc = term.split(':')[0]
            term_doc_ids.append(doc)
        return term_doc_ids
                
    def assignment_1_results(self):
        '''
        This is used to separate assignment 1 results from assignment 2.

        Assignment 1 will use simple results, whereas assignment 2 produces more complex results.
        '''
        ps = PorterStemmer()
        if '--term' in self.arguments and '--doc' not in self.arguments:
            term_id = self._get_id('data/termids.txt', ps.stem(self.arguments[1]))
            doc_frequency, total_frequency = self._get_term_info(term_id)
            print(f'Listing for term: %s' % self.arguments[1])
            print(f'TERMID: %s' % term_id)
            print(f'Number of documents containing term: %s' % doc_frequency)
            print(f'Term frequency in corpus: %s' % total_frequency)
        elif '--doc' in self.arguments and '--term' not in self.arguments:
            docid = self._get_id('data/docids.txt', self.arguments[1])
            distinct_terms, total_terms = self._get_doc_info(docid)
            print(f'Listing for document: %s' % self.arguments[1])
            print(f'DOCID: %s' % docid)
            print(f'Distinct terms: %s' % distinct_terms)
            print(f'Total terms: %s' % total_terms)
        elif '--doc' in self.arguments and '--term' in self.arguments:
            term = ps.stem(self.arguments[self.arguments.index('--term') + 1])
            document = self.arguments[self.arguments.index('--doc') + 1]
            term_id = self._get_id('data/termids.txt', term)
            docid = self._get_id('data/docids.txt', document)
            term_frequency = 0
            positions = 0
            term_frequency, positions = self._get_specific_term_in_doc_info(docid, term_id)
            print(f'Inverted list for term: %s' % term)
            print(f'In document: %s' % document)
            print(f'TERMID: %s' % term_id)
            print(f'DOCID: %s' % docid)
            print(f'Term frequency in document: %s' % term_frequency)
            print(f'Positions: %s' % ', '.join(positions))
        else:
            print('Invalid command provided')

    def _get_byte_offset(self, term_id):
        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(term_id):
                    if term_id == line.split()[0]:
                        offset = line.split()[1]

        return int(offset)

    def _get_specific_term_in_doc_info(self, docid, term_id):
        term_frequency = 0
        positions = []
        offset = 0

        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(term_id):
                    if term_id == line.split()[0]:
                        offset = int(line.split()[1])

        with open('data/term_index.txt', 'r') as f:
            f.seek(offset)
            data = f.readline().split()

        for item in data[1:]:
            if docid == item.split(':')[0]:
                positions.append(item.split(':')[1])
                term_frequency += 1

        return term_frequency, positions

    def _get_doc_info(self, docid):
        distinct_terms = set()
        total_terms = 0
        doc_string = f'%s:' % docid
        with open('data/term_index.txt', 'r') as f:
            for line in f:
                if doc_string in line:
                    for item in line.split()[1:]:
                        if docid == item.split(':')[0]:
                            total_terms += 1
                            distinct_terms.add(line.split()[0])

        if total_terms == 0 or len(distinct_terms) == 0:
            raise(ValueError)

        return len(distinct_terms), total_terms

    def _get_term_info(self, term_id):
        doc_frequency = None
        total_frequency = None
        docids = []

        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(term_id):
                    if term_id == line.split()[0]:
                        total_frequency = line.split()[3]
                        doc_frequency = line.split()[2]

        if total_frequency is None or doc_frequency is None:
            raise(ValueError)

        return doc_frequency, total_frequency

    def _get_id(self, file_name, search_item):
        id = None 
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    if search_item.lower() in line.lower():
                        if search_item.lower() == line.split()[1].lower():
                            id = line.split()[0]

            if id is None:
                raise(ValueError)
        except ValueError:
            print('Word or document not found')

        return id
