/**
 * Created by FuJinsong on 2017/8/25.
 */
$(document).ready(function(){

/*电源管理函数*/
    function power(optype,uuid) {
        var info = '';
        switch (optype){
            case 0:
                info = "禁用";
                break;
            case 1:
                info = "启用";
                break;
        }
        bootbox.confirm("确定要" + info + "吗？", function (result) {
            if(result){
                $.ajax({
                    type: "GET",
                    url: "/backend/stopvm?uuid=" + uuid + "&type=" + optype,
                    success: function (msg) {

                    }
                });
            }

        })
    }

    $(".findpasword button").on("click",function(){
        var email = $(this).find('input[name="f_email_tip"]').attr("value");
        var id = $(this).find('input[name="f_id_tip"]').attr("value");
         alert(id);
        //  if ($(this).attr('class').indexOf('star') != -1) {
        //     optype = 1;
        //     power(optype, uuid);
        // }
    });
});