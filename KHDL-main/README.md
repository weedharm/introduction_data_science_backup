# Hướng dẫn thực hiện project KHDL
## Thành viên
- Nguyễn Đức Nguyên 20183600
- Trần Đức Thọ 20183634
- Trần Văn Điệp
- Vũ Tấn Khang 20183561

## Tổng quan về đề tài
- Tên đề tài: Dự đoán giá laptop bằng ....
- Nguồn dữ liệu: An Phát, Hà Nội Computer, Phong Vũ

## Hướng dẫn chạy project

- Crawl dữ liệu gồm tên, url các sản phẩm laptop: thực hiện chạy file Crawl_for_KHDL.ipynb
- Crawl chi tiết các trường thông tin yêu cầu từ 3 file Crawl_Search_*.csv: Crawl_details_laptop.ipynb và file hanoipc.py
- Tạo dataframe từ 3 file Product_An_Phat.csv, Product_HNCom.csv, Product_Phong_Vu.csv: chạy file concat.py ==> tạo được file 1.csv
- Xử lý data: chạy file main.py ==> thu được file final_data.csv là dữ liệu qua bước tiền xử lý

