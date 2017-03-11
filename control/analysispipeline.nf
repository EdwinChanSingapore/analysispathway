#!/usr/bin/env nextflow

home = '/data/backup/metacaller/stage'
project ='pdx_version_1.0'
projectout ='pdx_version_1.0_2.2_analysis/analysis'
inpath ="$home/data/$project"
inputpath="$inpath"
outpath ="$home/output/$projectout"
outputpath="$outpath"
referencepath="/data/reference/human/GRCh37p5/fasta/hs37d5.fa"
ucscreferencepath="/data/reference/human/ucsc.hg19.GATK-sorted/ucsc.hg19.fa"
vcf_input_path="$inputpath/"
model_path="$home/output/mason_version_3.0/ANN"
model_name_path="model"
annovarpath="/data/reference/human/annovar/"
threshold="0.99"

process predict {

input:

output:
file signal into signal1
script:
"""
mkdir -p $outputpath
\${ANALYSISPATH} \${TRUEANALYSISPATH} $vcf_input_path $ucscreferencepath $outputpath $model_path $model_name_path $threshold
echo "done" > signal
"""
}

process annotate {

input:
file signal from signal1
output:
file signal into signal2

script:
"""
\${ANNOTATEPATH} $outputpath/truevcf.vcf $outputpath/annotatedoutput $annovarpath
"""
}

process bayesian {

input:
file signal from signal2
output:

script:
"""
"""
}
