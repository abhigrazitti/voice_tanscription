'''voice processing inference'''
import os
import pathlib
import requests
import iso639
import whisper
import yt_dlp as youtube_dl
import json
import base64
cnvrg_workdir = os.getcwd()
print('CWD->'+cnvrg_workdir)

def yt_vid_to_audio(url):
    '''
    download the audio file either from youtube or s3

    Parameters
    ----------
    url : URL to the youtube video to be converted and used as an audio input

    Returns
    -------
    out_file : converted youtube vid to audio file

    '''
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': cnvrg_workdir+'/audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([str(url)])

    out_file = os.path.join(cnvrg_workdir, "audio.wav")
    print('OUTFILE->>>>'+out_file)
    # result of success
    #print(yt_.title + " has been successfully downloaded.")
    
    return out_file

def download_test_file(url_):
    """
    Downloads the model files if they are not already present or
    pulled as artifacts from a previous train task
    """
    current_dir = str(pathlib.Path(__file__).parent.resolve())
    if not os.path.exists(current_dir + f'/{url_}') and not os.path.exists('/input/cnn/' + url_):
        print(f'Downloading file: {url_}')
        response = requests.get(url_)
        file = url_.split("/")[-1]
        path_ = os.path.join(current_dir, file)
        with open(path_, "wb") as file_:
            file_.write(response.content)


def predict(audio_file):
    '''

    Parameters
    ----------
    audio_file : audio file containing speech

    Returns
    ------- 
    text extracted from the sudio file
    '''
    ### SCALE TEST DATA ###
    print('Running NEW Stand Alone Endpoint')
    print(audio_file)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print(audio_file['file_name'])

    if 'output_audio.mp3' in audio_file['file_name']:

        file_name = str(audio_file['file_name'])
        lang = str(audio_file['language'])
        model_size = str(audio_file['model_size'])

        #file_name = script_dir+file_name
        print('NEW file_name NAME------------------------------')
        print(file_name)

    else:
        script_dir = pathlib.Path(__file__).parent.resolve()
        audio_f = str(audio_file['file_name'])
        lang = str(audio_file['language'])
        model_size = str(audio_file['model_size'])
        
        if 'www.youtube.com' in audio_f:
            audio_file = yt_vid_to_audio(audio_f)
            name = 'audio.wav'
        else:
            download_test_file(audio_f)
            name = audio_f.rsplit("/", maxsplit=1)[-1]

        file_name = os.path.join(script_dir,name)
        print('NEW file_name NAME------------------------------')
        print(file_name)

    dic = {}
    model = whisper.load_model(model_size)
    print('model downloaded')
    result = model.transcribe(file_name, task='transcribe', fp16=False,
                            language=iso639.to_iso639_1(lang)) 
    # print the recognized text
    dic = result['text']
    
    return {'text': result['text']}

from moviepy.editor import *

# Input MP4 file
mp4_file = 'cnvrg Platform-20211227.mp4'

# Output MP3 file
mp3_file = 'output_audio.mp3'

# Load the MP4 file
video = VideoFileClip(mp4_file)

# Extract the audio from the video
audio = video.audio

# Save the audio as an MP3 file
audio.write_audiofile(mp3_file)

# Close the video and audio clips
video.close()
audio.close()


# https://www.youtube.com/watch?v=e5xxejlecLs
print(predict({'file_name':'output_audio.mp3',
                'language':'english',
                'model_size':'small.en'}))
