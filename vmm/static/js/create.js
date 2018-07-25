// $(document).ready(function(){
//
//        $('.create').click(function () {
//             $.ajax({
//                 url: "createvm",
//                 type : "POST",
//                 data: $('#form1').serialize(),
//                 success: function (data) {
//                         new $.zui.Messager(data["status"], {
//                         type: 'warning',
//                         icon: 'warning-sign',
//                         time: '3000',
//                         placement: 'center' // 定义显示位置
//                     }).show();
//
//                         if(data["status"]=="成功"){
//                         setTimeout("window.location.href='/login'",3000);
//                         }
//                 }
//             });
//         });
//     });
