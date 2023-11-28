# ImageRestoration

Image sizes:
1. June Brewer          644x773         96dpi           32bit
2. Wilhelmina Perry     876x944         144dpi          32bit
3. Redd Dudley          1351x1656       600dpi          24bit
4. Arleen Lawson        1220x1746       600dpi          32bit

ILO:
1. git clone ilo (https://github.com/giannisdaras/ilo)
    May need to pip install torchvision, scikit-image, ninja
    if "CUDA_HOME environment variable is not set":
        conda install -c conda-forge cudatoolkit-dev
        conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
2. Change line 7 of lpips/__init__.py from "from skimage.measure import compare_ssim" to
    "from skimage.metrics import structural_similarity as compare_ssim" 
    (module has been renamed within the library)