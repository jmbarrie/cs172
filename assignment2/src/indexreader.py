import re
from nltk.stem import PorterStemmer

class IndexReader:
    def __init__(self, args):
        self.arguments = args
        self.intermediate_data = {}

    def print_args(self):
        print(self.arguments)

    def run_command(self, output=True):
        self.process_intermediate_data()

    def process_intermediate_data(self):
        # TODO: Create a way for assignment 2 to query for complex results e.g. multiple things
        '''
        Process:
            1. Get the termid, store it
            2. Get the byte offset
            3. Traverse the term_index using byteoffset to get all the documents that the term belongs to, store them all
            4. Do a --doc and --term query for EACH document to compute the cosine similarity

            {
                "query": [word, termid, [doc1, ... , docn]]
            }
        '''

        for key, values in self.arguments.items():
            for term in values:
                termid = self._get_id('data/termids.txt', term)
                offset = self._get_byte_offset(termid)
                docids = self._get_doc_ids(offset)
                self.intermediate_data.setdefault(key, []).append([term, termid, [*docids]])

        for key, values in self.intermediate_data.items():
            print(key, values)

    def _get_doc_ids(self, offset):
        doc_ids = set()

        with open('data/term_index.txt') as f:
            f.seek(offset)
            data = f.readline().split()

        for item in data[1:]:
            doc_ids.add(item.split(':')[0])

        return doc_ids
                
    def assignment_1_results(self):
        '''
        This is used to separate assignment 1 results from assignment 2.

        Assignment 1 will use simple results, whereas assignment 2 produces more complex results.
        '''
        ps = PorterStemmer()
        if '--term' in self.arguments and '--doc' not in self.arguments:
            termid = self._get_id('data/termids.txt', ps.stem(self.arguments[1]))
            doc_frequency, total_frequency = self._get_term_info(termid)
            print(f'Listing for term: %s' % self.arguments[1])
            print(f'TERMID: %s' % termid)
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
            termid = self._get_id('data/termids.txt', term)
            docid = self._get_id('data/docids.txt', document)
            term_frequency = 0
            positions = 0
            term_frequency, positions = self._get_specific_term_in_doc_info(docid, termid)
            print(f'Inverted list for term: %s' % term)
            print(f'In document: %s' % document)
            print(f'TERMID: %s' % termid)
            print(f'DOCID: %s' % docid)
            print(f'Term frequency in document: %s' % term_frequency)
            print(f'Positions: %s' % ', '.join(positions))
        else:
            print('Invalid command provided')

    def _get_byte_offset(self, termid):
        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(termid):
                    if termid == line.split()[0]:
                        offset = line.split()[1]

        return int(offset)

    def _get_specific_term_in_doc_info(self, docid, termid):
        term_frequency = 0
        positions = []
        offset = 0

        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(termid):
                    if termid == line.split()[0]:
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

    def _get_term_info(self, termid):
        doc_frequency = None
        total_frequency = None
        docids = []

        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(termid):
                    if termid == line.split()[0]:
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
