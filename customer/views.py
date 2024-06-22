from django.shortcuts import render, redirect
from customer.forms import FormDangKy
from customer.models import Customer
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher
from cart.cart import Cart
from cart.models import Order, OrderItem
from store.models import Product


# Create your views here.
def dang_nhap(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    if 's_khachhang' in request.session:
        return redirect('store:trang_chu')

    # Giỏ hàng
    cart = Cart(request)

    # Đăng ký
    form = FormDangKy()
    result_register = ''
    if request.POST.get('btnDangKy'):
        form = FormDangKy(request.POST, Customer)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                hasher = PBKDF2PasswordHasher()
                request.POST._mutable = True
                post = form.save(commit=False)
                post.first_name = form.cleaned_data['first_name']
                post.last_name = form.cleaned_data['last_name']
                post.email = form.cleaned_data['email']
                post.password = hasher.encode(form.cleaned_data['password'], '123456')  # salt
                post.phone = form.cleaned_data['phone']
                post.address = form.cleaned_data['address']
                post.save()

                result_register = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành viên thành công
                </div>
                '''
            else:
                result_register = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu và Xác nhận mật khẩu không khớp
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger" role="alert">
                    Dữ liệu nhập không hợp lệ
                </div>
                '''

    # Đăng nhập
    result_login = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = PBKDF2PasswordHasher()
        mat_khau_encoded = hasher.encode(mat_khau, '123456')

        # Xử lý đọc thông tin từ CSDL
        nguoi_dung = Customer.objects.filter(email=email, password=mat_khau_encoded)
        if nguoi_dung.count() > 0:
            dict_nguoi_dung = nguoi_dung.values()[0]
            del(dict_nguoi_dung['password'])
            request.session['s_khachhang'] = dict_nguoi_dung
            return redirect('store:trang_chu')
        else:
            result_login = '''
            <div class="alert alert-danger" role="alert">
                Đăng nhập thất bại. Vui lòng kiểm lại thông tin
            </div>
            '''

    return render(request, 'store/login.html', {
        'form': form,
        'result_register': result_register,
        'result_login': result_login,
        'cart': cart,
    })


def tai_khoan_cua_toi(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    if 's_khachhang' not in request.session:
        return redirect('customer:dang_nhap')

    # Giỏ hàng
    cart = Cart(request)

    # Hồ sơ của tôi
    result_info = ''
    if request.POST.get('btnCapNhat'):
        # Gán biến
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        dien_thoai = request.POST.get('dien_thoai')
        dia_chi = request.POST.get('dia_chi')

        # Load đối tượng khách hàng từ CSDL (model)
        dict_khach_hang = request.session.get('s_khachhang')
        khach_hang = Customer.objects.get(pk=dict_khach_hang['id'])

        # Update thông tin vào các fields và lưu vào CSDL
        khach_hang.first_name = ho
        khach_hang.last_name = ten
        khach_hang.phone = dien_thoai
        khach_hang.address = dia_chi
        khach_hang.save()

        # Update thông tin vào session s_khachhang
        dict_khach_hang['first_name'] = ho
        dict_khach_hang['last_name'] = ten
        dict_khach_hang['phone'] = dien_thoai
        dict_khach_hang['address'] = dia_chi
        request.session['s_khachhang'] = dict_khach_hang

        result_info = '''
        <div class="alert alert-success" role="alert">
            Cập nhật thông tin thành công
        </div>
        '''

    # Đổi mật khẩu
    result_change_pwd = ''
    if request.POST.get('btnDoiMatKhau'):
        # Gán biến
        mat_khau_hien_tai = request.POST.get('mat_khau_hien_tai')
        mat_khau_moi = request.POST.get('mat_khau_moi')
        xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau')

        # Load đối tượng khách hàng từ CSDL (model)
        dict_khach_hang = request.session.get('s_khachhang')
        khach_hang = Customer.objects.get(pk=dict_khach_hang['id'])

        # Xét mật khẩu hiện tại
        hasher = PBKDF2PasswordHasher()
        mat_khau_hien_tai_encoded = hasher.encode(mat_khau_hien_tai, '123456')
        if mat_khau_hien_tai_encoded == khach_hang.password:
            if mat_khau_moi == xac_nhan_mat_khau:
                # Cập nhật mật khẩu vào CSDL
                khach_hang.password = hasher.encode(mat_khau_moi, '123456')
                khach_hang.save()

                result_change_pwd = '''
                <div class="alert alert-success" role="alert">
                    Đổi mật khẩu thành công
                </div>
                '''
            else:
                result_change_pwd = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu mới và Xác nhận mật khẩu không khớp
                </div>
                '''
        else:
            result_change_pwd = '''
            <div class="alert alert-danger" role="alert">
                Mật khẩu hiện tại không đúng
            </div>
            '''

    # Hiển thị danh sách đơn hàng
    orders = Order.objects.filter(customer=request.session['s_khachhang']['id'])
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order=order.pk).values())
        for order_item in order_items:
            product = Product.objects.get(pk=order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total_price'] = order.total
        else:
            dict_order_items = {
                order.pk: order_items
            }
            dict_orders.update(dict_order_items)

    return render(request, 'store/my-account.html', {
        'cart': cart,
        'result_info': result_info,
        'result_change_pwd': result_change_pwd,
        'orders': orders,
        'dict_orders': dict_orders,
    })


def dang_xuat(request):
    if 's_khachhang' in request.session:
        del request.session['s_khachhang']
    return redirect('customer:dang_nhap')




