#!/bin/bash

# Create directories if they don't exist
mkdir -p deckTex
mkdir -p deckIntermediate
mkdir -p deckPDF

python deck_generator.py

for file in deckTex/*; do
  pdflatex -output-directory deckIntermediate $file
done

mv deckIntermediate/*pdf deckPDF