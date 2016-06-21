from bs4 import BeautifulSoup

htmldoc = """
<html>
	<head>
		<meta http-equiv="X-UA-Compatible" content="IE=8" />
		
		<title>Dining Menus | UCLA Dining Services</title>
		
		<!-- <script type="application/javascript" src="http://m.ucla.edu/assets/redirect/js.php?m=http://m.dining.ucla.edu/menu/index.cfm?restaurantType=Residential"></script> -->
		
		<link rel="stylesheet" href="/lib/fancybox/jquery.fancybox-1.3.4.css" type="text/css" media="screen" />
		
		<link rel="stylesheet" type="text/css" href="css/global.css" />
		<link rel="stylesheet" type="text/css" href="css/menu.css" />
		
		<script type="text/javascript" src="/lib/jquery/jquery-1.6.4.min.js"></script>
		<script type="text/javascript" src="/lib/fancybox/jquery.fancybox-1.3.4.pack.js"></script>
		<script type="text/javascript" src="/lib/tooltip/jquery.tools.min.js"></script>
		<script type="text/javascript" src="/lib/sticky/jquery.sticky.js"></script>
		
		<script type="text/javascript" src="js/global.js"></script>
		<script type="text/javascript" src="js/controls.js"></script>
		<script type="text/javascript" src="js/menu.js"></script>
		<script type="text/javascript" src="js/recipebox.js"></script>
		<script type="text/javascript" src="js/tooltip.js"></script>
		
		<script language="javascript">
		
			
			recipeInfo["031001"] = "Smooth and comforting wheat porridge served hot.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["031002"] = "A mildly sweet porridge made from a blend of farina wheat and malted barley.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["031003"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061005"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["061016"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["161029"] = "Roasted potatoes seasoned with salt and paprika.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061074"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["061001"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["061034"] = "Fluffy cage-free scrambled eggs.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["217033"] = "Belgian waffle cooked until crispy and golden-brown. \n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["161012"] = "Crispy bite-sized potatoes, fried until golden-brown. \n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["217041"] = "Cinnamon french toast, cooked until golden brown.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979291"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["157149"] = "Thick and savory gravy. ";
			recipeInfo["400035"] = "Soft and fluffy medium grain rice grown in California.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["979340"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979416"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979412"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979425"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979418"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979423"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979398"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["979402"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["031010"] = "Warm and creamy hot cereal made from toasted wheat.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061035"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["047122"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061073"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["132026"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["061025"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061013"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["061020"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["061014"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["089011"] = "Thick cut bacon, baked until crisp. ";
			recipeInfo["161013"] = "Potato hash browns, grilled until golden brown. \n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["089020"] = "Spicy grilled sausage.";
			recipeInfo["189029"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["204010"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["204001"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["217001"] = "Light and fluffy buttermilk pancakes, cooked until golden brown. \n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["970242"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["201011"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["201031"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["031007"] = "A warm and hearty breakfast porridge made from steel-cut oats.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["042081"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["132033"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["047155"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["047160"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["160023"] = "Warmed flour tortilla.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["977188"] = "Roast tomato salsa with Jalapeño peppers, garlic, onion, and fresh cilantro.  \n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["189130"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["205002"] = "<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/V.png\" alt=\"Vegetarian Menu Option\" />&nbsp;Vegetarian Menu Option</div>\n";
			recipeInfo["161003"] = "Crispy, golden-brown potato hash brown patties.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";
			recipeInfo["167132"] = "<i>Com Tam</i>&nbsp;|&nbsp;Vietnam<br />Broken jasmine rice with a nutty flavor, steamed until fluffy.\n<hr class=\"ttspacer\" />\n<div class=\"ttlegend\"><img class=\"webcode\" src=\"images/webcodes/VG.png\" alt=\"Vegan Menu Option\" />&nbsp;Vegan Menu Option</div>\n";

		
		</script>
		
		<!-- Google Analytics Code -->
		<script type="text/javascript">
			var _gaq = _gaq || [];
			_gaq.push(['_setAccount', 'UA-32722183-1']);
			_gaq.push(['_trackPageview', '/foodpro/default.asp?date=6%2F20%2F2016&meal=1&threshold=2&DaysAhead=2']);

			(function() {
				var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
				ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
				var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
			})();

		</script>
		<!-- End Google Analytics Code -->
	</head>
	
	<body id="top">
		<div id="globalwrapper">
			<div class="hdr sticky-wrapper">
				
			<table class="hdrtable"><tbody><tr>
				<td class="hdrlogo">
					<a href="http://www.dining.ucla.edu/"><img src="images/ds_logo_2015.png"></a>
				</td>
				<td>
					<table><tbody><tr>
                                   	<td class="hdrchunk" valign="middle">
							<ul class="hdrlist">
								<li class="hdrtitle">UCLA Dining Services</li>
								<li><a href="http://www.dining.ucla.edu/">Dining Home</a></li>
								<li><a href="https://secure5.ha.ucla.edu/restauranthours/dining-hall-hours-by-day.cfm">Hours of Operation</a></li>
								<li><a href="http://housing.ucla.edu/dining-services/overview/facilities-services">Dining Locations</a></li>
								<!-- <li><a href="http://housing.ucla.edu/dining-services/services-programs">Services &amp; Programs</a></li> -->
								<li><a href="default.asp">Today's Entr&eacute;es</a></li>
							<!-- </ul>
						</td>
						<td class="hdrchunk" valign="middle">
							<ul class="hdrlist">
								<li class="hdrtitle">Quick-Service Restaurants</li>
								<li><a href="http://menu.ha.ucla.edu/foodpro/bruincafe.asp">Bruin Caf&eacute; Menu</a></li> -->
								<li><a href="http://menu.ha.ucla.edu/foodpro/cafe1919_summer.asp">Caf&eacute; 1919 Menu</a></li> 
								<!-- <li><a href="http://menu.ha.ucla.edu/foodpro/denevelatenight.asp">De Neve Late Night Menu</a></li>
								<li><a href="http://menu.ha.ucla.edu/foodpro/deneveonthego.asp">De Neve Grab 'N Go Menu</a></li>
								<li><a href="http://menu.ha.ucla.edu/foodpro/rendezvous.asp">Rendezvous Menu</a></li>
							</ul>
						</td>
						<td class="hdrchunk" valign="middle">
							<ul class="hdrlist">
								<li class="hdrtitle">Additional Services</li>
								<li><a href="https://shib.hhs.ucla.edu/mypizza/index.cfm">MyPizza &amp; Wings</a></li>
								<li><a href="http://housing.ucla.edu/dining-services/nutrition-education">Nutrition Education</a></li> 
								<li><a href="http://housing.ucla.edu/dining-services/comments-suggestions">Comments &amp; Suggestions</a></li>
								<li><a href="http://m.dining.ucla.edu/">Mobile Site</a></li>-->
							</ul>
						</td>
					</tr></tbody></table>
					&nbsp;
				</td>
			</tr></tbody></table>


		
			
				<div class="midnav sticky-wrapper">
		
					<span class="midnavbreadcrumb"><a href="default.asp">Menus</a>&nbsp;&gt;&nbsp;<a href="default.asp?date=6%2F20%2F2016">Monday, 6/20/2016</a>&nbsp;&gt;&nbsp;Breakfast</span>
				
					

			<div class="midnavcontrols">
				<form name="searchform" action="search.asp" method="post">
				
					<a id="filterlink" href="filter.asp">Configure Menu Filters</a>&nbsp;
					
					<!-- The following is required by Aurora Information Systems, DO NOT MODIFY OR REMOVE -->
						<!-- allergenfilterinc.asp, Version 2.3.3  -->
					<!-- End of Aurora Information Systems Required Text --> 
				
					<select name="dateselect" id="dateselect" onChange="window.location = this.options[this.selectedIndex].value">
						<option value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F20%2F2016&meal=1&threshold=2">Jump to Date...</option>
												<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F17%2F2016&meal=1&threshold=2">Yesterday, Jun 17</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F18%2F2016&meal=1&threshold=2">Today, Jun 18</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F19%2F2016&meal=1&threshold=2">Tomorrow, Jun 19</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F20%2F2016&meal=1&threshold=2">Monday, Jun 20</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F21%2F2016&meal=1&threshold=2">Tuesday, Jun 21</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F22%2F2016&meal=1&threshold=2">Wednesday, Jun 22</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F23%2F2016&meal=1&threshold=2">Thursday, Jun 23</option>
						<option Value="http://menu.ha.ucla.edu/foodpro/default.asp?date=6%2F24%2F2016&meal=1&threshold=2">Friday, Jun 24</option>

					</select>
		
					<!-- The following is required by Aurora Information Systems, DO NOT MODIFY OR REMOVE -->
						<!-- date.asp, Version 2.3.0  -->
					<!-- End of Aurora Information Systems Required Text --> 
			

					<input class="searchboxblurred" id="searchbox" type="text" name="search" value="Menu Search" onFocus="SearchFocus()" onBlur="SearchBlur()" />
					<input class="midnavbutton" type="image" src="images/search.png" />
				</form>
			</div>
				
		
				
				</div>
			</div>
				
			<hr class="clearall" />
		
			<div id="tooltip">&nbsp;</div>
			
			<div id="menuwrapper">
			
				<div class="menucontent">
				<table class="menugridtable" cellspacing="0"><tbody>
					<tr>
						<td class="menumealheader" colspan="3">
							Breakfast Menu for Monday, June 20, 2016
						</td>					</tr>
					<tr>
						<td class="menulocheader"><a class="menuloclink" href="default.asp?location=07&date=6%2F20%2F2016">Covel Dining</a></td>
						<td class="menulocheader"><a class="menuloclink" href="default.asp?location=02&date=6%2F20%2F2016">Sproul Dining</a></td>
						<td class="menulocheader"><a class="menuloclink" href="default.asp?location=04&date=6%2F20%2F2016">Rieber Dining</a></td>
					</tr>
					<tr>
						<td class="menunutritionlink"><a href="default.asp?location=07&date=6%2F20%2F2016">Full Menu</a>&nbsp;|&nbsp;<a href="nutritiveanalysis.asp?location=07&date=6%2F20%2F2016&meal=1">Nutritive Analysis</a></td>
						<td class="menunutritionlink"><a href="default.asp?location=02&date=6%2F20%2F2016">Full Menu</a>&nbsp;|&nbsp;<a href="nutritiveanalysis.asp?location=02&date=6%2F20%2F2016&meal=1">Nutritive Analysis</a></td>
						<td class="menunutritionlink"><a href="default.asp?location=04&date=6%2F20%2F2016">Full Menu</a>&nbsp;|&nbsp;<a href="nutritiveanalysis.asp?location=04&date=6%2F20%2F2016&meal=1">Nutritive Analysis</a></td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category4">Hot Cereals</li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031001&PortionSize=6" onmouseover="SetRecDesc('031001');">Cream of Wheat</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031002&PortionSize=6" onmouseover="SetRecDesc('031002');">Malt-O-Meal</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031003&PortionSize=6" onmouseover="SetRecDesc('031003');">Oatmeal</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category4">Hot Cereals</li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031003&PortionSize=6" onmouseover="SetRecDesc('031003');">Oatmeal</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031010&PortionSize=6" onmouseover="SetRecDesc('031010');">Wheatena</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category4">Hot Cereals</li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031001&PortionSize=6" onmouseover="SetRecDesc('031001');">Cream of Wheat</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=031007&PortionSize=6" onmouseover="SetRecDesc('031007');">Oatmeal</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category5">Exhibition Kitchen</li>
								<li class="level5"><a class="itemlink" href="recipedetail.asp?RecipeNumber=061039&PortionSize=1" onmouseover="SetRecDesc('061039');">Cheese Omelet</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061005&PortionSize=1" onmouseover="SetRecDesc('061005');">Egg White</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlink" href="recipedetail.asp?RecipeNumber=061028&PortionSize=1" onmouseover="SetRecDesc('061028');">Ham &amp; Cheese Omelet</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061016&PortionSize=1" onmouseover="SetRecDesc('061016');">Spinach, Tomato &amp; Cheese Omelet</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category5">Exhibition</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061005&PortionSize=1" onmouseover="SetRecDesc('061005');">Egg White</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061035&PortionSize=1" onmouseover="SetRecDesc('061035');">Omelet Bar</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">w/&nbsp;<a class="itemlink" href="recipedetail.asp?RecipeNumber=061012&PortionSize=1" onmouseover="SetRecDesc('061012');">Bacon</a></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=047122&PortionSize=1" onmouseover="SetRecDesc('047122');">Diced Green Peppers</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061073&PortionSize=1" onmouseover="SetRecDesc('061073');">Diced Tomatoes</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=132026&PortionSize=1" onmouseover="SetRecDesc('132026');">Feta Cheese</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061025&PortionSize=1" onmouseover="SetRecDesc('061025');">Green Onions</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlink" href="recipedetail.asp?RecipeNumber=977264&PortionSize=1" onmouseover="SetRecDesc('977264');">Ham</a></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061013&PortionSize=1" onmouseover="SetRecDesc('061013');">Shredded Cheddar Cheese</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061020&PortionSize=1" onmouseover="SetRecDesc('061020');">Sliced Mushrooms</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061014&PortionSize=1" onmouseover="SetRecDesc('061014');">Spinach</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category5">Exhibition</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061005&PortionSize=1" onmouseover="SetRecDesc('061005');">Egg White</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061035&PortionSize=1" onmouseover="SetRecDesc('061035');">Omelet Bar</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">w/&nbsp;<a class="itemlink" href="recipedetail.asp?RecipeNumber=061012&PortionSize=1" onmouseover="SetRecDesc('061012');">Bacon</a></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=047122&PortionSize=1" onmouseover="SetRecDesc('047122');">Diced Green Peppers</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061073&PortionSize=1" onmouseover="SetRecDesc('061073');">Diced Tomatoes</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061025&PortionSize=1" onmouseover="SetRecDesc('061025');">Green Onions</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlink" href="recipedetail.asp?RecipeNumber=977264&PortionSize=1" onmouseover="SetRecDesc('977264');">Ham</a></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061013&PortionSize=1" onmouseover="SetRecDesc('061013');">Shredded Cheddar Cheese</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061020&PortionSize=1" onmouseover="SetRecDesc('061020');">Sliced Mushrooms</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061014&PortionSize=1" onmouseover="SetRecDesc('061014');">Spinach</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category5">Euro Kitchen</li>
								<li class="level5"><a class="itemlink" href="recipedetail.asp?RecipeNumber=089001&PortionSize=2" onmouseover="SetRecDesc('089001');">Bacon</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161029&PortionSize=3" onmouseover="SetRecDesc('161029');">Breakfast Potato</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061074&PortionSize=2" onmouseover="SetRecDesc('061074');">Fried Egg Whites</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061001&PortionSize=1" onmouseover="SetRecDesc('061001');">Fried Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061034&PortionSize=2" onmouseover="SetRecDesc('061034');">Scrambled Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlink" href="recipedetail.asp?RecipeNumber=115009&PortionSize=2" onmouseover="SetRecDesc('115009');">Turkey Links (Breakfast Sausage)</a></li>
							</ul>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category5">Euro Kitchen</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=089011&PortionSize=2" onmouseover="SetRecDesc('089011');">Bacon</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161013&PortionSize=2" onmouseover="SetRecDesc('161013');">Country Hash Browns</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061001&PortionSize=1" onmouseover="SetRecDesc('061001');">Fried Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=089020&PortionSize=2" onmouseover="SetRecDesc('089020');">Grilled Hot Links</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061034&PortionSize=2" onmouseover="SetRecDesc('061034');">Scrambled Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category5">Euro Kitchen</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=089011&PortionSize=2" onmouseover="SetRecDesc('089011');">Bacon</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161013&PortionSize=2" onmouseover="SetRecDesc('161013');">Country Hash Browns</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061001&PortionSize=1" onmouseover="SetRecDesc('061001');">Fried Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=089020&PortionSize=2" onmouseover="SetRecDesc('089020');">Grilled Hot Links</a></li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=061034&PortionSize=2" onmouseover="SetRecDesc('061034');">Scrambled Eggs</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=160023&PortionSize=1" onmouseover="SetRecDesc('160023');">Flour Tortilla</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=977188&PortionSize=1" onmouseover="SetRecDesc('977188');">Roasted Tomato Salsa</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
								<span class="category0">&nbsp;</span>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category5">Pizza Oven</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=217033&PortionSize=1/2" onmouseover="SetRecDesc('217033');">Belgian Waffle</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">w/&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=189029&PortionSize=1" onmouseover="SetRecDesc('189029');">Chocolate Syrup</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=204010&PortionSize=1" onmouseover="SetRecDesc('204010');">Peach Toppping</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=204001&PortionSize=1" onmouseover="SetRecDesc('204001');">Strawberry Topping</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category5">Pizza Oven</li>
								<li class="level5"><a class="itemlink" href="recipedetail.asp?RecipeNumber=082130&PortionSize=1/2" onmouseover="SetRecDesc('082130');">Strawberry Cream Cheese Flatbread</a></li>
								<li class="level3">w/&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=189130&PortionSize=1" onmouseover="SetRecDesc('189130');">Bananas Foster</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=205002&PortionSize=1" onmouseover="SetRecDesc('205002');">Blueberry Topping</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=189029&PortionSize=1" onmouseover="SetRecDesc('189029');">Chocolate Syrup</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level3">&amp;&nbsp;&nbsp;<a class="itemlinkt" href="recipedetail.asp?RecipeNumber=204001&PortionSize=1" onmouseover="SetRecDesc('204001');">Strawberry Topping</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category5">Grill</li>
								<li class="level5"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=217033&PortionSize=1/2" onmouseover="SetRecDesc('217033');">Belgian Waffle</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161012&PortionSize=3" onmouseover="SetRecDesc('161012');">Tator Tots</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=217041&PortionSize=1" onmouseover="SetRecDesc('217041');">French Toast</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category4">Grill</li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=217001&PortionSize=2" onmouseover="SetRecDesc('217001');">Pancakes</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161012&PortionSize=3" onmouseover="SetRecDesc('161012');">Tator Tots</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category4">Grill</li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=217041&PortionSize=1" onmouseover="SetRecDesc('217041');">French Toast</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level4"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=161003&PortionSize=1" onmouseover="SetRecDesc('161003');">Hash Brown Patty</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category2">Hot Food Bar</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979291&PortionSize=1" onmouseover="SetRecDesc('979291');">Biscuit</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=157149&PortionSize=1" onmouseover="SetRecDesc('157149');">Country Gravy</a></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=400035&PortionSize=3" onmouseover="SetRecDesc('400035');">Sticky Rice</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell">
								<span class="category0">&nbsp;</span>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category2">Hot Food Bar</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979291&PortionSize=1" onmouseover="SetRecDesc('979291');">Biscuit</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=167132&PortionSize=3" onmouseover="SetRecDesc('167132');">Broken Rice</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=157149&PortionSize=1" onmouseover="SetRecDesc('157149');">Country Gravy</a></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
								<span class="category0">&nbsp;</span>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category2">Fruit</li>
								<li class="level2"><a class="itemlink" href="recipedetail.asp?RecipeNumber=977406&PortionSize=1" onmouseover="SetRecDesc('977406');">Cantaloupe</a></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=970242&PortionSize=1" onmouseover="SetRecDesc('970242');">Grapefruit</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlink" href="recipedetail.asp?RecipeNumber=977407&PortionSize=1" onmouseover="SetRecDesc('977407');">Honeydew Melon</a></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=201011&PortionSize=1" onmouseover="SetRecDesc('201011');">Pineapple</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=201031&PortionSize=1" onmouseover="SetRecDesc('201031');">Watermelon</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
								<span class="category0">&nbsp;</span>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
							<ul>
								<li class="category2">From the Bakery</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979340&PortionSize=1" onmouseover="SetRecDesc('979340');">Banana Nut Bread</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979416&PortionSize=1" onmouseover="SetRecDesc('979416');">Banana Nut Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979412&PortionSize=1" onmouseover="SetRecDesc('979412');">Blueberry Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979425&PortionSize=1" onmouseover="SetRecDesc('979425');">Chocolate Bar</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979418&PortionSize=1" onmouseover="SetRecDesc('979418');">Chocolate Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979423&PortionSize=1" onmouseover="SetRecDesc('979423');">Cinnamon Twist Donuts</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979398&PortionSize=1" onmouseover="SetRecDesc('979398');">Mini Almond Bear Claw</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979402&PortionSize=1" onmouseover="SetRecDesc('979402');">Pumpkin Cheese Coffee Cake</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell">
							<ul>
								<li class="category2">Sweets</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979340&PortionSize=1" onmouseover="SetRecDesc('979340');">Banana Nut Bread</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979416&PortionSize=1" onmouseover="SetRecDesc('979416');">Banana Nut Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979412&PortionSize=1" onmouseover="SetRecDesc('979412');">Blueberry Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979425&PortionSize=1" onmouseover="SetRecDesc('979425');">Chocolate Bar</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979418&PortionSize=1" onmouseover="SetRecDesc('979418');">Chocolate Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979423&PortionSize=1" onmouseover="SetRecDesc('979423');">Cinnamon Twist Donuts</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979398&PortionSize=1" onmouseover="SetRecDesc('979398');">Mini Almond Bear Claw</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979402&PortionSize=1" onmouseover="SetRecDesc('979402');">Pumpkin Cheese Coffee Cake</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category2">Sweets</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979340&PortionSize=1" onmouseover="SetRecDesc('979340');">Banana Nut Bread</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979416&PortionSize=1" onmouseover="SetRecDesc('979416');">Banana Nut Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979412&PortionSize=1" onmouseover="SetRecDesc('979412');">Blueberry Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979425&PortionSize=1" onmouseover="SetRecDesc('979425');">Chocolate Bar</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979418&PortionSize=1" onmouseover="SetRecDesc('979418');">Chocolate Muffin</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979423&PortionSize=1" onmouseover="SetRecDesc('979423');">Cinnamon Twist Donuts</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979398&PortionSize=1" onmouseover="SetRecDesc('979398');">Mini Almond Bear Claw</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=979402&PortionSize=1" onmouseover="SetRecDesc('979402');">Pumpkin Cheese Coffee Cake</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
							</ul>
						</td>
					</tr>
					<tr>
						<td class="menugridcell">
								<span class="category0">&nbsp;</span>
						</td>
						<td class="menugridcell">
								<span class="category0">&nbsp;</span>
						</td>
						<td class="menugridcell_last">
							<ul>
								<li class="category2">Sandwich Bar</li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=042081&PortionSize=1" onmouseover="SetRecDesc('042081');">Arugula Salad</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=132033&PortionSize=1" onmouseover="SetRecDesc('132033');">Low Fat Cream Cheese</a>&nbsp;<img class="webcode" src="images/webcodes/V.png" alt="Vegetarian Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=047155&PortionSize=1" onmouseover="SetRecDesc('047155');">Red Onion</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
								<li class="level2"><a class="itemlinkt" href="recipedetail.asp?RecipeNumber=047160&PortionSize=1" onmouseover="SetRecDesc('047160');">Tomatoes</a>&nbsp;<img class="webcode" src="images/webcodes/VG.png" alt="Vegan Menu Option"></li>
							</ul>
						</td>
					</tr>
			</tbody></table>
			</div>
<br />

		
				<p id="back-top"><a href="#top"><span></span>Back to Top</a></p>

				<div class="push"></div>
			
			</div> <!-- END #MENUWRAPPER -->
		
		</div> <!-- END #GLOBALWRAPPER -->
		
		
			<div id="footer">
				
				<div class="legend_info">
					<h3>Legend</h3>
					<p>						<img class="webcode" src="images/webcodes/V.png" />&nbsp;&nbsp;Vegetarian Menu Option<br />
						<img class="webcode" src="images/webcodes/VG.png" />&nbsp;&nbsp;Vegan Menu Option
					</p>
				</div>

				
				
				<div class="copyright_disclaimer">
					<p>
						Menus are subject to change based on operational needs.
					
						<!-- The following is required by Aurora Information Systems, DO NOT MODIFY OR REMOVE -->
						<br />
						Powered by FoodPro<sup>&#174;</sup>&nbsp;
						<!-- End of Aurora Information Systems Required Text -->
					</p>
				</div>
			</div>
	</body>
</html>
"""

soup = BeautifulSoup(htmldoc, 'html.parser')

tds = soup.findAll('td', { "class": lambda x: 
	x and (x == "menugridcell" or x == "menugridcell_last") })

if len(tds) % 3 == 0:
	count = 0
	m0 = []
	m1 = []
	m2 = []

	for td in tds:
		if count == 0:
			m0.append(td)
		elif count == 1:
			m1.append(td)
		elif count == 2:
			m2.append(td)

		count = count + 1
		if count > 2:
			count = 0

	menu = []

	for m in m0:
		text = m.text
		if text.strip() != "":
			lines = []
			for line in text.split('\n'):
				if line.strip() != "":
					lines.append(line)
					print(line)
			print()
			menu.append(lines)




