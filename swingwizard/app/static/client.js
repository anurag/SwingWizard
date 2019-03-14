function showFilePicked(input) {
    document.getElementById('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('image-picked').src = e.target.result;
        document.getElementById('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}
