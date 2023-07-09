from flask import Flask, render_template, request
import moviepy.editor as mp
import speech_recognition as sr

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        video.save('temp.mp4')

        # Extract audio from the video
        video_clip = mp.VideoFileClip('temp.mp4')
        video_clip.audio.write_audiofile('temp.wav')

        # Transcribe the audio
        r = sr.Recognizer()
        with sr.AudioFile('temp.wav') as source:
            audio = r.record(source)
        transcript = r.recognize_google(audio)

        # Delete temporary files
        video_clip.close()
        os.remove('temp.mp4')
        os.remove('temp.wav')

        return render_template('result.html', transcript=transcript)

    return render_template('index.html')
