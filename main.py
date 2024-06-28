print("Initializing:")
print("Importing packages.")

try:
    from pydpkg import Dpkg
    import os
    import requests
    import urllib.request
    from time import sleep
    import bz2
    import gzip
    from pathlib import Path
    import subprocess
    import shutil
    import re
except:
    print("""
Error when importing libraries. To fix, try running "pip install -r requirements.txt" in this directory.
If you're still having errors, please message /u/East-Box-8015.
""")
    input("Press ENTER to exit.")
    exit(1)
    
print("Defining functions.")

################################################################################## Functions

from rc_libs import * # import functions from repo archiver file

# Function to check whether the URL provided is valid
def get_cydiarepo_reachable_url(repoURL):
    # cydiarepo_Packages_URL = repoURL + '/Packages'
    # cydiarepo_Packages_bz2_URL = repoURL + '/Packages.bz2'
    # cydiarepo_Packages_gz_URL = repoURL + '/Packages.gz'
    # print(f"cydiarepo_Packages_URL: {cydiarepo_Packages_URL}")
    cydiarepo_Packages_URL = join_url_path_components(repoURL, '/Packages')
    cydiarepo_Packages_bz2_URL = join_url_path_components(repoURL, '/Packages.bz2')
    cydiarepo_Packages_gz_URL = join_url_path_components(repoURL, '/Packages.gz')
    # print(f"cydiarepo_Packages_URL: {cydiarepo_Packages_URL}")
    
    cydiareporeachable_URL = None
    usesDebian = None

    if handle_old_cydia_repo(repoURL):
        ret = handle_old_cydia_repo(repoURL)
        zip_type = ret[1]
        if zip_type == "gz":
            cydiarepo_Packages_gz_URL = ret[0]
            usesDebian = True
        elif zip_type == "bz2":
            cydiarepo_Packages_bz2_URL = ret[0]
            usesDebian = True
        else:
            # print("[-] unknown old cydia repo zip type")
            # exit(1)
            return cydiarepo_reachable_URL, usesDebian
    
    is_need_unzip = False
    unzip_type = ''
    
    usesDebian = usesDebian if usesDebian is True else False
    if is_url_reachable(cydiarepo_Packages_URL):
        cydiarepo_reachable_URL = cydiarepo_Packages_URL
    elif is_url_reachable(cydiarepo_Packages_bz2_URL):
        cydiarepo_reachable_URL = cydiarepo_Packages_bz2_URL
        is_need_unzip = True
        unzip_type = "bz2"
        
    elif is_url_reachable(cydiarepo_Packages_gz_URL):
        cydiarepo_reachable_URL = cydiarepo_Packages_gz_URL
        is_need_unzip = True
        unzip_type = "gz"
    else:
        # print(("[-] {} : did not find Packages or Packages.bz2 or Packages.gz file in this repo, verify it!".format(repoURL)))
        # exit(1)
        return cydiarepo_reachable_URL, None
        pass
    return cydiarepo_reachable_URL, usesDebian, cydiarepo_Packages_URL

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

print("Finished Initializing.")
############################################################################################
    
while True:
    clear()
    print("""

    Repo-Archive-Kit
    by calvink19

    1) Clone Repository                 2) Archive Depictions
    3) Check for archived depictions    4) Generate Packages File
    5) Compress Packages file           6) Sort Packages by Repo
    7) Credits
    """)
    mode = input("  > ")
    clear()

    ########################################################################################## Mode 1 # Clone Repository
    if mode == "1":
        url = ''
        while True:
            
            # Scuffed Mode Selection
            mode1 = input(f"""

    [Clone Repository]
    URL: {url}
    1) Set URL               2) Clone
    3) Go back to main menu

  > """)

            if mode1 == "1":
            
                url = input("   URL: ")
                print("   Verifying URL...")
                if not "http" in url: #append http:// to url
                    url = f"http://{url}"

                try:
                    get_cydiarepo_reachable_url(url)
                    print("   Set URL.")
                    input("   Press ENTER to continue. ")

                except:
                    print("   Not a valid URL.")
                    input("   Press ENTER to continue. ")
                    url = ''
                    
            elif mode1 == "2":
                
                if len(url) > 0:
                    if 'y' in input(f"""    Are you sure you want to clone {url}?
    [y/n] """).lower():
                        print("    Press CTRL + C to stop downloading.")
                        print("    Starting download...")
                        sleep(5) # Give people time to read the message
                        try:
                            os.system(f'python __repo-cloner__/cydiarepor.py {url} -s "" --preselection all')
                            print("Finished. Check the folder 'downloads'.")
                        except KeyboardInterrupt:
                            clear()
                            print("    Canceled.")
                    else:
                        print("    Canceled.")
                    input("    Press ENTER to continue. ")

                else:
                    print("    No URL has been set.")
                    input("    Press ENTER to continue. ")

            elif mode1 == "3":
                break
            
            clear()
    ########################################################################################## Mode 2 # Archive depictions
    elif mode == "2": #for later...
        print("Adding later")
        input("Press ENTER to continue.")
    ########################################################################################## Mode 3 # Check for archived depictions
    elif mode == "3": #for later...
        print("Adding later")
        input("Press ENTER to continue.")
    ########################################################################################## Mode 4 # Generate Packages file
    elif mode == "4":
        while True:
            clear()
            # Scuffed Mode Selection
            mode6 = input(f"""

    [Generate Packages]
    (FIX BY FILE!)
    1) By Folder             2) By File
    3) Go back to main menu

  > """)
            clear()
            if mode6 == "1":
                try:
                    os.mkdir('./debs')
                except FileExistsError:
                    pass
                print("\n\n    [Generate Packages]\n")
                input("    Move your deb files into the 'debs' directory.\n    Press ENTER once you have moved the files.\n    (this will delete older generated 'Packages' files.)")
                print("    Generating...")
                os.system("dpkg-sp.py --multiversion --output Generated_Packages ./debs")
                input("    Finished. Press ENTER to continue.")

            elif mode6 == "2":
                print("\n\n    [Sort Packages]\n")
                filename=input("    Type in the name of the file. Make sure it's in the same directory as 'main.py'.\n    (this will delete older generated 'Packages' files.)\n  > ")
                print("    Generating...")
                os.system("dpkg-sp.py --multiversion --output Generated_Packages ./{filename}")
                input("    Finished. Press ENTER to continue.")

            elif mode6 == "3":
                break
    ########################################################################################## Mode 5
    elif mode == "5": # Compress Packages file
        clear()
        print("\n\n    [Compress Packages File]\n")
        
        # Check whether directory exists. if not, create it.
        if not os.path.exists('./compress'):
            os.makedirs('./compress')
        
        input("    Move your Packages file into the 'compress' directory.\n    Press ENTER once you have moved the file.\n    (this will delete older generated files which are still in the folder.)")

        try: #delete older files
            os.remove("Packages.bz2")
            os.remove("Packages.gz")
        except:
            pass
        
        try: #compress files
            packages = open("./compress/Packages",'r', encoding='utf-8').read()
            newcontent = bz2.compress(packages.encode())
            f = open("./compress/Packages.bz2", "wb")
            f.write(newcontent)
            f.close()

            with open("./compress/Packages", 'rb') as orig_file:
                with gzip.open("./compress/Packages.gz", 'wb') as zipped_file:
                    zipped_file.writelines(orig_file)
            print("    Successfully generated Packages.bz2 and Packages.gz.")
        except:
            print("\n    Error- Try checking that the file is named Packages, or that you've put it in the correct folder.")
        input("    Press ENTER to continue.")

    ########################################################################################## Mode 6 # Sort Packages
    elif mode == "6":
        print("\n\n    [Sort Packages]\n")
        input("    Move your deb files into the 'debs' directory.\n    Press ENTER once you have moved the files.\n    (this will delete older generated 'Packages' files.)")
        print("    Generating...")

        try:
            os.mkdir('./temp')
        except FileExistsError:
            pass

        try:
            os.mkdir('./sort/__cracked')
        except FileExistsError:
            pass

        try:
            os.mkdir('./sort')
        except FileExistsError:
            pass

        # Delete all contents inside temp folder
        folder = './temp'
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        try:
            open("temp.txt", "x")
        except FileExistsError:
            pass

        # get count of deb files
        deb_files = [file for file in os.listdir('./debs') if file.endswith('.deb')]
        deb_count = len(deb_files)

        debsdone = 0
        
        # Loop through all files in the 'debs' directory
        for root, dirs, files in os.walk('./debs'):
            for file in files:
                packages = ''
                filename = file
                try:
                    if 'crack' in filename.lower():
                        os.rename(f"./debs/{file}", f"./sort/__cracked/{file}")
                    elif 'deb' in filename:
                        #print(f"    Processing file: {filename}")

                        os.rename(f"./debs/{file}", f"./temp/{file}")
                        os.system("python dpkg-sp.py --multiversion --output temp.txt ./temp")

                        sleep(0.5) # give file time to save
                        with open("temp.txt", "r", encoding="utf8") as f:
                            packages = f.read()


                        # Find Maintainer
                        maintainer_info = None
                        lines = packages.split('\n')

                        for line in lines:
                            if line.startswith("Sponsor: "):
                                maintainer_info = line[len("Sponsor: "):]
                                break

                        if maintainer_info == None:
                            for line in lines:
                                if line.startswith("Maintainer: "):
                                    maintainer_info = line[len("Maintainer: "):]
                                    break
                            #print(maintainer_info)

                        maintainerlist = ['']

                        # make compatible with folder names
                        modified_string = re.sub(r'[^a-zA-Z0-9]', '_', str(maintainer_info))

                        maintainer_dir = f'./sort/{modified_string}'
                        if not os.path.exists(maintainer_dir):
                            os.mkdir(maintainer_dir)

                        os.rename(f"./temp/{file}", f"{maintainer_dir}/{file}")

                        if modified_string not in maintainerlist:
                            maintainerlist.append(modified_string)

                        print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/{modified_string}/.")
                except:
                    print(f"    [{debsdone}/{deb_count}] Error on {file}. Not sorted.")

                    debsdone += 1


        shutil.rmtree('./temp')
        os.remove('temp.txt')

        input("\n    Finished.\n    Press ENTER to continue.")
        
    ########################################################################################## Mode 7 # Credits
    elif mode == "7":
        clear()
        print("""
   Credits:
 - @calvink19,                     for writing the Depiction Archiver, Wayback Machine Depiction, and the Package Sorter. 
 - @4ch12dy, @Acreson, and @JeffMv for the Repository Cloner code.
 - @memory,                        for the pydpkg library.
 - @supermamon,                    for the python implementation of dpkg-scanpackages.
""")
        input("   Press ENTER to continue.")
