from flask import Flask, request, render_template, send_file
from pytube import YouTube
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['youtube_link']
        video_stream, video_title = download_video(link)
        if video_stream:
            return send_file(video_stream, as_attachment=True, download_name=video_title + '.mp4')
        else:
            return "Erreur lors du téléchargement de la vidéo. Veuillez vérifier le lien YouTube ou réessayer plus tard."
    return render_template('index.html')

def download_video(link):
    try:
        yt = YouTube(link)
        vs = yt.streams.get_highest_resolution()
        video_stream = io.BytesIO()
        vs.stream_to_buffer(video_stream)
        video_stream.seek(0)
        video_title = yt.title
        print('Téléchargement réussi :', video_title)
        return video_stream, video_title
    except Exception as e:
        print("Erreur lors du téléchargement de la vidéo:", str(e))
        return None, None

if __name__ == '__main__':
    app.run(debug=True)
