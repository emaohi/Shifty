/**
 * Created by rsegev on 01/07/2017.
 */
$(document).ready(function() {

    var employeeIndex = 0;

    // Add button click handler
    $('.addButton').click(function() {
        employeeIndex++;
        var $template = $('#employeeTemplate'),
            $clone    = $template
                            .clone()
                            .removeClass('hide')
                            .removeAttr('id')
                            .attr('data-book-index', employeeIndex)
                            .insertBefore($(".submit-group"));

        // Update the name attributes
        $clone
            .find('[class="counter"]').text(employeeIndex+1).end()
            .find('[name="firstName"]').attr('name', 'employee_' + employeeIndex + '_firstName').end()
            .find('[name="lastName"]').attr('name', 'employee_' + employeeIndex + '_lastName').end()
            .find('[name="email"]').attr('name', 'employee_' + employeeIndex + '_email').end()
            .find('[name="role"]').attr('name', 'employee_' + employeeIndex + '_role').end()
            .find('[name="date"]').attr('name', 'employee_' + employeeIndex + '_dateJoined').end();
    });

    // Remove button click handler
    $('.container').on('click', '.removeButton', function() {
        var $row  = $(this).parents('.form-group');

        // Remove element containing the fields
        $row.remove();

        employeeIndex --;
    });

    $('.btn-submit').on('click', function() {
        $('.progress').show();
        setTimeout(doProgress, 200);
    });
    function doProgress() {
        var i = 0;
        var counterBack = setInterval(function(){
          i++;
          if (i <= 100){
            $('.progress-bar').css('width', i+'%');
          } else {
            clearInterval(counterBack);
          }
          var is_plural_mail;
          if (employeeIndex > 0){
              is_plural_mail = "messages";
          }else{
              is_plural_mail = "message";
          }
          $("#percent").text((employeeIndex+1) + " " + is_plural_mail);

        }, (employeeIndex+1) * 30);

    }
});