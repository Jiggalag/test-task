0. Clone repository locally.
1. Install dependencies from requirements.txt.
2. Run docker image with command `docker run -it -p 8091:8091 azshoo/alaska:1.0`
3. Move to project directory and run tests with command `pytest --html=report.html`
4. Test report will be stored to report.html in local directory, you can browse it with any html-viewer (e.g. `firefox report.html`)
5. You can see checklist.ods in root-project dir.

Known issues:
1. Implement multithreading load test.
2. Support dynamically generating of data-sets depending on
pytest-markers.
3. Move datasets from python lists to fixtures.
4. Remove double defining methods like generate_valid_bear from
different tests - they should be defined once.
5. Probably add checking of status_code to all tests.