# Install required R packages for Nature figure generation
pkgs <- c("ggplot2", "ggpubr", "patchwork", "cowplot", "scales", "ggrepel", "readxl", "reshape2", "grid")
inst <- rownames(installed.packages())
to_install <- setdiff(pkgs, inst)

if (length(to_install) > 0) {
  cat("Installing missing packages:", paste(to_install, collapse = ", "), "\n")
  install.packages(to_install, repos = "https://cloud.r-project.org")
} else {
  cat("All required R packages are already installed.\n")
}
