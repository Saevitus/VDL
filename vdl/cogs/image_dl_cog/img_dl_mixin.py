from gallery_dl import config, job
import os
import disnake

from pathlib import Path


class img_dl_mixin:
    async def img_dl(self, url, filename):
        retn_list = []  # forward declare the return list
        it = 0  # iterator for the image gallaries, start it at 0
        start_dir = "vdl/media/"

        """
        set up the config
        this code is really odd, quite finicky as well
        """
        config.load()  # load default config files
        # without setting this, it creates a directory specifically for each different site, leave value blank
        config.set((), "directory", "")
        """ 
        set the extractor's base directory as vdl/media/, without this it defaults to creating a gallery-dl folder 
        you need to add a comma after extractor to define it as a tuple, otherwise the variable is the wrong type
        even if you add empty quotes it'll still break, so it's best to just leave it empty to set the default
        for every website
        """
        config.set(("extractor",), "base-directory", "vdl/media/")
        # supply cookies for instagram so no login is required to download, other sites may need this as well
        config.set(
            ("extractor", "instagram"),
            "cookies",
            "vdl/backend/placeholder/insta_cookies.txt",
        )
        # config.set((), "filename", "{id}.{extension}")
        # config.set((), "oauth", "reddit")

        # download the image
        job.DownloadJob(url).run()

        # loop images & rename them all, then append to retn_list
        # print(Path.cwd() + "")
        # for p in Path("vdl/media/").iterdir():
        # print(p.stem)
        # print(p.suffix)

        for fn in Path("vdl/media/").iterdir():
            extension = fn.suffix

            # here i could've added another if statement to stop the mp3 files being added to the shazam code
            # mzstatic is the file extension that gets downloaded from the shazam code
            if "mzstatic" in extension:
                extension = ".jpg"

            # op_dir = f"{start_dir}{fn.stem}{fn.suffix}"
            path = f"{start_dir}{filename}{str(it)}{extension}"

            fn.rename(path)

            retn_list.append(disnake.File(path))
            it += 1

        return retn_list


# download_image("https://www.instagram.com/p/CuM8xiRsKLrn4vJxLAONnBG2-GYz7YumY7RGQg0/", "test")
