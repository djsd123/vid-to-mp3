from __future__ import unicode_literals
import json
import os
import time

import streamlit as st
import yt_dlp


class Logger(object):
    def is_not_used(self):
        pass

    def debug(self, msg):
        self.is_not_used()
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        self.is_not_used()
        print(msg)


def progress_hook_downloading(download):
    with st.spinner('Downloading'):
        if download['status'] == 'downloading':
            print('Downloading')


def progress_hook_finished(download):
    if download['status'] == 'finished':
        st.success('All finished....')
        print('All finished....')


youtube_dl_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [progress_hook_downloading, progress_hook_finished],
    'outtmpl': '/tmp/%(title)s.%(ext)s',
}


if __name__ == '__main__':

    # Set the title of the tab in the browser
    st.set_page_config(
        page_title='vid to mp3',
        page_icon='📺',
        layout='wide'
    )

    # Create a heading and sub-heading
    st.title('Videos to MP3')
    st.write('Let\'s convert this thing!')

    # Create a text input field to type or paste the video url
    input_video_url: str = st.text_input('Please enter the video url')


    def delete_file(file_path):
        os.path.isfile(file_path) and os.remove(file_path)


    def wrangle_meta_data(meta_data):
        return json.loads(json.dumps(meta_data))


    def fetch(download_mp3: bool = True) -> str:
        """Callback function to initiate download and conversion of video to MP3

           Args:
               download_mp3: Whether to download the MP3 while fetching the metadata

           Returns:
               title: The title of the video extracted from the video's metadata
        """
        try:
            with st.spinner('Downloading and converting...'):
                with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
                    info = ydl.extract_info(input_video_url, download=download_mp3)
                    json_data = wrangle_meta_data(ydl.sanitize_info(info))
                return json_data['title']
        except yt_dlp.utils.DownloadError as error:
            print(error)


    st.button(label='Convert', on_click=fetch)

    if input_video_url:

        title = fetch(download_mp3=False)

        print(title)

        file_path = f'/tmp/{title}.mp3'

        while not os.path.exists(file_path):
            time.sleep(5)
            if os.path.isfile(file_path): break

        with open(file_path, 'rb') as file:
            st.download_button(
                label='Download',
                data=file,
                file_name=f'{title}.mp3',
                mime='audio/mpeg',
            ) and delete_file(file_path)


# if __name__ == '__main__':
#     import subprocess
#
#     url = 'https://www.youtube.com/watch?v=FGBhQbmPwH8'
#
#     subprocess.call(['youtube-dl', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', '-o', 'output.mp4', url])
