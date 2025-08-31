const header = document.querySelector("header");
window.addEventListener("scroll", function () {
    header.classList.toggle("sticky", window.scrollY > 0);
});

let menu = document.querySelector("#menu-icon");
let navbar = document.querySelector(".navbar");

menu.onclick = () => {
    menu.classList.toggle("bx-x");
    navbar.classList.toggle("navx"); // Certifique-se de que o CSS usa `.navbar.open`
    console.log('click nav run')
};

function comprar(button) {
    // Pegar os dados do produto
    const productCard = button.closest('.product-card');
    const productName = productCard.querySelector('.product-title').textContent;
    const productPrice = productCard.querySelector('.product-price').textContent;

    // Armazenar os dados no localStorage
    localStorage.setItem('productName', productName);
    localStorage.setItem('productPrice', productPrice);

    // Redirecionar para a página de pagamento
    window.location.href = "pagina-de-pagamento.html";
}

  // Função para adicionar ao carrinho
  function adicionarCarrinho(button) {
    // Localiza os dados do produto
    const productCard = button.closest('.product-card');
    const productName = productCard.querySelector('.product-title').textContent;
    const productPrice = productCard.querySelector('.product-price').textContent;

    // Recupera o carrinho do localStorage (se já existir)
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

    // Adiciona o produto ao carrinho
    carrinho.push({ name: productName, price: productPrice });

    // Salva o carrinho atualizado no localStorage
    localStorage.setItem('carrinho', JSON.stringify(carrinho));

    alert(`${productName} foi adicionado ao carrinho!`);
}



