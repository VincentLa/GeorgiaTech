<?php

include('lib/common.php');
// written by GTusername3

if (!isset($_SESSION['email'])) {
	header('Location: login.php');
	exit();
}

$query = "SELECT firstname, lastname, sex, birthdate, currentcity, hometown " .
		 "FROM user " .
		 "INNER JOIN regularuser ON user.email = regularuser.email " .
		 "WHERE user.email = '{$_SESSION['email']}'";
         
$result = mysqli_query($db, $query);
include('lib/show_queries.php');
    
if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $count = mysqli_num_rows($result);
} else {
        array_push($error_msg,  "SELECT ERROR: user profile " . __FILE__ ." : ". __LINE__ );
}

    $user_name = $row['firstname'] . " " . $row['lastname'];
?>

<?php include("lib/header.php"); ?>
		<title>GTOnline View Friends</title>
	</head>
	
	<body>
        <div id="main_container">
		    <?php include("lib/menu.php"); ?>
            
			<div class="center_content">
				<div class="center_left">
					<div class="title_name"><?php print $user_name; ?></div>          
					
					<div class="features">   	
						<div class="profile_section">
                        	<div class="subtitle">View Friends</div>   
							<table>
								<tr>
									<td class="heading">Name</td>
									<td class="heading">Relationship</td>
									<td class="heading">Connected Since</td>
								</tr>
																
								<?php								
                                    $query = "SELECT firstname, lastname, relationship, dateconnected " .
                                             "FROM friendship " .
                                             "INNER JOIN regularuser ON regularuser.email = friendship.friendemail " .
                                             "INNER JOIN user ON user.email = regularuser.email " .
                                             "WHERE friendship.email='{$_SESSION['email']}'" .
                                             "AND dateconnected IS NOT NULL " .
                                             "ORDER BY dateconnected DESC";
                                             
                                    $result = mysqli_query($db, $query);
                                     if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                         array_push($error_msg,  "SELECT ERROR: find friendship" . __FILE__ ." : ". __LINE__ );
                                    }
                                    
                                    while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)){
                                        print "<tr>";
                                        print "<td>{$row['firstname']} {$row['lastname']}</td>";
                                        print "<td>{$row['relationship']}</td>";
                                        print "<td>{$row['dateconnected']}</td>";
                                        print "</tr>";							
                                    }									
                                ?>
							</table>						
						</div>	
					 </div> 
				</div> 
                
                <?php include("lib/error.php"); ?>
                    
				<div class="clear"></div> 
			</div>    

               <?php include("lib/footer.php"); ?>
		 
		</div>
	</body>
</html>