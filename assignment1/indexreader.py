class IndexReader:
    def __init__(self, args):
        self.arguments = args

    def print_args(self):
        print(self.arguments)

    def run_command(self):
        if '--term' in self.arguments and '--doc' not in self.arguments:
            termid = self._get_term_id()
            doc_frequency, total_frequency = self._get_term_info(termid)
            print(f'Listing for term: %s' % self.arguments[1])
            print(f'TERMID: %s' % termid)
            print(f'Number of documents containing term: %s' % doc_frequency)
            print(f'Term frequency in corpus: %s' % total_frequency)
        elif '--doc' in self.arguments and '--term' not in self.arguments:
            pass
        elif '--doc' in self.arguments and '--term' in self.arguments:
            pass
        else:
            print('Invalid command provided')

    def _get_term_info(self, termid):
        doc_frequency = None
        total_frequency = None

        try:
            with open('data/term_info.txt', 'r') as f:
                for line in f:
                    if line.startswith(termid):
                        total_frequency = line.split()[3]
                        doc_frequency = line.split()[2]

            if total_frequency is None or doc_frequency is None:
                raise(ValueError)
        except ValueError:
            print('Term ID not found')

        return doc_frequency, total_frequency

    def _get_term_id(self):
        termid = None 
        try:
            with open('data/termids.txt', 'r') as f:
                for line in f:
                    if self.arguments[1] in line:
                        termid = line.split()[0]

            if termid is None:
                raise(ValueError)
        except ValueError:
            print('Word not found')

        return termid

            