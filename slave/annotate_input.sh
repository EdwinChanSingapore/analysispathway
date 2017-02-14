#!/bin/bash

module load bio/annovar
ANNOVAR_LOCATION=/data/reference/human/annovar/

SAMPLE_NAME=$(basename $1 .vcf)

convert2annovar.pl -format vcf4 $3 -allsample -withfreq -includeinfo -outfile $2/$SAMPLE_NAME.avinput

table_annovar.pl $2/$SAMPLE_NAME.avinput ${ANNOVAR_LOCATION} -buildver hg19 -out $2/$SAMPLE_NAME -remove -protocol refGene,cytoBand,snp138,clinvar_20150629,ljb26_all,caddgt20 -operation g,r,f,f,f,f -nastring . -csvout --otherinfo

