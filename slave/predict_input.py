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

    # set scaling factor
    scale_real_gene=0.5
    scale_mutated_gene=1
    scale_clinvar_gene=1

    # set probabilities
    prob_real_gene=0.9
    prob_mutated_gene=0.5
    prob_clinvar_gene=0.5

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
