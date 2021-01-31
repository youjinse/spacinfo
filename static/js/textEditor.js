function saveData(category){
    let markupStr = $("#summernote").summernote('code');

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

function sendFile(file, el) {
    let form_data = new FormData();
    form_data.append('file', file);
    $.ajax({
        data: form_data,
        type: "POST",
        url: '/upload/image',
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        success: function (img_name) {
            $(el).summernote('editor.insertImage', img_name);
        }
    });
}

$(document).ready(function () {
    $('#summernote').summernote({
        placeholder: '작성하고 싶은 글을 작성하세요',
        height: 410,
        callbacks: {
            onImageUpload: function (files) {
                // upload image to server and create imgNode...
                for (let i = files.length - 1; i >= 0; i--) {
                    console.log("1234" + files[i]);
                    sendFile(files[i], this);
                }
                $summernote.summernote('insertNode', imgNode);
            }
        }
    });
});