# Danh gia kha nang dung chung 1 model cho Dataset 1 va Dataset 2

## 1. Muc tieu danh gia

Muc tieu cua tai lieu nay la xac dinh xem Dataset 1 va Dataset 2 co the dung chung 1 model de giai quyet cung mot bai toan hay khong.

De tai hien tai:

```text
Phan tich va du doan doanh thu coffee shop dua tren cac yeu to ben ngoai
```

Bai toan model nen huong den:

```text
Input:
- thoi gian
- dia diem
- nhom san pham
- thoi tiet
- ngay le

Output:
- doanh thu
```

Neu dung chung 1 model, hai dataset khong bat buoc phai giong nhau 100% o du lieu goc. Tuy nhien, sau khi xu ly, chung phai duoc dua ve cung mot don vi phan tich va cung mot y nghia du doan.

Vi du don vi du lieu phu hop:

```text
moi dong = doanh thu theo ngay, gio, dia diem, nhom san pham
target = revenue
features = hour, weekday, month, location, weather, holiday, product_category
```

## 2. Ket luan tong quan ban dau

Hien tai co the thu dung chung 1 model, nhung chua nen khang dinh ngay la dung chung se tot.

Nhan dinh nhanh:

| Tieu chi | Danh gia ban dau |
|---|---|
| Domain scope | Kha tuong thich vi ca hai dataset deu ve coffee shop transaction |
| Schema | Co the chuan hoa duoc sau khi aggregate |
| Temporal scope | Lech vi Dataset 1 co ca nam 2023, Dataset 2 chi co 01-06/2023 |
| Spatial scope | Lech nhe vi Dataset 1 o muc New York, Dataset 2 co cac store location cu the hon |
| External features | Chua dong deu vi Dataset 1 co weather/holiday, Dataset 2 chua co |
| Data imbalance | Lech manh vi Dataset 2 co so dong lon hon Dataset 1 rat nhieu |

Huong dung nhat la:

```text
1. Chuan hoa schema
2. Aggregate ve cung cap do
3. Bo sung weather/holiday cho Dataset 2
4. Train thu model chung
5. Danh gia rieng tung dataset
6. So sanh model chung voi model rieng
```

Neu model chung hoat dong tot tren ca Dataset 1 va Dataset 2, luc do co the ket luan hai dataset co tinh interchangeable o muc bai toan da duoc chuan hoa va aggregate.

## 3. Van de 1: Xac dinh cung mot don vi du lieu

### Y nghia

Truoc khi train model chung, can xac dinh moi dong du lieu dai dien cho dieu gi.

Du lieu goc cua ca hai dataset deu gan voi giao dich. Tuy nhien, voi bai toan du doan doanh thu dua tren yeu to ben ngoai, khong nen giu moi dong la mot giao dich rieng le. Ly do la cac yeu to ben ngoai nhu thoi tiet, ngay le, gio trong ngay, dia diem thuong anh huong den tong doanh thu trong mot khoang thoi gian, chu khong chi anh huong den tung giao dich rieng le.

Don vi phu hop hon:

```text
moi dong = doanh thu theo gio / ngay / dia diem / nhom san pham
```

Vi du:

```text
date | hour | location | product_category | weather | holiday | revenue
```

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Giu transaction-level | Giu duoc chi tiet tung giao dich, so dong nhieu | De sai bai toan vi model du doan giao dich rieng le, khong phan anh tot tac dong cua yeu to ben ngoai |
| Aggregate theo ngay | On dinh, de phan tich, phu hop voi bao cao tong quan | Mat chi tiet theo gio, kho thay peak hour |
| Aggregate theo gio | Phu hop voi hanh vi coffee shop, giu duoc pattern sang/trua/chieu | Du lieu nho hon, can xu ly nhung gio khong co giao dich |
| Aggregate theo gio + location + product_category | Giu duoc ca yeu to thoi gian, dia diem va san pham | Phuc tap hon, so dong giua hai dataset co the lech |

### Khuyen nghi

Nen dung muc aggregate:

```text
date + hour + location + product_category
```

Ly do:

- Phu hop voi bai toan du doan doanh thu.
- Van giu duoc tac dong cua thoi gian trong ngay.
- Co the gan them weather va holiday theo date/location.
- Co the so sanh doanh thu giua cac location va product category.

## 4. Van de 2: Kiem tra schema co chuan hoa duoc khong

### Y nghia

Schema la cau truc cot cua dataset. Hai dataset khong can giong nhau ngay tu dau, nhung neu muon dung chung model thi phai dua ve cung mot bo cot chuan.

Schema chuan nen co:

```text
date
hour
weekday
month
is_weekend
location
product_category
weather_condition
temperature_c
is_holiday
revenue
source_dataset
```

### Van de hien tai

Dataset 1 co mot so thong tin external nhu:

```text
weather_condition
temperature_c
holiday_name
```

Dataset 2 hien tai chua co weather/holiday. Neu train model chung ngay, model se thay Dataset 1 co external features, Dataset 2 thi bi thieu. Dieu nay lam model de hoc su khac nhau giua nguon dataset thay vi hoc quy luat doanh thu that.

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Chi dung cac cot chung hien co | Nhanh, de tao baseline | Chua dung trong tam de tai vi thieu weather/holiday |
| Cao them weather/holiday cho Dataset 2 | Dung huong nhat, lam hai dataset tuong thich hon | Ton cong thu thap, can join theo date/location |
| Giu cot thieu bang NaN va them missing indicator | Khong mat du lieu | Model co the hoc "dataset nao bi thieu cot nao" thay vi hoc quy luat doanh thu |
| Bo het weather/holiday de train chung | Cong bang ve schema | Lam yeu de tai vi khong con nhan manh yeu to ben ngoai |

### Khuyen nghi

Nen cao them weather/holiday cho Dataset 2, sau do chuan hoa ca hai dataset ve cung bo cot.

Trong giai doan baseline co the train voi cac cot chung, nhung trong bao cao can ghi ro:

```text
Model baseline chua su dung day du external features vi Dataset 2 chua co weather/holiday.
```

## 5. Van de 3: Kiem tra temporal scope

### Y nghia

Temporal scope la pham vi thoi gian ma dataset bao phu.

Hien tai:

```text
Dataset 1: ca nam 2023
Dataset 2: 01/2023 - 06/2023
```

Day la diem can can trong. Neu train chung toan bo du lieu, model co the hoc nham:

```text
thang 07-12 chi xuat hien o Dataset 1
```

Luc do model khong chi hoc pattern theo thang, ma con hoc ca su khac nhau ve nguon dataset.

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Chi dung khoang chung 01-06/2023 | Cong bang nhat de so sanh hai dataset | Bo mat du lieu 07-12 cua Dataset 1 |
| Dung toan bo du lieu va them `source_dataset` | Tan dung het du lieu | Model co the phu thuoc vao nguon dataset |
| Train 2 phien ban: common period va full period | Danh gia khach quan hon | Ton them thoi gian va can giai thich nhieu hon |
| Tach train/test theo thoi gian | Phu hop voi bai toan du doan tuong lai | Neu scope lech, ket qua co the kho doc |

### Khuyen nghi

Nen lam toi thieu 2 thi nghiem:

```text
Experiment 1: chi dung khoang chung 01-06/2023
Experiment 2: dung toan bo du lieu
```

Neu model chung chi tot o Experiment 1 nhung kem o Experiment 2, co the ket luan temporal scope dang anh huong manh den kha nang dung chung model.

## 6. Van de 4: Kiem tra spatial scope

### Y nghia

Spatial scope la pham vi khong gian/dia diem ma dataset bao phu.

Hien tai:

```text
Dataset 1: New York
Dataset 2: Astoria, Hell's Kitchen, Lower Manhattan
```

Dataset 1 co ve o muc thanh pho, Dataset 2 co ve o muc khu vuc/cua hang cu the hon. Neu khong xu ly, cot `location` se khong hoan toan cung cap do.

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Gop tat ca thanh mot cot `location` | De lam, du cho baseline | Muc dia ly chua dong nhat |
| Chuan hoa thanh cac cap `city`, `district`, `store_location` | Ro rang, tot cho phan tich scope | Can xu ly thu cong |
| Train rieng theo location | Co the chinh xac hon neu moi location rat khac nhau | Khong con la 1 model chung don gian |
| Them `source_dataset` de model biet nguon | Giam nham lan giua location va dataset | Model co the qua phu thuoc vao source |

### Khuyen nghi

Nen giu cot `location` cho model baseline, nhung trong bao cao can neu ro:

```text
Spatial scope cua hai dataset chua hoan toan dong nhat.
Dataset 1 o muc New York, Dataset 2 o muc store location cu the.
```

Neu muon lam tot hon, nen tao them cac cot:

```text
city
area_or_district
store_location
```

## 7. Van de 5: Kiem tra domain scope

### Y nghia

Domain scope la pham vi linh vuc va doi tuong nghien cuu.

Day la diem tuong thich nhat cua hai dataset vi ca hai deu lien quan den:

```text
coffee shop
transaction
product category
quantity
unit price
revenue
```

Tuy nhien van can kiem tra xem cac gia tri trong `product_category` co cung y nghia khong.

Vi du:

```text
Coffee o Dataset 1 co tuong duong Coffee o Dataset 2 khong?
Tea o Dataset 1 co cung cach phan loai voi Tea o Dataset 2 khong?
```

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Giu nguyen product_category | Nhanh, don gian | Co the lech neu ten giong nhau nhung cach dinh nghia khac |
| Mapping category ve nhom chung | Tot cho so sanh va model chung | Can kiem tra thu cong |
| Chi dung category xuat hien o ca hai dataset | Cong bang hon | Mat mot phan du lieu |
| Gop category hiem vao `Other` | Giam nhieu, giam overfitting | Mat chi tiet san pham |

### Khuyen nghi

Nen tao bang mapping `product_category` giua Dataset 1 va Dataset 2.

Muc tieu la dam bao category sau khi chuan hoa co cung y nghia kinh doanh.

## 8. Van de 6: Kiem tra data imbalance

### Y nghia

Data imbalance la tinh trang mot dataset co qua nhieu dong so voi dataset con lai.

Sau khi aggregate hien tai:

```text
Dataset 1: 919 dong
Dataset 2: 30,789 dong
```

Dataset 2 lon hon Dataset 1 khoang 33 lan. Neu train chung binh thuong, model se hoc chu yeu tu Dataset 2. Khi do metric tong the co the dep, nhung model co the du doan kem tren Dataset 1.

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Train chung binh thuong | Don gian, de co baseline | Dataset 1 bi lan at |
| Dung sample weight cho Dataset 1 | Can bang anh huong cua Dataset 1 | Can giai thich ky, co the lam model kem hon tren Dataset 2 |
| Downsample Dataset 2 | Can bang so dong | Lang phi du lieu |
| Aggregate o muc tho hon | Giam lech so dong | Mat chi tiet theo gio/category |
| Danh gia metric rieng theo source_dataset | Phat hien duoc model co thien lech khong | Khong tu sua imbalance, chi giup nhan dien |

### Khuyen nghi

Bat buoc phai danh gia metric rieng:

```text
Overall
Dataset 1 only
Dataset 2 only
```

Sau do moi ket luan model chung co dung duoc hay khong.

Neu metric Dataset 2 tot nhung Dataset 1 kem, thi chua the noi model chung tot.

## 9. Van de 7: Kiem tra target distribution

### Y nghia

Target distribution la phan phoi cua bien can du doan, o day la `revenue`.

Can kiem tra:

```text
mean revenue
median revenue
min revenue
max revenue
boxplot revenue theo source_dataset
histogram revenue theo source_dataset
```

Neu doanh thu sau aggregate cua Dataset 2 lon hon Dataset 1 qua nhieu, model chung co the bi lech ve Dataset 2.

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Du doan revenue goc | De hieu, de giai thich | De bi anh huong boi outlier |
| Du doan `log1p(revenue)` | On dinh hon, giam anh huong outlier | Can inverse transform khi dien giai |
| Chuan hoa revenue theo location/category | So sanh cong bang hon | Kho giai thich voi nguoi khong chuyen |
| Train rieng roi so sanh | Thay ro su khac biet giua dataset | Khong phai loi giai truc tiep cho 1 model chung |

### Khuyen nghi

Nen thu hai cach:

```text
Model 1: target = revenue
Model 2: target = log1p(revenue)
```

Sau do so sanh metric va residual plot.

## 10. Van de 8: Kiem tra leakage

### Y nghia

Data leakage la khi model duoc dung nhung bien ma trong thuc te luc du doan khong the biet truoc, hoac nhung bien gan nhu truc tiep tao ra target.

Vi de tai la du doan doanh thu dua tren yeu to ben ngoai, model chinh khong nen dung cac bien da biet sau khi giao dich xay ra.

Khong nen dung lam input cho model chinh:

```text
quantity
transaction_count
avg_transaction_value
unit_price neu unit_price truc tiep tao ra revenue
```

Ly do:

```text
revenue = quantity * unit_price
```

Neu dua `quantity` hoac `transaction_count` vao model, model se co diem cao nhung khong dung y nghia du doan bang yeu to ben ngoai.

Nen dung:

```text
hour
weekday
month
is_weekend
location
product_category
weather_condition
temperature_c
is_holiday
```

### Cac phuong phap

| Phuong phap | Uu diem | Nhuoc diem |
|---|---|---|
| Dung ca quantity/transaction_count | Model co diem cao | Sai y nghia bai toan, bi leakage |
| Chi dung yeu to ben ngoai | Dung voi de tai | Model co the kem hon |
| Lam 2 model: external-only va full-feature | Hay cho bao cao, chung minh leakage/feature impact | Can giai thich ro model nao la model chinh |

### Khuyen nghi

Model chinh nen la:

```text
external-only model
```

Co the lam them full-feature model de so sanh, nhung phai ghi ro full-feature model khong phai model chinh neu no dung bien sau giao dich.

## 11. Van de 9: Thiet ke thi nghiem de ket luan

### Muc tieu

Khong nen ket luan cam tinh rang Dataset 1 va Dataset 2 dung chung model duoc. Can thiet ke thi nghiem de chung minh.

### Bo thi nghiem de xuat

Nen train va so sanh it nhat 4 mo hinh:

```text
Model A: train rieng Dataset 1
Model B: train rieng Dataset 2
Model C: train chung Dataset 1 + Dataset 2
Model D: train tren Dataset 2, test tren Dataset 1
```

Co the them:

```text
Model E: train tren Dataset 1, test tren Dataset 2
```

### Y nghia tung model

| Model | Y nghia |
|---|---|
| Model A | Xem Dataset 1 tu no co hoc duoc pattern doanh thu khong |
| Model B | Xem Dataset 2 tu no co hoc duoc pattern doanh thu khong |
| Model C | Kiem tra kha nang dung chung 1 model |
| Model D | Kiem tra Dataset 2 co generalize sang Dataset 1 khong |
| Model E | Kiem tra Dataset 1 co generalize sang Dataset 2 khong |

### Metric nen dung

```text
MAE
RMSE
R2
MAPE neu revenue khong co nhieu gia tri gan 0
```

Trong do:

- MAE de giai thich sai so trung binh bang don vi doanh thu.
- RMSE phat nang cac loi du doan lon.
- R2 cho biet model giai thich duoc bao nhieu phan bien thien cua revenue.
- MAPE de doc theo ti le phan tram, nhung can can than neu revenue gan 0.

### Cach bao cao metric

Khong chi bao cao metric tong the. Can bao cao rieng:

```text
Overall
Dataset 1 only
Dataset 2 only
Theo location
Theo product_category
Theo thang
```

## 12. Cach ket luan co dung chung model duoc hay khong

### Truong hop 1: Model chung tot gan bang model rieng

Neu:

```text
Model C gan bang Model A tren Dataset 1
Model C gan bang Model B tren Dataset 2
```

Thi co the ket luan:

```text
Hai dataset co the dung chung 1 model sau khi da chuan hoa schema va aggregate.
```

### Truong hop 2: Model chung tot tren Dataset 2 nhung kem tren Dataset 1

Dieu nay co the do:

- Dataset 2 lon hon qua nhieu.
- Dataset 1 bi lan at khi train.
- Scope cua Dataset 1 khac Dataset 2.
- Feature mapping chua tot.

Giai phap:

- Dung sample weight.
- Aggregate o muc tho hon.
- Chi train tren khoang thoi gian chung.
- Kiem tra lai target distribution.

### Truong hop 3: Train Dataset 2 test Dataset 1 qua te

Dieu nay cho thay tinh interchangeable chua tot.

Co the ket luan:

```text
Hai dataset cung domain nhung chua the thay the nhau tot trong modeling.
```

Giai phap:

- Bo sung external features dong deu.
- Chuan hoa location/category tot hon.
- Train model rieng tung dataset, sau do so sanh insight.
- Chi dung model chung o muc baseline.

### Truong hop 4: Sau khi them weather/holiday, model tot hon

Day la ket qua rat tot cho de tai.

Co the ket luan:

```text
Cac yeu to ben ngoai nhu thoi tiet va ngay le co dong gop vao viec giai thich va du doan doanh thu.
```

Neu metric tot hon tren ca hai dataset, day la bang chung manh rang viec bo sung Dataset 3 ve weather/holiday la co gia tri.

## 13. Giai thich tinh interchangeable trong boi canh nay

Interchangeable khong co nghia la hai dataset phai giong het nhau o du lieu goc.

Trong project nay, interchangeable nen duoc hieu la:

```text
Hai dataset co the duoc dua ve cung mot schema, cung mot don vi phan tich,
cung mot target, va co the dung trong cung mot pipeline phan tich/modeling.
```

Co 3 muc do interchangeable:

### Muc 1: Interchangeable ve phan tich

Hai dataset co the dung cung framework EDA:

```text
doanh thu theo gio
doanh thu theo ngay
doanh thu theo category
doanh thu theo location
```

Muc nay kha kha thi voi Dataset 1 va Dataset 2.

### Muc 2: Interchangeable ve schema sau xu ly

Hai dataset sau khi chuan hoa co cung cot:

```text
date
hour
location
product_category
weather
holiday
revenue
```

Muc nay kha thi, nhung can bo sung weather/holiday cho Dataset 2.

### Muc 3: Interchangeable ve modeling

Model train tren dataset nay co the du doan tot tren dataset kia, hoac model chung co the hoat dong tot tren ca hai.

Muc nay chua the khang dinh. Can kiem tra bang thuc nghiem.

## 14. Checklist thuc hien

### Buoc 1: Chuan hoa schema

Can tao bang chung co cac cot:

```text
date
hour
weekday
month
is_weekend
location
product_category
weather_condition
temperature_c
is_holiday
revenue
source_dataset
```

### Buoc 2: Aggregate cung cap do

Nen aggregate theo:

```text
date + hour + location + product_category
```

Target:

```text
revenue = sum(total_amount)
```

### Buoc 3: Bo sung external features

Can bo sung cho Dataset 2:

```text
weather_condition
temperature_c
is_holiday
holiday_name
```

Join theo:

```text
date + location
```

Neu weather chi co theo thanh pho, can ghi ro gioi han:

```text
Weather duoc gan theo cap city, khong phai cap store chinh xac.
```

### Buoc 4: Kiem tra imbalance

Can tinh:

```text
so dong theo source_dataset
ty le dong Dataset 1 / Dataset 2
revenue distribution theo source_dataset
```

### Buoc 5: Train baseline model

Baseline nen gom:

```text
Linear Regression
Random Forest
Gradient Boosting neu co
```

Feature chinh:

```text
hour
weekday
month
is_weekend
location
product_category
weather_condition
temperature_c
is_holiday
```

Khong nen dung:

```text
quantity
transaction_count
avg_transaction_value
```

### Buoc 6: Danh gia rieng tung dataset

Metric can bao cao:

```text
MAE overall
MAE Dataset 1
MAE Dataset 2
RMSE overall
RMSE Dataset 1
RMSE Dataset 2
R2 overall
R2 Dataset 1
R2 Dataset 2
```

### Buoc 7: So sanh model chung va model rieng

Can lap bang:

| Model | Train data | Test data | Muc dich |
|---|---|---|---|
| A | Dataset 1 | Dataset 1 test set | Baseline rieng Dataset 1 |
| B | Dataset 2 | Dataset 2 test set | Baseline rieng Dataset 2 |
| C | Dataset 1 + Dataset 2 | Test chung, report rieng theo source | Kiem tra model chung |
| D | Dataset 2 | Dataset 1 | Kiem tra generalization |
| E | Dataset 1 | Dataset 2 | Kiem tra generalization nguoc |

## 15. Ket luan chuyen gia Data Science

Hien tai, Dataset 1 va Dataset 2 co the duoc dung trong cung mot project va co tiem nang dung chung model, nhung phai qua cac buoc xu ly bat buoc:

```text
chuan hoa schema
aggregate cung cap do
bo sung external features
kiem tra imbalance
danh gia rieng theo source_dataset
so sanh model chung voi model rieng
```

Khong nen noi ngay:

```text
Hai dataset chac chan dung chung 1 model duoc.
```

Nen noi:

```text
Hai dataset co cung domain coffee shop va co the duoc dua ve cung bai toan
du doan doanh thu sau khi chuan hoa va aggregate. Tuy nhien, do co khac biet
ve temporal scope, spatial scope, external features va kich thuoc du lieu,
can thuc hien cac thi nghiem modeling va danh gia rieng theo tung dataset
truoc khi ket luan model chung co phu hop hay khong.
```

Day la cach lap luan dung tinh than Data Science: khong chi dua vao cam tinh, ma kiem tra bang du lieu, metric va thiet ke thi nghiem ro rang.
