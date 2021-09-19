var dota;
var myD = [];
var ICAO_keys = [];
// const api_url = 'http://localhost:8001';
const api_url = 'http://192.168.50.12:8001';
// const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
const image = '/plane1.png' // the imgage we'll use as a marker
// this creates a map on the web page and marks objects on it
let markers = [];
let markerICAO = [];
let markerDic = {}; // contains dictionary of all aircraft info received
var map;

function initMap(){
    var options = {
            zoom:7,
            center:{lat:23.8363 , lng: 90.4177}
    };  
    

    map = new google.maps.Map(document.getElementById('map'), options);
    addMarker({lat:23.8363 , lng: 90.4177});
    addMarker({lat:23.8434 , lng: 90.4029});
    // addMarker({lat:23.8444 , lng: 90.4035});
    function addMarker(coords, icao){
        var marker = new  google.maps.Marker({
            position:coords,
            map: map,
            icon: image,
            labelContent: "airport",
            labelAnchor: new google.maps.Point(18, 12),
            labelInBackground: true
        });
        markers.push(marker);
        markerDic[icao]=marker;
    };

}
function getIcaoKeys(data){
    keys = []
    for (indx in data){
        keys.push(data[indx]['icao']);
    }
    return keys;
}
function getMarkerLatFromIcao(icao){
    for(indx in markers){
        if(markers[indx]["label"] == icao){
            console.log('aajajajjaja');
            console.log(markers[indx].position.lat());
            return markers[indx].position.lat();
        }
    }
}
async function addMarker(coords, icao){ // adds new marker 

       
        // var myIcon ={
        //         path: "M134.875,19.74c0.04-22.771,34.363-22.771,34.34,0.642v95.563L303,196.354v35.306l-133.144-43.821v71.424l30.813,24.072 v27.923l-47.501-14.764l-47.501,14.764v-27.923l30.491-24.072v-71.424L3,231.66v-35.306l131.875-80.409V19.74z",

                
        //         fillColor: "red",
        //         fillOpacity: 0.8,
        //         strokeWeight: 0,
        //         rotation: 0,
        //         scale: .08,
        //         anchor: new google.maps.Point(15, 30),
        //         labelOrigin: new google.maps.Point(-150,-80),
        //         // labelClass : "my-custom-class-for-label",
        //         labelInBackground: true
        //     }

        //new google.maps.Marker({
        //new MarkerWithLabel({
        // icon: myIcon,    
        var marker = new google.maps.Marker({
            position:coords,
            icon: {
                path: "M134.875,19.74c0.04-22.771,34.363-22.771,34.34,0.642v95.563L303,196.354v35.306l-133.144-43.821v71.424l30.813,24.072 v27.923l-47.501-14.764l-47.501,14.764v-27.923l30.491-24.072v-71.424L3,231.66v-35.306l131.875-80.409V19.74z",

                
                fillColor: "red",
                fillOpacity: 0.8,
                strokeWeight: 0,
                rotation: 0,
                scale: .08,
                anchor: new google.maps.Point(15, 30),
                labelOrigin: new google.maps.Point(-150,-80),
                // labelClass : "my-custom-class-for-label",
                labelInBackground: true
            },
            label: {
                text: icao,
                color: "blue",
                fontSize: "10px",
                fontWeight: "bold"
            }
        });
        var infoWindow = new google.maps.InfoWindow({
            content: `<h5>ICAO: ${icao}</h5>
                      <p>lat: ${ getMarkerLatFromIcao(icao)}</p>
                      <p>long: ${coords["lng"]}</p>
                      <p>inFlight: </p>
                      <p>ground: </p>`
        });
        marker.addListener('click', function(){
            infoWindow.open(map, marker);
        })
        marker.addListener('click', function(){
            myIcao = marker.label.text;
            // console.log(myIcao);
            openNav(myIcao);
        })

        markerICAO.push(icao);
        markers.push(marker);
        markerDic[icao]=marker;
        // console.log(icao);
        marker.setMap(map);
    }
async function updateMarker(coords, icao, angle){ // updates marker position and angle
    var marker = markerDic[icao];
    marker.setPosition(coords);

    myIcon = markerDic[icao].getIcon() 
    myIcon["rotation"] = angle
    // console.log(myIcon);
    markerDic[icao].setIcon(myIcon)
}

async function getData(){
    const response = await fetch(api_url);
    const data = await response.json();
    // this.ICAO_keys = Object.keys(data); //
    this.ICAO_keys = getIcaoKeys(data); //
    var data_length = ICAO_keys.length;
    dota = data; // for testing purpose the data we get is set to global var dota
    // console.log(ICAO_keys);
    // console.log('data');
    // console.log(data);
    // console.log("data")
    
    for(indx in data){
        var latT = data[indx]["flightInfo"]["lat"]; // latitude of current info received
        var lngT = data[indx]["flightInfo"]["long"]; // longitude of current info received
        var angle =  data[indx]["flightInfo"]["angle"];
        var key = data[indx]['icao'] // key is the icao number
        
        if(markerICAO.includes(data[indx]['icao'])){
            updateMarker({lat: Number(latT) , lng: Number(lngT)}, key, angle);
            // console.log("update marker");
        }
        else{
            addMarker({lat: Number(latT) , lng: Number(lngT)}, key);
            console.log("add marker");
        }
        // if icao doesn't exist then addMarker() else updateMarker() 
        // if( markerICAO.includes(key) ){
        //     // updateMarker({lat: Number(latT) , lng: Number(lngT)}, key);
        // }else{
        //     addMarker( {lat: Number(latT) , lng: Number(lngT)}, key);
        // }
    }
}


getData();
setInterval(getData, 2000);