<?php

if(isset($_POST["id"]))
{
$data = array();
$mysqli = new mysqli("localhost", "root", "root", "ihlp");	
$sql = "select peer_ip,peer_lat,peer_lon,peer_city,count(*) as count from top_tx group by peer_ip,peer_lat,peer_lon,peer_city;";
$result = $mysqli->query($sql);
while($row = $result->fetch_assoc())
{
	$data[]=$row;
}
echo json_encode($data);

}
?>
