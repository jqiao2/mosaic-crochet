# High Level Design

## Requirements

### Hard Requirements

* User image upload

### Inputs

* Two toned image (black and white)
* Width (in stitches)

### Outputs

* Crochet pattern grid
    * Shades of final output
    * Xs for each double crochet

#### Algo Requirements

* Mosaic crochet colors must alternate every line
* A reach-down double crochet must reach down to a stitch of the same color

* Constants that need to be defined
    * single-stitch threshold
    * double stitch threshold (could be the same)

1. Start from bottom row, work your way up
    1. Each column is independent (diagonal stitches in later update)
3. Assume white row WLOG: if pixel is greater than threshold set display color to white
    1. If not, set display color to black
4. If pixel below (black row) has display color as white, two cases:
    1. White row below display pixel is white: set current pixel to double crochet
    2. White row below display pixel is black: shouldn't be? will have to check algo

#### Below-the-line requirements

* Custom double crochet width/height ratio
* Diagonal stitches
* More than two colors
* Reversible mosaic guide
* In service crop

### Soft Requirements

* Fancy ass UI