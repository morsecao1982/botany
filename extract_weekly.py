#!/usr/bin/env python3
"""
Extract Botany-relevant Campbell Biology sections into one PDF PER WEEK of
the study plan (instead of one combined file), and assign each week to
Student A or Student B so two teammates can split initial deep study and
teach each other later.

Page numbers are 1-indexed as printed in the source PDF's own TOC.
Fixes applied vs. the original single-file extraction:
  - Ch.6 now starts at p.150 (was 147) -- skips cell-fractionation/scale-bar
    methodology content, starts right at the animal-vs-plant cell diagram.
  - Ch.25 now starts at p.580 (was 578) -- skips abiogenesis/RNA-world,
    starts at fossil-dating methodology (paleo-botany relevant).
  - Ch.28 now starts at p.653 (was 651) -- skips Trypanosoma/Euglena
    (disease parasites, not plant-relevant), starts at brown algae/seaweed.
"""
import pymupdf
from pathlib import Path

SRC = "Campbell Biology, 12th (2020)188MB.pdf"
OUT_DIR = Path("site/study-guide/weeks")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (filename, week label, student, [(title, [(start,end), ...]), ...])
WEEKS = [
    ("week01-cell-structure.pdf", "Week 1 — Plant Cell Structure", "A", [
        ("Ch.6 (partial) — Eukaryotic Cell Structure incl. Plant Organelles", [(150, 175)]),
    ]),
    ("week02-photosynthesis.pdf", "Week 2 — Photosynthesis", "A", [
        ("Ch.10 — Photosynthesis", [(237, 261)]),
    ]),
    ("week03-algae-land-plants.pdf", "Week 3 — Algae & How Plants Colonized Land", "B", [
        ("Ch.28 (partial) — Algae: Closest Relatives of Plants", [(653, 667)]),
        ("Ch.29 — Plant Diversity I: How Plants Colonized Land", [(668, 685)]),
    ]),
    ("week04-seed-plants-paleobotany.pdf", "Week 4 — Seed Plants & Paleo-botany", "B", [
        ("Ch.30 — Plant Diversity II: Evolution of Seed Plants", [(686, 703)]),
        ("Ch.25 (partial) — Fossil Record & Colonization of Land", [(580, 587)]),
    ]),
    ("week05-vascular-plant-structure.pdf", "Week 5 — Vascular Plant Structure & Growth", "A", [
        ("Ch.35 — Vascular Plant Structure, Growth & Development", [(808, 833)]),
    ]),
    ("week06-transport-nutrition.pdf", "Week 6 — Transport, Soil & Nutrient Deficiencies", "A", [
        ("Ch.36 — Resource Acquisition & Transport in Vascular Plants", [(834, 854)]),
        ("Ch.37 — Soil and Plant Nutrition (incl. Nutrient Deficiencies)", [(855, 871)]),
    ]),
    ("week07-reproduction-gmos.pdf", "Week 7 — Reproduction, Genetics & GMOs", "B", [
        ("Ch.38 — Angiosperm Reproduction & Biotechnology (incl. GMOs)", [(872, 891)]),
    ]),
    ("week08-signals-disease.pdf", "Week 8 — Plant Signals, Disease & Defense", "B", [
        ("Ch.39 — Plant Responses to Signals (incl. Pathogen/Herbivore Defense)", [(892, 921)]),
        ("Ch.31 (partial) — Fungi: Nutrition, Mycorrhizae & Plant Disease", [(704, 710), (717, 722)]),
    ]),
    ("week09-ecology.pdf", "Week 9 — Competition & Nutrient Cycling", "Both", [
        ("Ch.54 (partial) — Competition & Species Interactions", [(1265, 1271)]),
        ("Ch.55 (partial) — Energy Flow & Nutrient Cycling in Ecosystems", [(1289, 1290), (1298, 1302)]),
    ]),
]

def main():
    src = pymupdf.open(SRC)
    print(f"{'File':40s} {'Student':6s} {'Pages':6s}  Week")
    print("-" * 90)
    for fname, week_label, student, sections in WEEKS:
        out = pymupdf.open()
        toc = []
        for title, ranges in sections:
            start_out_page = out.page_count + 1
            for start_1idx, end_1idx in ranges:
                out.insert_pdf(src, from_page=start_1idx - 1, to_page=end_1idx - 1)
            toc.append((1, title, start_out_page))
        out.set_toc(toc)
        out_path = OUT_DIR / fname
        out.save(str(out_path), garbage=4, deflate=True)
        print(f"{fname:40s} {student:6s} {out.page_count:6d}  {week_label}")
        out.close()
    src.close()

if __name__ == "__main__":
    main()
