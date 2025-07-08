/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  var sidenav = document.getElementById("mySidenav");
  if (sidenav.style.width === "250px") {
    closeNav();
  } else {
    sidenav.style.width = "250px";
    document.getElementById("content-wrapper").style.marginLeft = "250px";
  }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("content-wrapper").style.marginLeft = "0";
}
