/**
 * Created by rsegev on 02/07/2017.
 */

setTimeout(function(){
  $('.alert-success').hide()
}, 60000);

$(document).ready(function() {
    if (location.hash) {
        $("a[href='" + location.hash + "']").tab("show");
    }
    $(document.body).on("click", "a[data-toggle]", function(event) {
        location.hash = this.getAttribute("href");
    });

    $('.approve').click(function () {
        var request_id = $(this).parents('div').siblings("span:first").text();
        handle_request("A", request_id);
    });
    $('.reject').click(function () {
        var request_id = $(this).parents('div').siblings("span:first").text();
        handle_request("R", request_id);
    });
});
$(window).on("popstate", function() {
    var anchor = location.hash || $("a[data-toggle='tab']").first().attr("href");
    $("a[href='" + anchor + "']").tab("show");
});

function handle_request(new_status, request_id) {
    $.ajax({
      url: handle_emp_request_url,
      type: "post", //send it through get method
      data: {
        emp_request_id: request_id,
        new_status: new_status
      },
      headers: {
          'X-CSRFToken': csrf_token
      },
      success: function(response){
                window.location.reload();
            }
    });
}
