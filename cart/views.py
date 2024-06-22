from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from customer.models import Customer
from cart.models import Order, OrderItem


# Create your views here.
def gio_hang(request):
    cart = Cart(request)

    # Mã giảm giá
    ds_ma_giam_gia = [
        {'TTTH': 0.8},
        {'LNT': 0.9}
    ]

    if request.POST.get('btnMaGiamGia'):
        # Gán biến
        ma_giam_gia = request.POST.get('ma_giam_gia').strip()
        for dict_ma_giam_gia in ds_ma_giam_gia:
            if ma_giam_gia in dict_ma_giam_gia:
                giam_gia = dict_ma_giam_gia[ma_giam_gia]
                cart_new = {}
                for c in cart:
                    product_cart = {
                        str(c['product'].pk): {
                            'quantity': c['quantity'],
                            'price': str(c['price']),
                            'coupon': str(giam_gia)
                        }
                    }
                    cart_new.update(product_cart)
                    c['coupon'] = giam_gia  # Giữ lại giảm giá mới sau khi click nút sử dụng
                else:
                    request.session['cart'] = cart_new

    # Cập nhật giỏ hàng (thay đổi số lượng)
    if request.POST.get('btnCapNhatGioHang'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get('quantity2_' + str(c['product'].pk)))
            if quantity_new != 0:
                product_cart = {
                    str(c['product'].pk): {
                        'quantity': quantity_new,
                        'price': str(c['price']),
                        'coupon': str(c['coupon'])
                    }
                }
                cart_new.update(product_cart)
                c['quantity'] = quantity_new  # Giữ lại số lượng mới trong ô số lượng của giỏ hàng sau khi update
            else:
                cart.remove(c['product'])
        else:
            request.session['cart'] = cart_new

    return render(request, 'store/cart.html', {
        'cart': cart,
    })


def thanh_toan(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart:gio_hang')

    if request.POST.get('btnDatHang'):
        khach_hang = Customer.objects.get(pk=request.session.get('s_khachhang')['id'])

        # Lưu Order
        order = Order()
        order.customer = khach_hang
        order.total = cart.get_final_total_price()
        order.save()

        # Lưu OrderItem
        for c in cart:
            OrderItem.objects.create(order=order,
                                     product=c['product'],
                                     price=c['price'],
                                     quantity=c['quantity'])

        # Gửi mail

        # Clear giỏ hàng
        cart.clear()

        # Thông báo thành công
        return render(request, 'cart/result.html', {
            'cart': cart,
        })

    return render(request, 'store/checkout.html', {
        'cart': cart,
    })


def mua_ngay(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        quantity = int(request.POST.get('quantity'))
        cart.add(product, quantity)
    return redirect('cart:gio_hang')


def xoa_san_pham(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:gio_hang')
