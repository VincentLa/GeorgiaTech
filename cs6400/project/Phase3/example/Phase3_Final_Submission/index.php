<?php

// written by GTusername1

session_start();
if (empty($_SESSION['email']) ){
    header("Location: login.php");
    die();
}else{
    header("Location: view_profile.php");
    die();
}
?>