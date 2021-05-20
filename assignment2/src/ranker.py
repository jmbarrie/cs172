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
            self.calculate_top_ten_docs_for_query(cosine_similarities, k)
            break

    def calculate_doc_weight_sum(self, query_num):
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
        A * B / (sqrt(A^2) * sqrt(B^2))
        """
        cosine_similarities = []
        query_length = len(self.intermediate_data[query_key][:-1])
        for query_weight in query_sum_weights:
            numerator = query_weight
            denominator = sqrt(query_length**2) * sqrt(query_weight**2) 
            cosine_similarities.append(numerator / denominator)
        return cosine_similarities

    def calculate_top_ten_docs_for_query(self, query_sum_weight, query_key):
        top_ten_values = heapq.nlargest(10, query_sum_weight)
        top_ten_indices = []
        print('top 10 values: %s, len: %s' % (list(top_ten_values), len(top_ten_values)))

        for top_value in top_ten_values:
            for i, value in enumerate(query_sum_weight):
                if top_value == value and i not in top_ten_indices:
                    top_ten_indices.append(i)
                    if len(top_ten_indices) == 10:
                        break
            if len(top_ten_indices) == 10:
                break
        
        print('top 10 indices: %s, len: %s' % (list(top_ten_indices), len(top_ten_indices)))

        top_ten_docs = []
        # print('tops: ')
        for value in top_ten_indices:
        #     print(self.intermediate_data[query_key][-1][value])
            top_ten_docs.append(self.intermediate_data[query_key][-1][value])
        print('top 10 docs: %s, len: %s' % (list(top_ten_docs), len(top_ten_docs)))
        


