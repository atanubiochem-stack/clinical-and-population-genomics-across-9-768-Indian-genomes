@echo off
echo ===================================================
echo GenomeIndia: Running Nature Figures & Analysis
echo ===================================================
Rscript scripts\figure_generation\build_nature_article_figures.R
echo Complete! Figures generated in results/
pause
