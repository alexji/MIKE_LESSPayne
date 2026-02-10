#!/bin/bash

commands="-12348"

while read p; do
    python /Users/alexji/lib/LESSPayne/LESSPayne/cli/run.py $commands $p
done < all_cfgs.txt


# python /Users/alexji/lib/LESSPayne/LESSPayne/cli/run.py $commands cfgs/cfg_antii-01n1.yaml
