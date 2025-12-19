# cafe_inventory_backend
Cafe Inventory Management System
Hệ thống quản lý kho hàng dành cho quán cà phê và doanh nghiệp nhỏ
Một giải pháp mã nguồn mở đơn giản, hiệu quả, sử dụng công nghệ hiện đại và hoàn toàn miễn phí.
Python
FastAPI
PostgreSQL
License
Giới thiệu
Cafe Inventory là hệ thống quản lý kho hàng được thiết kế dành riêng cho các quán cà phê, cửa hàng bán lẻ nhỏ và doanh nghiệp vừa. Hệ thống giúp theo dõi tồn kho nguyên liệu (hạt cà phê, syrup, bột cacao, trà, v.v.) một cách chính xác, giảm thiểu sai sót thủ công và hỗ trợ chủ doanh nghiệp ra quyết định nhanh chóng.
Dự án hoàn toàn mã nguồn mở, dễ triển khai, dễ tùy chỉnh và không phụ thuộc vào bất kỳ nền tảng thương mại nào.
Tính năng chính

Dashboard tổng quan: KPI, biểu đồ nhập/xuất kho 7 ngày gần nhất, top sản phẩm nhập/xuất nhiều nhất.
Quản lý sản phẩm: Thêm/sửa/xóa, tìm kiếm, lọc theo nhóm hàng, cảnh báo tồn kho thấp.
Nhập kho: Tạo phiếu nhập từ nhà cung cấp, tự động cập nhật tồn kho.
Xuất kho: Tạo phiếu xuất (bán hàng hoặc sử dụng nội bộ), kiểm tra tồn kho trước khi xuất.
Kiểm kho định kỳ: So sánh tồn hệ thống vs thực tế, tự động cân bằng kho sau khi lưu.
Giao diện thân thiện: Responsive, hoạt động tốt trên máy tính và điện thoại.
Không cần cài đặt phức tạp: Chỉ cần chạy backend và mở file HTML.

Công nghệ sử dụng

Backend: FastAPI (Python)
Database: PostgreSQL
ORM: SQLAlchemy
Frontend: HTML5 + Tailwind CSS + JavaScript thuần
Biểu đồ: Chart.js

Hướng dẫn cài đặt và chạy
1. Yêu cầu

Python 3.10+
PostgreSQL 13+
git clone https://github.com/tigerr14436/cafe_inventory_backend.git
cd cafe_inventory_backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

3. Cấu hình database
Tạo database trong PostgreSQL:
SQLCREATE DATABASE cafe_inventory;
CREATE USER fastapi_user WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON DATABASE cafe_inventory TO fastapi_user;

4. Chạy ứng dụng
Bashuvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Truy cập giao diện
Mở các file HTML trong thư mục frontend (hoặc phục vụ tĩnh qua FastAPI):

Dashboard: index.html
Quản lý sản phẩm: san_pham.html
Nhập kho: nhap_kho.html
Xuất kho: xuat_kho.html
Kiểm kho: kiem_kho.html

Đóng góp
Dự án rất hoan nghênh mọi đóng góp từ cộng đồng!

Fork repository
Tạo branch mới (git checkout -b feature/ten-tinh-nang)
Commit thay đổi (git commit -m 'Thêm tính năng X')
Push lên branch (git push origin feature/ten-tinh-nang)
Tạo Pull Request

Tính năng dự kiến trong tương lai

Phân quyền người dùng (admin / nhân viên)
In phiếu nhập/xuất (PDF)
Báo cáo doanh thu cơ bản
Tích hợp mobile app (PWA hoặc Flutter)
Dự báo nhu cầu nguyên liệu bằng AI đơn giản
Hỗ trợ đa kho
