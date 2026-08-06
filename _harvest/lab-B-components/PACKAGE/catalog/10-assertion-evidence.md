# Luận điểm dạng câu đầy đủ, một bằng chứng duy nhất bên dưới

`KHỐI 10 · THẺ LUẬN ĐIỂM (ASSERTION-EVIDENCE, KIỂU TUFTE)`

## Mô tả / khi nào dùng

Nguyên tắc Michael Alley (Assertion-Evidence, Penn State): tiêu đề là MỘT CÂU HOÀN CHỈNH mang kết luận, không phải cụm danh từ; bên dưới là đúng MỘT bằng chứng, không bullet, không chartjunk. Trả lời: "Kết luận này dựa trên bằng chứng cụ thể nào?" KHÔNG dùng khi cần trình bày >1 bằng chứng đồng thời (dùng bảng hoặc statgrid).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<article class="assertion-card">
    <h3>Chi phí nhiên liệu đã vượt chi phí thuyền viên, trở thành khoản mục lớn nhất trong giá vốn khai thác.</h3>
    <div class="ae-evidence">
      <div class="ae-figure">
        <span class="ae-num neg">42,3%</span>
        <span class="ae-caption">TỶ TRỌNG NHIÊN LIỆU / GIÁ VỐN KHAI THÁC, FY2025<br>(FY2023: 38,5% · thuyền viên FY2025: 24,1%)</span>
      </div>
      <p class="ae-note">Tăng 3,8 điểm phần trăm trong 2 năm, chủ yếu do giá VLSFO bình quân tăng 14% và tỷ giá USD/VND mất giá 4,2% cùng kỳ.</p>
    </div>
  </article>
```
