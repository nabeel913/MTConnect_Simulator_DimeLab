# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:32:51 2019

@author: smehdi@ncsu.edu
"""

import folium
import pandas as pd



master = pd.read_csv('dbs\master.csv')

lat=list(master['latitude'])
lon=list(master['longitude'])
orgs = list(master['names'])
machs = list(master['machines'])
cu = list(master['CapacityUtil'])
ports =list(master['agentPorts'])


#These coordinates are to position the map to the best view. 
US_COORDINATES = (39.0902,-98.7129)

NumOrg = len(orgs)


# create empty map zoomed in on US_Coordinates
mape = folium.Map(location=US_COORDINATES,control_scale=False, zoom_start=5)

# add a marker for every record in the filtered data, use a clustered view
for i in range(NumOrg):
    P=ports[i]
    M=machs[i]
    C=cu[i]
    
    if C==0:
        COL='red'
    if (1<=C<=30):
        COL='orange'
    if (C>30):
        COL='green'
    
    info = folium.Html(f'''<h4><span style="color: #3366ff;">{orgs[i]} - port : {P}</span></h4>
<table style="height: 30px;" width="284">
<tbody>
<tr>
<td style="width: 169px;">
<h4>MTConnect :</h4>
</td>
<td style="width: 99px;"><h6><a href="http://localhost:{P}/current" target="_blank" rel="noopener">Current |</a><a href="http://localhost:{P}/probe" target="_blank" rel="noopener"> Probe</h6></a></td>
</tr>
<tr>
<td style="width: 169px;">
<h4>Total Machines:
</td>
<td style="width: 99px;"><b>{M}</b></td>
</tr>
<tr>
<td style="width: 169px;">
<h4>Capacity Utilization:
</td>
<td style="width: 99px;"><b>{C}%</h4></b></td>
</tr>
</tbody>
</table>''',width=300, script=True)
    if (C==100):
        I='star'
    else:
        I='info-sign'
    
    popup = folium.Popup(info, max_width=2650)
    #put custom text whenever the marker of machine clicked on map.
    folium.Marker(location=[lat[i],lon[i]],icon=folium.Icon(icon=I,color=COL), popup=popup).add_to(mape)
#save map in the view html file to be rendered by flask.  
mape.save("templates/view.html")