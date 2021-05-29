function readURL(input, element_id) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $(element_id).attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
