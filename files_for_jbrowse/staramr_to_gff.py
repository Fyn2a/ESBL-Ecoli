from BCBio import GFF
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, SimpleLocation


import pandas as pd
df=pd.read_csv('staramr.filtered.tsv',sep='\t',header=None)
#0 filename, 1 gene, 2 seqtype, 3 phenotype, 4 drugs, 5 identity, 6 overlap,
#7 hsp length/total length, 8 contigname, 9 start, 10 end, 11 accession

contignames=df[8].unique()

allgffs=[]
for currentcontig in contignames:
    seq=Seq("")
    rec=SeqRecord(seq,currentcontig)
    contig_info_=df[df[8]==currentcontig].values
    subfeatures=[]
    for i,subinfo in enumerate(contig_info_):
        gene=subinfo[1]
        seqtype=subinfo[2]
        drugs=subinfo[4]
        perc_identity=subinfo[5]
        start=int(subinfo[9])
        end=int(subinfo[10])
        accession=subinfo[11]
        feature_type='sequence_feature'

        strand=1
        if start > end:
            start,end=end,start
            strand=-1

        qualifiers={'source':seqtype,'score':perc_identity,
                    'ID':f"{currentcontig}_{gene.replace(' ','_')}_{i+1}",
                    'Name':gene}
        if pd.notna(drugs):
            # point mutations list drugs per mutation separated by ';', so drop repeats
            druglist=[d.strip() for d in drugs.replace(';',',').split(',')]
            qualifiers['Phenotype']=', '.join(dict.fromkeys(druglist))
        if pd.notna(accession):
            qualifiers['Accession']=accession

        # staramr coordinates are 1-based inclusive; Biopython locations are 0-based
        subfeatures.append(SeqFeature(SimpleLocation(start-1,end,strand=strand),
                                      type=feature_type,qualifiers=qualifiers))
    rec.features=subfeatures
    allgffs.append(rec)


outfile='staramr_hits.gff'
with open(outfile, "w") as out_handle:
    GFF.write(allgffs, out_handle)
