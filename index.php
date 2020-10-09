<?php
 $bdd = new PDO('mysql:host=localhost;dbname=TestProjetYES', 'root', 'pass');
 
 $req = $bdd->prepare("SELECT cycliste FROM comptage");
 $req->execute();
 $data = $req->fetch();

?>
<!DOCTYPE html>

<html lang="en">

<head>
  <meta charset="utf-8" name="viewport" content="device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="wrapper">
    <div class="one">
      <div class="text">Cyclistes</div>
      <div class="numbers">1000</div>
    </div>
    <div class="two">
      <div class="text">Qualité de l'air</div>
      <div class="numbers">BON</div>
    </div>
    <div class="three">
      <div class="text">Température</div>
      <div class="numbers">32˚C</div>
    </div>
    <div class="four">
      <div class="text">Informations</div>
      <div class="numbers"> Accident sur votre trajet</div>
    </div>
  </div>
</body>

<script type="text/javascript">
  setTimeout(function(){
    window.location.reload(1);
  }, 30000);
</script>
	<div>
		<h1><?php echo $data['score'];?> pts</h1>
	</div>

</html>
