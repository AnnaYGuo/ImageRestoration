#TACC Setup/Usage
(11.30.2023)
##Setup
1. Ensure Multi-Factor Authentication is setup
    * https://docs.tacc.utexas.edu/basics/mfa/
2. SSH into TACC with the following command in a terminal `ssh {tacc_username}@login2.frontera.tacc.utexas.edu`
    _Note: Going through VSCode will cause many extra downloads, which is space inefficient_
3. Install conda
    https://docs.conda.io/projects/miniconda/en/latest/index.html
    1. `wget {link}`
        * example link: https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        * need to use right click instead of Ctrl+V to paste in terminal
    2. `bash Miniconda3-latest-Linux-x86_64.sh`
    3. Hold \<ENTER\>, type `yes`, install into `$WORK/Miniconda3`, type `yes`
    4. `exit` to save changes (relogin if desired)
##Access
1. 
##Useful Commands
###General
* `pwd` checks current path
* `scp {source} {destination}`
    * {local_path} 
    * {tacc_username}@login2.frontera.tacc.utexas.edu:{server_path}
###Conda
* `conda env list`
###TACC
* `module list`
* `module avail`
* `module load {desired_module}` 
* `idev -m {minutes_timeout} -p {rtx-dev}`
    * `rtx-dev` specifies a GPU node rather than a regular node

    `usr/local/etc/taccinfo`