import streamlit as st
import s3fs
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋"
    )
    # Create S3 file system object
    s3 = s3fs.S3FileSystem()
    #####################Uploading New content:
    # File uploader to get new content
    new_content = st.text_area("Новый текст для родителей")

    # Audio file uploader restricted to MP3
    audio_file = st.file_uploader("Новый аудиофайл (только .mp3)!", type=["mp3"])

    # Save button
    if st.button("Сохранить"):
        save_content_to_s3(new_content, audio_file)
    
    ###############################Displaying old content
    # Read current content from S3
    with s3.open("streamlitgreetingscard/greetings.txt", "r") as file:
        current_content = file.read()

    # Print results.
    st.write("# Как оно выглядит сейчас:")
    st.write(current_content)

    # Play audio if file is uploaded
    with s3.open("streamlitgreetingscard/audio_file.mp3", "rb") as audio_file:
        audio_content = audio_file.read()
        st.audio(audio_content, format='audio/mpeg', start_time=0)

def save_content_to_s3(text_content, audio_file):
    # Create S3 file system object
    s3 = s3fs.S3FileSystem()

    # Write text content to S3
    if len(text_content) > 1:
        with s3.open("streamlitgreetingscard/greetings.txt", "w") as text_file:
            text_file.write(text_content)

    # Write audio file to S3
    if audio_file:
        audio_path = "streamlitgreetingscard/audio_file." + audio_file.name.split(".")[-1]
        with s3.open(audio_path, "wb") as audio_s3_file:
            audio_s3_file.write(audio_file.read())

if __name__ == "__main__":
    run()