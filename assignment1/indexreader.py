import re

class IndexReader:
    def __init__(self, args):
        self.arguments = args

    def print_args(self):
        print(self.arguments)

    def run_command(self):
        if '--term' in self.arguments and '--doc' not in self.arguments:
            termid = self._get_id('data/termids.txt')
            doc_frequency, total_frequency = self._get_term_info(termid)
            print(f'Listing for term: %s' % self.arguments[1])
            print(f'TERMID: %s' % termid)
            print(f'Number of documents containing term: %s' % doc_frequency)
            print(f'Term frequency in corpus: %s' % total_frequency)
        elif '--doc' in self.arguments and '--term' not in self.arguments:
            docid = self._get_id('data/docids.txt')
            distinct_terms, total_terms = self._get_doc_info(docid)
            print(f'Listing for document: %s' % self.arguments[1])
            print(f'DOCID: %s' % docid)
            print(f'Distinct terms: %s' % distinct_terms)
            print(f'Total terms: %s' % total_terms)
        elif '--doc' in self.arguments and '--term' in self.arguments:
            pass
        else:
            print('Invalid command provided')

    def _get_doc_info(self, docid):
        distinct_terms = set()
        total_terms = 0
        doc_string = f'%s:' % docid
        with open('data/term_index.txt', 'r') as f:
            for line in f:
                if doc_string in line:
                    for item in line.split():
                        if doc_string == item[:2]:
                            total_terms += 1
                            distinct_terms.add(line.split()[0])

        if total_terms == 0 or len(distinct_terms) == 0:
            raise(ValueError)

        return len(distinct_terms), total_terms

    def _get_term_info(self, termid):
        doc_frequency = None
        total_frequency = None

        with open('data/term_info.txt', 'r') as f:
            for line in f:
                if line.startswith(termid):
                    total_frequency = line.split()[3]
                    doc_frequency = line.split()[2]

        if total_frequency is None or doc_frequency is None:
            raise(ValueError)

        return doc_frequency, total_frequency

    def _get_id(self, file_name):
        id = None 
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    if self.arguments[1].lower() in line.lower():
                        id = line.split()[0]

            if id is None:
                raise(ValueError)
        except ValueError:
            print('Word or document not found')

        return id
