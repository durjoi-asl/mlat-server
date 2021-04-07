console.log('indide sidebar file');

let sidebarIcao;
let sidebarUpdaterTimerID;
function wasupSidebar(){
    console.log('wassssup');
}


/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav(icao) {
    console.log(icao);
    sidebarIcao = icao
    lat = markerDic[icao].getPosition().lat();
    lng = markerDic[icao].getPosition().lng();
    console.log(markerDic[icao].getPosition());
    console.log("opening nav");
    // console.log(document.getElementById("mySidebar").innerHTML);
    document.getElementById("mySidebar").innerHTML = "";
    document.getElementById("mySidebar").innerHTML += ` <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
                                                        <p>Plane info</p>
                                                        <h2>icao: ${icao}</h2>
                                                        <h2 id="sideLat">lat: ${lat}</h2>
                                                        <h2 id="sideLng">lng: ${lng}</h2>`
    
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    
    sidebarUpdaterTimerID=setInterval(changeLatLong,1500)
  }

  function changeLatLong(){
      document.getElementById('sideLat').innerText="lat: "+markerDic[sidebarIcao].getPosition().lat();
      document.getElementById('sideLng').innerText="lng: "+markerDic[sidebarIcao].getPosition().lng();
      console.log('changed lat lng');
  }
  
  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
  function closeNav() {
    clearInterval(sidebarUpdaterTimerID);
    console.log('closing nav');
    document.getElementById("mySidebar").innerHTML = "";
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0"; 
  } 