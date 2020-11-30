const inputs = document.querySelectorAll('.form input, textarea');
Array.from(inputs).forEach(function (txt) {
  txt.addEventListener('keyup', function (event) {
    label = this.previousElementSibling;
    if (this.value === '') {
      label.classList.remove('active');
      label.classList.remove('highlight');
    } else {
      label.classList.add('active');
      label.classList.add('highlight');
    }
  });
  txt.addEventListener('blur', function (event) {
    label = this.previousElementSibling;
    if (this.value === '') {
      label.classList.remove('active');
    }
    label.classList.remove('highlight')
  });
  txt.addEventListener('focus', function (event) {
    label = this.previousElementSibling;
    if (this.value === '') {
      label.classList.remove('highlight');
    } else {
      label.classList.add('highlight');
    }
  });
});

const links = document.querySelectorAll('.tab a');
Array.from(links).forEach(function (a) {
  a.addEventListener('click', function (event) {
    event.preventDefault();
    toMakeInactive = this.parentNode.parentNode.children;
    Array.from(toMakeInactive).forEach(function (elt) {
      elt.classList.remove('active');
    });
    this.parentNode.classList.add('active');
    target = this.getAttribute("href");
    toHide = document.querySelectorAll('.tab-content > div')
    Array.from(toHide).forEach(function (elt) {
      if (!(elt.matches(target))) {
        elt.style.display = 'none';
      }
    });
    document.querySelector(target).style.display = 'block';
  });
});
