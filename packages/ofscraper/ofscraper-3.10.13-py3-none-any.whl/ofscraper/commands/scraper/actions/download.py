r"""_____  _______         _______  _______  _______  _______  _______  _______  _______ 
(  ___  )(  ____ \       (  ____ \(  ____ \(  ____ )(  ___  )(  ____ )(  ____ \(  ____ )
| (   ) || (    \/       | (    \/| (    \/| (    )|| (   ) || (    )|| (    \/| (    )|
| |   | || (__     _____ | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
| |   | ||  __)   (_____)(_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
| |   | || (                   ) || |      | (\ (   | (   ) || (      | (      | (\ (   
| (___) || )             /\____) || (____/\| ) \ \__| )   ( || )      | (____/\| ) \ \__
(_______)|/              \_______)(_______/|/   \__/|/     \||/       (_______/|/   \__/
"""

import logging
import time
import pathlib


import ofscraper.classes.placeholder as placeholder
import ofscraper.download.download as download
import ofscraper.utils.constants as constants
import ofscraper.utils.live.screens as progress_utils
from ofscraper.commands.helpers.strings import  download_activity_str,all_paid_progress_download_str,all_paid_download_str
from ofscraper.commands.helpers.scrape_paid import process_scrape_paid,process_user_info_printer,process_user
from ofscraper.utils.context.run_async import run
import ofscraper.utils.config.data as config_data
import ofscraper.utils.paths.common as common_paths
from ofscraper.utils.string import format_safe



log = logging.getLogger("shared")


async def downloader(ele=None, posts=None, media=None, **kwargs):
    model_id = ele.id
    username = ele.name
    download_str=download_activity_str.format(username=username)
    path_str=format_safe(f"\nSaving files to [deep_sky_blue2]{str(pathlib.Path(common_paths.get_save_location(),config_data.get_dirformat(),config_data.get_fileformat()))}[/deep_sky_blue2]",username=username,model_id=model_id,model_username=username,modelusername=username,modelid=model_id)

    progress_utils.update_activity_task(description=download_str+path_str)
    logging.getLogger("shared_other").warning(download_activity_str.format(username=username))
    progress_utils.update_activity_task(description="")
    return await download.download_process(username, model_id, media, posts=posts)





def unique_name_warning():
    if not placeholder.check_uniquename():
        log.warning(
            "[red]Warning: Your generated filenames may not be unique\n \
            https://of-scraper.gitbook.io/of-scraper/config-options/customizing-save-path#warning[/red]      \
            "
        )
        time.sleep(constants.getattr("LOG_DISPLAY_TIMEOUT") * 3)

@run
async def scrape_paid_all():
    out=["[bold yellow]Scrape Paid Results[/bold yellow]"]

    async for count,value,length in process_scrape_paid():
        process_user_info_printer(value,length,count,all_paid_update=all_paid_download_str,all_paid_activity=download_activity_str,
        log_progress=all_paid_progress_download_str
        )
        out.append(await process_user(value,length))
    return out




    # progress_utils.update_activity_task(description="Downloading Paid Content")
    # return process_scrape_paid(download_progress_message=download_activity_str,log_progress_message=all_paid_progress_download_str)
