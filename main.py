from flask import Flask, render_template, request, send_file, session, redirect, url_for, get_flashed_messages, flash
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
    track_link = request.form.get('url')
    if request.method == "POST":
        try:
            session['link'] = request.form.get('url')
            url = YouTube(session['link'])
            source_url = request.form["url"]
            track_streams = AudioStream().fetch_streams(source_url)
            return render_template("results.html", all_streams=track_streams, url=url, year=current_year)
        except Exception as e:
            print(e)
            flash(f'Sorry, the link "{track_link}" caused an error. Please try again.')
            return redirect(url_for('home'))
    else:
        flash(f'Sorry, there was a problem. Please try again.')
        return redirect(url_for('home'))

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        try:
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
                mimetype="audio/mpeg",
            )
        except Exception as e:
            print(e)
            flash(f'Sorry, there was a problem with the download. Please try again.')
            return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
