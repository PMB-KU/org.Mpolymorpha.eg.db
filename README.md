# **Unoficial** Org Db for *Marchantia Polymorpha*

!important
This is **Unoficial Annotation Packages**

## Usage

You can install this package with the following commands.

```r
remotes::install_github("PMB-KU/org.Mpolymorpha.eg.db")
library(org.Mpolymorpha.eg.db)
```

## Creating your own OrgDb packages

### makeOrgDb.R

| require files   |                                                                               |
| --------------- | ----------------------------------------------------------------------------- |
| `gene_info.csv` | This file should have the columns, "GID", "SYMBOL", "PRODUCT" and "REFERENCE" |
| `gene2go.csv`   | This file should have the columns, "GID", "GO" and "EVIDENCE CODE"            |

Please check these files located in the same directory as `makeOrgDb.R` and run scripts. 

```bash
Rscript makeOrgDb.R
```

I recommend to use docker.

```bash
# docker
docker build -t annotationforge .
docker run --rm -it -v $(pwd):/local annotationforge Rscript makeOrgDb.R
```

`org.Mpolymorpha.eg.db` is generated.  
In R console,

```r
install.packages("./org.Mpolymorpha.eg.db", repos=NULL)
library(org.Mpolymorpha.eg.db)
```

You can use `org.Mpolymorpha.eg.db` in `clusterProfiler`, `topGO` or `goseq` etc.,

**Example of `clusterProfiler`**

```R
library(clusterProfiler)
library(org.Mpolymorpha.eg.db)
ego <- enrichGO(gene          = geneList,
                OrgDb         = org.Mpolymorpha.eg.db,
                keyType       = "GID",
                ont           = "CC",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05)
```

### make gene2go.csv and gene_info.csv

You can make MpTak v6.1 `gene2go.csv` and `gene_info.csv` from [MarpolBase](https://marchantia.info) annotations and nomenclatures.

```bash
python make_geneinfo/run.py --use-api
```

## REFERENCE

1. Carlson M, Pagès H (2021). AnnotationForge: Tools for building SQLite-based annotation data packages. R package version 1.34.0, https://bioconductor.org/packages/AnnotationForge.