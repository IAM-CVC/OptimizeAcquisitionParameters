# Multi-objective Pareto Analysis for Optimization of Acquisition Parameters and Interactive Visualization

This repository provides an implementation of a **multi-objective Pareto-based framework** for the analysis of acquisition parameter configurations, together with an **interactive visualization tool** for exploring the resulting solution spaces.
The code is generic, dimension-agnostic, and applicable to a wide range of acquisition or system optimization problems.


## Contents

- `ExplainHQ.py and ExplainHQV2.py`
  Implementation of the multi-objective Pareto methodology.

- `HQ_ParetoCubes.html and HQ_ParetoCubesV2.html`  
  Interactive visualization tool for exploring Pareto layers and admissible regions. Download and execute it into a navigator.

- `Radiolung3Param.csv`
  Example .csv with p-values for the different parameter combinations.
  

## Multi-objective Pareto Analysis

The Pareto analysis module implements a generic multi-objective framework to identify and organize acquisition configurations according to dominance relations.

Given a set of configurations and their associated p-val, the method:
- extracts hierarchical Pareto layers (HQ levels) using iterative dominance analysis,
- defines inequality-based admissible regions associated with each Pareto-optimal configuration,
- aggregates these regions by quality level to characterize flexible, quality-preserving parameter subspaces.

The implementation supports an arbitrary number of parameters and does not rely on geometric assumptions such as convexity.


## Interactive Visualization Tool

The visualization module provides an interactive interface to explore the acquisition parameter space when dimensionality permits (e.g., three parameters).

The tool displays:
- valid configurations as points,
- hierarchical Pareto layers (HQ levels),
- inequality-defined admissible regions associated with Pareto-optimal configurations.

Users can toggle admissible regions by HQ level and inspect overlaps between regions, highlighting that Pareto-optimal solutions represent **sets of acceptable configurations rather than isolated operating points**.

The visualization is intended as an exploratory aid and is not a required component of the methodology.


## Notes

- The methodology is applicable to higher-dimensional parameter spaces, where analysis relies on quantitative summaries rather than direct visualization.
- The visualization component is provided for interpretability and illustrative purposes.


## License

This project is provided for research and academic use. Please cite the associated publication if you use this code.
