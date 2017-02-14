#!/usr/bin/env nextflow

home = '/data/backup/metacaller/stage'
project ='na_version_1.0_2.4/ann'
projectout ='NA_version_1.0_2.4/analysis'
inpath ="$home/output/$project"
inputpath="$inpath"
outpath ="$home/output/$projectout"
outputpath="$outpath"
referencepath="/data/reference/human/GRCh37p5/fasta/hs37d5.fa"
ucscreferencepath="/data/reference/human/ucsc.hg19.GATK-sorted/ucsc.hg19.fa"
vcf_input_path="$inputpath/"
model_path="$inputpath"
model_name_path="model.h5"
annovarpath="/data/reference/human/annovar/"

process movefiles {

input:

output:
file signal into signal1
script:
"""
mkdir -p $outputpath
#\${ANALYSISPATH} \${TRUEANALYSISPATH} $vcf_input_path $ucscreferencepath $outputpath $model_path $model_name_path
echo "done" > signal
"""
}

process movefiles {

input:
file signal from signal1
output:
file signal into signal2

script:
"""
\${ANNOTATEPATH} $vcf_input_path $outputpath $annovarpath
"""
}

process movefiles {

input:
file signal from signal2
output:

script:
"""
"""
}