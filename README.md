# BÁO CÁO KIỂM THỬ TỰ ĐỘNG SELENIUM

## 1. Giới thiệu
- Website được kiểm thử: **https://www.saucedemo.com/**
- Công cụ: **Selenium WebDriver + Python + pytest + pytest-html**
- Mục tiêu: Thực hiện tối thiểu 5 test case tự động; dự án cung cấp **6 test case**.
- Repository: https://github.com/silentn9990/Testing_-Selenium

Selenium tự điều khiển Chrome; pytest chạy test và kiểm tra assertion; pytest-html xuất báo cáo HTML.

## 2. Cấu trúc dự án

```text
Testing_-Selenium/
├── tests/
│   ├── conftest.py           # Khởi tạo Chrome, lưu screenshot
│   └── test_saucedemo.py     # 6 test case
├── reports/
│   └── .gitkeep             # report và ảnh được sinh khi chạy
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## 3. Cài đặt và chạy

Yêu cầu: Python 3.10+, trình duyệt Google Chrome, Internet.

```powershell
git clone https://github.com/silentn9990/Testing_-Selenium.git
cd Testing_-Selenium
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Nếu kích hoạt được virtual environment, cũng có thể chạy:
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

Selenium Manager tự hỗ trợ tìm driver phù hợp trên môi trường thông thường. Có thể chạy không hiện cửa sổ bằng cách đặt `$env:HEADLESS="1"` trước khi chạy pytest.

Chạy từng test riêng:
```powershell
python -m pytest tests/test_saucedemo.py::test_tc01_login_success
```

## 4. Bảng test case

| ID | Tình huống | Thao tác kiểm thử | Kết quả mong đợi |
|---|---|---|---|
| TC01 | Đăng nhập đúng | Nhập `standard_user` / `secret_sauce`, nhấn Login | Trang Products hiển thị |
| TC02 | Đăng nhập sai | Nhập `standard_user` / `wrong_password` | Hiện thông báo sai tài khoản/mật khẩu |
| TC03 | Sắp xếp sản phẩm | Đăng nhập, chọn Price (low to high) | Giá hiển thị theo thứ tự tăng dần |
| TC04 | Thêm vào giỏ | Đăng nhập, thêm Sauce Labs Backpack, mở giỏ | Giỏ có đúng sản phẩm, số lượng 1 |
| TC05 | Xóa khỏi giỏ | Thêm sản phẩm rồi Remove | Giỏ không còn sản phẩm |
| TC06 | Đăng xuất | Đăng nhập, mở menu, Logout | Trở lại màn hình đăng nhập |

Các bài test độc lập, có WebDriverWait, và dùng assertion để tự động kết luận thành công/thất bại.

## 5. Kết quả chạy kiểm thử

**Kết quả thực tế trên Windows 11, Python 3.13.2, Chrome, pytest 9.1.1:** 6 PASSED, 0 FAILED, 0 ERROR trong **51.04 giây**. Dữ liệu dựa trên log Terminal do người thực hiện cung cấp sau khi chạy `python -m pytest -v`.

| ID | Kết quả thực tế | Ảnh bằng chứng sau khi chạy |
|---|---|---|
| TC01 | PASSED | `reports/screenshots/test_tc01_login_success_PASS.png` |
| TC02 | PASSED | `reports/screenshots/test_tc02_login_wrong_password_PASS.png` |
| TC03 | PASSED | `reports/screenshots/test_tc03_sort_prices_low_to_high_PASS.png` |
| TC04 | PASSED | `reports/screenshots/test_tc04_add_product_to_cart_PASS.png` |
| TC05 | PASSED | `reports/screenshots/test_tc05_remove_product_from_cart_PASS.png` |
| TC06 | PASSED | `reports/screenshots/test_tc06_logout_PASS.png` |

**Báo cáo HTML:** `reports/report.html` được pytest-html tạo tự động.
**Ảnh tự động:** `reports/screenshots/` được tạo khi chạy. Các ảnh đã được tạo khi chạy trên máy người thực hiện; cần tải ảnh PNG thực tế lên repo để minh họa kết quả. File `.gitignore` loại trừ các kết quả chạy cục bộ, nên có thể dùng GitHub Web → Add file → Upload files để tải ảnh hoặc điều chỉnh .gitignore rồi commit.

### Những ảnh nên chụp để nộp
1. Terminal kết quả tổng hợp pytest.
2. TC01 đăng nhập thành công.
3. TC02 thông báo lỗi đăng nhập.
4. TC03 sản phẩm được sắp giá tăng.
5. TC04 sản phẩm nằm trong giỏ.
6. TC05 giỏ hàng trống.
7. TC06 đã đăng xuất.
8. Báo cáo HTML nếu cần.

Sau khi có ảnh trong GitHub, thay đường dẫn ảnh phù hợp vào README theo cú pháp `![TC01](reports/screenshots/test_tc01_login_success_PASS.png)`.

## 6. Nhận xét và kết luận

Đã xây dựng 06 kịch bản tự động bao gồm trường hợp hợp lệ, không hợp lệ, sắp xếp và thao tác giỏ hàng. Mỗi bài test mở trình duyệt riêng, giúp tránh phụ thuộc trạng thái. Lần chạy thực tế đã hoàn thành 6/6 test case với kết quả PASSED. Kết quả chỉ phản ánh sáu kịch bản được xây dựng, không đồng nghĩa website không còn lỗi ở các chức năng khác.

## 7. Tài liệu
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
- [pytest](https://docs.pytest.org/)
- [SauceDemo](https://www.saucedemo.com/)
