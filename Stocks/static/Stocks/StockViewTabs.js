
function openTab(button_object_id, tab_content_id){
  //Variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tab_content_id).style.display = "block";
  document.getElementById(button_object_id).className += " active";

}

//========================================================================================================


function update_Price(){

  const symbol2 = document.getElementById('title').innerHTML;
  const APIKey2 = "bs5qbcfrh5rajuf8m9ig";
  const url2 = `https://finnhub.io/api/v1/quote?symbol=${symbol2}&token=${APIKey2}`;

  fetch(url2)

      .then(function (responsex){
        // Convert response object to json() format
        return responsex.json();
      })
      .then(function(data){
        console.log(data["c"]);

        document.getElementById("CurrentQuote").innerHTML = data["c"];
        document.getElementById("Open").innerHTML = `Open: ${data["o"]}`;
        document.getElementById("High").innerHTML = `High: ${data["h"]}`;
        document.getElementById("Low").innerHTML = `Low: ${data["l"]}`;

        let current = document.getElementById("CurrentQuote").style.color;
        let open = document.getElementById("Open").style.color;
        let high = document.getElementById("High").style.color;
        let low = document.getElementById("Low").style.color;

        document.getElementById("CurrentQuote").style.color = "#00cc00";
        document.getElementById("Open").style.color = "#00cc00";
        document.getElementById("High").style.color = "#00cc00";
        document.getElementById("Low").style.color = "#00cc00";

        setTimeout(function() {

          document.getElementById("CurrentQuote").style.color = current;
          document.getElementById("Open").style.color = open;
          document.getElementById("High").style.color = high;
          document.getElementById("Low").style.color = low;

        }, 1000);
      })

}
