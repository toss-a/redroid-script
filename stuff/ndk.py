import os
import re
import shutil
from stuff.general import General
from tools.helper import bcolors, get_download_dir, print_color, run

class Ndk(General):
    download_loc = get_download_dir()
    copy_dir = "./ndk"
    dl_links = {
        "11.0.0": [
            "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/0c6b0aad45498bbdb22eb1311b145d08ff4ce1fc.zip",
            "6d4b3788ac9e7e953aada561f64a2563"],
        "12.0.0": [
            "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/181d9290a69309511185c4417ba3d890b3caaaa8.zip",
            "0beff55f312492f24d539569d84f5bfb"],
        "13.0.0": [
            "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/faece8cc787a520193545116501cad40534063fc.zip",
            "f7605b31e51eaa69f13b508b20e74d10"],
        "14.0.0": [
            "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/faece8cc787a520193545116501cad40534063fc.zip",
            "f7605b31e51eaa69f13b508b20e74d10"]
        # "15.0.0": [
        #     "https://github.com/supremegamers/vendor_google_proprietary_ndk_translation-prebuilt/archive/faece8cc787a520193545116501cad40534063fc.zip",
        #     "f7605b31e51eaa69f13b508b20e74d10"]
        # "9.0.0":[],
        # "8.1.0":[]
    }
    dl_file_name = os.path.join(download_loc, "libndktranslation.zip")
    extract_to = "/tmp/libndkunpack"
    
    def __init__(self, version):
        self.version = version
        if version in self.dl_links.keys():
            self.dl_link = self.dl_links[version][0]
            self.act_md5 = self.dl_links[version][1]
        else:
            raise ValueError(
                "No available libndk for Android {}".format(version))
    
    def download(self):
        print_color("Downloading libndk now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        run(["chmod", "+x", self.extract_to, "-R"])
    
        print_color("Copying libndk library files ...", bcolors.GREEN)
        name = re.findall("([a-zA-Z0-9]+)\.zip", self.dl_link)[0]
        shutil.copytree(os.path.join(self.extract_to, "vendor_google_proprietary_ndk_translation-prebuilt-" + name, "prebuilts"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)

        init_path = os.path.join(self.copy_dir, "system", "etc", "init", "ndk_translation.rc")
        os.chmod(init_path, 0o644)
