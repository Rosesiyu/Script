#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re

CONFIG = {
	"charts":[
		{
			"title":"CPUTemp",
			"axisYtitle":" ",
			"axisXtitle":"Unit:s",
			"source":['\\shaper_1.0.6\CPU_Temp.txt']
		},
	],
	"output":'E:\script\\results\Results_html\\shaper_1.0.6.html',
	"parentPath":'E:\script\\results'
}

def readfile(src):
	legendText = src.split("\\")[-1].split(".")[0]
	appendStr = "data.push({type: \"line\", markerType:\"none\", showInLegend: true, legendText: \""+legendText+"\", dataPoints: ["
        
	index = 0
	with open(src.decode('utf-8'), 'r') as f:
		dataPoints = []
		for line in f.readlines():
			index += 1
			pointY = line.strip()
			if len(pointY)<4:
				pointY += "000"
			if not re.match(r'\d', pointY):
				pointY = "null"
			dataPoints.append("{x:"+str(index)+", y:"+pointY+"}")
	appendStr += ",".join(dataPoints) + "]});\n"
	return appendStr

def main(config):
	result = """<!DOCTYPE HTML>
		<html>
		  <head>  
		    <script type="text/javascript" src="http://canvasjs.com/assets/script/canvasjs.min.js"></script>
		  </head>
		  <body>
		  """
	i = 0
	for ct in config["charts"]:
		chartStr = "<div id=\"chartContainer"+str(i)+"\" style=\"height: 400px; width: 60%;\"></div>\n"
		chartStr += """<script type="text/javascript">
			var data = [];
			"""
		for src in ct["source"]:
			chartStr += readfile(CONFIG["parentPath"]+src)
		chartStr +="var chart = new CanvasJS.Chart(\"chartContainer"+str(i)
		chartStr +="""\",
          {
            zoomEnabled: true,
            title:{
              text: \"""" + ct["title"] +"""\"
            },
            animationEnabled: true,
            axisX:{
              title: \"""" + ct["axisXtitle"] +"""\",
              labelAngle: 30
            },
            axisY :{
              title: \"""" + ct["axisYtitle"] +"""\",
              includeZero:true
            },
            legend: {
           	  verticalAlign: "bottom"
          	},
          data: data
        });
        chart.render();
		"""
		result += chartStr+"\n</script>"
		i+=1
	result += """
		  </body>
		</html>"""
	with open(config["output"].decode('utf-8'), 'w') as res:
		res.write(result)

if __name__ == '__main__':
	if len(sys.argv)>1:
		CONFIG["parentPath"] = sys.argv[1]
	if len(sys.argv)>2:
		CONFIG["output"] = sys.argv[2]
	main(CONFIG)