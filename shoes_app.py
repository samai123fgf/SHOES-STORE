import streamlit as st
from collections import Counter

for key in ['cart', 'order_placed']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'cart' else False

products = {
    "Nike Air Max": {"price": 10200, "category": "Running", "brand": "Nike", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"},
    "Adidas Superstar": {"price": 6800, "category": "Casual", "brand": "Adidas", "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400"},
    "Puma Sneakers": {"price": 7650, "category": "Sports", "brand": "Puma", "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"},
    "Reebok Classic": {"price": 6375, "category": "Casual", "brand": "Reebok", "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400"},
    "Jordan Retro": {"price": 17000, "category": "Sports", "brand": "Jordan", "image": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400"},
    "Vans Old Skool": {"price": 5525, "category": "Casual", "brand": "Vans", "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400"}
}


st.sidebar.title("👟 Shoe Store")
page = st.sidebar.radio("Go to", ["Home", "Products", "Cart"])


if page == "Home":
    st.title("👟 Welcome to Shoe Store")
    st.write("Your one-stop shop for premium footwear!")
    st.subheader("Why Shop With Us?")
    c1, c2, c3 = st.columns(3)
    c1.write("✅ Free Shipping")
    c2.write("✅ 30-Day Returns")
    c3.write("✅ Best Prices")
    st.subheader("Featured Collection")
    featured = list(products.items())[:4]
    cols = st.columns(4)
    for idx, (name, details) in enumerate(featured):
        with cols[idx]:
            st.image(details["image"], caption=name, use_container_width=True)
            st.write(f"₹{details['price']:,}")


elif page == "Products":
    if st.session_state.order_placed:
        st.session_state.order_placed = False
    st.title("👟 Our Shoes Collection")
    c1, c2 = st.columns(2)
    with c1:
        category_filter = st.selectbox("Category", ["All", "Running", "Casual", "Sports"])
    with c2:
        brand_filter = st.selectbox("Brand", ["All"] + sorted({p["brand"] for p in products.values()}))
    
    filtered = [(n, d) for n, d in products.items() 
                if (category_filter == "All" or d["category"] == category_filter)
                and (brand_filter == "All" or d["brand"] == brand_filter)]
    
    if filtered:
        for i in range(0, len(filtered), 2):
            col1, col2 = st.columns(2)
            for j, col in enumerate([col1, col2]):
                if i + j < len(filtered):
                    name, details = filtered[i + j]
                    with col:
                        st.image(details["image"], caption=name, use_container_width=True)
                        st.markdown(f"**{name}**")
                        st.write(f"🏷️ **Brand:** {details['brand']}")
                        st.write(f"📂 **Category:** {details['category']}")
                        st.write(f"💰 **Price:** ₹{details['price']:,}")
                        if st.button(f"🛒 Add to Cart", key=f"add_{name}_{j}"):
                            st.session_state.cart.append(name)
                            st.success(f"✓ {name} added to cart!", icon="✅")
                            st.rerun()
                        st.markdown("---")
    else:
        st.warning("No products found matching your filters!")


elif page == "Cart":
    st.title("🛒 Your Shopping Cart")
    
    if st.session_state.order_placed:
        st.balloons()
        st.success("🎉 **THANK YOU FOR YOUR PURCHASE!** 🎉")
        st.success("✅ Your order has been placed successfully!")
        if st.button("🛍️ Continue Shopping", type="primary"):
            st.session_state.order_placed = False
            st.rerun()
    elif not st.session_state.cart:
        st.info("Your cart is empty. Add some shoes!")
        if st.button("🛍️ Start Shopping"):
            st.rerun()
    else:
        cart_items = Counter(st.session_state.cart)
        total = 0
        for item, qty in cart_items.items():
            price = products[item]["price"]
            subtotal = price * qty
            total += subtotal
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.image(products[item]["image"], width=100)
            with c2:
                st.markdown(f"**{item}**")
                st.write(f"Price: ₹{price:,} each | Quantity: {qty}")
            with c3:
                st.write(f"**Subtotal: ₹{subtotal:,}**")
                if st.button(f"🗑️ Remove", key=f"remove_{item}"):
                    for _ in range(qty):
                        st.session_state.cart.remove(item)
                    st.rerun()
            st.divider()
        
        st.subheader("Order Summary")
        c1, c2 = st.columns(2)
        with c1:
            shipping = 0 if total > 4250 else 510  
            st.write(f"**Subtotal:** ₹{total:,}")
            st.write(f"**Shipping:** ₹{shipping}")
            st.write(f"**Total:** ₹{total + shipping:,}")
        with c2:
            if st.button("✅ Proceed to Checkout", type="primary", use_container_width=True):
                st.session_state.order_placed = True
                st.session_state.cart = []
                st.rerun()
            if st.button("🗑️ Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()