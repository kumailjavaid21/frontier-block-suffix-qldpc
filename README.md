# Compiled block-parity lookahead for finite-frontier quantum LDPC decoding — reported aggregate results

This is a curated, results-only release for the paper's Studies A–C. It contains 15 aggregate numerical files, seven original vector result PDFs, provenance, and a read-only aggregate verification script. It preserves the paper-relevant comparator, control, uncertainty, and adverse-result rows. It is not the complete research history or a standalone reproduction of the decoding experiments.

The method is an attributed extension to **Frontier**, introduced by Anthony Leverrier and Rüdiger Urbanke in [*Approximating optimal decoding of quantum LDPC codes with narrow frontiers*, v1](https://arxiv.org/html/2606.20513v1). The inherited implementation reference is the [upstream Frontier repository at commit `5d5a60968182eb17cdc12c5ac1949732ead0905b`](https://github.com/aleverrier/frontier/tree/5d5a60968182eb17cdc12c5ac1949732ead0905b). This release does not claim an independently invented decoder or a general quantum speedup.

## Reported studies

| Paper study | Historical label | Evidence and boundary |
| --- | --- | --- |
| Study A | C10 | BB144, circuit error-rate parameter p=0.006, 32,768 paired shots per X/Z memory sector. Preserved b4 K512 versus parent K640 met the original paired risk guard of +0.005 and warm B128 cost contract. Complete service was 51.731441 versus 67.726320 ms/output, ratio 0.76383. This is amortized batched GPU service, not B1 latency, a CPU speedup, energy, or universal hardware evidence. |
| Study B | C11 | Secondary controlled scoring ablations, parent envelope, external comparator qualification, and bounded scaling screens. These retain their original cohorts and uncertainty. They are not additional confirmatory samples or evidence of superiority to every parent setting or external decoder. |
| Study C | C12 | BB144, p=0.006, 65,536 paired shots per sector. b4 errors were X: 9,552 versus preserved b2: 9,988; Z: 8,948 versus b2: 9,649. Repeated timing applies to physical GPU1 only. B2 is the specifically preserved recipe, not all pairwise methods. Smaller attribution cohorts and BB288 screens remain secondary. |

Do not pool C10/C11/C12 into a new confirmatory dataset or combine X/Z into an undeclared endpoint. The original PDFs retain their historical study labels. The C10 cost reduction is against parent K640: the equal-K512 comparison instead has a 3.46% service premium. Native CPU/B1 costs, adverse regimes, and uncertainty remain in the released tables. BB288 results are bounded operating screens, not a threshold estimate or a size-only conclusion.

The construction computes exact within-block future-parity laws from model-only compiled tables. Their combination into an across-block pruning score is approximate. Frontier's boundary/logical mass recursion, merging, pruning, ordering and committee remain inherited. The released comparisons do not establish equivalence to the authors' original detector-pair experiment, historical priority for pairwise lookahead, or an irreducible four-way mechanism.

## Files and verification

All release assets are in [`published_results/`](published_results/). Its [file map](published_results/README.md) links the tables and result PDFs to the studies. [Method and evidence scope](published_results/METHOD_SCOPE.md) records the attribution and reproduction limits.

Run the copied verifier with Python 3.10 or newer:

```sh
python published_results/audit_manuscript_data.py --root published_results
```

SciPy enables recomputation of the saved exact paired binomial tests and Clopper–Pearson component intervals. Without SciPy, the script explicitly reports those statistical checks as skipped. The included fresh [`AUDIT_RESULTS.json`](published_results/AUDIT_RESULTS.json) records **211 checks, PASS, zero failures**, including the SciPy statistical checks. This audit checks aggregate arithmetic and copied-file integrity; it does not rerun quantum simulation, decoder inference, or timing bootstraps.

[`DATA_PROVENANCE.csv`](published_results/DATA_PROVENANCE.csv) and [`FIGURE_PROVENANCE.csv`](published_results/FIGURE_PROVENANCE.csv) retain the original relative source identifiers and authoritative SHA256 values. Fourteen numerical files and all seven PDFs are byte-identical historical copies. `data_compiler_summary.csv` is derived accounting; its formula is documented in the data provenance. [`RELEASE_MANIFEST.csv`](published_results/RELEASE_MANIFEST.csv) gives root-relative paths, byte lengths, hashes and provenance for every other tracked release file; it excludes its own hash to avoid circularity.

This repository distributes no manuscript source or manuscript PDF, raw physical shot-level dataset, runtime implementation, native/CUDA binary, model environment, trained policy, private archive, or complete exploratory history. An unsuccessful adaptive-width exploratory follow-up is outside this curated Studies A–C release; its detailed artifacts are not distributed. The reported experiments used circuit simulations, not physical-QPU measurements.

Upstream software and third-party implementations retain their own attribution and licensing. They are not copied or relicensed here, and no repository-wide software-license claim is made. This repository does not establish journal acceptance, a paper DOI, independent hardware replication, or full public scientific re-execution.
