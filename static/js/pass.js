const eye = document.querySelector('.as-eye');
const eye_slash = document.querySelector('.as-eye-slash');
const inp = document.getElementById('password');

eye.addEventListener("click", function() {
    eye_slash.classList.remove('active')
    inp.type = 'text';
    eye.classList.add('active')
    console.log('work')
});


eye_slash.addEventListener("click", function() {
    eye_slash.classList.add('active')
    eye.classList.remove('active')
    inp.type = 'password';
    console.log('no')
});