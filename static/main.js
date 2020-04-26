$(document).ready(function(){

  // Start
  $.ajax({
    url : 'start',
    type : 'POST',
    success : function(response) {

    }
  })
  // Generate Sectors
  for (i = 0; i < 25; i++) {
    $("#panel").append('<i class="sector" data-coord-number="' + i + '"></i>')
  }
  
  // Buttons
  $("#f").on("click", function() {
    $.ajax({
      url : "forward",
      type: "POST"
    })
  });
  
  $("#b").on("click", function() {
    $.ajax({
      url : "backward",
      type: "POST"
    })
  });
  
  $("#l").on("click", function() {
    $.ajax({
      url : "left",
      type: "POST"
    })
  });
  
  $("#r").on("click", function() {
    $.ajax({
      url : "right",
      type: "POST"
    })
  });
  
  $("#temp").on("click", function() {
    $.ajax({
      url : "get_data",
      type: "POST",
      dataType: "json",
      success : function(response) {
        $("#clearRC").text(response['temp'] + " C | " + response['humidity'] + " Hum")
      }
    })
  })
  
  function runBlueLED() {
    $.ajax({
      url : "b_led",
      type: "POST"
    })
  };
  
  setInterval(function() {
    runBlueLED()
  }, 1000);
  

  let count = 0
  function getUpdate() {
    $.ajax({
      url : 'update',
      type : 'POST',
      success : function(response) {
        count += 1
        // if (response.data == "Done!") {
        //   return
        // }
        for(i = 0; i < response.data.length; i++) {
            if (response.data[i].type == 1) {
              $(".sector").removeClass("current")
              $(".sector").eq(i).addClass("current")
            } else if (response.data[i].type == 2) {
              $(".sector").eq(i).addClass("hot")
            } else if (response.data[i].type == 3) {
              $(".sector").eq(i).addClass("object")
            } else if (response.data[i].type == 4) {
              $(".sector").eq(i).addClass("target")
            } else if (response.data[i].type == 5) {
              $(".sector").eq(i).addClass("visited")
            } else {
              $(".sector").eq(i).removeClass("hot")
              $(".sector").eq(i).removeClass("object")
              $(".sector").eq(i).removeClass("target")
            }
        }
        setTimeout(() => {
          getUpdate()
        },3000)
      }
    })
  }
  getUpdate()
})
