
(function ($) {
    "use strict";

    $('#recommendation-form').parsley();

    $(".selection-2").select2({
        minimumResultsForSearch: 20,
        dropdownParent: $('#dropDownSelect1')
    });

    var today = new Date().toISOString().split('T')[0];
    document.getElementsByName("child-birthdate")[0].setAttribute('max', today);
    document.getElementsByName("child-enrolment")[0].setAttribute('min', today);
    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input3').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
            

    /*==================================================================
    [ Chose Radio ]*/
    $("#radio1").on('change', function(){
        if ($(this).is(":checked")) {
            $('.input3-select').slideUp(300);
        }
    });

    $("#radio2").on('change', function(){
        if ($(this).is(":checked")) {
            $('.input3-select').slideDown(300);
        }
    });
        
  
    
    /*==================================================================
    [ Validate ]*/
    var name = $('.validate-input input[name="name"]');
    var email = $('.validate-input input[name="email"]');
    var message = $('.validate-input textarea[name="message"]');


    $('.validate-form .input3').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    function getStudyLevel(){
        let study_level_str = "Infant";
        if(($("#child-birthdate").val() != "")&($("#child-enrolment").val() != "")){
            let birthdate = new Date($("#child-birthdate").val());
            let enrolment_date = new Date($("#child-enrolment").val());
            let diff  = new Date(enrolment_date - birthdate);
            let years_diff  = diff/1000/60/60/24/365;

            if((years_diff > 1) && (years_diff < 2)){
                let months_diff = years_diff * 12;
                if(months_diff <= 18){
                    study_level_str = "Infant";
                } else {
                    study_level_str = "Playgroup";
                }
            } else {
                years_diff = Math.floor(years_diff);
                switch (years_diff) {
                    case 0 :
                        study_level_str = "Infant";
                        break;
                    case 1 :
                        study_level_str = "Infant";
                        break;
                    case 2 :
                        study_level_str = "Playgroup";
                        break;
                    case 3 :
                        study_level_str = "Pre-Nursery";
                        break;
                    case 4 :
                        study_level_str = "Nursery";
                        break;
                    case 5 :
                        study_level_str = "Kindergarten 1";
                        break;
                    case 6 :
                        study_level_str = "Kindergarten 2";
                        break;
                    default :
                        study_level_str = "";
                }
            }
        }
        return study_level_str;
    }

    $('#child-enrolment').change(function (e) {
            let study_level_str = getStudyLevel();
            $('#select2-study-level-container').html(study_level_str);
            $('#select2-study-level-container').attr("title", study_level_str);

            $("#div-study-level").show();

            $(this).parsley().validate();
    });

    $('#child-birthdate').change(function (e) {
            let study_level_str = getStudyLevel();
            $('#select2-study-level-container').html(study_level_str);
            $("#div-study-level").show();

            $(this).parsley().validate();

    });

    // Custom validator for date range
    window.Parsley.addValidator('daterangevalidation', {
      validateString: function(value) {
        var allowed = true;
        if($("#child-birthdate").val() !== "" && $('#child-enrolment').val() !== ''){
          return Date.parse($('#child-birthdate').val()) <= Date.parse($('#child-enrolment').val());
        }
        return allowed;
      },
      messages: {
        en: "Enrolment date must be after child's birth date.",
      }
    });

})(jQuery);