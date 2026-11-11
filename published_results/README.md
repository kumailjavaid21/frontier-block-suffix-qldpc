# Released aggregate evidence

Historical C10, C11 and C12 correspond to manuscript Studies A, B and C. These are separate studies and separate X/Z memory-sector endpoints. All files below retain their authenticated original bytes; the compiler summary is explicitly derived accounting.

| Evidence | Files |
| --- | --- |
| Study A/C10 primary, accuracy and service | `data_C10_primary.json`, `data_C10_accuracy.csv`, `data_C10_service.csv` |
| Study B/C11 secondary ablation, parent, paired uncertainty and external comparison | `data_C11_ablation.csv`, `data_C11_parent.csv`, `data_C11_paired.csv`, `data_C11_external.csv` |
| Study C/C12 primary and complete paired/accuracy tables | `data_C12_primary.csv`, `data_C12_pairs.csv`, `data_C12_accuracy.csv` |
| Study C/C12 secondary scaling, attribution and native/B1 service | `data_C12_bb288.csv`, `data_C12_attribution.csv`, `data_C12_native_cost.csv`, `data_C12_B1_cost.csv` |
| Derived compiler accounting | `data_compiler_summary.csv`; source records and formula in `DATA_PROVENANCE.csv` |

| Original result PDFs | Mapping |
| --- | --- |
| `fig_accuracy_cost.pdf`, `fig_paired_risk.pdf` | Study A/C10; primary and secondary cohorts retain their labels and intervals |
| `fig_parent_envelope.pdf`, `fig_scaling_screens.pdf` | Study B/C11 secondary parent/scaling screens |
| `fig_b2_confirmation.pdf`, `fig_bb288.pdf` | Study C/C12 primary B2 comparison and labeled bounded scaling screens |
| `fig_attribution.pdf` | C13 evidence synthesis of distinct C11 NP2 and C12 all-pair controls; different cohorts are not pooled |

`DATA_PROVENANCE.csv` and `FIGURE_PROVENANCE.csv` map each result file to its original relative evidence identifier and SHA256. The original source package and historical dossier were authenticated during curation; no private source-machine locations are needed to inspect these identifiers.

`audit_manuscript_data.py` is the sole verification script in this release. Run it from the repository root as documented in the root README. `AUDIT_RESULTS.json` is its fresh output for these staged files, including the statistical checks available in the recorded SciPy version. `RELEASE_MANIFEST.csv` hashes all other tracked files, using paths relative to the repository root. It deliberately excludes itself.

No adverse row, denominator, p-value, interval or numerical precision was edited. The aggregate audit verifies saved-file agreement, not decoder/compiler correctness, a timing-bootstrap replay, or independent hardware reproduction. See `METHOD_SCOPE.md` for the method and scientific boundary.
