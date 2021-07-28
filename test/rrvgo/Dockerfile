FROM rocker/r-base

RUN apt-get update --fix-missing -y && \
    apt-get install -y libxml2-dev libcurl4-openssl-dev openssl r-cran-openssl libssl-dev


RUN Rscript -e 'install.packages("BiocManager")' && \
    Rscript -e 'BiocManager::install(c("AnnotationDbi", "GO.db", "GOSemSim", "rrvgo"), ask = FALSE)'