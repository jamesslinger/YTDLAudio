from flask import Flask, render_template, request, send_file, session
from audio_data import AudioStream
from pytube import YouTube
from io import BytesIO
import datetime as dt
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


@app.route("/", methods=["GET", "POST"])
def home():
    current_year = dt.datetime.now().year
    return render_template("index.html", year=current_year)


@app.route("/results", methods=["GET", "POST"])
def results():
    current_year = dt.datetime.now().year
    if request.method == "POST":
        session['link'] = request.form.get('url')
    try:
        url = YouTube(session['link'])
        # url.check_availability()
        source_url = request.form["url"]
        track_streams = AudioStream().fetch_streams(source_url)
        return render_template("results.html", all_streams=track_streams, url=url, year=current_year)
    except:
        return render_template("index.html", year=current_year, error="Sorry, that URL didn't work. Please try again.")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        buffer = BytesIO()
        session['link'] = request.form.get('url')
        streams = YouTube(session['link'])
        track_id = int(request.form.get('track_id'))
        track = streams.streams.get_by_itag(track_id)
        track.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{track.title}.mp3",
            mimetype="audio/mp3",
        )


if __name__ == "__main__":
    app.run()
