import os
import subprocess

# run in Bringing-Old-Photos-to-Life
microsoft_cmd = "python run.py \
--input_folder ../../test_set/img_in \
--output_folder ../results \
--GPU 1 \
--with_scratch \
--HR"

preprocessing_cmd = "python test_set/generate_test_imgs.py -r 512 -bw -i Microsoft/results -o test_set/img_preprocessed"

stablesr_cmd = ""

for root, _, files in os.walk('img_in'):
    for file in files:
        if file.lower().endswith('.png'):
            # remove scratches (Microsoft)
            os.chdir('Microsoft/Bringing-Old-Photos-Back-to-Life')
            subprocess.run('bash -c "conda activate microsoft; ' + microsoft_cmd + '"')
            # run preprocessing script
            
            # StableSR
            # upscale further