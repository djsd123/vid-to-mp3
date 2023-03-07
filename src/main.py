from __future__ import unicode_literals
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
    'outtmpl': '~/Downloads/%(title)s-%(id)s.%(ext)s',
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

    def downloading():
        """Callback function to initiate download and conversion of video to MP3

           Args:
               None: None

           Returns:
               None: None
        """
        try:
            with st.spinner('Downloading and converting...'):
                with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
                    ydl.download([input_video_url])
        except yt_dlp.utils.DownloadError as error:
            print(error)

    st.button(label='convert/download', on_click=downloading)


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     import subprocess
#
#     url = 'https://www.youtube.com/watch?v=FGBhQbmPwH8'
#
#     subprocess.call(['youtube-dl', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', '-o', 'output.mp4', url])
