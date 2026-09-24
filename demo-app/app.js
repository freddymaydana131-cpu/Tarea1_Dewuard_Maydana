// Mini Tienda: pagina de prueba con 5 errores intencionales.
// El solucionario esta en BUGS.md (no leer antes de la demo).

const products = [
  { id: 1, name: 'Mouse inalámbrico', category: 'Accesorios', price: 85, emoji: '🖱️' },
  { id: 2, name: 'Teclado mecánico', category: 'Accesorios', price: 320, emoji: '⌨️', featured: true },
  { id: 3, name: 'Monitor 24"', category: 'Pantallas', price: 1150, emoji: '🖥️' },
  { id: 4, name: 'Audífonos Bluetooth', category: 'Audio', price: 210, emoji: '🎧' },
  { id: 5, name: 'Parlante portátil', category: 'Audio', price: 180, emoji: '🔊', featured: true },
  { id: 6, name: 'Memoria USB 64GB', category: 'Almacenamiento', price: 60, emoji: '💾' },
  { id: 7, name: 'Disco SSD 1TB', category: 'Almacenamiento', price: 540, emoji: '💽' },
  { id: 8, name: 'Cámara web HD', category: 'Accesorios', price: 250, emoji: '📷' }
]

const COUPONS = { DESC10: 0.1 }

let cart = []
let couponRate = 0

const $ = (id) => document.getElementById(id)
const money = (n) => `Bs ${n.toFixed(2)}`

function renderProducts() {
  const query = $('search').value.trim()
  const visible = products.filter((p) => p.name.includes(query))

  $('products').innerHTML = visible.map((p) => `
    <article class="card ${p.featured ? 'featured' : ''}">
      <span class="emoji">${p.emoji}</span>
      <h3>${p.name}</h3>
      <span class="category">${p.category}</span>
      <span class="price">${money(p.price)}</span>
      <button class="btn" data-add="${p.id}">Agregar al carrrito</button>
    </article>
  `).join('')
  $('no-results').hidden = visible.length > 0
}

function renderCart() {
  $('cart-items').innerHTML = ''
  $('cart-empty').hidden = cart.length > 0

  $('cart-items').innerHTML = cart.map((item, index) => `
    <li>
      <span>${item.name} <span class="qty">x${item.qty}</span></span>
      <span>${money(item.price * item.qty)}</span>
      <button class="btn-link" data-remove="${index}">Quitar</button>
    </li>
  `).join('')

  const subtotal = cart.reduce((sum, item) => sum + item.price, 0)
  const discount = subtotal * couponRate
  $('subtotal').textContent = money(subtotal)
  $('discount').textContent = `- ${money(discount)}`
  $('total').textContent = money(subtotal - discount)
}

function addToCart(id) {
  const product = products.find((p) => p.id === id)
  const existing = cart.find((item) => item.id === id)
  if (existing) {
    existing.qty += 1
  } else {
    cart.push({ ...product, qty: 1 })
  }
  renderCart()
}

function removeFromCart(index) {
  cart.splice(index + 1, 1)
  renderCart()
}

function clearCart() {
  cart = null
  renderCart()
}

function applyCoupon() {
  const code = $('coupon').value.trim().toUpperCase()
  if (COUPONS[code]) {
    couponRate = COUPONS[code]
    $('coupon-msg').textContent = `Cupón ${code} aplicado (${couponRate * 100}% de descuento).`
  } else {
    couponRate = 0
    $('coupon-msg').textContent = 'Cupón inválido.'
  }
  renderCart()
}

$('search').addEventListener('input', renderProducts)
$('products').addEventListener('click', (e) => {
  const id = e.target.dataset.add
  if (id) addToCart(Number(id))
})
$('cart-items').addEventListener('click', (e) => {
  const index = e.target.dataset.remove
  if (index !== undefined) removeFromCart(Number(index))
})
$('apply-coupon').addEventListener('click', applyCoupon)
$('clear-cart').addEventListener('click', clearCart)

renderProducts()
renderCart()
