
			<div id="header">
                <div class="logo"><img src="img/gtonline_logo.png" style="opacity:0.5;background-color:E9E5E2;" border="0" alt="" title="GT Online Logo"/></div>
			</div>
			
			<div class="nav_bar">
				<ul>    
                    <li><a href="view_profile.php" <?php if($current_filename=='view_profile.php') echo "class='active'"; ?>>View Profile</a></li>                       
					<li><a href="edit_profile.php" <?php if(strpos($current_filename, 'edit_profile.php') !== false) echo "class='active'"; ?>>Edit Profile</a></li>  
                    <li><a href="view_friends.php" <?php if($current_filename=='view_friends.php') echo "class='active'"; ?>>View Friends</a></li>  
                    <li><a href="search_friends.php" <?php if($current_filename=='search_friends.php') echo "class='active'"; ?>>Search for Friends</a></li>  
                    <li><a href="view_requests.php" <?php if($current_filename=='view_requests.php') echo "class='active'"; ?>>View Requests</a></li>  
                    <li><a href="view_updates.php" <?php if($current_filename=='view_updates.php') echo "class='active'"; ?>>View Status Updates</a></li>  
                    <li><a href="logout.php" <?php if($current_filename=='logout.php') echo "class='active'"; ?>>Log Out</a></li>              
				</ul>
			</div>