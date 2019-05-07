$(document).ready(function() {
  $(document).on("click", ".updateMissons", function() {
    $.ajax({
      type: "GET",
      url: new_mission_url // URL to your view that serves new info
    });
  });
  $(document).on("click", ".addMission", function() {
    var mission_id = $(this).attr("member_id");
    console.log(mission_id);
    $.ajax({
      type: "GET",
      url: add_mission_url, // URL to your view that serves new info
      data: { mission_id: mission_id }
    }).done(function(response) {
      $("#_appendHere").html(response);
    });
  });

  $(document).on("click", ".abort", function() {
    var mission_queue_id = $(this).attr("member_id");
    console.log(mission_queue_id);
    $.ajax({
      type: "GET",
      url: cancel_mission_url, // URL to your view that serves new info
      data: { mission_queue_id: mission_queue_id }
    }).done(function(response) {
      $("#_appendHere").html(response);
    });
  });
});
