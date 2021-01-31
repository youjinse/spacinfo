function saveData(category){
    let markupStr = $("#summernote").summernote('code');
    console.log(markupStr);

    // 팝업창을 위한 설정
    let Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000
    });

    $.ajax({
        url: '/post/' + category,
        method: 'POST',
        dataType: 'json',
        data: {
            'subject': $("#subject").val(),
            'category_code': category,
            'contents': markupStr
        }
    }).done(function (response) {
        if (response['result'] == 'Fail') {
            Toast.fire({
                icon: 'error',
                title: '글쓰기가 실패했습니다.'
            })
        } else {
            Toast.fire({
                icon: 'success',
                title: '글쓰기가 완료되었습니다.'
            })
            window.location.replace(document.referrer);
        }
    });
}
