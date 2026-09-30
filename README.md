Abstract
This repository contains a Python-based computational pipeline for processing and analyzing single-cell RNA sequencing (scRNA-seq) data. The primary objective is to evaluate the expression of key mechanotransduction effectors—YAP1 and WWTR1 (TAZ)—across distinct cell populations within normal breast tissue. By leveraging 10x Genomics data, this workflow categorizes cells into YAP-only, TAZ-only, and double-positive phenotypes, providing a quantitative foundation for understanding mechanosignaling heterogeneity.

 Pipeline Architecture
The workflow is divided into four primary modules, designed to be executed sequentially:

1. Data Preprocessing & Integration (`01_convert` & `02_batches`)**
   * Converts raw 10x Genomics `.h5` sparse matrices into annotated `AnnData` (`.h5ad`) objects using Scanpy.
   * Automates the batching and merging of multiple samples to optimize memory usage during large-scale integration.

2. Expression Profiling & Feature Extraction (`03_analysis` & `04_new_bcell`)**
   * Extracts Ensembl ID-matched expression vectors (ENSG00000137693 for YAP1; ENSG00000174684 for WWTR1).
   * Generates boolean masking to classify individual cells into specific expression subsets.
   * Aggregates summary statistics (mean expression, standard deviation, positivity rates) across diverse cell lineages, including B cells, Epithelial, Fibroblasts, Lymphatics, Myeloid, Perivascular, T cells, and Vascular cells.

3. Statistical Validation (`05_anova` & `06_wallis`)**
   * Executes One-Way ANOVA via `statsmodels` to assess broad variance across cell types.
   * Implements non-parametric Kruskal-Wallis testing (`scipy.stats`) to account for single-cell expression distributions.
   * Performs Tukey's HSD post-hoc testing to identify statistically significant pairwise expression differences between distinct cell clusters.

4. Data Visualization (`07_boxplot` & `08_finalplot`)**
   * Generates grouped bar charts with asymmetric error bars to represent mean expression distributions.
   * Produces high-resolution, outlier-filtered box plots using `seaborn` and `matplotlib` to visualize population-level variance.
