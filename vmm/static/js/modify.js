/**
 * Created by FuJinsong on 2017/8/22.
 */
//
// $('.tj').click(function () {
//             $.ajax({
//         url:"vmm/user.modify", //提交到那里
//         type:"POST", //提交类型
//         success:function(data){ //success不会直接运行，当服务器有数据传输过来才会触发执行。
// 　　　　　　　　　　　　　　　　　　　　//匿名函数必须要有一个参数，用来接受数据，data1用来接受是服务器端返回字符串数据
//         alter(data);
//     }
//     })
//
//
//
// });



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



