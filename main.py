print("Initializing")
print("Importing packages")

try:
    from pydpkg import Dpkg
    import os
    import requests
    import urllib.request
    from time import sleep
    import bz2
    import gzip
    from pathlib import Path
    import shutil
    import re
    import hashlib
    import subprocess
    import datetime
except:
    print("""
An error occured when importing libraries. To fix it, try running "pip install -r requirements.txt" in this directory.
""")
    input("Press ENTER to exit.")
    exit(1)
    
print("Defining functions")

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

print("Initialized")

############################################################################################
    
while True:
    # oh dear here we go
    clear()
    print("""

    Cydia-Repo-Kit v1.0 (2024/11/10)
    by calvink19

    1) Clone Repository                 2) Depiction Checker
    3) Generate Packages File           4) Compress Packages File
    5) Sort Packages by Repo.           6) Credits
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

            if mode1 == "1": #Maybe add a "local mode" where Packages file is from a local file, if it's not possible to download it (as is the case for the Galactic Repo)
            
                url = input("   URL: ")
                print("   Verifying URL...")
                if not "http" in url:
                    url = f"http://{url}"

                try:
                    get_cydiarepo_reachable_url(url)
                    print("   Set URL.")
                    input("   Press ENTER to continue. ")

                except:
                    print("   Not a valid URL.")
                    print("   Warning: some sources which can be added on an iDevice are 'restricted' meaning that\n   computers (for some reason) cannot access them, like ZodTTD.\n   (you can see this when going to http://cydia.zodttd.com/repo/cydia/Release.)")
                    input("   Press ENTER to continue. ")
                    url = ''
                    
            elif mode1 == "2":
                
                if len(url) > 0:
                    if 'y' in input(f"""    Are you sure you want to clone {url}?
    [y/n] """).lower():
                        print("    Press CTRL + C to stop downloading.")
                        print("    Starting download...")
                        try:
                            # Original code from @hail.4803 in the iOSObscura Discord.
                            # It has been modified.
                            try:
                                pkg = requests.get(f"{url}/Packages.bz2")
                                print("Got Packages.bz2.")
                                print("Compressed length: " + str(len(pkg.content)))
                                #print("Uncompressed length: " + str(len(packages)))
                                packages = bz2.decompress(pkg.content).decode('ISO-8859-1', 'ignore')
                            except:
                                print("Error with Packages.bz2, trying Packages.gz")
                                pkg = requests.get(f"{url}/Packages.gz")
                                with gzip.open(str(pkg), 'r', encoding="ISO-8859-1") as f:
                                    packages = f.read()
                            lines = packages.splitlines()
                            for line in lines:
                                if line.startswith("Filename:"):
                                    if os.path.isfile(f"./downloads/{url}/" + line[10:len(line)]):
                                        print(line[10:] + " already saved, skipping...")
                                        continue
                            print("Retrieving " + line[10:] + "...")
                            r = requests.get(url + line[10:])
                            if r.status_code != requests.codes.ok:
                                print("Failed to get file with HTTP error code: " + str(r.status_code))
                                continue
                            if len(r.content) == 0:
                                print("Got " + line[10:] + ", it has no contents.")
                                continue
                            print("Got " + line[10:] + ". Size: " + str(len(r.content)))
                            try:
                                os.makedirs("./downloads/{url}/" + line[10:len(line)])
                                os.rmdir("./downloads/{url}/" + line[10:len(line)])
                            except:
                                print("Already exists.")
                            out = open("./downloads/{url}/" + line[10:len(line)], 'wb')
                            out.write(r.content)
                            out.close()
                            print("Saved " + line[10:] + ".")

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

        
    ########################################################################################## Mode 3 # Check for archived depictions
    elif mode == "2": 
        # Define the prefix to append
        prefix = "https://web.archive.org/web/20140130003333if_/"
        pdone = 0

        # Function to run before appending each line
        def pre_append_processing(line):
            global pdone
            global URL
            global s
            global m
            global h
            global sec
            global cooldown
            global p
            pdone += 1
            secsofar = 0

            # fancy cooldown animation
            chars = "/-\|"
            idx = 0
            
            while cooldown > secsofar:

                seconds_remaining = cooldown - secsofar
                print(f"\r[{chars[idx % len(chars)]}] {round(int(seconds_remaining))} waiting for cooldown...", end="")

                secsofar += 0.2
                idx = (idx + 1) % len(chars)
                sleep(0.2)

            print(f"\rRequesting data...", end="")
            print(f"\r", end="")
                    
            if line.startswith("Depiction: "):
                URL = line[len("Depiction: "):].strip()

                # Rate limit prevention (I lost two 10-hour processing because of this ;-;)
                while True:
                    try:
                        response = requests.get(f"https://web.archive.org/web/20140130003333if_/{URL}")
                        break
                    except:
                        print(f"[!] Error while requesting URL web.archive.org/web/20140130003333if_/{URL}.\nTrying again in 5 minutes. (Rate limit prevention)")
                        sleep(300)

                # Unreadable time calculation
                psf = p - pdone
                s = psf * cooldown
                h = s // 3600
                m = (s % 3600) // 60
                sec = s % 60
                
                # Is the URL dead? (e.g. not directs to a wayback machine page, to techradar, or to an older save of modmyi's homepage instead of the depiction.)
                if "The Wayback Machine is an initiative" in response.text or "techradar" in response.text.lower() or "tear down" in response.text.lower(): 
                    print(f"{h}hr {m}min / Dead (not archived) [{URL}]")
                    return False
                else:
                    print(f"{h}hr {m}min / Live (archived)     [{URL}]") # the link was archived by the wayback machine.
                    return True
                
            elif line.lower().startswith("homepage:"):
                if len(chpurl) > 0:
                    new_line = f"Homepage: {chpurl}\n" # Links homepage from dead depiction to the specified page
                    return new_line
                else:
                    return line

            else:
                return True # Keep the line unchanged if it doesn't start with "Depiction: " or "Homepage: "

        def process_file(input_file, output_file):

            try:
                with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
                    
                    for line in infile:

                        if line.startswith("Depiction: "):
                            write_line = pre_append_processing(line)
                            
                            if isinstance(write_line, str):
                                outfile.write(write_line)

                            elif write_line:
                                new_line = f"Depiction: {prefix}{URL}\n"
                                outfile.write(new_line)

                        else:
                            outfile.write(line)
                    
                    print(f"File processing complete. Modified content saved to '{output_file}'.")

            except KeyboardInterrupt: # Doesn't work (never saves packages file) but too lazy to remove
                print("Keyboard interrupt detected. Saving current progress and exiting.")
                outfile.close()
                infile.close()
                exit()

        input_file = "_Packages.txt"
        output_file = "Modified_Packages.txt"
        
        with open(input_file, "r") as in_file:
            lines = in_file.readlines()
            p2 = 0
            for line in lines:
                if "Package" in line:
                    p += 1

        print(f"{p} packages to process\nThis script takes an existing Packages file and replaces the Depiction section\nwith a wayback machine link if it was previously archived.\nIf it was not archived, the link gets removed so users can see the description of the package in the Cydia app.\nTo archive existing depiction links, see Depiction Archiver in the main menu.\n")

        while True:
            try:
                cooldown = input("Enter cooldown in seconds (recommended is 60 seconds to prevent rate limiting)\n> ")
                chpurl = input("\nEnter a custom homepage URL (see the github page for more info) or leave blank to keep default.\n> ")
                cooldown = int(cooldown)
                if cooldown <= 0:
                    raise ValueError("Cooldown should be a positive number.")

                # Another unreadable time calculation
                s = p * cooldown
                h = s // 3600
                m = (s % 3600) // 60
                sec = s % 60
                
                # Print the estimated time in custom format
                print(f"Time estimated: {h}hr {m}min {sec}sec")
                
                break
            except ValueError:
                print("Invalid input. Please enter a valid positive integer for cooldown.")
            except Exception as e:
                print(f"Error: {e}")

        input("Press ENTER to start, or enter CTRL + C to exit.")

        process_file(input_file, output_file)

    ##########################################################################################Mode 4 # Generate Packages file
    elif mode == "3":
        while True:
            clear()

            try:
                os.mkdir('./generate')
            except FileExistsError:
                pass
            # Scuffed Mode Selection
            mode6 = input(f"Move your deb files into the 'generate' directory.\n    Press 1 once you have moved the files.\n    (this will delete older generated 'Packages' files.) To go back to the main menu, press 2.\n> ")
            # Generate folder: Keep debs
            # Debs folder: move debs there
            clear()
            if mode6 == "1":
                print("The ./debs directory is for generation. Do not delete it, rename it, or mess with it while this is running.")

                try:
                    os.mkdir('./debs')
                except FileExistsError:
                    pass

                folder = './debs'
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
                    open("Generated_Packages", "x")
                except FileExistsError:
                    pass

                deb_files = [file for file in os.listdir('./generate') if file.endswith('.deb')]
                deb_count = len(deb_files)

                debsdone = 0
                writetofile = ''

                # Loop through all files in the 'generate' directory
                for root, dirs, files in os.walk('./generate'):
                    for file in files:
                        packages = ''
                        filename = file
                        if 'deb' in filename:                                
                            #print(f"    Processing file: {filename}")

                            # There has to be a better way of doing this
                            os.rename(f"./generate/{file}", f"./debs/{file}")

                            # I've had problems with UTF-8 in the past
                            proc = subprocess.run(['python', 'dpkg-sp.py', '--multiversion', './debs'], encoding='ISO-8859-1', stdout=subprocess.PIPE)
                            for line in proc.stdout.split('\n'):
                                packages += line + "\n"

                            # reused old code from cydiacrawler grabber
                            pattern = r'^([^_]+)\.([^_]+)\.([^_]+)_([^_]+)_([^_]+)\.deb$'
                            match = re.match(pattern, file)
                            if 'Error' in packages and match:
                                print(f"    [{debsdone}/{deb_count}] Error on {file}. Generated altenative.")

                                package_id = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
                                author = match.group(2)
                                name = match.group(3)
                                version = match.group(4)
                                architecture = match.group(5)
                                f = open(f"./debs/{file}", "rb")
                                filecontent = f.read()
                                md5 = hashlib.md5(filecontent).hexdigest() ####
                                f.close()

                                #byte
                                file_name = f"./debs/{file}"
                                file_stats = os.stat(f"./debs/{file}")
                                size = file_stats.st_size
                                
                                packages = f"""
Package: {package_id} 
Version: {version}
Section: unknown
Maintainer: unknown
Filename: ./debs/{file}
Size: {size}
MD5sum: {md5}
Description: {package_id}
Author: {author} 
    """
                                writetofile += packages + "\n"
                                    
                            elif 'Error' in packages:
                                print(f"    [{debsdone}/{deb_count}] Error on {file}. Generated altenative.")
                                # Last resort- file doesn't match 'pattern' and can't grab dpkg info from it.
                                f = open(f'./debs/{file}', "rb")
                                filecontent = f.read()
                                md5 = hashlib.md5(filecontent).hexdigest() ####
                                f.close()

                                #byte
                                file_name = f'./debs/{file}'
                                file_stats = os.stat(file_name)
                                size = file_stats.st_size
                                
                                packages = f"""
Package: xyz.unknown.{file}
Version: 1.0
Section: unknown
Maintainer: unknown
Name: {file}
Filename: ./debs/{file}
Size: {size}
MD5sum: {md5}
Description: [unknown]
Author: unknown
"""
                                writetofile += packages + "\n"
                            elif not 'Error' in packages:
                                # got dpkg data
                                writetofile += packages + "\n"
                                print(f"    [{debsdone}/{deb_count}] Generated {file}.") 
                
                            os.rename(f"./debs/{file}", f"./generate/{file}")


                        debsdone += 1

                # Wrote at the end instead of at each file for preformance
                with open("Generated_Packages", "w", encoding='ISO-8859-1', errors='ignore') as f1:
                    f1.write(writetofile)


                shutil.rmtree('./debs')
                input("    Finished. Press ENTER to continue.")
                """
                try:
                    os.mkdir('./debs')
                except FileExistsError:
                    pass
                print("\n\n    [Generate Packages]\n")
                input("    Move your deb files into the 'debs' directory.\n    Press ENTER once you have moved the files.\n    (this will delete older generated 'Packages' files.)")
                print("    Generating...")
                os.system("dpkg-sp.py --multiversion --output Generated_Packages ./debs")
                input("    Finished. Press ENTER to continue.")
                """
            elif mode6 == "2":
                break
    ########################################################################################## Mode 5 # Compress Packages file
    elif mode == "4":
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
            packages = open("./compress/Packages",'r', encoding='ISO-8859-1').read()
            newcontent = bz2.compress(packages.encode())
            f = open("./compress/Packages.bz2", "wb")
            f.write(newcontent)
            f.close()

            with open("./compress/Packages", 'rb') as orig_file:
                with gzip.open("./compress/Packages.gz", 'wb') as zipped_file:
                    zipped_file.writelines(orig_file)
            print("    Successfully generated Packages.bz2 and Packages.gz.")
        except Exception as e:
            print(f"\n    Error- {e}.")
        input("    Press ENTER to continue.")

    ########################################################################################## Mode 6 # Sort Packages
    elif mode == "5":

        try:
            os.mkdir('./unsorted')
        except FileExistsError:
            pass

        print("\n\n    [Sort Packages]\n")
        input("    Move your deb files into the 'debs' directory.\n    Press ENTER once you have moved the files.\n    (this will delete older generated 'Packages' files.)")
        print("    Generating...")

        # Make folders required
        try:
            os.mkdir('./temp')
        except FileExistsError:
            pass
        try:
            os.mkdir('./sort')
        except FileExistsError:
            pass
        """
        # Was using this to sort through large deb archives for my repos
        try:
            os.mkdir('./sort/__cracked')
        except FileExistsError:
            pass
        try:
            os.mkdir('./sort/__bigboss')
        except FileExistsError:
            pass
        try:
            os.mkdir('./sort/__modmyi')
        except FileExistsError:
            pass
        try:
            os.mkdir('./sort/__general')
        except FileExistsError:
            pass
        """


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

        # get count of deb files
        deb_files = [file for file in os.listdir('./unsorted') if file.endswith('.deb')]
        deb_count = len(deb_files)

        debsdone = 1
        
        # Loop through all files in the 'debs' directory
        for root, dirs, files in os.walk('./unsorted'):
            for file in files:
                packages = ''
                filename = file
                try:
                    #if 'crack' in filename.lower():
                    #    os.rename(f"./unsorted/{file}", f"./sort/__cracked/{file}")
                    #elif 'deb' in filename:
                    if 'deb' in filename:
                        #print(f"    Processing file: {filename}")

                        os.rename(f"./unsorted/{file}", f"./temp/{file}")
                        
                        # Capture stdout
                        proc = subprocess.run(['python', 'dpkg-sp.py', '--multiversion', './temp'], encoding='ISO-8859-1', stdout=subprocess.PIPE)
                        for line in proc.stdout.split('\n'):
                            packages += line + "\n"


                        # Old system of reading from text file, used stdout capturing instead
                        #os.system("python dpkg-sp.py --multiversion --output temp.txt ./temp")
                        #sleep(0.1) # give file time to save
                        #with open("temp.txt", "r", encoding="utf8") as f:
                        #    packages = f.read()


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
                        # Sort by repo here in defined folders so I don't have to later.
                        """if 'bigboss' in str(maintainer_info).lower():
                        #    os.rename(f"./temp/{file}", f"./sort/__bigboss/{file}")
                        #    print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/__bigboss/.")

                        elif 'modmyi' in str(maintainer_info).lower():
                            os.rename(f"./temp/{file}", f"./sort/__modmyi/{file}")
                            print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/__modmyi/.")

                        elif 'xsellize'  in str(maintainer_info).lower() or 'beyoip' in str(maintainer_info).lower() or 'clubifone' in str(maintainer_info).lower() or 'cydia.vn' in str(maintainer_info).lower() or 'hackulo.us'  in str(maintainer_info).lower() or 'heaveniphone' in str(maintainer_info).lower() or 'iphoneinthailand' in str(maintainer_info).lower() or 'sinful' in str(maintainer_info).lower():
                            os.rename(f"./temp/{file}", f"./sort/__cracked/{file}")
                            print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/__cracked/.")
                        """
                        if True:

                            # Not in any repo stated above

                            # make compatible with folder names
                            modified_string = re.sub(r'[^a-zA-Z0-9]', '_', str(maintainer_info))

                            maintainer_dir = f'./sort/{modified_string}'
                            if not os.path.exists(maintainer_dir):
                                os.mkdir(maintainer_dir)
                            
                            if modified_string == 'None':
                                os.rename(f"./temp/{file}", f"./sort/__general/{file}")
                                print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/__general/.")
                            else:
                                os.rename(f"./temp/{file}", f"{maintainer_dir}/{file}")
                                print(f"    [{debsdone}/{deb_count}] Sorted {file} to ./sort/{modified_string}/.")

                            if modified_string not in maintainerlist:
                                maintainerlist.append(modified_string)

                            
                except Exception as e:
                    print(f"    [{debsdone}/{deb_count}] Error '{e}' on {file}. Not sorted.")

                debsdone += 1


        shutil.rmtree('./temp')

        input("\n    Finished.\n    Press ENTER to continue.")
        
    ########################################################################################## Mode 7 # Credits
    elif mode == "6":
        clear()
        print("""
   Credits:
 - @memory,     for the pydpkg library.
 - @supermamon, for the python implementation of dpkg-scanpackages.
 - @calvink19,  for writing the Depiction Checker, Depiction Downloader, Package Sorter, Compressor, and Packages File Generator. 
""")
        input("   Press ENTER to continue.")
