# LeIA Project

LeIA is an application that leverages artificial intelligence models for audio and video transcription. Users can transcribe new files or consult previously transcribed cases.

## Repository and Documentation

- **Repository**: [https://github.com/andrecorumba/leia](https://github.com/andrecorumba/leia)
- **Documentation**: [https://andrecorumba.github.io/leia/](https://andrecorumba.github.io/leia/)
- **Web Version for Testing**: [https://andrecorumba-leia-appapp-web-b757de.streamlit.app](https://andrecorumba-leia-appapp-web-b757de.streamlit.app)

## Python Version

The project is implemented in Python version 3.12.2.

## Key Libraries Used

- `os`: A library for interacting with the operating system, enabling the manipulation of file paths, directories, environment variables, etc.
- `whisper`: A library for audio and video transcription ([https://github.com/openai/whisper](https://github.com/openai/whisper)).
- `pandas`: A library for working with tabular data, supporting manipulation, cleaning, analysis, and visualization.
- `sqlite3`: A library for working with SQLite databases, a widely used embedded relational database.
- `streamlit`: A library for creating interactive web applications for data analysis and visualization, allowing users to build interactive data analysis dashboards and control panels.
- `streamlit_option_menu`: An additional library for Streamlit that enables the creation of custom dropdown menus with multiple options.
- `pydub`: A library for audio file manipulation, supporting various operations such as cutting, merging, and volume adjustment.

## Important Requirements

The `ffmpeg` application must be installed on the machine for converting various audio types and is a requirement for using the `whisper` library. Download it from: [https://ffmpeg.org](https://ffmpeg.org). On MacOS, version 5.2 can be installed via Homebrew with `brew install ffmpeg`.

## Docker Image

To download the Docker image, Docker must be installed. Use the following command in the terminal:

```
docker pull andrecorumba/leia-docker
```