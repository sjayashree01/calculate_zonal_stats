'''
Can you turn steps 3 and 4 above into a simple API? The API input takes in an image, an ROI (in GeoJSON),
and a reducer selector. API functionality can be mocked if you are short on time.


Note: Simple implementation ofm POST method. This service can be extended to support GET, PUT, PATCH, DELETE too depending on the requirements.

Reference:
https://pythonhosted.org/rasterstats/
'''

from flask import Flask, request, jsonify
import calculate_zonal_stats as service

app = Flask(__name__)


@app.route('/calculate_zonal_stats', methods=['POST'])
def calculate_zonal_stats():
    service.main()
    return jsonify("Zonal stats are successfully calculated")


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=False, port=5555)
