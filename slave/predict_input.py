import math
from pomegranate import *
import vcf
import argparse


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

    real = DiscreteDistribution({'True': probability_from_vcf, 'False': 1- probability_from_vcf })

    importgene = ConditionalProbabilityTable(
        [['True', 'True', 0.66],
         ['True', 'False', 0.33],
         ['False', 'True', 0.66],
         ['False', 'False', 0.33]], [asia])


    # initialize  probability distributions
    realgene = DiscreteDistribution( { 'True': prob_real_gene * scale_real_gene, 'False': 1-(prob_real_gene * scale_real_gene) } )
    mutatedgene = DiscreteDistribution( { 'True': prob_mutated_gene * scale_mutated_gene, 'False': 1-(prob_mutated_gene * scale_mutated_gene) })
    clinvargene = DiscreteDistribution( { 'True': prob_clinvar_gene * scale_clinvar_gene, 'False': 1-(prob_clinvar_gene * scale_clinvar_gene) })

    # set prior belief in importance of gene (50% chance)
    importgene = DiscreteDistribution( { 'True': 0.5, 'False': 0.5 } )

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
