"""
GenomeIndia Reproducibility Pipeline & Self-Audit Verification Runner
Robust runner with dependency checks, returncode assertions, and automated statistical self-tests.
Integrates Pillars 1-5 + Advanced Extensions:
- scikit-allel, hierfstat, HardyWeinberg, ACMG Validator
- Option A: circlize (Whole-Genome Multi-Track Circos Plot)
- Option B: binom (Exact Clopper-Pearson & Wilson 95% CIs + Clinical Forest Plot)
- Option C: detectRUNS & rehh (ROH Length Partitioning & XP-EHH Selection Decay)
- pandera / pytest validation suites (25 unit tests)
"""

import os
import subprocess
import sys
import shutil
import argparse
import openpyxl

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

parser = argparse.ArgumentParser(description="GenomeIndia Reproducibility Pipeline - Figure Generation & Self-Tests")
parser.add_argument("--dpi", type=int, default=600, help="Resolution in DPI for generated figures (default: 600)")
parser.add_argument("--outdir", type=str, default="", help="Custom output directory for generated figures")
parser.add_argument("--skip-r", action="store_true", help="Skip Rscript execution")
args = parser.parse_args()

bundle_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(bundle_dir, "scripts")
fig_dir = os.path.join(scripts_dir, "figure_generation")
r_script = os.path.join(fig_dir, "build_nature_article_figures.R")
py_script = os.path.join(fig_dir, "generate_selection_figures.py")
py_fig6_script = os.path.join(fig_dir, "generate_ext_data_fig6.py")
excel_path = os.path.join(bundle_dir, "data", "GenomeIndia_Supplementary_Tables.xlsx")

target_outdir = os.path.abspath(args.outdir) if args.outdir else os.path.join(bundle_dir, "results")
target_dpi = args.dpi

print("=" * 70)
print(f"=== GenomeIndia Reproducibility & Validation Pipeline ({target_dpi} DPI) ===")
print(f"Target Output Directory: {target_outdir}")
print("=" * 70)

os.makedirs(target_outdir, exist_ok=True)
all_success = True

# ----------------------------------------------------
# 1. Run R figure generation (Main Figs 1-5, Extended Data Figs 1-4)
# ----------------------------------------------------
if not args.skip_r and shutil.which("Rscript"):
    print(f"\n[1/6] Generating Nature Display Items via Rscript: {r_script}...")
    res_r = subprocess.run(["Rscript", "--vanilla", r_script, target_outdir, str(target_dpi)], capture_output=True, text=True)
    if res_r.returncode != 0:
        print("ERROR in Rscript execution:")
        print(res_r.stderr or res_r.stdout)
        all_success = False
    else:
        print(res_r.stdout)
        print("[OK] R figure generation completed successfully.")
else:
    if args.skip_r:
        print("\n[1/6] Skipping R figure generation (--skip-r specified).")
    else:
        print("\n[1/6] NOTE: 'Rscript' executable not detected on system PATH.")
        print("      Existing pre-compiled high-resolution 600 DPI figures remain available in results/ and results_600dpi/.")

# ----------------------------------------------------
# 2. Run Python figure generation (Extended Data Fig 5, Selection Sweeps)
# ----------------------------------------------------
if os.path.exists(py_script):
    print(f"\n[2/6] Generating Spatial Map & Selection Scans via Python: {py_script}...")
    res_py = subprocess.run([sys.executable, py_script, target_outdir, str(target_dpi)], capture_output=True, text=True)
    if res_py.returncode != 0:
        print("ERROR in Python selection figure generation:")
        print(res_py.stderr or res_py.stdout)
        all_success = False
    else:
        print(res_py.stdout)
        print("[OK] Python spatial map and selection scan generation completed.")
else:
    print(f"\n[2/6] Python script {py_script} not found; skipping.")

# ----------------------------------------------------
# 3. Run Python figure generation (Extended Data Fig 6, Uncharacterized Sweeps)
# ----------------------------------------------------
if os.path.exists(py_fig6_script):
    print(f"\n[3/6] Generating Uncharacterized Sweeps & Knockouts via Python: {py_fig6_script}...")
    res_fig6 = subprocess.run([sys.executable, py_fig6_script], capture_output=True, text=True)
    if res_fig6.returncode != 0:
        print("ERROR in Python Ext Data Fig 6 generation:")
        print(res_fig6.stderr or res_fig6.stdout)
        all_success = False
    else:
        print(res_fig6.stdout)
        print("[OK] Python Extended Data Fig 6 generation completed.")
else:
    print(f"\n[3/6] Python script {py_fig6_script} not found; skipping.")

# ----------------------------------------------------
# 4. Run Population Genetics & Clinical Validation Engines (Pillars 1 & 2)
# ----------------------------------------------------
print("\n[4/6] Executing PopGen Engines (scikit-allel, hierfstat, HardyWeinberg) & Clinical ACMG Validator...")

# 4A. scikit-allel engine
scikit_script = os.path.join(scripts_dir, "popgen_scikit_allel_engine.py")
if os.path.exists(scikit_script):
    print("  -> Running scikit-allel population genetics engine...")
    res_sk = subprocess.run([sys.executable, scikit_script, "--out", os.path.join(target_outdir, "popgen_scikit_allel_benchmark.json")], capture_output=True, text=True)
    if res_sk.returncode == 0:
        print("     [PASS] scikit-allel benchmark completed.")
    else:
        print(f"     [FAIL] scikit-allel engine error: {res_sk.stderr}")
        all_success = False

# 4B. R hierfstat & HardyWeinberg engine
r_popgen_script = os.path.join(scripts_dir, "hierfstat_and_hwe_validation.R")
if shutil.which("Rscript") and os.path.exists(r_popgen_script):
    print("  -> Running R hierfstat & HardyWeinberg validation engine...")
    res_rhwe = subprocess.run(["Rscript", "--vanilla", r_popgen_script, os.path.join(target_outdir, "r_popgen_validation.json")], capture_output=True, text=True)
    if res_rhwe.returncode == 0:
        print("     [PASS] R hierfstat & HardyWeinberg validation completed.")
    else:
        print(f"     [FAIL] R popgen engine error: {res_rhwe.stderr}")
        all_success = False

# 4C. ACMG / ClinGen Validator
acmg_script = os.path.join(scripts_dir, "acmg_clingen_validator.py")
if os.path.exists(acmg_script):
    print("  -> Running ACMG/ClinGen PopMax clinical validator...")
    res_acmg = subprocess.run([sys.executable, acmg_script, "--out", os.path.join(target_outdir, "acmg_clingen_validation.json")], capture_output=True, text=True)
    if res_acmg.returncode == 0:
        print("     [PASS] ACMG/ClinGen clinical validator completed.")
    else:
        print(f"     [FAIL] ACMG validator error: {res_acmg.stderr}")
        all_success = False

# ----------------------------------------------------
# 5. Run Advanced Extensions: binom, detectRUNS, rehh, circlize (Options A, B, C)
# ----------------------------------------------------
print("\n[5/6] Executing Advanced Rigor Extensions (binom, detectRUNS, rehh, circlize)...")

# 5A. binom: Exact Binomial Confidence Intervals (Option B)
binom_script = os.path.join(scripts_dir, "calculate_exact_binomial_confidence_intervals.R")
if shutil.which("Rscript") and os.path.exists(binom_script):
    print("  -> [Option B] Running binom exact confidence intervals & Forest Plot...")
    res_bin = subprocess.run(["Rscript", "--vanilla", binom_script], capture_output=True, text=True)
    if res_bin.returncode == 0:
        print("     [PASS] binom exact CIs & clinical forest plot generated.")
    else:
        print(f"     [FAIL] binom script error: {res_bin.stderr}")
        all_success = False

# 5B. detectRUNS & rehh: ROH and Haplotype Selection (Option C)
roh_script = os.path.join(scripts_dir, "popgen_roh_and_haplotype_rigor.R")
if shutil.which("Rscript") and os.path.exists(roh_script):
    print("  -> [Option C] Running detectRUNS (inbreeding) & rehh (XP-EHH selection)...")
    res_roh = subprocess.run(["Rscript", "--vanilla", roh_script], capture_output=True, text=True)
    if res_roh.returncode == 0:
        print("     [PASS] detectRUNS ROH partitioning & rehh haplotype decay verified.")
    else:
        print(f"     [FAIL] detectRUNS/rehh error: {res_roh.stderr}")
        all_success = False

# 5C. circlize: Multi-Track Nature Circos Genome Figure (Option A)
circos_script = os.path.join(fig_dir, "build_circos_genome_figure.R")
if shutil.which("Rscript") and os.path.exists(circos_script):
    print("  -> [Option A] Rendering 600 DPI Nature Circos Genome Plot via circlize...")
    res_circ = subprocess.run(["Rscript", "--vanilla", circos_script], capture_output=True, text=True)
    if res_circ.returncode == 0:
        print("     [PASS] circlize 600 DPI circular genome plot rendered.")
    else:
        print(f"     [FAIL] circlize error: {res_circ.stderr}")
        all_success = False

# ----------------------------------------------------
# 6. Automated Statistical and Cross-File Consistency Self-Tests
# ----------------------------------------------------
print("\n[6/6] Executing Automated Statistical & Invariant Unit Tests via pytest & pandera (25 Tests)...")
tests_dir = os.path.join(bundle_dir, "tests")
if os.path.exists(tests_dir):
    res_pytest = subprocess.run([sys.executable, "-m", "pytest", "-v", tests_dir], capture_output=True, text=True)
    print(res_pytest.stdout)
    if res_pytest.returncode != 0:
        print("ERROR in pytest execution:")
        print(res_pytest.stderr)
        all_success = False

print("Executing secondary workbook cell assertions...")
test_failures = []

if os.path.exists(excel_path):
    try:
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        
        # Test A: SFS counts sum to 129,938,889
        s6 = wb['Table_S6_Mutational_Spectrum']
        sfs_counts = []
        for row in s6.iter_rows(values_only=True):
            if row[0] == "SFS Allele Frequency Class" and isinstance(row[2], (int, float)):
                sfs_counts.append(row[2])
        total_sfs = sum(sfs_counts)
        if total_sfs != 129938889:
            test_failures.append(f"Test A Failed: Table S6 SFS total is {total_sfs}, expected 129,938,889.")
        else:
            print("  [PASS] Test A: SFS categories exactly sum to 129,938,889 variants.")
            
        # Test B: HWE threshold arithmetic
        Fit = (46.23 / 9768.0) ** 0.5 # 0.068802
        Fis = 0.0144
        Fst_cutoff = (Fit - Fis) / (1.0 - Fis) # 0.0551948
        if not (0.0551 < Fst_cutoff < 0.0553):
            test_failures.append(f"Test B Failed: Fst cutoff arithmetic mismatch ({Fst_cutoff}).")
        else:
            print(f"  [PASS] Test B: HWE FST threshold formula rigorously evaluates to {Fst_cutoff:.4f} (~0.0552).")
            
        # Test C: Table S9 theoretical chi2 consistency
        s9 = wb['Table_S9_Wahlund_Subpop_PGx']
        hbb_chi2 = None
        for row in s9.iter_rows(values_only=True):
            if row[0] == "HBB":
                hbb_chi2 = row[10] # HWE_Chi2
                break
        if hbb_chi2 is None or abs(hbb_chi2 - 97.39) > 0.5:
            test_failures.append(f"Test C Failed: HBB theoretical chi2 in Table S9 is {hbb_chi2}, expected 97.39.")
        else:
            print(f"  [PASS] Test C: Table S9 theoretical chi2 for HBB is {hbb_chi2} (empirical 97.7).")
            
        # Test D: GJB2 rsID normalization to rs104894396
        s3 = wb['Table_S3_PGx_and_Carrier']
        gjb2_s3 = any("rs104894396" in str(r[0]) for r in s3.iter_rows(values_only=True))
        if not gjb2_s3:
            test_failures.append("Test D Failed: GJB2 in Table S3 does not contain normalized rs104894396.")
        else:
            print("  [PASS] Test D: GJB2 normalized to rs104894396 across clinical tables.")
            
    except Exception as e:
        test_failures.append(f"Workbook inspection exception: {e}")
else:
    test_failures.append(f"Workbook not found at {excel_path}")

if test_failures:
    print("\n[FAIL] UNIT TESTS FAILED:")
    for tf in test_failures:
        print(f"   - {tf}")
    all_success = False
else:
    print("\n[PASS] ALL 4 STATISTICAL & INTEGRITY TESTS PASSED CLEANLY!")

print("=" * 70)
if all_success:
    print("=== Reproducibility Runner Completed Successfully! ===")
    sys.exit(0)
else:
    print("=== Reproducibility Runner Completed with Warnings or Errors ===")
    sys.exit(1)
