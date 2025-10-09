# Chess960 Card Generator - Documentation

## Overview
This LaTeX document (`chess_card.tex`) generates a 3"×3" printable card for 4-player Chess960. The card features chess piece setups at all four corners with rotational symmetry, allowing four players to sit around a square table with each player having their starting position visible from their perspective.

## Output Description
- **Card Size**: 3 inches × 3 inches (no margins)
- **Center**: "CHESS 960" text label
- **Four Corners**: Each corner has 2 rows of 8 chess squares with pieces
- **Rotational Symmetry**: Each corner is rotated 0°, 90°, 180°, 270° so pieces face the correct direction for each player

## Document Structure

### Lines 1-11: Document Setup and Preamble

```latex
\documentclass[12pt]{article}
```
- Uses standard article class with 12pt base font size

```latex
\usepackage[margin=0.0in,paperwidth=3in,paperheight=3in]{geometry}
```
- Sets paper to exactly 3"×3" with zero margins (full bleed)
- This gives us the entire page for our chess board

```latex
\usepackage{tikz}
```
- TikZ is the graphics package used to draw squares, position pieces, and handle rotations

```latex
\usepackage{xskak}
```
- Chess package providing chess piece symbols with proper styling
- Provides commands like `\WhiteRookOnBlack`, `\WhitePawnOnWhite`, etc.
- These commands automatically render chess pieces with appropriate backgrounds

```latex
\usepackage{graphicx}
```
- Graphics package for general image manipulation (dependency for xskak)

```latex
\pagestyle{empty}
```
- Removes page numbers and headers/footers

```latex
\definecolor{lightgray}{gray}{0.8}
\definecolor{darkgray}{gray}{0.8}
```
- Defines the two colors for the chessboard squares
- Both set to 0.8 (80% gray) - note: these are currently the same color
- To get alternating squares, change one to a different value (e.g., darkgray to 0.5)

### Lines 12-14: Document Start and TikZ Setup

```latex
\begin{document}
\centering
```
- Begins document and centers content on page

```latex
\begin{tikzpicture}[x=0.5in,y=0.5in]
```
- Starts TikZ drawing environment
- Sets coordinate system: 1 unit = 0.5 inches
- With this scale, our card of 3 inches = 6 units in each direction

### Lines 15-18: Coordinate System Constants

```latex
\useasboundingbox (0,0) rectangle (6,6);
```
- Explicitly sets the drawing boundary to prevent overflow
- (0,0) is bottom-left, (6,6) is top-right
- 6 units × 0.5in/unit = 3 inches

```latex
\def\cardsize{6}
```
- Defines the card size in our coordinate units (6 = 3 inches)

```latex
\def\squaresize{\fpeval{6/11}}
```
- Calculates size of each chess square
- Formula: 6 units ÷ 11 = ~0.545 units per square
- Why 11? Because each corner has: 1 empty square + 8 chess squares + 2 rows = leaves space for center

### Line 20: Center Label

```latex
\node[align=center] at (3 , 3) {\textbf{CHESS}\\ \textbf{960}};
```
- Places "CHESS 960" text at the center of the card (3, 3)
- `align=center` centers the text
- `\\` creates a line break between "CHESS" and "960"
- `\textbf{}` makes text bold

### Lines 22-67: Main Loop - Four Corner Setups

This is the core of the document. It uses nested loops to programmatically generate all four chess setups.

#### Outer Loop (Lines 23-67): Iterate Through Corners

```latex
\foreach \corner in {0,1,2,3} {
```
- Loops 4 times for the 4 corners
- `\corner` = 0: bottom-left
- `\corner` = 1: bottom-right
- `\corner` = 2: top-right
- `\corner` = 3: top-left

```latex
\pgfmathtruncatemacro{\angle}{\corner * 90}
```
- Calculates rotation angle for this corner
- Corner 0 → 0°, Corner 1 → 90°, Corner 2 → 180°, Corner 3 → 270°
- `\pgfmathtruncatemacro` ensures we get an integer (needed for conditionals)

```latex
\pgfmathsetmacro{\cornerx}{(\corner==1 || \corner==2) ? \cardsize : 0}
\pgfmathsetmacro{\cornery}{(\corner==2 || \corner==3) ? \cardsize : 0}
```
- Determines the (x,y) position of each corner
- Uses ternary operator: `(condition) ? value_if_true : value_if_false`
- Results:
  - Corner 0: (0, 0) - bottom-left
  - Corner 1: (6, 0) - bottom-right
  - Corner 2: (6, 6) - top-right
  - Corner 3: (0, 6) - top-left

#### Transformation Scope (Lines 29-66)

```latex
\begin{scope}[rotate around={\angle:(\cornerx,\cornery)}, shift={(\cornerx,\cornery)}]
```
- Creates a transformation scope for this corner
- `shift={(\cornerx,\cornery)}`: Moves origin to the corner position
- `rotate around={\angle:(\cornerx,\cornery)}`: Rotates everything around the corner point by `\angle` degrees
- Everything drawn inside this scope will be transformed automatically

#### Inner Loop (Lines 31-65): Draw 8 Squares and Pieces

```latex
\foreach \x in {0,...,7} {
```
- Loops through 8 files (columns) of the chessboard

```latex
\pgfmathsetmacro{\xpos}{\x * \squaresize + \squaresize/2}
```
- Calculates the center x-position of square \x
- Formula: (column_index × square_width) + (half_square_width)
- This gives us the center of each square for piece placement

#### Square Coloring (Lines 34-41)

```latex
\pgfmathtruncatemacro{\colormod}{mod(\x,2)}
```
- Determines if column is even (0) or odd (1) using modulo
- This creates the alternating pattern

```latex
\ifnum\colormod=0
  \fill[darkgray] (\x*\squaresize, 1*\squaresize) rectangle (\x*\squaresize+\squaresize, 2*\squaresize);
  \fill[lightgray] (\x*\squaresize, 2*\squaresize) rectangle (\x*\squaresize+\squaresize, 3*\squaresize);
\else
  \fill[lightgray] (\x*\squaresize, 1*\squaresize) rectangle (\x*\squaresize+\squaresize, 2*\squaresize);
  \fill[darkgray] (\x*\squaresize, 2*\squaresize) rectangle (\x*\squaresize+\squaresize, 3*\squaresize);
\fi
```
- If column is even (0): darkgray on row 1, lightgray on row 2
- If column is odd (1): lightgray on row 1, darkgray on row 2
- This creates the classic chessboard alternating pattern
- Note: Rows start at 1*squaresize (not 0) to leave gap between corner and board
- Each rectangle is drawn from bottom-left to top-right corners

#### Piece Placement (Lines 43-64)

**Back Rank Pieces (Lines 43-53):**
```latex
\node[rotate=\angle] at (\xpos, \fpeval{(6/11)*(3/2)}) {
```
- Places pieces at the center of each square in the first (back) rank
- `rotate=\angle`: Counter-rotates the piece so it stays upright when viewed from that corner
- Y-position: `(6/11)*(3/2)` = 1.5 square heights = middle of second row
- `\small`: Reduces piece size to fit nicely in squares

Piece assignment based on column:
- Column 0: `\WhiteRookOnBlack` (Rook on dark square)
- Column 1: `\WhiteKnightOnWhite` (Knight on light square)
- Column 2: `\WhiteBishopOnBlack` (Bishop on dark square)
- Column 3: `\WhiteQueenOnWhite` (Queen on light square)
- Column 4: `\WhiteKingOnBlack` (King on dark square)
- Column 5: `\WhiteBishopOnWhite` (Bishop on light square)
- Column 6: `\WhiteKnightOnBlack` (Knight on dark square)
- Column 7: `\WhiteRookOnWhite` (Rook on light square)

This is the standard chess starting position: R-N-B-Q-K-B-N-R

**Pawns (Lines 54-64):**
```latex
\node[rotate=\angle] at (\xpos, \fpeval{(6/11)*(5/2)}) {
```
- Places pawns in the second rank
- Y-position: `(6/11)*(5/2)` = 2.5 square heights = middle of third row
- Pawns alternate `OnWhite` and `OnBlack` based on the column parity
- This ensures each pawn is on the opposite color from its back rank piece

## Compilation

To compile this file to PDF:
```bash
pdflatex chess_card.tex
```

This will generate `chess_card.pdf`.

## Customization Guide

### Change Square Colors
Modify lines 9-10:
```latex
\definecolor{lightgray}{gray}{0.9}  % Lighter squares
\definecolor{darkgray}{gray}{0.4}   % Darker squares
```

### Change Card Size
Modify line 2 (must maintain square aspect):
```latex
\usepackage[margin=0.0in,paperwidth=4in,paperheight=4in]{geometry}
```
And update line 14 to match (in half-inches):
```latex
\begin{tikzpicture}[x=0.5in,y=0.5in]  % Keep this for 4"
```

### Change to Chess960 Position
Modify lines 45-52 to use a different piece arrangement. For example, position #518:
```latex
\ifnum\x=0 \WhiteBishopOnBlack\fi
\ifnum\x=1 \WhiteKnightOnWhite\fi
\ifnum\x=2 \WhiteKingOnBlack\fi
\ifnum\x=3 \WhiteQueenOnWhite\fi
\ifnum\x=4 \WhiteBishopOnBlack\fi
\ifnum\x=5 \WhiteRookOnWhite\fi
\ifnum\x=6 \WhiteKnightOnBlack\fi
\ifnum\x=7 \WhiteRookOnWhite\fi
```

### Remove Center Label
Comment out or delete line 20:
```latex
% \node[align=center] at (3 , 3) {\textbf{CHESS}\\ \textbf{960}};
```

### Change Piece Size
Modify `\small` on lines 44 and 55 to:
- `\tiny` - smaller pieces
- `\footnotesize` - slightly smaller
- `\normalsize` - regular size
- `\large` - larger pieces

## Dependencies

Required LaTeX packages:
- **geometry**: Page layout control
- **tikz**: Drawing and graphics (part of pgf package)
- **xskak**: Chess piece symbols and styling
- **graphicx**: Image handling

On Ubuntu/Debian systems:
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-games
```

## Design Rationale

**Why programmatic generation?**
- Single definition of the piece layout
- Easy to modify for different Chess960 positions
- Automatically maintains rotational symmetry
- Much cleaner than copying the same code 4 times

**Why this square size calculation (6/11)?**
- Each corner needs 8 squares wide
- We want a gap between corners and center
- We have 2 rows of pieces, starting offset from corner
- 6/11 ≈ 0.545 provides good balance

**Why counter-rotate pieces?**
- The `scope` rotation rotates everything including pieces
- Without counter-rotation, pieces would be upside-down
- `rotate=\angle` on each piece node keeps them upright

## Common Issues

**Pieces overlap center:**
- Increase the gap by changing line 36 from `1*\squaresize` to `1.5*\squaresize`

**Colors don't show:**
- Check that lightgray and darkgray are different values
- Line 10 should be something like `\definecolor{darkgray}{gray}{0.5}`

**PDF is blank:**
- Ensure all packages are installed
- Check the log file (chess_card.log) for errors
- Verify chess piece commands are from xskak package

## File Structure

```
2025-chess960/
├── chess_card.tex       # Main LaTeX source
├── chess_card.pdf       # Generated output (after compilation)
├── chess_card.log       # Compilation log
├── chess_card.aux       # LaTeX auxiliary file
└── Claude.md           # This documentation file
```
