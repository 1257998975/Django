$(document).ready(function(){
       $('.tj').click(function () {
            $.ajax({
                url: "modify",
                type : "POST",
                data: $('#form1').serialize(),
                success: function (data) {
                    // alert(data["status"]);

                        new $.zui.Messager(data["status"], {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();

                        if(data["status"]=="修改成功"){
                        setTimeout("window.location.href='/login'",3000);
                        }
                }
            });
        });
    });



