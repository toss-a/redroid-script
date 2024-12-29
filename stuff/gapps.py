import os
import shutil
from stuff.general import General
from tools.helper import get_download_dir, host, print_color, run, bcolors

class Gapps(General):
    dl_links = {
        "11.0.0": {
            "x86_64": [
                "https://sourceforge.net/projects/opengapps/files/x86_64/20220503/open_gapps-x86_64-11.0-pico-20220503.zip",
                "5a6d242be34ad1acf92899c7732afa1b",
            ],
            "x86": [
                "https://sourceforge.net/projects/opengapps/files/x86/20220503/open_gapps-x86-11.0-pico-20220503.zip",
                "efda4943076016d00b40e0874b12ddd3",
            ],
            "arm64": [
                "https://sourceforge.net/projects/opengapps/files/arm64/20220503/open_gapps-arm64-11.0-pico-20220503.zip",
                "67e927e4943757f418e4f934825cf987",
            ],
            "arm": [
                "https://sourceforge.net/projects/opengapps/files/arm/20220215/open_gapps-arm-11.0-pico-20220215.zip",
                "8719519fa32ae83a62621c6056d32814",
            ],
        },
        "10.0.0": {
            "x86_64": [
                "https://sourceforge.net/projects/opengapps/files/x86_64/20220503/open_gapps-x86_64-10.0-pico-20220503.zip",
                "5fb186bfb7bed8925290f79247bec4cf",
            ]
        },
        "9.0.0": {
            "x86_64": [
                "https://sourceforge.net/projects/opengapps/files/x86_64/20220503/open_gapps-x86_64-9.0-pico-20220503.zip",
                "020676410aa354e4d6c524fc4d7e8200",
            ]
        },
        "8.1.0": {
            "x86_64": [
                "https://sourceforge.net/projects/opengapps/files/x86_64/20220503/open_gapps-x86_64-8.1-pico-20220503.zip",
                "dcde2fb5b69761982baf728e9be3ade2",
            ],
            "x86": [
                "https://sourceforge.net/projects/opengapps/files/x86/20220503/open_gapps-x86-8.1-pico-20220503.zip",
                "380b35d21d776bf2fd230f6159ba969e",
            ]
        },
    }
    arch = host()
    download_loc = get_download_dir()
    dl_file_name = os.path.join(download_loc, "open_gapps.zip")
    dl_link = ...
    act_md5 = ...
    copy_dir = "./gapps"
    extract_to = "/tmp/ogapps/extract"

    non_apks = [
        "defaultetc-common.tar.lz",
        "defaultframework-common.tar.lz",
        "googlepixelconfig-common.tar.lz",
        "vending-common.tar.lz"
        ]
    skip = [
        "setupwizarddefault-x86_64.tar.lz",
        "setupwizardtablet-x86_64.tar.lz"
        ]
    
    def __init__(self, version):
        self.version = version
        self.dl_link = self.dl_links[self.version][self.arch[0]][0]
        self.act_md5 = self.dl_links[self.version][self.arch[0]][1]

    def download(self):
        print_color("Downloading OpenGapps now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.extract_to):
            os.makedirs(self.extract_to)
        if not os.path.exists(os.path.join(self.extract_to, "appunpack")):
            os.makedirs(os.path.join(self.extract_to, "appunpack"))

        for lz_file in os.listdir(os.path.join(self.extract_to, "Core")):
            for d in os.listdir(os.path.join(self.extract_to, "appunpack")):
                shutil.rmtree(os.path.join(self.extract_to, "appunpack", d))
            if lz_file not in self.skip:
                if lz_file not in self.non_apks:
                    print("    Processing app package : "+os.path.join(self.extract_to, "Core", lz_file))
                    run(["tar", "--lzip", "-xvf", os.path.join(self.extract_to, "Core", lz_file), "-C", os.path.join(self.extract_to, "appunpack")])
                    app_name = os.listdir(os.path.join(self.extract_to, "appunpack"))[0]
                    xx_dpi = os.listdir(os.path.join(self.extract_to, "appunpack", app_name))[0]
                    app_priv = os.listdir(os.path.join(self.extract_to, "appunpack", app_name, "nodpi"))[0]
                    app_src_dir = os.path.join(self.extract_to, "appunpack", app_name, xx_dpi, app_priv)
                    for app in os.listdir(app_src_dir):
                        shutil.copytree(os.path.join(app_src_dir, app), os.path.join(self.copy_dir, "system", "priv-app", app), dirs_exist_ok=True)
                else:
                    print("    Processing extra package : "+os.path.join(self.extract_to, "Core", lz_file))
                    run(["tar", "--lzip", "-xvf", os.path.join(self.extract_to, "Core", lz_file), "-C", os.path.join(self.extract_to, "appunpack")])
                    app_name = os.listdir(os.path.join(self.extract_to, "appunpack"))[0]
                    common_content_dirs = os.listdir(os.path.join(self.extract_to, "appunpack", app_name, "common"))
                    for ccdir in common_content_dirs:
                        shutil.copytree(os.path.join(self.extract_to, "appunpack", app_name, "common", ccdir), os.path.join(self.copy_dir, "system", ccdir), dirs_exist_ok=True)