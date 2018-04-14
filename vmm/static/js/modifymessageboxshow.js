/**
 * Created by FuJinsong on 2017/8/22.
 */


//-------------------------------------- 注册框验证是否为空------------------------------------------------------------
$('.tj').click(function () {



            $(".regform").ajaxSubmit({
                type: "POST",
                dataType: "json", //json格式，后台返回的数据为json格式的。
                success: function (result) {
                    console.log(result);
                    if(result.reg == "输入错误"){
                        new $.zui.Messager('输入错误字段。', {
                            type: 'warning',
                            icon: 'warning-sign',
                            time: '3000',
                            placement: 'center' // 定义显示位置
                        }).show();
                    }


                }
            });



});
