from gallery_dl import config, job
import os
import disnake

class img_dl_mixin:
    async def img_dl(self, url, filename):
        retn_list = [] # forward declare the return list
        it = 0 # iterator for the image gallaries, start it at 0
        start_dir = f"vdl/media/"
        
        '''
        set up the config
        this code is really odd, quite finicky as well
        '''
        config.load()  # load default config files
        # without setting this, it creates a directory specifically for each different site, leave value blank
        config.set((), "directory", "")
        ''' 
        set the extractor's base directory as vdl/media/, without this it defaults to creating a gallery-dl folder 
        you need to add a comma after extractor to define it as a tuple, otherwise the variable is the wrong type
        even if you add empty quotes it'll still break, so it's best to just leave it empty to set the default
        for every website
        '''
        config.set(("extractor",), "base-directory", "vdl/media/")
        # supply cookies for instagram so no login is required to download, other sites may need this as well
        config.set(("extractor", "instagram"), "cookies", "vdl/backend/placeholder/cookies.txt")
        #config.set((), "filename", "{id}.{extension}")
        #config.set((), "oauth", "reddit")
        
        # download the image
        job.DownloadJob(url).run()
        
        
        # loop images & rename them all, then append to retn_list
        for fn in os.listdir("vdl/media/"):
            extension = fn.split(".")[1]

            # here i could've added another if statement to stop the mp3 files being added to the shazam code
            # mzstatic is the file extension that gets downloaded from the shazam code
            if "mzstatic" in extension:
                extension = "jpg"
            
            op_dir = f"{start_dir}{fn}"
            path = f"{start_dir}{filename}{str(it)}.{extension}"
            
            os.rename(op_dir, path)
            retn_list.append(disnake.File(path))
            it += 1
            
        return retn_list

#download_image("https://www.instagram.com/p/CuM8xiRsKLrn4vJxLAONnBG2-GYz7YumY7RGQg0/", "test")