import Camera
import requests
import json
import numpy as np
from datetime import datetime

url = "http://25.57.227.183:8080"
plates_array = []
def main():
    #connect
    body_connect = {"email": "camera", "password": "pass"}
    r = requests.post(url + '/authenticate', json=body_connect)
    json_data = r.text
    if r.status_code == 200:
        json_data = json.loads(json_data)
        success = json_data["success"]
        token = json_data["data"]["token"]
        headers = {
            'X-Auth-Token': token
        }

        if success:
            while True:
                plate_number = Camera.main()
                # plate_number = "VYH698"
                plates_array.append(plate_number)
                if len(plates_array) == 10:
                    (values, counts) = np.unique(plates_array, return_counts=True)
                    ind = np.argmax(counts)
                    plate_number = values[ind]
                    print("License plate number: " + plate_number)
                    print("--------------------------------------")
                    plates_array.clear()

                    if plate_number != "no plate":
                        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

                        body = {"number": plate_number, "timestamp": timestamp}
                        r = requests.post(url + '/camera', json=body, headers=headers)
                        if r.status_code == 200:
                            print("Post sent")
                        else:
                            print("Error ", r.text)
        else:
            print("Error! ", "Status code: ", r.status_code, r.text)

if __name__ == '__main__':
    main()
