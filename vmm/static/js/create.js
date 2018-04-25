$(document).ready(function(){
       $('.create').on("click",function(){
            $.ajax({
                url: "createvm",
                type : "POST",
                data: $('#form1').serialize(),
                success: function (data) {
                       alert(data["status"]);

                        new $.zui.Messager("dddd", {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();

                }
            });
        });
    });



