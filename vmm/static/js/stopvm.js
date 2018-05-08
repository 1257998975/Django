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

    $(".stopvm button").on("click",function(){
        var uuid = $(this).parents('tr').find('input[name="checkbox"]').attr("value");
        var optype = '';
        // alert(uuid);
        if ($(this).attr('class').indexOf('stop') != -1) {
            optype = 0;
            power(optype, uuid);
        } else if ($(this).attr('class').indexOf('star') != -1) {
            optype = 1;
            power(optype, uuid);
        }
    });
});