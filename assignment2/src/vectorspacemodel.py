import string 
from nltk.stem import PorterStemmer

class VectorSpaceModel:
    def __init__(self, query_file, output_file):
        self.query_file = query_file
        self.output_file = output_file
        self.stop_words = self._create_stopwords()
        self.queries = []
        self.vsm = {}

    def vectorize(self):
        self._process_queries()
        self._create_vsm()
    
    def _process_queries(self):
        '''
        Reads in the queries from the file and appends to a list.
        '''
        with open(self.query_file, 'r') as f:
            for line in f:
                query = line.lower().translate(str.maketrans('','', string.punctuation))
                self.queries.append(query)

    def _create_vsm(self):
        '''
        Creates the VSM and removes all stop words that are included in the query.

        { 
            QueryNo: [Tokens]
        }
        '''
        ps = PorterStemmer()

        for query in self.queries:
            tokens = query.split()
            for token in tokens[1:]:
                if token not in self.stop_words:
                    self.vsm.setdefault(tokens[0], []).append(ps.stem(token))
        
    def _create_stopwords(self):
        '''
        Creates stop words using the provided file.
        '''
        stop_words = []

        with open('stopwords.txt', 'r') as f:
            for line in f:
                stop_words.append(line.rstrip('\n'))

        return stop_words

if __name__=="__main__":
    query_f = "query_list.txt"
    output_f = "\data\output.txt"
    vsm = VectorSpaceModel(query_f, output_f)
    vsm.vectorize()
