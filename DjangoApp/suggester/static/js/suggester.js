var csrftoken = Cookies.get('csrftoken');

// This is to save the restaurantID, to be used during the saving of the model
var restaurantID;

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

// On click of the element with id=btn-suggest, perform the ajax call
$("#btn-suggest").click(function() {
  var cuisineType = [];
  var hasVisited;

  $.each($("#cuisine-type option:selected"), function() {
    cuisineType.push($(this).val());
  });

  $.each($("#has-visited option:selected"), function() {
    hasVisited = $(this).val();
  });

  console.log("You have selected the restaurant types - " + cuisineType);
  console.log("You have selected the been there option as " + hasVisited);

  querySuggestion(cuisineType, hasVisited);
});

// Function to save the has_visited variable to do the database
$("#checkbox-visited").click(function() {
  // Get the current state of the checkbox
  var currentState = $("#checkbox-visited").prop("checked");

  // Post the data to the backend
  saveModel(currentState);
});

function querySuggestion(cuisineType, hasVisited) {
  $.ajax({
    url: '/ajax/query_suggestion/',
    dataType: 'json',
    data: {
      cuisineType: cuisineType,
      hasVisited: hasVisited,
    },
    // If ajax call returns successfully, reflect on screen the response of the ajax call
    success: function(data) {

      $("#suggestion-text").text(data.restaurant_name);

      restaurantID = data.restaurant_id;

      // Check if there is a restaurant id. If there is no id, it means that no result is returned
      if (restaurantID) {
        // Check if its visited but checkbox is not displaying
        if ((data.has_visited == true) && $("#checkbox-visited").prop("checked") == false) {
          $("#checkbox-visited").prop("checked", true);
        } else if ((data.has_visited == false) && $("#checkbox-visited").prop("checked") == true) {
          $("#checkbox-visited").prop("checked", false);
        }
      } else {
        console.log("dont hep restaurant ID");
        $('#error-modal').modal('open');
      }
    }
  });
}

function saveModel(currentState) {
  $.post("ajax/save_suggestion/", {
      restaurant_id: restaurantID,
      has_visited: currentState
    },
    function(data) {
      console.log("Data saved successfully");
    });
}

$("#btn-filter").click(function() {
  $(".bottom-drawer-container").show()
  $(".bottom-drawer").toggleClass("bottom-drawer-active");
  $("#page-mask").toggleClass("mask-active");
});

$("#page-mask").click(function() {
  $("#page-mask").toggleClass("mask-active");
  $(".bottom-drawer").toggleClass("bottom-drawer-active");
  $(".bottom-drawer-container").hide()
})
