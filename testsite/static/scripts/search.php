<?php
$mysqli = new mysqli('localhost', 'root', 'admin', 'django');

if($mysqli->connect_errno) {
  printf("Connection Failed: %s\n", $mysqli->connect_error);
  exit;
}

$stmt = $mysqli->prepare("SELECT id, name FROM `phototagz_tag` WHERE LOWER(CAST(name AS CHAR)) LIKE LOWER(?) ORDER BY count DESC LIMIT 15");

if(!$stmt){
	printf("Query Prep Failed: %s\n", $mysqli->error);
	exit;
}

$query = '%'.$_GET['query'].'%';


$stmt->bind_param('s', $query);
$stmt->execute();
$stmt->bind_result($id, $name);

$result = array();
$i=0;

while($stmt->fetch()) {
	$result[$i]['title']=$name;
	$result[$i]['id']=$id;
	$i++;
}

echo json_encode($result);

$stmt->close();

exit;
?>
