<?php
 $bdd = new PDO('mysql:host=localhost;dbname=TestProjetYES', 'root', 'pass');
 
 $req = $bdd->prepare("SELECT * FROM comptage");
 $req->execute();
 $data = $req->fetch();


?>
<!DOCTYPE html>

<html lang="en">

<head>
  <meta charset="utf-8" name="viewport" content="device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
</head>
<meta http-equiv="refresh" content="2">
<body>
  <div class="wrapper">
    <div class="one">
	<h1>Félicitations vous êtes le <?php echo $data['cycliste'];?> ème cycliste</h1>
    </div>
    <div class="two">
      <h1>La qualité de l'air est de <?php echo $data['valeur_air'];?> /5</h1>
    </div>
    <div class="three">
      <h1>L'air est : <?php echo $data['qualif_air'];?></h1>
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


</html>
