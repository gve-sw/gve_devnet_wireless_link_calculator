$(function() {
    /*Show corresponding network list as soon as organization is choosen in dropdown + reset child fields*/
    $('#organizations_select').bind('change', function() {
          $('.network-select').attr("hidden", true);
          $('.network-select .networks').val("0");
          $('.network-select .networks').attr("required", true);
          $('.camera-checkboxes').attr("hidden", true);
          var selectid = $( "#organizations_select option:selected" ).val();
          $('#' + selectid).attr("hidden",false);       
      });                            
  });  

  $(function() {
    /*Show corresponding channel list as soon as organization is choosen in dropdown + reset child fields*/
    $('#frequency-select').bind('change', function() {
        if ($('#frequency-select').val() === "5ghz") {
            $('#24ghzin').attr("hidden", true);
            $('#24ghzout').attr("hidden", true);
            $('#unii1').attr("hidden", false);
            $('#unii1').attr("selected", "");
            $('#unii2').attr("hidden", false);
            $('#unii2e').attr("hidden", false);
            $('#unii3').attr("hidden", false);
            $('#58ghz').attr("hidden", false);
            $('#bw-select').attr("hidden", false);
            $('#channel-select').val("unii1");
        } else {
            $('#24ghzin').attr("hidden", false);
            $('#24ghzin').attr("selected", "");
            $('#24ghzout').attr("hidden", false);
            $('#unii1').attr("hidden", true);
            $('#unii2').attr("hidden", true);
            $('#unii2e').attr("hidden", true);
            $('#unii3').attr("hidden", true);
            $('#58ghz').attr("hidden", true);
            $('#bw-select').attr("hidden", true);
            $('#channel-select').val("2.4ghzin");
        }     
      });                            
  });  