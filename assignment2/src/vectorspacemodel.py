import string 

class VectorSpaceModel:
    def __init__(self, query_file, output_file):
        self.query_file = query_file
        self.output_file = output_file
        self.stop_words = self._create_stopwords()
        self.queries = []

    def vectorize(self):
        self._process_queries()
    
    def _process_queries(self):
        with open(self.query_file, 'r') as f:
            for line in f:
                query = line.lower().translate(str.maketrans('','', string.punctuation))
                self.queries.append(query)
        
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
    for query in vsm.queries:
        print(query)
