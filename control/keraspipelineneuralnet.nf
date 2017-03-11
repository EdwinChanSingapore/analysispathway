#!/usr/bin/env nextflow

home = '/data/backup/metacaller/stage'
project ='mason_version_3.0'
projectout ='mason_version_3.00_freeze_normal'
inpath ="$home/data/$project"
inputpath="$inpath"
outpath ="$home/output/$projectout"
outputpath="$outpath"
referencepath="/data/reference/human/GRCh37p5/fasta/hs37d5.fa"
ucscreferencepath="/data/reference/human/ucsc.hg19.GATK-sorted/ucsc.hg19.fa"

process movefiles {

input:

output :
file signal into startlearning0,startlearning1,startlearning2,startlearning3,startlearning4,startlearning5,startlearning6,startlearning7

script:
"""
#mkdir -p $outputpath/
#cat $inputpath/pindel.vcf.normalisedtrain.vcf | grep -v "<[A-Z]" > $inputpath/pindel.vcf
#mv -f $inputpath/pindel.vcf $inputpath/pindel.vcf.normalisedtrain.vcf
##cat $inputpath/fb.vcf.normalisedtrain.vcf | \${VCFFILTERPATH} -f "QUAL > 5" > $inputpath/fb.vcf
#mv -f $inputpath/fb.vcf $inputpath/fb.vcf.normalisedtrain.vcf
echo "done moving files" > signal
"""
}

process generatetruth {
input:
file signal from startlearning0

output:

script:
"""
mkdir -p $outputpath/ANN/
#chmod 777 $outputpath/ANN/
#rm -f $outputpath/ANN/model*
\${ANNPATH} \${TRUEANNPATH} $inputpath $ucscreferencepath $outputpath
#cp -f ${GENERATEANNPATH} $outputpath/ANN/
#\${CALPATH} $outputpath/ANN/ANNgenerateresults.py $outputpath/ANN/myXdata.txt.npy $outputpath/ANN/myydata.txt.npy $outputpath/ANN/ $outputpath/ANN/samplelist.p $outputpath/ANN/truthdict.p $outputpath/ANN/callerlengths.txt.npy $outputpath/ANN/vcf_list.p
"""

}

process concord1 {

input:
file signal from startlearning1

output:

script:
"""
mkdir -p $outputpath/concordance/1/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 1
mkdir -p $outputpath/concordance/2/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 2
mkdir -p $outputpath/concordance/3/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 3
mkdir -p $outputpath/concordance/4/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 4
mkdir -p $outputpath/concordance/5/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 5
mkdir -p $outputpath/concordance/6/
#\${CONCORDANCEPATH} \${TRUECONCORDANCEPATH} $inputpath $outputpath 6
"""

}
