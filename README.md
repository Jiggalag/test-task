0. Clone repository locally.
1. Install dependencies from requirements.txt.
2. Run docker image with command `docker run -it -p 8091:8091 azshoo/alaska:1.0`
3. Move to project directory and run tests with command `pytest --html=report.html`
4. Test report will be stored to report.html in local directory, you can browse it with any html-viewer (e.g. `firefox report.html`)