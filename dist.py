class DDist:
    def __init__(self, dictionary):
        total = sum([dictionary[key] for key in dictionary.keys()])
        if total - 1.0 > 1.0e-10:
            raise Exception('Distributions must sum to 1.0. Total: ' + str(total))
        self.dictionary = dictionary
    def prob(self,elt):
        return self.dictionary.get(elt,0)
    def support(self, dimension = None):
        if dimension != None:
            return list({elt[dimension] for elt in self.dictionary.keys()})
        return self.dictionary.keys()
    def total_probability(self, dimension = None, elt = None):
        if dimension == 0:
            return sum([self.dictionary.get((elt,elt2)) for elt2 in self.support(dimension)])
        else:
            return sum([self.dictionary.get((elt2,elt)) for elt in self.support(dimension)])

    @staticmethod
    def normalize_probability_table(table):
        total = sum([table.get(e, 0) for e in table.keys()])
        return {key : table[key]/total for key in table.keys()}

    @staticmethod
    def make_conditional_from_joint(joint):
        conditional_table = {}
        p_v_table = {v : sum(joint.prob((c,v)) for c in joint.support(0)) for v in joint.support(1)}
        p_v_dist = DDist(p_v_table)
        total = 0
        for c in joint.support(0):
            for v in joint.support(1):
                prob = joint.prob((c,v))/p_v_dist.prob(v)
                conditional_table[(c,v)] = prob
                total += prob
        conditional_table = DDist.normalize_probability_table(conditional_table)
        return DDist(conditional_table)

    def __str__(self):
        return "DDist: " + str(self.dictionary)