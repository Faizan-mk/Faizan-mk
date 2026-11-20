#!/usr/bin/env bash
# Regenerate everything locally after editing your details.
# (The daily GitHub Action only refreshes the city.)
set -e
cd "$(dirname "$0")/.."
python scripts/fetch_contributions.py Faizan-mk || python scripts/fetch_contributions.py --sample
python scripts/render_city.py
python scripts/make_ascii_svg.py      # needs source-prepped.png (run: python scripts/prep_photo.py source-photo.jpg)
python scripts/make_info_card.py
python scripts/make_sections.py
python scripts/build_readme.py
