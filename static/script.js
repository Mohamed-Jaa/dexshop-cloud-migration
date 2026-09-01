/* --- MOBILE NAVIGATION --- */
function initMobileNav() {
  const toggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".site-nav ul");
  const scrim = document.querySelector(".nav-scrim");
  if (!toggle || !navList) return;

  function closeNav() {
    navList.classList.remove("open");
    if (scrim) scrim.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }

  function toggleNav() {
    const isOpen = navList.classList.toggle("open");
    if (scrim) scrim.classList.toggle("open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }

  toggle.addEventListener("click", toggleNav);
  if (scrim) scrim.addEventListener("click", closeNav);
  navList.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeNav));
}

document.addEventListener("DOMContentLoaded", initMobileNav);

/* --- SHOPPING CART SYSTEM --- */

let cart = JSON.parse(localStorage.getItem("dexshop_cart")) || [];

// سنعلن عن المتغيرات هنا ولكن سنقوم بتهيئتها داخل DOMContentLoaded
let sidebar = null;
let overlay = null;
let floatingCart = null;

// 1. تهيئة النظام بعد تحميل الصفحة
function initCartSystem() {
  console.log("🔍 جاري البحث عن عناصر السلة...");

  sidebar = document.getElementById("sidebar");
  overlay = document.getElementById("overlay");
  floatingCart = document.querySelector(".floating-cart");

  console.log("✅ النتائج:");
  console.log("- Sidebar:", sidebar);
  console.log("- Overlay:", overlay);
  console.log("- Floating cart:", floatingCart);

  // إذا لم يتم العثور على العناصر
  if (!sidebar || !overlay || !floatingCart) {
    console.error("❌ لم يتم العثور على بعض عناصر السلة!");
    console.log("📋 جاري البحث يدوياً...");

    // بحث يدوي
    sidebar = document.querySelector(".checkout-sidebar");
    overlay = document.querySelector(".sidebar-overlay");
    floatingCart = document.querySelector(".floating-cart");

    console.log("🔍 البحث اليدوي:");
    console.log("- Sidebar:", sidebar);
    console.log("- Overlay:", overlay);
    console.log("- Floating cart:", floatingCart);
  }

  // إضافة event listeners للأزرار
  if (floatingCart) {
    floatingCart.addEventListener("click", openSidebar);
    console.log("✅ تم إضافة حدث النقر لزر السلة");
  }

  if (overlay) {
    overlay.addEventListener("click", closeSidebar);
    console.log("✅ تم إضافة حدث النقر للخلفية");
  }

  // تحديث واجهة السلة
  updateCartUI();
  console.log("🚀 نظام السلة جاهز للعمل!");
}

// 2. فتح السلة
window.openSidebar = function () {
  console.log("🎯 فتح السلة...");

  if (!sidebar) {
    console.error("❌ sidebar غير معرف");
    sidebar =
      document.getElementById("sidebar") ||
      document.querySelector(".checkout-sidebar");
  }

  if (!overlay) {
    overlay =
      document.getElementById("overlay") ||
      document.querySelector(".sidebar-overlay");
  }

  if (sidebar && overlay) {
    updateCartUI();

    // إظهار العناصر
    sidebar.style.display = "flex";
    sidebar.style.right = "0";

    overlay.style.display = "block";
    overlay.style.opacity = "1";

    document.body.style.overflow = "hidden";
    console.log("✅ السلة مفتوحة بنجاح!");
  } else {
    console.error("❌ فشل فتح السلة - العناصر غير موجودة");
    alert("عذراً، نظام السلة غير جاهز. حاول تحديث الصفحة.");
  }
};

// 3. إغلاق السلة
window.closeSidebar = function () {
  console.log("🎯 إغلاق السلة...");

  if (sidebar) {
    sidebar.style.right = "-450px";

    if (overlay) {
      overlay.style.opacity = "0";
      setTimeout(() => {
        overlay.style.display = "none";
      }, 300);
    }

    setTimeout(() => {
      sidebar.style.display = "none";
      document.body.style.overflow = "auto";
    }, 300);

    console.log("✅ السلة مغلقة");
  }
};

// === دالة جديدة: تحديث العداد فقط ===
function updateCartCounter() {
  const countBadge = document.getElementById("cart-count");
  if (countBadge) {
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    console.log("🔢 تحديث العداد مباشرة إلى:", totalCount);
    countBadge.textContent = totalCount;

    // تأثير مرئي
    countBadge.style.transform = "scale(1.3)";
    setTimeout(() => {
      countBadge.style.transform = "scale(1)";
    }, 300);
  }
}

// 4. إضافة منتج للسلة - معدلة
window.addToCart = function (button) {
  console.log("🎯 بدء إضافة المنتج...");

  if (!button) {
    console.error("❌ لم يتم تمرير الزر!");
    return false;
  }

  // جلب البيانات من الزر
  const id = button.getAttribute("data-id");
  const name = button.getAttribute("data-name");
  const priceString = button.getAttribute("data-price");
  const image = button.getAttribute("data-image");

  console.log("📦 بيانات المنتج:", { id, name, priceString, image });

  // إذا كانت البيانات مفقودة
  if (!id || !name || !priceString) {
    console.error("❌ بيانات المنتج مفقودة!");
    return false;
  }

  // تنظيف السعر وتحويله لرقم
  const price = parseFloat(priceString.replace(/[^0-9.]/g, ""));

  if (isNaN(price)) {
    console.error("❌ سعر غير صحيح:", priceString);
    return false;
  }

  console.log("💰 السعر بعد التنظيف:", price);

  // التحقق هل المنتج موجود؟
  const existingItem = cart.find((item) => item.id == id);

  if (existingItem) {
    existingItem.quantity += 1;
    console.log(`✅ زيادة كمية "${name}" إلى ${existingItem.quantity}`);
  } else {
    cart.push({
      id: id,
      name: name,
      price: price,
      image: image,
      quantity: 1,
    });
    console.log(`✅ إضافة "${name}" جديد`);
  }

  // === الإصلاح هنا ===
  // 1. حفظ السلة أولاً
  localStorage.setItem("dexshop_cart", JSON.stringify(cart));

  // 2. تحديث العداد مباشرة (فوراً)
  updateCartCounter();

  // 3. تحديث باقي الواجهة
  updateCartUI();

  // رسالة تأكيد صغيرة
  showAddNotification(name);

  console.log("🎉 تمت الإضافة بنجاح!");
  return false; // لمنع السلوك الافتراضي
};

// دالة لعرض إشعار الإضافة
function showAddNotification(productName) {
  console.log("💬 عرض إشعار لإضافة:", productName);

  // إزالة أي إشعار سابق
  const oldNote = document.querySelector(".add-notification");
  if (oldNote) oldNote.remove();

  // إنشاء الإشعار
  const notification = document.createElement("div");
  notification.className = "add-notification";
  notification.innerHTML = `
        <i class="bi bi-check-circle-fill"></i>
        <span>${productName} added to cart!</span>
    `;

  // تنسيقات CSS
  notification.style.cssText = `
        position: fixed;
        bottom: 120px;
        left: 40px;
        background: #22c55e;
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        z-index: 1002;
        font-weight: 600;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 12px;
        animation: slideIn 0.3s ease-out;
    `;

  document.body.appendChild(notification);

  // إخفاء بعد 3 ثوان
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.opacity = "0";
      notification.style.transform = "translateY(20px)";
      setTimeout(() => {
        if (notification.parentNode) notification.remove();
      }, 300);
    }
  }, 3000);

  // إضافة أنيميشن إذا لم يكن موجوداً
  if (!document.querySelector("#notification-style")) {
    const style = document.createElement("style");
    style.id = "notification-style";
    style.textContent = `
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        `;
    document.head.appendChild(style);
  }
}

// 5. تحديث واجهة السلة
function updateCartUI() {
  const container = document.getElementById("cart-items-container");
  const countBadge = document.getElementById("cart-count");
  const totalEl = document.getElementById("finalTotal");

  const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
  if (countBadge) countBadge.textContent = totalCount;

  if (container) {
    container.innerHTML = "";
    let totalPrice = 0;

    if (cart.length === 0) {
      container.innerHTML = `
                <div class="empty-cart">
                    <i class="bi bi-cart-x" style="font-size: 3rem; color: #94a3b8; margin-bottom: 15px;"></i>
                    <p>Your cart is empty</p>
                </div>
            `;
    } else {
      cart.forEach((item) => {
        const itemTotal = item.price * item.quantity;
        totalPrice += itemTotal;

        const itemHTML = `
                    <div class="cart-product">
                        <div class="product-row">
                            <img src="${item.image}" alt="${item.name}">
                            <div class="product-info">
                                <h4 class="product-name">${item.name}</h4>
                                <p class="product-price">$${item.price.toFixed(
                                  2
                                )} each</p>
                            </div>
                        </div>
                        
                        <div class="control-row">
                            <div class="quantity-controls">
                                <button class="qty-btn" onclick="updateQuantity('${
                                  item.id
                                }', ${item.quantity - 1})">-</button>
                                <span class="qty-value">${item.quantity}</span>
                                <button class="qty-btn" onclick="updateQuantity('${
                                  item.id
                                }', ${item.quantity + 1})">+</button>
                            </div>
                            
                            <div class="price-delete">
                                <p class="item-total-price">$${itemTotal.toFixed(
                                  2
                                )}</p>
                                <i class="bi bi-trash delete-icon" onclick="removeFromCart('${
                                  item.id
                                }')"></i>
                            </div>
                        </div>
                    </div>
                `;
        container.innerHTML += itemHTML;
      });
    }

    // تحديث السعر الكلي
    if (totalEl) {
      totalEl.textContent = `$${totalPrice.toFixed(2)} USD`;
    }
  }
}

// 6. تعديل الكمية
window.updateQuantity = function (id, newQty) {
  const qty = parseInt(newQty);
  if (qty < 1) return;

  const item = cart.find((item) => item.id == id);
  if (item) {
    item.quantity = qty;
    localStorage.setItem("dexshop_cart", JSON.stringify(cart));

    // تحديث العداد أولاً
    updateCartCounter();
    // ثم تحديث باقي الواجهة
    updateCartUI();
  }
};

// 7. حذف المنتج
window.removeFromCart = function (id) {
  cart = cart.filter((item) => item.id != id);
  localStorage.setItem("dexshop_cart", JSON.stringify(cart));

  // تحديث العداد أولاً
  updateCartCounter();
  // ثم تحديث باقي الواجهة
  updateCartUI();
};

// 8. إرسال الطلب
window.submitOrder = function (event) {
  event.preventDefault();

  if (cart.length === 0) {
    alert("Your cart is empty!");
    return;
  }

  const name = document.getElementById("customerName").value.trim();
  const phone = document.getElementById("customerPhone").value.trim();
  const address = document.getElementById("customerAddress").value.trim();

  if (!name || !phone || !address) {
    alert("Please fill in all required fields.");
    return;
  }

  // رسالة النجاح
  const messageDiv = document.createElement("div");
  messageDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #1e293b;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        z-index: 10000;
        border: 2px solid #0ea5e9;
        color: white;
        max-width: 400px;
        width: 90%;
        box-shadow: 0 20px 50px rgba(0,0,0,0.7);
    `;
  messageDiv.innerHTML = `
        <i class="bi bi-check-circle" style="font-size:3rem; color:#0ea5e9; margin-bottom:15px;"></i>
        <h3 style="margin:0 0 10px 0;">Order Submitted!</h3>
        <p style="color:#94a3b8; margin-bottom:20px;">Our team will contact you within 24 hours.</p>
        <button class="btn-ok" onclick="this.parentElement.remove()" style="
            padding:10px 30px; 
            background:#0ea5e9; 
            color:white; 
            border:none; 
            border-radius:5px; 
            cursor:pointer;
            font-weight:bold;
        ">OK</button>
    `;
  document.body.appendChild(messageDiv);

  // حفظ الطلب
  const orderData = {
    customer: { name, phone, address },
    items: [...cart],
    total: cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
    date: new Date().toLocaleString(),
  };

  const existingOrders =
    JSON.parse(localStorage.getItem("dexshop_orders")) || [];
  existingOrders.push(orderData);
  localStorage.setItem("dexshop_orders", JSON.stringify(existingOrders));

  // تفريغ السلة
  cart = [];
  localStorage.setItem("dexshop_cart", JSON.stringify(cart));

  // تحديث العداد أولاً (إلى 0)
  updateCartCounter();

  // ثم تحديث باقي الواجهة
  updateCartUI();

  closeSidebar();

  // مسح النموذج
  document.getElementById("customerName").value = "";
  document.getElementById("customerPhone").value = "";
  document.getElementById("customerAddress").value = "";

  console.log("✅ تم حفظ الطلب:", orderData);
};

/* --- SCROLL TO TOP --- */
const scrollBtn = document.getElementById("scrollTopBtn");

window.onscroll = function () {
  if (
    document.body.scrollTop > 300 ||
    document.documentElement.scrollTop > 300
  ) {
    scrollBtn.style.display = "block";
  } else {
    scrollBtn.style.display = "none";
  }
};

window.topFunction = function () {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

/* --- تهيئة النظام عند تحميل الصفحة --- */
document.addEventListener("DOMContentLoaded", function () {
  console.log("📄 تم تحميل الـ DOM بالكامل");
  initCartSystem();
});

// تهيئة احتياطية إذا فشل DOMContentLoaded
window.addEventListener("load", function () {
  console.log("🖼️ تم تحميل الصفحة بالكامل");
  if (!sidebar || !overlay) {
    console.log("🔄 إعادة محاولة تهيئة نظام السلة...");
    setTimeout(initCartSystem, 500);
  }
});
