#!/usr/bin/env python3
"""
Extract only the Botany-relevant sections of Campbell Biology 12e into a
single trimmed study PDF, with bookmarks, mapped to the official Science
Olympiad Division B Botany event rules.

Page numbers below are 1-indexed as printed in the PDF's own TOC (verified
to equal pymupdf's 0-indexed page number + 1).
"""
import pymupdf

SRC = "Campbell Biology, 12th (2020)188MB.pdf"
OUT = "study-guide/Botany-Source-Extract.pdf"

# (bookmark title, rules-topic tag, [(start_1indexed, end_1indexed), ...])
SECTIONS = [
    ("Ch.6 (partial) — Eukaryotic Cell Structure incl. Plant Organelles",
     "Plant cell structure", [(147, 175)]),

    ("Ch.10 — Photosynthesis",
     "Photosynthesis", [(237, 261)]),

    ("Ch.25 (partial) — Fossil Record & Colonization of Land",
     "History of botany / paleo-botany", [(578, 587)]),

    ("Ch.28 (partial) — Algae: Closest Relatives of Plants",
     "Algae vs. multicellular plants", [(651, 667)]),

    ("Ch.29 — Plant Diversity I: How Plants Colonized Land",
     "Major plant divisions / paleo-botany", [(668, 685)]),

    ("Ch.30 — Plant Diversity II: Evolution of Seed Plants",
     "Major plant divisions (gymnosperms, angiosperms)", [(686, 703)]),

    ("Ch.31 (partial) — Fungi: Nutrition, Mycorrhizae & Plant Disease",
     "Plant diseases / nutrient cycling", [(704, 710), (717, 722)]),

    ("Ch.35 — Vascular Plant Structure, Growth & Development",
     "Roots, stems, leaves, growth & differentiation", [(808, 833)]),

    ("Ch.36 — Resource Acquisition & Transport in Vascular Plants",
     "Transport/storage of gases, water, nutrients", [(834, 854)]),

    ("Ch.37 — Soil and Plant Nutrition (incl. Nutrient Deficiencies)",
     "Plant diseases: nutrient deficiencies", [(855, 871)]),

    ("Ch.38 — Angiosperm Reproduction & Biotechnology (incl. GMOs)",
     "Plant genetics/reproduction; GMOs; foodstuffs", [(872, 891)]),

    ("Ch.39 — Plant Responses to Signals (incl. Pathogen/Herbivore Defense)",
     "Growth & differentiation; plant diseases/infections", [(892, 921)]),

    ("Ch.54 (partial) — Competition & Species Interactions",
     "Competition in the plant community; use by animals", [(1265, 1271)]),

    ("Ch.55 (partial) — Energy Flow & Nutrient Cycling in Ecosystems",
     "Role of plants in global energy/nutrient cycles", [(1289, 1290), (1298, 1302)]),
]

def main():
    src = pymupdf.open(SRC)
    out = pymupdf.open()
    toc = []  # (level, title, page_in_output_1indexed)

    for title, tag, ranges in SECTIONS:
        start_out_page = out.page_count + 1  # 1-indexed page this section starts on
        for start_1idx, end_1idx in ranges:
            out.insert_pdf(src, from_page=start_1idx - 1, to_page=end_1idx - 1)
        toc.append((1, title, start_out_page))
        pages_used = sum(e - s + 1 for s, e in ranges)
        print(f"{title:65s} {pages_used:4d} pages  (source pp. {ranges})")

    out.set_toc(toc)
    out.save(OUT, garbage=4, deflate=True)
    print(f"\nWrote {OUT}: {out.page_count} pages total (source book was {src.page_count} pages)")

if __name__ == "__main__":
    main()
