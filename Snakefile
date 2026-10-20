# =============================================================================
# GenomeIndia Nature Article - Automated Snakemake Workflow Pipeline
# =============================================================================
# Direct Acyclic Graph (DAG) orchestrating data validation, 600 DPI figure
# generation, cross-table integrity verification, and document synchronization.
# Includes advanced popgen & clinical extensions: detectRUNS, rehh, binom, circlize.
# =============================================================================

import os

# Paths
DATA_DIR = "data"
RESULTS_DIR = "results"
DOCS_DIR = "docs"
SCRIPTS_DIR = "scripts"
FIG_GEN_DIR = os.path.join(SCRIPTS_DIR, "figure_generation")
SUPP_TABLES = os.path.join(DATA_DIR, "GenomeIndia_Supplementary_Tables.xlsx")
MANUSCRIPT_DOCX = os.path.join(DOCS_DIR, "GenomeIndia_Research_Paper_Manuscript.docx")

# Output Figures (600 DPI)
MAIN_FIGURES = [
    os.path.join(RESULTS_DIR, f"fig{i}_nature.png") for i in range(1, 6)
]
EXT_DATA_FIGURES = [
    os.path.join(RESULTS_DIR, f"ext_data_fig{i}.png") for i in range(1, 7)
]
ADVANCED_FIGURES = [
    os.path.join(RESULTS_DIR, "fig_circos_genome_nature.png"),
    os.path.join(RESULTS_DIR, "fig_acmg_sf_forestplot.png"),
    os.path.join(RESULTS_DIR, "ext_data_roh_distribution.png"),
    os.path.join(RESULTS_DIR, "ext_data_selection_ehh_profiles.png")
]

rule all:
    input:
        "results/.data_contracts_passed",
        os.path.join(RESULTS_DIR, "acmg_clingen_validation.json"),
        os.path.join(RESULTS_DIR, "r_popgen_validation.json"),
        os.path.join(RESULTS_DIR, "popgen_scikit_allel_benchmark.json"),
        os.path.join(RESULTS_DIR, "clinical_exact_confidence_intervals.json"),
        os.path.join(RESULTS_DIR, "detectruns_and_rehh_validation.json"),
        MAIN_FIGURES,
        EXT_DATA_FIGURES,
        ADVANCED_FIGURES

# -----------------------------------------------------------------------------
# 1. DATA CONTRACTS & INTEGRITY TESTING (Pillar 3: Pandera & Pytest)
# -----------------------------------------------------------------------------
rule test_data_contracts:
    input:
        tables = SUPP_TABLES
    output:
        flag = "results/.data_contracts_passed"
    shell:
        'python -m pytest -v tests/ && python -c "open(r\'{output.flag}\', \'w\').write(\'PASSED\')"'

# -----------------------------------------------------------------------------
# 2. POPULATION GENETICS BENCHMARK (Pillar 1: scikit-allel)
# -----------------------------------------------------------------------------
rule benchmark_scikit_allel:
    input:
        tables = SUPP_TABLES,
        py_script = os.path.join(SCRIPTS_DIR, "popgen_scikit_allel_engine.py")
    output:
        json_out = os.path.join(RESULTS_DIR, "popgen_scikit_allel_benchmark.json")
    shell:
        """
        python {input.py_script} --out {output.json_out}
        """

# -----------------------------------------------------------------------------
# 3. R POPULATION GENETICS & HWE VALIDATION (Pillar 1: hierfstat, HardyWeinberg, pegas)
# -----------------------------------------------------------------------------
rule validate_r_popgen:
    input:
        tables = SUPP_TABLES,
        r_script = os.path.join(SCRIPTS_DIR, "hierfstat_and_hwe_validation.R")
    output:
        json_out = os.path.join(RESULTS_DIR, "r_popgen_validation.json")
    shell:
        """
        Rscript --vanilla {input.r_script} {output.json_out}
        """

# -----------------------------------------------------------------------------
# 4. CLINICAL VARIANT INTERPRETATION (Pillar 2: ACMG/ClinGen PopMax Validator)
# -----------------------------------------------------------------------------
rule validate_acmg_clingen:
    input:
        tables = SUPP_TABLES,
        py_script = os.path.join(SCRIPTS_DIR, "acmg_clingen_validator.py")
    output:
        json_out = os.path.join(RESULTS_DIR, "acmg_clingen_validation.json")
    shell:
        """
        python {input.py_script} --out {output.json_out}
        """

# -----------------------------------------------------------------------------
# 5. EXACT BINOMIAL CONFIDENCE INTERVALS (Option B: binom & Forest Plot)
# -----------------------------------------------------------------------------
rule calculate_exact_confidence_intervals:
    input:
        tables = SUPP_TABLES,
        r_script = os.path.join(SCRIPTS_DIR, "calculate_exact_binomial_confidence_intervals.R"),
        contract = "results/.data_contracts_passed"
    output:
        json_out = os.path.join(RESULTS_DIR, "clinical_exact_confidence_intervals.json"),
        forest_png = os.path.join(RESULTS_DIR, "fig_acmg_sf_forestplot.png")
    shell:
        """
        Rscript --vanilla {input.r_script}
        """

# -----------------------------------------------------------------------------
# 6. ROH INBREEDING & HAPLOTYPE SELECTION (Option C: detectRUNS & rehh)
# -----------------------------------------------------------------------------
rule validate_roh_and_haplotypes:
    input:
        tables = SUPP_TABLES,
        r_script = os.path.join(SCRIPTS_DIR, "popgen_roh_and_haplotype_rigor.R"),
        contract = "results/.data_contracts_passed"
    output:
        json_out = os.path.join(RESULTS_DIR, "detectruns_and_rehh_validation.json"),
        roh_png = os.path.join(RESULTS_DIR, "ext_data_roh_distribution.png"),
        ehh_png = os.path.join(RESULTS_DIR, "ext_data_selection_ehh_profiles.png")
    shell:
        """
        Rscript --vanilla {input.r_script}
        """

# -----------------------------------------------------------------------------
# 7. MULTI-TRACK CIRCULAR GENOME DISPLAY ITEM (Option A: circlize)
# -----------------------------------------------------------------------------
rule generate_circos_genome:
    input:
        tables = SUPP_TABLES,
        r_script = os.path.join(FIG_GEN_DIR, "build_circos_genome_figure.R"),
        contract = "results/.data_contracts_passed"
    output:
        circos_png = os.path.join(RESULTS_DIR, "fig_circos_genome_nature.png")
    shell:
        """
        Rscript --vanilla {input.r_script}
        """

# -----------------------------------------------------------------------------
# 8. NATURE MAIN DISPLAY ITEMS (R ggpubr/patchwork)
# -----------------------------------------------------------------------------
rule generate_nature_figures:
    input:
        tables = SUPP_TABLES,
        r_script = os.path.join(FIG_GEN_DIR, "build_nature_article_figures.R"),
        contract = "results/.data_contracts_passed"
    output:
        fig1 = os.path.join(RESULTS_DIR, "fig1_nature.png"),
        fig2 = os.path.join(RESULTS_DIR, "fig2_nature.png"),
        fig3 = os.path.join(RESULTS_DIR, "fig3_nature.png"),
        fig4 = os.path.join(RESULTS_DIR, "fig4_nature.png"),
        fig5 = os.path.join(RESULTS_DIR, "fig5_nature.png"),
        ext1 = os.path.join(RESULTS_DIR, "ext_data_fig1.png"),
        ext2 = os.path.join(RESULTS_DIR, "ext_data_fig2.png"),
        ext3 = os.path.join(RESULTS_DIR, "ext_data_fig3.png"),
        ext4 = os.path.join(RESULTS_DIR, "ext_data_fig4.png")
    shell:
        """
        Rscript --vanilla {input.r_script} {RESULTS_DIR} 600
        """

# -----------------------------------------------------------------------------
# 9. SPATIAL MAP & SELECTION SCANS (Python Matplotlib)
# -----------------------------------------------------------------------------
rule generate_spatial_maps:
    input:
        tables = SUPP_TABLES,
        py_script = os.path.join(FIG_GEN_DIR, "generate_selection_figures.py"),
        contract = "results/.data_contracts_passed"
    output:
        ext5 = os.path.join(RESULTS_DIR, "ext_data_fig5.png")
    shell:
        """
        python {input.py_script} {RESULTS_DIR} 600
        """

# -----------------------------------------------------------------------------
# 10. UNCHARACTERIZED SWEEPS & KNOCKOUTS (Python Matplotlib)
# -----------------------------------------------------------------------------
rule generate_uncharacterized_sweeps:
    input:
        tables = SUPP_TABLES,
        py_script = os.path.join(FIG_GEN_DIR, "generate_ext_data_fig6.py"),
        contract = "results/.data_contracts_passed"
    output:
        ext6 = os.path.join(RESULTS_DIR, "ext_data_fig6.png")
    shell:
        """
        python {input.py_script}
        """
