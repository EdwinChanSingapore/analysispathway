import argparse
import sys
import matplotlib
import vcf

matplotlib.use('Agg')

from pomegranate import *
from build_cdp import *

def load_reference(paths):
    paths = vars(paths)
    input = paths['input']
    opened_vcf_file = vcf.Reader(open(input, 'r'))
    return opened_vcf_file


def get_scores(record):
    new_list = []
    for i in range(7):
        new_list.append(0)
    new_list[0] = record.INFO['SIFT_score']
    new_list[1] = record.INFO['LRT_score']
    new_list[2] = record.INFO['MutationAssessor_score']
    new_list[3] = record.INFO['MutationTaster_score']
    new_list[4] = record.INFO['Polyphen2_HVAR_score']
    new_list[5] = record.INFO['FATHMM_score']
    new_list[6] = record.INFO['clinvar_20150629']
    return new_list


def execute_main(paths):
    vcf_object = load_reference(paths)

    # which gives posterior odds of
    # Prior          Likelihood  Posterior     Normalised
    # 0.5            1           0.5           0.66
    # 0.5            0.5         0.25          0.33
    count = 0
    for record in vcf_object :
        count +=1
        list_of_scores = get_scores(record)
        print list_of_scores
    import_cdp = get_cdp(2, [0.8, 0.8])

    real_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    ClinVar_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    PolyPhen2_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    LRT_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    MutationTaster_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    MutationAssessor_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    SIFT_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    FATHMM_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    functional_cdp = get_cdp(7,[0.8,0.8,0.8,0.8,0.8,0.8,0.8])
    functional_gene = ConditionalProbabilityTable(functional_cdp, [ClinVar_gene, PolyPhen2_gene,LRT_gene,
                                                                   MutationTaster_gene,MutationAssessor_gene,
                                                                   SIFT_gene, FATHMM_gene])
    import_cdp = get_cdp(2, [0.5, 0.5])
    importgene = ConditionalProbabilityTable(import_cdp, [real_gene, functional_gene])

    # set up states
    s1 = State(real_gene, name="Real Gene")
    s2 = State(functional_gene, name="Functional Gene")
    s3 = State(importgene, name="Important Gene")
    s4 = State(ClinVar_gene, name="ClinVar")
    s5 = State(PolyPhen2_gene, name="PolyPhen")
    s6 = State(LRT_gene, name="LRT")
    s7 = State(MutationTaster_gene, name="MutationTaster")
    s8 = State(MutationAssessor_gene, name="MutationAssessor")
    s9 = State(SIFT_gene, name="SIFT")
    s10 = State(FATHMM_gene, name="FATHMM_gene")

    # set up network
    network = BayesianNetwork("Gene Prediction")
    network.add_states(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10)
    network.add_edge(s1, s3)
    network.add_edge(s2, s3)
    network.add_edge(s4, s2)
    network.add_edge(s5, s2)
    network.add_edge(s6, s2)
    network.add_edge(s7, s2)
    network.add_edge(s8, s2)
    network.add_edge(s9, s2)
    network.add_edge(s10, s2)
    network.bake()

    network.plot()
    matplotlib.pyplot.savefig('foo.png', bbox_inches='tight')

    # predict probability that gene is important given other probabilities
    beliefs = network.predict_proba({'Real Gene': 'True', 'ClinVar': 'True'})

    # get the probability that the gene is important
    prob_gene_important = beliefs[-1].values()[0]
    print prob_gene_important


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="train neural net")
    parser.add_argument('-i', '--input', help="give directories with files")
    paths = parser.parse_args()
    execute_main(paths)
