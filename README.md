# Patent Novelty Analysis

## Description
This patent novelty analysis is a data pipeline that examines innovation trends across 1.16 million AI-relevant patents filed between 2016 and 2020. The tool combines Python-based NLP and classification with R statistical modeling to identify which technology domains are producing the most novel patents, how that's changing over time, and what specific innovation themes are driving those shifts.

## Features
* **Domain Classification:** Maps each patent to one of 10 technology domains (AI/ML, Computing/Software, Biotech/Medical, Semiconductors/Electronics, Energy/Power, and others) using official IPC (International Patent Classification) codes.
* **Novelty Trend Analysis:** Tracks average patent novelty scores by domain across 5 years to identify which fields are innovating fastest and which are slowing down.
* **Keyword Theme Extraction:** Surfaces the specific terms and phrases driving innovation within top domains year over year, revealing shifts in the type of work being patented (such as recognition → model training in AI/ML).
* **Statistical Trend Modeling:** Fits linear trend models per domain to quantify direction and rate of change, rather than relying on visual inspection alone.

## Technologies Used
* Python (pandas, json) — data loading, filtering, IPC-to-domain classification, keyword extraction
* R (tidyverse, ggplot2) — statistical trend analysis and visualization

## Setup
* Clone this repository
* Download `DeepPatentAI.csv` from [Figshare](https://doi.org/10.6084/m9.figshare.28578947) and place it in a local `data/` folder (excluded from this repo due to file size)
* Set up a Python virtual environment and install dependencies: `pip install pandas numpy`
* Install R and RStudio, then install the tidyverse package: `install.packages("tidyverse")`

## Usage
* Run `python/load_and_filter.py` to filter the dataset to 2016–2020 and clean missing values
* Run `python/build_domains.py` to classify each patent into a technology domain based on its primary IPC code
* Run `r/analysis.R` in RStudio to compute novelty trends by domain and generate visualizations
* Run `python/keyword_analysis.py` to extract top keyword themes for the fastest-growing domains
* Review outputs in the `output/` folder, including trend charts, summary tables, and the executive summary

## Key Findings
* Computing/Software and AI/ML were the two largest and fastest-growing domains by novelty score (+0.041 and +0.037 per year respectively), together representing nearly 45% of all patents analyzed.
* AI/ML patent language shifted from generic "recognition" and "detection" framing (2016–2017) toward explicit model-training terminology (2019–2020), reflecting a broader shift from applying pre-built models to building and refining them.
* Computing/Software showed a parallel shift toward higher-value, specific applications. "Recommendation method" and "natural language processing" entered the top keyword terms by 2020, replacing generic data-processing language.
* Semiconductors/Electronics showed the steepest novelty decline (−0.107/year) but on a small sample (~2,800 patents total), so this finding is directional rather than conclusive.

## Data Source & Attribution
This project uses `DeepPatentAI.csv`, part of the DeepInnovationAI dataset, licensed under [CC-BY 4.0](http://creativecommons.org/licenses/by/4.0/):

> Gong, H., Zou, H., Liang, X., Meng, S., Cai, P., Xu, X., & Qu, J. (2025). A global dataset mapping the AI innovation from academic research to industrial patents. *Scientific Data*, and figshare. https://doi.org/10.6084/m9.figshare.28578947

The dataset was developed by researchers at Shanghai Artificial Intelligence Laboratory and contains 2.35M AI-classified patent records with novelty scores derived from hypergraph-based innovation modeling. This project uses the DeepPatentAI.csv file only, filtered to patents from 2016–2020. No modifications were made to the original dataset beyond filtering and IPC-to-domain classification performed for this analysis.

## Limitations
* The dataset is pre-filtered to AI-relevant patents only, so smaller domains (Semiconductors, Energy) reflect AI-adjacent activity within those fields, not total patent volume in those industries.
* Dataset coverage ends at 2020; findings reflect historical trends rather than current-year activity.
* Domain classification uses each patent's primary IPC code only; patents with multiple IPC codes are categorized by their first-listed code.
