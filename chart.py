from quickchart import QuickChart

def draw_chart(labels, data):
  qc = QuickChart()
  qc.width = 500
  qc.height = 300
  qc.device_pixel_ratio = 2.0

  qc.config = {
    "type": "outlabeledPie",
   "data": {
     "labels": labels,
      "datasets": [{
          "backgroundColor": ["#FF9D9D", "#E49DFF", "#9DACFF", "#9DFFE7", "#FFBE9D", "#FFC974", "#00FA9A", "#191970", "#4B0082", "#6A5ACD", "#7CFC00"],
          "data": data
     }]
    },
   "options": {
    "plugins": {
      "backgroundImageUrl": 'https://cdn.pixabay.com/photo/2022/01/24/10/53/10-53-48-156_960_720.png',
      "legend": False,
      "outlabels": {
        "text": "%l %p",
        "color": "black",
        "stretch": 35,
        "font": {
          "resizable": "true",
          "minSize": 12,
          "maxSize": 18
        }
      }
    }
  }
}
  chart_url = qc.get_url()
  return chart_url



def draw_chart_for_category(value, sum):
  qc = QuickChart()
  qc.width = 500
  qc.height = 300
  qc.device_pixel_ratio = 2.0


  qc.config = {
      "type": "radialGauge",
      "data": {
          "datasets": [{
              "backgroundColor": ["#f3ca20"],
              "data": [value]
          }]
      },
      "options": {
          "domain": [0, sum],
          "trackColor": '#000000',
          "centerPercentage": 90,
          "centerArea": {
              "text" : str(value/sum*100) + '%',
          },
          "plugins": {
              "backgroundImageUrl": 'https://cdn.pixabay.com/photo/2022/01/24/10/53/10-53-48-156_960_720.png',
          }
                }
  }

  chart_url = qc.get_url()
  return chart_url



