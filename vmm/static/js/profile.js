/**
 * Created by FuJinsong on 2017/8/25.
 */
$(document).ready(function(){

/*电源管理函数*/
    function power(optype,uid) {
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
                    url: "/backend/pf?uid=" + uid + "&type=" + optype,
                    success: function (msg) {

                    }
                });
            }

        })
    }

    $(".opt button").on("click",function(){
        var uid = $(this).parents('tr').find('input[name="checkbox"]').attr("value");
        var optype = '';
        // alert(uid);
        if ($(this).attr('class').indexOf('btn_stop') != -1) {
            optype = 0;
            power(optype, uid);
        } else if ($(this).attr('class').indexOf('btn_star') != -1) {
            optype = 1;
            power(optype, uid);
        }
    });
});