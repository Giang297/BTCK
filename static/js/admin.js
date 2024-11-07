function runSchedule() {
    // Hiển thị thông báo người dùng biết rằng quá trình đang chạy
    alert("Đang chạy phân lịch...");

    // Gửi yêu cầu tới server để xử lý phân lịch
    fetch('/run_schedule', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Có lỗi xảy ra khi phân lịch");
        }
    })
    .then(data => {
        // Sau khi hoàn thành phân lịch, cập nhật giao diện hoặc thông báo cho người dùng
        alert("Phân lịch thành công!");
        console.log("Kết quả phân lịch:", data);
        // Bạn có thể thêm logic để cập nhật lịch mới lên trang nếu cần thiết
        location.reload();  // Reload trang để hiển thị lịch mới
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Có lỗi xảy ra: " + error.message);
    });
}
