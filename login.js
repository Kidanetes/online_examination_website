const signUp = document.querySelector('.signup');

signUp.addEventListener('click', function() {
  const form = document.querySelector('.form')
  const children = form.children;
  for (let i = 0; i < children.length; i++) {
  	children[i].remove();
  }
  const list = [];
  for (let i = 0; i < 5; i++) {
  	let tmp = document.createElement('input')
  	form.appendChild(tmp)
  	tmp.classList.add('input');
  	tmp.setAttribute('type', 'text');
  	list.push(tmp);
  }
  const placeHolders = ['First name', 'Last name', 'email', 'password', 'refill password'];
  for (let i = 0; i < 5; i++) {
  	list[i].setAttribute('placeholder', placeHolders[i]);
  }
});
