# E. coli ST156: genome assembly and antibiotic resistance genes

Analysis of one *Escherichia coli* isolate (nanopore sequencing run ERR17374884) that makes an ESBL enzyme, a protein that destroys many common antibiotics. I assembled the genome, typed the strain, searched for resistance genes, and mapped the reads back to check the assembly.

## Major findings

- **Strain:** sequence type ST156. All seven typing genes matched exactly.
- **Genome:** 15 contigs, 4.75 Mb, N50 634 kb, no unknown bases. One contig is a complete circular plasmid.
- **ESBL gene:** *bla*CTX-M-15 sits on the 1.44 Mb chromosomal contig, not on the plasmid. 33 reads run through it and 1 kb past each end.
- **Plasmid:** an IncF plasmid carries genes for five more resistance types.
- **Fluoroquinolones:** three mutations (*gyrA* S83L and D87N, *parC* S80I) plus the plasmid pump gene *qepA1*.
- **Prediction:** resistance to six antibiotic classes. No carbapenemase and no *mcr* gene found.
- **Quality:** every base of every contig is covered by reads, and no resistance gene was split by a contig break.

These are predictions from DNA, not lab tests.

## Glossary

| Term | Plain meaning |
|---|---|
| Read | One piece of DNA sequence from the machine, 4,000 to 7,000 letters long on average here. |
| Depth | How many reads cover each spot. 100x means about 100. |
| Assembly, contig | The genome rebuilt by stitching reads together. A contig is one unbroken stretch of it. |
| N50 | Half the genome sits in contigs at least this long. Bigger is better. |
| Plasmid | A ring of DNA separate from the chromosome. Bacteria can pass it to each other, and resistance genes often travel on it. |
| Sequence type (ST) | A strain label from seven housekeeping genes. |
| ESBL | An enzyme that destroys penicillins and many cephalosporins. |

## Pipeline

| Step | Tool |
|---|---|
| Read quality and filtering | NanoPlot, Filtlong |
| Assembly | Flye |
| Assembly check | QUAST, seqkit |
| Strain typing | mlst |
| Resistance genes, mutations, plasmid types | staramr (ResFinder, PointFinder, PlasmidFinder) |
| Gene annotation | Prokka |
| Mapping reads back | minimap2, samtools |
| Browsing | JBrowse 2 |

Versions recorded: staramr 0.12.3, mlst 2.35.0, ResFinder commit 65c9ba3, PointFinder commit 694919f, PlasmidFinder commit 49c24c1.

## Results

### Reads

244,373 raw reads (1,068 Mb, about 230x) were filtered to 72,507 reads (500 Mb, about 109x), keeping the longest and best. Mean read length rose from 4,370 to 6,896 bases and mean quality from Q20.5 to Q22.4. The longest read was 31 kb.

### Assembly

| Measure | Value |
|---|---|
| Contigs | 15 |
| Total length | 4,750,402 bp |
| Largest contig | 1,442,361 bp |
| N50 / N90 | 633,914 / 140,286 bp |
| L50 / L90 | 3 / 8 |
| GC content | 51.03% |
| Unknown bases | 0 |

The GC plot has a single main peak, so there is no sign of a second organism. The genome is a draft, not a closed one. A second Flye run on the unfiltered reads gave 20 contigs, which was worse.

contig_15 is a complete circular plasmid: the assembler joined its end back to its start, and it carries IncFIA and IncFIB(pB171) replicon genes.

| Contig | Length (bp) | GC % | Mean depth | Notes |
|---|---|---|---|---|
| contig_6 | 1,442,361 | 50.73 | 99x | Chromosome piece. Carries *bla*CTX-M-15. |
| contig_2 | 731,186 | 51.04 | 115x | Chromosome piece. |
| contig_1 | 633,914 | 51.47 | 113x | Chromosome piece. Carries *parC* S80I. |
| contig_3 | 471,624 | 51.72 | 110x | Chromosome piece. |
| contig_13 | 378,970 | 50.30 | 85x | Chromosome piece. |
| contig_12 | 350,964 | 51.23 | 103x | Chromosome piece. Carries *gyrA* S83L and D87N. |
| contig_14 | 175,866 | 49.99 | 100x | Chromosome piece. |
| contig_4 | 140,286 | 51.76 | 103x | Chromosome piece. |
| contig_5 | 133,366 | 52.09 | 112x | Chromosome piece. |
| contig_8 | 124,019 | 50.83 | 106x | Chromosome piece. |
| contig_15 | 98,724 | 52.87 | 116x | Complete circular IncF plasmid. |
| contig_7 | 29,675 | 49.65 | 87x | Small contig. |
| contig_9 | 18,967 | 49.90 | 68x | Small contig. |
| contig_10 | 11,908 | 41.45 | 33x | Low GC, low depth. Prokka annotates a Tn2 transposon with a second *bla*TEM-1B, and an IS1 element. |
| contig_11 | 8,572 | 46.23 | 69x | Two genes with a 6 kb gap between them. |

### Strain type

Alleles adk 6, fumC 29, gyrB 32, icd 16, mdh 11, purA 8, recA 44 give ST156. mlst and staramr agree, and staramr rates the match perfect.

ST156 is not one of the famous ESBL clones such as ST131, but it has been reported in multidrug-resistant *E. coli* from animals and wastewater, often with NDM-5 and *mcr-1* ([duck](https://pmc.ncbi.nlm.nih.gov/articles/PMC5075103), [poultry farm](https://bmcmicrobiol.biomedcentral.com/track/pdf/10.1186/s12866-019-1454-2), [wastewater](https://www.mdpi.com/2079-6382/15/3/275)). This isolate has neither gene.

### Resistance

staramr passed its quality check. Every hit matched at 99% identity or better, and every resistance gene matched over its full length.

| Gene or mutation | Location | Resistance |
|---|---|---|
| *bla*CTX-M-15 (ESBL) | contig_6, 636,285 to 637,160 | Penicillins, cefotaxime, ceftriaxone, ceftazidime, cefepime, aztreonam |
| *bla*TEM-1B | contig_15 and contig_10 | Penicillins (not an ESBL) |
| *aac(3)-IId* | contig_15 | Gentamicin, tobramycin |
| *aph(3'')-Ib*, *aph(6)-Id* | contig_15 | Streptomycin |
| *sul2* | contig_15 | Sulfonamides |
| *dfrA17* | contig_15 | Trimethoprim |
| *tet(B)* | contig_15 | Tetracycline, doxycycline, minocycline |
| *qepA1* | contig_15 | Quinolone efflux pump |
| *gyrA* S83L, D87N | contig_12 | Ciprofloxacin, nalidixic acid |
| *parC* S80I | contig_1 | Ciprofloxacin, nalidixic acid (together with *gyrA*) |

Plasmid types: IncFIA and IncFIB(pB171) on contig_15, plus a partial IncQ1 hit (66% of the reference) next to *sul2* and the streptomycin genes.

The six predicted classes are beta-lactams, fluoroquinolones, aminoglycosides, trimethoprim, sulfonamides and tetracyclines. Searched and not found: carbapenemase genes (NDM, KPC, OXA-48 types) and *mcr* genes.

### Annotation

Prokka found 4,388 protein-coding genes, 91 tRNAs, 25 rRNAs, 1 tmRNA and 2 repeat regions, which is normal for a genome this size. Around *bla*CTX-M-15, ordinary chromosomal genes sit on both sides (taurine uptake, heme synthesis, regulators, transporters). The nearest mobile element is a partial Tn2 transposase 640 bases to the left. Prokka annotated no ISEcp1.

### Mapping check

I mapped all 72,507 filtered reads back onto the assembly.

- Every base of every contig is covered, with mapping quality near 60 on almost every contig.
- The 12 chromosome contigs average 104x. The plasmid is at 116x, 1.11 times the chromosome. Flye had estimated 131x.
- 33 reads span *bla*CTX-M-15 plus 1 kb on each side. The left 1 kb lies inside the partial Tn2 sequence, so a stricter check is on the to-do list.
- contig_10 has only 0.32 times the chromosome depth. 15 reads span its *bla*TEM-1B plus 1 kb on each side, and the left side is sequence found only on that contig. So the second copy is supported by real reads, at lower depth than the rest of the genome.

### Genome browser

The assembly, Prokka genes, staramr hits (converted to GFF) and read alignments load together in JBrowse 2. On the plasmid, the staramr and Prokka tracks line up, so the coordinates converted correctly.

## Limitations

- The assembly is a draft in 15 pieces. Gene order and repeat layout are uncertain, and where contig_10 sits in the genome is unknown.
- No polishing step (such as Medaka) was run.
- Resistance results are predictions from known genes and mutations. Genes outside the databases won't be found.
- One isolate, one run. ST156 is a coarse label and doesn't show relatedness.
- Unexplained: the lower depth of contig_9, contig_11 and contig_13, what fills the gap in contig_11, and the rRNA count (25, against the 22 expected for 7 operons).

## Future work

- Rebuild this analysis as a **Nextflow pipeline** so it runs end to end on any isolate.
- Check for ISEcp1 next to *bla*CTX-M-15 (contig_6, 633,000 to 641,000) using an insertion-sequence database such as ISfinder.
- Run the stricter spanning-read check for *bla*CTX-M-15, anchored in the unique gene to its left.
- Work out where contig_10 sits and why its depth is low.
- Try a second assembler (such as Raven) or longer reads, to try to close the genome.
- Polish with Medaka and re-run the resistance search.
- Run the pipeline on more isolates.

## References and tools

- Flye: <https://github.com/mikolmogorov/Flye>
- Filtlong: <https://github.com/rrwick/Filtlong>
- NanoPlot: <https://github.com/wdecoster/NanoPlot>
- QUAST: <https://github.com/ablab/quast>
- seqkit: <https://github.com/shenwei356/seqkit>
- mlst: <https://github.com/tseemann/mlst>
- staramr: <https://github.com/phac-nml/staramr> (uses ResFinder, PointFinder and PlasmidFinder from the Center for Genomic Epidemiology)
- Prokka: <https://github.com/tseemann/prokka>
- minimap2: <https://github.com/lh3/minimap2>
- samtools: <https://github.com/samtools/samtools>
- JBrowse 2: <https://jbrowse.org/jb2/>
- ST156 reports: [duck isolate with NDM-5 and mcr-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC5075103), [poultry farm, NDM-5](https://bmcmicrobiol.biomedcentral.com/track/pdf/10.1186/s12866-019-1454-2), [wastewater, IncHI2 plasmid](https://www.mdpi.com/2079-6382/15/3/275)