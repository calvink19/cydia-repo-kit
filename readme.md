# Cydia Repo Kit
### By CalvinK19
All-in-one tool to help with managing your APT repository.

```
    Cydia-Repo-Kit v1.0 (2024/11/10)
    by calvink19

    1) Clone Repository                 2) Depiction Checker
    3) Generate Packages File           4) Compress Packages File
    5) Sort Packages by Repo            6) Credits
```
### Functions:
1. Clone Repository  
   Downloads all files from the Packages.bz2 file.

2. Depiction Checker  
   Checks whether depictions have been archived on the WayBack Machine. If so, it applies the archived URL. If the depiction has not been archived, it removes the depiction URL from the Packages file.

3. Generate Packages file  
   Generates a Packages file based off deb files.

4. Compress Packages file  
   Compresses the Packages file into `.gz` and `.bz2`.

5. Sort Packages by Repo  
   Sorts deb files into different folders based off the repository URL.

6. Credits  
   Shows credits. Pretty simple.
   
***

Requires Python 3.9+.

`dpkg-sp.py` and `rc_libs.py` are all licensed under APACHE 2.0.
A copy of the license can be found under `LICENSE.txt`.

Thanks to:
- [@memory](https://github.com/memory) for the `pydpkg` library, a python implementation of dpkg-scanpackages (used only by `rc_libs.py`)
- [@supermamon](https://github.com/supermamon) for `dpkg-sp.py`, a python implementation of dpkg-scanpackages (mainly used)
- [@4ch12dy](https://github.com/4ch12dy) for `rc_libs.py`, originally from `4ch12dy/cydiarepor/cydiarepor.py`
- [u/Littens4Life](https://reddit.com/u/Littens4Life) for most of the Clone Repository code (modified)
