<?php
include('conn.php');
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Optimation Route Aplication</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="../Implementasi ke Web/index.css">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100&family=Poppins:wght@300&display=swap" rel="stylesheet">
    </head>
    <body>
        <section class="menu">

           <h1 class="text-center" style="font-family: 'Poppins', sans-serif; font-weight: bold; font-size: 2rem; font-style: italic;">Optimation Route Application</h1> 

            <form>
                <div class="btn-menu d-grid gap-2">
                    <a href="../Implementasi ke Web/TSP/tsp.php" class="btn btn-success" type="button">Traveling Salesperson</a>
                    <a href="../Implementasi ke Web/VRP/vrp.html" class="btn btn-success" type="button">Vehicle Routing Problem</a>
                    <a href="../Implementasi ke Web/Capacity/capacity.html" class="btn btn-success" type="button">Capacity Constraint</a>
                </div>
            </form>
            <div class="add-locations">
                <div class="btn-add d-grid gap-2 rounded">
                    <p style="margin: 0rem">Tambahkan lokasi <a href="#">disini</a></p>
                <div>
            </div>
        </section>
    </body>
</html>