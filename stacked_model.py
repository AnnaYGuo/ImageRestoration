import os
import subprocess

microsoft_cmd = "python Microsoft/Bringing-Old-Photos-Back-to-Life/run.py \
--input_folder test_set/img_preprocessed \
--output_folder Microsoft/results \
--GPU 1 \
--with_scratch \
--HR"

preprocessing_cmd = ""

stablesr_cmd = ""

for root, _, files in os.walk('img_in'):
    for file in files:
        if file.lower().endswith('.png'):
            # remove scratches (Microsoft)
            subprocess.run('bash -c "conda activate microsoft; ' + microsoft_cmd + '"')
            # run preprocessing script
            
            # StableSR
            # upscale further