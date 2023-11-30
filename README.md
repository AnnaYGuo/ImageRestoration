# ImageRestoration
Image sizes:
1. June Brewer          644x773         96dpi           32bit
2. Wilhelmina Perry     876x944         144dpi          32bit
3. Redd Dudley          1351x1656       600dpi          24bit
4. Arleen Lawson        1220x1746       600dpi          32bit
##Day 2 (11.29.23)
###Planning
* Meet with grad student whenever available
1. Consolidate results and narrow down models
2. Run 4 sample photos with all models
    * convert tif files (higher quality?) to png

Models/Tools
* fotor.com
* ILO (cuda required)
* Microsoft
* SuperSR (cuda required)
* PSLD
* ancestry
* hotpot.ai
Additional Considerations
* Conversions to jpeg inputs may work better than png on some models
##Day 1 (11.28.23)
### 
* Fotor is surprisingly good (but tends to apply makeup)
* Microsoft is good for scratches
* PLSD is bad
###Planning
Potential Models:
1. ILO (https://github.com/giannisdaras/ilo) (Anna, Luke)
2. PLSD (Arnold)
3. SuperSR (Isshan)
4. Microsoft (Raymond)
4. HuggingFace (Brandon)
Evaluation:
1. Manual Check
2. Structural Similarity Index (SSI)
3. Peak Signal-to-Noise Ratio (PSNR)
4. Visual Information Fidelity (VIF)
5. Crowd Sourcing/Polling


MPRNet
from PIL import __version__ as PILLOW_VERSION in /home/ayg479/opt/anaconda3/envs/pytorch1/lib/python3.7/site-packages/torchvision/transforms/functional.py
