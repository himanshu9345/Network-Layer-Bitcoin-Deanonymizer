<?php  $mysqli = new mysqli("localhost", "root", "root", "ihlp");
if($mysqli->connect_error) {
  exit('Could not connect');
} ?>

<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script type="text/javascript"></script>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Circles</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="map">
      
    </div>
    <script >
$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 5000);
});

function executeQuery()
{

}

  
      // This example creates circles on the map, representing populations in North
      // America.
var cityz = {};
      // First, create an object containing LatLng and population for each city.
      var citymap = {
       
         Australia: {
          center: {lat: -25.274, lng: 133.775},
          population: 170000
        },
         
      };

      function initMap() {
        
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: {lat: 37.090, lng: -95.712},
          mapTypeId: 'terrain'
        });

        
var queue=[];


        // Construct the circle for each value in citymap.
        // Note: We scale the area of the circle based on the population.

setInterval(function(){


       
<?php 
$sql = "SELECT distinct peer_lat,peer_lon FROM top_tx ";
$result = $mysqli->query($sql);

while($row = $result->fetch_assoc()) { ?>
            
          // Add the circle for this city to the map.
          var gg={lat: parseFloat(<?php echo $row["peer_lat"]; ?> ), lng:  parseFloat(<?php echo $row["peer_lon"]; ?>)};
	

            var cityCircle= new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center:gg ,
            radius: Math.sqrt(16) * 20000
          });

queue.push(cityCircle);

setTimeout(function(){
var ok =queue.shift();
       ok.setMap(null);
            delete ok;

		          },5000);
     

     

     
      <?php 

} 

 ?>

        
      },10000);
}

    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBbr04VUifYCzcyLyjl5fePn6kpc6IL4oE&callback=initMap">
    </script>
  </body>
</html>

