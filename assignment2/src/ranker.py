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
            break

        self.calculate_doc_weight_sum('85')

    def calculate_doc_weight_sum(self, query_num):
        weights = self.all_query_weights[query_num]
        weights_sum = [sum(x) for x in zip(*weights)]
        temp = max(weights_sum)
        print(temp, weights_sum.index(temp))
        print(self.intermediate_data[query_num][-1][weights_sum.index(temp)])

    def calculate_query_weight(self, query_data, query_docs):
        """
        Calculates the document weight (binary) for a single query.
        """
        weights = []
        for i in range(len(query_docs)):
            if query_docs[i] in query_data[2]:
                weights.append(query_data[2].count(query_docs[i]))
            else:
                weights.append(0)

        # WRONG, we need to make sure we have the right document number
        # for doc in query_docs:
        #     if doc in query_data[2]:
        #         weights.append(query_docs.count(doc))
        #     else:
        #         weights.append(0)

        return weights
