# GenomeIndia: Population Genomics, Natural Selection, and Endogamy Architecture

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23451643.svg)](https://doi.org/10.5281/zenodo.23451643)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Nature Format](https://img.shields.io/badge/Article_Format-Nature-blue.svg)](https://www.nature.com)
[![R](https://img.shields.io/badge/R-%3E%3D4.3.0-blue.svg)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg)](https://www.python.org/)

This repository contains the complete analytical codebase, mathematical modeling pipelines, and publication figure generation routines for the **GenomeIndia** population genomics and clinical deconvolution study across **9,768 whole genomes** from the Indian subcontinent.

---

## Scientific Scope & Novelty Beyond Published Literature

While earlier foundational reports established broad cohort metrics, uniparental lineages, and polygenic score transferability ([Bhattacharyya et al., *Nature Genetics* 2025](https://doi.org/10.1038/s41588-025-02153-x); [Subramanian et al., *medRxiv* 2026](https://doi.org/10.64898/2026.03.20.26348801)), this repository implements the first mathematical deconvolution across the **83 constituent ethnolinguistic and tribal subpopulations**, resolving key clinical and evolutionary problems:

1. **Wahlund Variance Deconvolution ($F_{ST}$)**: Proves that uniform pan-Indian models ($F_{IT}=0.02$) severely underestimate recessive disease burdens—e.g., Sickle Cell Disease (*HBB* `rs334`) homozygote burden is inflated **11.31-fold** over Hardy-Weinberg equilibrium (10.2 expected homozygotes), concentrated in isolated tribal communities (peaking at $16.67\%$ AF in `DR_T`, $F_{ST}=0.0867$).
2. **Pan-Cohort HWE False-Positive Filter Artifact**: Formulates the mathematical proof that joint calling Hardy-Weinberg equilibrium filters ($p \le 10^{-11}$, $\chi^2 \ge 46.2$) automatically discard authentic biological alleles with $F_{ST} \ge 0.054$ in substructured populations.
3. **ClinGen/ACMG PopMax Dual-Track Deconvolution**: Evaluates 348 ClinVar variant assertions across 82 subpopulations, defining:
   - **Track 1**: 103 outbred benign reclassifications (eliminating false-positive clinical reports).
   - **Track 2**: 55 protected founder drift alleles (preventing inappropriate benign filtering in high-risk tribal/founder groups).
4. **Subpopulation Unmasking of 123 Loss-of-Function Genes**: Recovers 123 high-confidence homozygous knockouts completely obscured by national pooling ($E_{\text{pooled}} < 1.0$, mean $0.08$).
5. **Resolution of the *EDAR* Selection Paradox**: Resolves the absence of mainland selection at *EDAR* (`rs3827760`) by identifying intense, lineage-specific selection in Tibeto-Burman populations ($\text{PBS}_{\text{TB}} = 0.0846$).

---

## Repository Structure

```text
GenomeIndia_GitHub_Repo/
├── README.md                   # Project documentation and quickstart guide
├── LICENSE                     # MIT Open Source License
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment definition
├── install_packages.R          # R dependencies installer (ggpubr, patchwork, cowplot)
├── run_all_reproducibility.py  # Master end-to-end Python runner
├── run_pipeline.bat            # Windows 1-click execution script
├── run_pipeline.sh             # Linux/macOS execution script
├── data/                       # Input datasets and 83-subpopulation matrices
│   ├── pgx_heatmap_matrix.csv
│   ├── acmg_popmax_founder_deconvolution.csv
│   ├── table_s12_2_founder_knockout_deconvolution.csv
│   ├── india_boundary_coords.csv
│   └── pbs_selection_regional_summary.csv
├── scripts/
│   ├── analysis/               # Statistical and population genetics modules
│   │   ├── 01_wahlund_variance_calculator.py
│   │   ├── 02_clingen_popmax_deconvolution.py
│   │   ├── 03_founder_knockout_unmasking.py
│   │   └── 04_pbs_selection_scans.py
│   └── figure_generation/      # Nature publication graphics (ggpubr + patchwork + cowplot)
│       └── build_nature_article_figures.R
└── results/                    # Publication-ready figures (300 DPI Nature format)
    ├── main_fig1_nature.png    # SFS & gnomAD SAS density overlay
    ├── main_fig2_nature.png    # Autosomal diversity & 4-panel selection scans
    ├── main_fig3_nature.png    # 83-subpopulation PGx heatmap & Wahlund HWE artifact
    ├── main_fig4_nature.png    # ClinGen PopMax deconvolution (348 ClinVar variants)
    ├── main_fig5_nature.png    # Regional founder knockouts (Official SOI Map) & unmasking
    ├── ext_data_fig1.png       # Zoomed Tajima's D & theta_W / pi ratio
    ├── ext_data_fig2.png       # ACMG tiers, CPIC carriers & autozygosity burden
    ├── ext_data_fig3.png       # Ti/Tv mutational spectrum & DPYD homozygote yield
    └── ext_data_fig4.png       # Regional PBS selection peaks (EDAR locus)
```

---

## Installation & Quickstart

### Prerequisites
- **R (>= 4.3.0)** with `ggplot2`, `ggpubr`, `patchwork`, `cowplot`, `scales`, `ggrepel`, `readxl`, `reshape2`.
- **Python (>= 3.10)** with `pandas`, `numpy`, `scipy`, `python-docx`, `pillow`.

### Setup
```bash
# Clone the repository
git clone https://github.com/GenomeIndia-Analysis/GenomeIndia-Population-Genomics-Nature-2026.git
cd GenomeIndia-Population-Genomics-Nature-2026

# Install Python requirements
pip install -r requirements.txt

# Install R dependencies
Rscript install_packages.R
```

### Reproduce All Analysis & Figures
```bash
# Run complete end-to-end reproducibility pipeline
python run_all_reproducibility.py

# Or generate all Nature figures directly:
Rscript scripts/figure_generation/build_nature_article_figures.R
```

---

## Citation

If you use this codebase or data in your research, please cite:
```bibtex
@article{GenomeIndia2026Nature,
  title={Population genomics, natural selection, and endogamy architecture across 9,768 Indian whole genomes},
  author={GenomeIndia Collaborative Research Initiative},
  journal={Nature},
  year={2026},
  doi={10.5281/zenodo.10892451}
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
