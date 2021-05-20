import heapq
from math import sqrt

class Ranker:
    def __init__(self, intermediate_dict):
        self.intermediate_data = intermediate_dict
        self.all_query_weights = {}

    def compute(self):
        for k, v in self.intermediate_data.items():
            one_query_weights = []
            for i in range(len(v)):
                all_query_docs = self.intermediate_data[k][-1]
                one_query_weights.append(self.calculate_query_weight(self.intermediate_data[k][i], all_query_docs))
            self.all_query_weights[k] = one_query_weights

        for k in self.intermediate_data.keys():
            query_sum_weight = self.calculate_doc_weight_sum(k)
            cosine_similarities = self.compute_cosine_similarity(query_sum_weight, k)
            top_ten_doc_ids, top_ten_values = self.calculate_top_ten_docs_for_query(cosine_similarities, k)
            self._write_results(top_ten_doc_ids, top_ten_values, k)

    def calculate_doc_weight_sum(self, query_num):
        """
        Creates the weights for each document
        """
        weights = self.all_query_weights[query_num]
        weights_sum = [sum(x) for x in zip(*weights)]
        return weights_sum

    def calculate_query_weight(self, query_data, query_docs):
        """
        Calculates the document weight (binary) for a single query.
        The end result is a 1D list of summed up weights:
        [summed_weight_doc1, summed_weight_doc2, ... , summed_weight_docn]
        """
        weights = []
        for i in range(len(query_docs)):
            if query_docs[i] in query_data[2]:
                weights.append(query_data[2].count(query_docs[i]))
            else:
                weights.append(0)

        return weights

    def compute_cosine_similarity(self, query_sum_weights, query_key):
        """
        Computes the cosine similarity:
        A * B / (sqrt(A) * sqrt(B))
        A*B is already the query weight
        The values are already squared (just the sums of 1^2)
        """
        cosine_similarities = []
        query_length = len(self.intermediate_data[query_key][:-1])
        for query_weight in query_sum_weights:
            numerator = query_weight
            denominator = sqrt(query_length) * sqrt(query_weight) 
            cosine_similarities.append(numerator / denominator)
        return cosine_similarities

    def calculate_top_ten_docs_for_query(self, query_sum_weight, query_key):
        top_ten_values = heapq.nlargest(10, query_sum_weight)
        top_ten_indices = []

        for top_value in top_ten_values:
            for i, value in enumerate(query_sum_weight):
                if top_value == value and i not in top_ten_indices:
                    top_ten_indices.append(i)
                    if len(top_ten_indices) == 10:
                        break
            if len(top_ten_indices) == 10:
                break

        top_ten_doc_ids = []
        for value in top_ten_indices:
            top_ten_doc_ids.append(self.intermediate_data[query_key][-1][value])
        # print('top 10 indices: %s, len: %s' % (list(top_ten_indices), len(top_ten_indices)))

        return top_ten_doc_ids, top_ten_values

    def _write_results(self, top_ten_doc_ids, top_ten_values, query_key):
        """
        Prints in the schema:
        <query−number> Q0 <docno> <rank> <score> Exp
        """
        docs = []

        with open('./data/docids.txt') as f:
            for line in f:
                if line.split('\t')[0] in top_ten_doc_ids:
                    docs.append(line.split('\t')[1].replace('\n', ''))

        print('-' * 15)
        print('Top documents for query %s' % query_key)
        print('top values: %s, len: %s' % (top_ten_values, len(top_ten_values)))
        print('top documents: %s, len: %s' % ("".join(docs), len(docs)))

        with open('./data/output.txt', 'a+') as f:
            for i in range(len(top_ten_doc_ids)):
                f.write('%s Q0 %s %s %s Exp\n' % (query_key, top_ten_doc_ids[i], i + 1, top_ten_values[i]))


