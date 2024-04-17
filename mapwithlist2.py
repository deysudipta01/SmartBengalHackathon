from codecs import latin_1_decode
from fileinput import filename
import json
import folium
import geopy.distance
import math
import webbrowser
from geopy.geocoders import ArcGIS
from urllib.request import urlopen
import pymongo

nom = ArcGIS()


def generate_mapwithlist2():
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    client = pymongo.MongoClient("mongodb+srv://sudipta01:Sudipta01@cluster0.pmtaryj.mongodb.net/ambulance")
    mydb = client["ambulance"]
    mycol = mydb["gari"]

    loc = "22.559628171320554,88.39632949346063"

    s = loc.split(',')
    lat = s[0]
    lon = s[1]
    coords_1 = (lat, lon)

    li1 = []
    li2 = []

    filcol = mycol.find()
    for z in filcol:
        if (math.isnan(z['latitude']) == False and math.isnan(z['longitude']) == False):
            coords_2 = (z['latitude'], z['longitude'])
            dis = geopy.distance.geodesic(coords_1, coords_2).km
            if (dis < 100):
                li1.append({'longitude': z['longitude'],
                            'latitude': z['latitude'], 'Name': z['Health Facility Name']})
                li2.append(
                    {'Name': z['Health Facility Name'], 'Distance': int(int(dis) * 1.12)})

    # Map ka code
    hos_map = folium.Map(location=[lat, lon], zoom_start=12)

    fg = folium.FeatureGroup(name='Sixcodeminds')

    for i in li1:
        fg.add_child(folium.Marker(
            location=[i['latitude'], i['longitude']], popup=i['Name'],
            icon=folium.Icon(color='green', icon='ambulance', prefix='fa')))

    fg.add_child(folium.Marker(
        location=[lat, lon], icon=folium.Icon(color='blue'), popup="Your Location"))

    hos_map.add_child(fg)

    hos_map.save('templates/hos2map.html')

    # MAP END

    # List Ka Code
    li2.sort(key=lambda x: x["Distance"])
    tbl = "<tr><td>car no</td><td>Distance</td><td>Contact</td></tr>"
    c = 0
    for y in li2:
        if c == 8:
            break

        c = c + 1
        a = "<tr onclick='fetchRowData(\"%s\")'><td class='hfn'>%s</td>" % (y['Name'], y['Name'])

        b = "<td>%s</td>" % y['Distance']


        tbl = tbl + a + b

    contents = '''<!DOCTYPE html>
    <html lang="en">
    <html>
    <head>
    <script src="https://kit.fontawesome.com/de9d45e1c6.js" crossorigin="anonymous"></script>
    <meta http-equiv="content-type">
    <link rel="stylesheet" href="/static/mapliststyle.css">
    <title>Hospital</title>
    </head>
    <body>
    <div class="twoparts">
        <div class="container">
            <div class="containerhead">
                <label for="Search" class="label1">Choose a Ambulance</label>
                    <form action="" class="searchbar">
                    <input type="text" id="myinput" placeholder="Search Nearby Ambulance" onkeyup="searchFun()">
                    </form>
                <label for="mention" class="label2">Nearby Ambulences</label>
            </div>
    <table  id="mytable">
    %s
    </table>
    <div class="button">
        <a type="button" onclick=window.location='payment.html' class="btn">BOOK AMBULANCE</a>
    </div>    
        </div>
        <div class = container2>
            <iframe src="hos2map.html" width="1700px" height="900" >
        </iframe>
        </div>

        </div>
        <script>
        
        
        
             function fetchRowData(name) {
    // Make an asynchronous request to fetch data using the name of the hospital
    fetch('http://127.0.0.1:5000/get_data?name=' + encodeURIComponent(name))
        .then(response => response.json())
        .then(data => {
            // Construct the URL with the data parameter using template literals
            const url = `confirmation.html?name=${encodeURIComponent(data.name)}`;
            
            // Navigate to the new URL
            window.location.replace(url);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


            const searchFun = () => {
                let filter = document.getElementById('myinput').value.toUpperCase();

                let myTable = document.getElementById('mytable');

                let tr = myTable.getElementsByTagName('tr');

                for (var i = 0; i < tr.length; i++) {
                    let td = tr[i].getElementsByTagName('td')[0];

                    if (td) {
                        let textvalue = td.textContent || td.innerHTML;

                        if (textvalue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        }
                        else 
                        {
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
            </script>
            
    </body>
    </html>
    ''' % (tbl)

    filename = 'templates/info2.html'

    # List Code End

    def main(contents, filename):
        output = open(filename, "w")
        output.write(str(contents))
        output.close()

    main(contents, filename)

    # webbrowser.open(filename)
    # webbrowser.open('info.html')

# generate_mapwithlist()

# window.location = "confirmation.html";
