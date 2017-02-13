#!/usr/bin/env nextflow

home = '/data/backup/metacaller/stage'
projectin ='mason1.0'
projectout ='mason1.0'
inpath ="$home/data/$project"
inputpath="$inpath"
outpath ="$home/output/$projectout"
outputpath="$outpath"
referencepath="/data/reference/human/GRCh37p5/fasta/hs37d5.fa"
vcf_input_path="$inputpath/truevcf.vcf"
model_path="$inputpath/model"

process movefiles {

input:

output:

script:
"""
\${ANALYSISPATH} \{TRUEANALYSISPATH} $vcf_input_path $referencepath $outputpath $model_path
"""
}