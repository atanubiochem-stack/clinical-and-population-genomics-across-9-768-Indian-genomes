import os, subprocess, sys

print("=== Running GenomeIndia Reproducibility Pipeline ===")
scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
r_script = os.path.join(scripts_dir, "figure_generation", "build_nature_article_figures.R")

print(f"Generating Nature Article Figures with Rscript: {r_script}")
res = subprocess.run(["Rscript", r_script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)

print("=== Reproducibility Execution Completed Successfully ===")
