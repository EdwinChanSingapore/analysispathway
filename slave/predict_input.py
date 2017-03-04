import math
from pomegranate import *
import vcf
import argparse
from pgmpy.models import BayesianModel


def load_reference(paths):
    paths = vars(paths)
    input = paths['input']
    opened_vcf_file = vcf.Reader(open(input, 'r'))
    return opened_vcf_file

def execute_main(paths):
    vcf_object = load_reference(paths)

#which gives posterior odds of
#Prior          Likelihood  Posterior     Normalised
#0.5            1           0.5           0.66
#0.5            0.5         0.25          0.33
    dummy_variable_1 = 0.8
    dummy_variable_2 = 0.8
    dummy_variable_3 = 0.8
    dummy_variable_4 = 0.8
    dummy_variable_5 = 0.8
    dummy_variable_6 = 0.8
    dummy_variable_7 = 0.8
    dummy_variable_8 = 0.8

    real_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5  })
    functional_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    ClinVar_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5 })
    Mut_tstr_gene = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    real_prob = dummy_variable_1
    ClinVar_prob = dummy_variable_2
    Mut_tstr_prob = dummy_variable_3
    functional_prob = dummy_variable_4

    importgene = ConditionalProbabilityTable(
         [['True', 'True', 'True', p(1)*p(2)/(p1*p2 + (1-p(1))*(1-p(2)))],
          ['True', 'True', 'False', 1-p(1)*(1-p(2))],
          ['True', 'False', 'True', 0.66],
          ['True', 'False', 'False', 0.33],
          ['False', 'True', 'True', 0.66],
          ['False', 'True', 'False', 0.33],
          ['False', 'False', 'True', 0.66]
          ['False', 'False', 'False', 0.33]], [real_gene, functional_gene])



    # set up states
    s1 = State( realgene, name="Real Gene" )
    s2 = State( mutatedgene, name="Mutated Gene" )
    s3 = State( clinvargene, name="Clinvar Gene" )
    s4 = State( importgene, name="Important Gene" )

    # set up network
    network = BayesianNetwork( "Gene Prediction" )
    network.add_states(s1, s2, s3, s4)
    network.add_edge(s4, s1)
    network.add_edge(s4, s2)
    network.add_edge(s4, s3)
    network.bake()

    %pylab inline
    network.plot()

    # predict probability that gene is important given other probabilities
    beliefs = network.predict_proba({ 'Real Gene':'True','Mutated Gene':'True','Clinvar Gene': 'True'})

    # get the probability that the gene is important
    prob_gene_important = beliefs[-1].values()[0]
    print prob_gene_important

if __name__ = "__main__":
    np.seterr(divide='raise', invalid='raise')
    parser = argparse.ArgumentParser(description="train neural net")
    parser.add_argument('-i', '--input', help="give directories with files", nargs='+')
    paths = parser.parse_args()
    execute_main(paths)
