ILO:
1. git clone ilo (https://github.com/giannisdaras/ilo)
    May need to pip install torchvision, scikit-image, ninja
    if "CUDA_HOME environment variable is not set":
        conda install -c conda-forge cudatoolkit-dev
        conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
2. Change line 7 of lpips/__init__.py from "from skimage.measure import compare_ssim" to
    "from skimage.metrics import structural_similarity as compare_ssim" 
    (module has been renamed within the library)