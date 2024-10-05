from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt

async def getNDVI(cord1, cord2, cord3, cord4):
  CLIENT_ID = "fba95cfe-bb9f-405e-af99-e26e803c5b88"
  CLIENT_SECRET = "XwzRbSHZPTkYmUknHjsOmWGbJU1UmCEi"
  print(cord1)
  cord1.reverse()
  cord2.reverse()
  cord3.reverse()
  cord4.reverse()
  print(cord1)
  # set up credentials
  client = BackendApplicationClient(client_id=CLIENT_ID)
  oauth = OAuth2Session(client=client)

  # get an authentication token
  token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
                            client_secret=CLIENT_SECRET, include_client_id=True)

  bbox = [-87.72171, 17.11848, -87.342682, 17.481674]
  start_date = "2020-06-01"
  end_date = "2020-08-31"
  collection_id = "sentinel-2-l2a"

  evalscript = """
  //VERSION=3
  function setup() {
    return {
        input: ["B04", "B08", "dataMask"],
        output: { bands: 4 }
    };
  }

  const ramp = [
    [-0.5, 0x0c0c0c],
    [-0.2, 0xbfbfbf],
    [-0.1, 0xdbdbdb],
    [0, 0xeaeaea],
    [0.025, 0xfff9cc],
    [0.05, 0xede8b5],
    [0.075, 0xddd89b],
    [0.1, 0xccc682],
    [0.125, 0xbcb76b],
    [0.15, 0xafc160],
    [0.175, 0xa3cc59],
    [0.2, 0x91bf51],
    [0.25, 0x7fb247],
    [0.3, 0x70a33f],
    [0.35, 0x609635],
    [0.4, 0x4f892d],
    [0.45, 0x3f7c23],
    [0.5, 0x306d1c],
    [0.55, 0x216011],
    [0.6, 0x0f540a],
    [1, 0x004400],
  ];

  const visualizer = new ColorRampVisualizer(ramp);

  function evaluatePixel(samples) {
    let ndvi = index(samples.B08, samples.B04);
    let imgVals = visualizer.process(ndvi);
    return imgVals.concat(samples.dataMask)
  }
  """

  json_request = {
  "input": {
    "bounds": {
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            cord1,
            cord2,
            cord3,
            cord4,
            cord1
          ]
        ],
        "properties": {
        "crs": "http://www.opengis.net/def/crs/EPSG/0/  "
      }
      }
    },
    "data": [
      {
        "dataFilter": {
          "timeRange": {
            "from": "2024-09-05T00:00:00Z",
            "to": "2024-10-05T23:59:59Z"
          }
        },
        "type": "sentinel-2-l2a"
      }
    ]
  },
  "output": {
    "width": 500,
    "height": 500,
    "responses": [
      {
        "identifier": "default",
        "format": {
          "type": "image/jpeg"
        }
      }
    ]
  },
  "evalscript": evalscript
  }

  # Set the request url and headers
  url_request = 'https://services.sentinel-hub.com/api/v1/process'
  headers_request = {
      "Authorization" : "Bearer %s" %token['access_token']
  }

  #Send the request
  response = oauth.request(
      "POST", url_request, headers=headers_request, json = json_request
  )

  image = (Image.open(io.BytesIO(response.content)))
  return image

