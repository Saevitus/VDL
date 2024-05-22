from pathlib import Path
import disnake


class utils:
    def split(a, n):
        """
        a = list, n = number to split the list into chunks of
        a[x:x+n] = list[index:split+chunk_number]
        only if x is in the range of the list & chunk number
        """
        return [a[x : x + n] for x in range(0, len(a), n)]

    def get_size(file_details):
        """
        file_details = {"ctx": ctx, "url": url, "is_tiktok": is_tiktok, "custom_file_name": custom_file_name, "audio_only": audio_only}
        size checking function, all we pass into here is the file_details,
        then preform a couple checks and return a disnake file which is appended into a list
        """

        file_size = None  # forward declare
        # if in a server, without any boosts, file size limit is 8mb, with at minimum 2 boosts its 25mb
        if file_details["ctx"].guild:
            file_size = (
                25000000
                if file_details["ctx"].guild.premium_subscription_count >= 2
                else 8000000
            )
        else:
            file_size = 25000000

        # check file type, if audio_only is true, we use .mp3, vice versa
        file_type = ".mp3" if file_details["audio_only"] == True else ".mp4"

        """ 
                preform the size check, if file is too big return the placeholder to be appended
                otherwise return the file to be appended and uploaded
                """
        file = Path("vdl/media/" + str(file_details["custom_file_name"]) + file_type)

        if file.stat().st_size > file_size:
            file.unlink()
            # os.remove("vdl/media/" + str(fd[2]) + file_type)
            # disnake.File("./placeholder/FSTB.png")
            return disnake.File("vdl/backend/placeholder/FSTB.png")
        else:
            return disnake.File(
                "vdl/media/" + str(file_details["custom_file_name"]) + file_type
            )
