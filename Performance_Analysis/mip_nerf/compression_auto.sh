#!/bin/bash

HM_BIN="/root/HM/bin/TAppEncoderStatic"
HM_CFG="/root/HM/cfg/encoder_intra_main_444.cfg"

INPUT_DIR="/mnt/c/Users/PC012/Desktop/dataset/yuv"
OUTPUT_DIR="/mnt/c/Users/PC012/Desktop/dataset"

videos=(stump bonsai kitchen counter room garden bicycle flowers treehill)
widths=(622 390 388 388 388 648 618 628 634)
heights=(412 260 260 260 258 420 410 414 416)
frames=(126 292 279 240 311 185 195 173 141)
framerate=30

for i in "${!videos[@]}"; do
vid="${videos[$i]}"
w="${widths[$i]}"
h="${heights[$i]}"
f="${frames[$i]}"

```
echo "=== Encoding $vid ($w x $h, $f frames) ==="

$HM_BIN -c $HM_CFG \\
    -i "$INPUT_DIR/${vid}.yuv" \\
    -b "$OUTPUT_DIR/${vid}.hevc" \\
    -wdt $w \\
    -hgt $h \\
    -fr $framerate \\
    -f $f

```

done
