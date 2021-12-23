library(AnnotationForge)

geneInfo <- read.csv("gene_info.csv", row.names = NULL)
gene2go <- read.table("gene2go.csv", row.names = NULL, header = TRUE, sep = ",")

makeOrgPackage(gene_info=geneInfo, go=gene2go,
               version="0.1",
               maintainer="illumination-k <illumination.k.27@gmail.com>",
               author="illumination-k <illumination.k.27@gmail.com>",
               outputDir = ".",
               tax_id="3197",
               genus="Marchantia",
               species="polymorpha",
               goTable='go')