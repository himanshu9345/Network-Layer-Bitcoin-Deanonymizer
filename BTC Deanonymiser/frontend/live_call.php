<?php

if(isset($_POST["id"]))
{
$data = array();
$mysqli = new mysqli("localhost", "root", "root", "ihlp");	
$sql = " select tx_id,peer_lat,peer_lon,peer_ip from live_tx where tx_time in (select max(tx_time) from live_tx group by peer_lat,peer_lon having count(*)<10);";
$result = $mysqli->query($sql);
while($row = $result->fetch_assoc())
{
	$data[]=$row;
}
echo json_encode($data);

}
?>
