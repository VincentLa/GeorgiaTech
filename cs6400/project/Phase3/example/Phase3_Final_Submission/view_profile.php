<?php

include('lib/common.php');
// written by GTusername4

if (!isset($_SESSION['email'])) {
	header('Location: login.php');
	exit();
}

    $query = "SELECT firstname, lastname, sex, birthdate, currentcity, hometown " .
		 "FROM user " .
		 "INNER JOIN regularuser ON user.email=regularuser.email " .
		 "WHERE user.email='{$_SESSION['email']}'";

    $result = mysqli_query($db, $query);
    include('lib/show_queries.php');
 
    if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    } else {
        array_push($error_msg,  "Query ERROR: Failed to get user profile..." . __FILE__ ." : ". __LINE__ );
    }
?>

<?php include("lib/header.php"); ?>
<title>GTOnline Profile</title>
</head>

<body>
		<div id="main_container">
    <?php include("lib/menu.php"); ?>

    <div class="center_content">
        <div class="center_left">
            <div class="title_name">
                <?php print $row['firstname'] . ' ' . $row['lastname']; ?>
            </div>          
            <div class="features">   
            
                <div class="profile_section">
                    <div class="subtitle">View Profile</div>   
                    <table>
                        <tr>
                            <td class="item_label">Sex</td>
                            <td>
                                <?php if ($row['sex'] == 'M') { print 'Male';} else {print 'Female';} ?>
                            </td>
                        </tr>
                        <tr>
                            <td class="item_label">Birthdate</td>
                            <td>
                                <?php print $row['birthdate'];?>
                            </td>
                        </tr>
                        <tr>
                            <td class="item_label">Current City</td>
                            <td>
                                <?php print $row['currentcity'];?>
                            </td>
                        </tr>

                        <tr>
                            <td class="item_label">Hometown</td>
                            <td>
                                <?php print $row['hometown'];?>
                            </td>
                        </tr>

                        <tr>
                            <td class="item_label">Interests</td>
                            <td>
                                <ul>
                                    <?php
                                            $query = "SELECT interest FROM userinterests WHERE email='{$_SESSION['email']}'";
                                            $result = mysqli_query($db, $query);
                                            include('lib/show_queries.php');
                                             
                                             if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                                    array_push($error_msg,  "Query ERROR: Failed to get user interests..." . __FILE__ ." : ". __LINE__ );
                                             }
                                                 
                                            while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)){
                                                print "<li>{$row['interest']}</li>";
                                            }
										?>
                                </ul>
                            </td>
                        </tr>
                    </table>						
                </div>

                <div class="profile_section">
                    <div class="subtitle">Education</div>  
                    <table>
                        <tr>
                            <td class="heading">School</td>
                            <td class="heading">Year Graduated</td>
                        </tr>							

                        <?php
									    $query = "SELECT schoolname, yeargraduated " . 
											 "FROM attend " .
											 "WHERE email='{$_SESSION['email']}' " .
											 "ORDER BY yeargraduated DESC";
									    $result = mysqli_query($db, $query);
                                        include('lib/show_queries.php');
                                        
                                        if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                                    array_push($error_msg,  "Query ERROR: Failed to get school information..." . __FILE__ ." : ". __LINE__ );
                                             } 
									while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
										print "<tr>";
										print "<td>" . $row['schoolname'] . "</td>";
										print "<td>" . $row['yeargraduated'] . "</td>";
										print "</tr>";
									}
								?>
                    </table>						
                </div>	

                <div class="profile_section">
                    <div class="subtitle">Professional</div>  
                    <table>
                        <tr>
                            <td class="heading">Employer</td>
                            <td class="heading">Job Title</td>
                        </tr>							

                        <?php
                                        $query = "SELECT employername, jobtitle " . 
											 "FROM employment " .
											"WHERE email='{$_SESSION['email']}' " .
											 "ORDER BY employername DESC";
									   $result = mysqli_query($db, $query);
                                       include('lib/show_queries.php');
                                       if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                                    array_push($error_msg,  "Query ERROR: Failed to get employment information..." . __FILE__ ." : ". __LINE__ );
                                             } 
                                             
									while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
										print "<tr>";
										print "<td>" . $row['employername'] . "</td>";
										print "<td>" . $row['jobtitle'] . "</td>";
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