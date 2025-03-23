# RDAP to MikroTik Address-List Generator

## 📌 Description

This Python script processes a list of public IP addresses, fetches RDAP (WHOIS) data for each, and generates two ready-to-import MikroTik RouterOS `.rsc` address-list files:

- **address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc** — contains network CIDRs (WHOIS assigned networks)
- **address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc** — contains ASN CIDRs (BGP-announced prefixes)

Additionally, it creates a CSV report with all collected data.

---

## 📂 Input File: `input_ips.txt`
A plain text file containing one IP address per line:
```
8.8.8.8
1.1.1.1
185.189.49.6
```
The script automatically removes duplicates and sorts the IP addresses.

---

## 📄 Output Files

### 1. **CSV Report:**
```
result_YYYY-MM-DD_HH-MM-SS.csv
```
Contains detailed RDAP data for each IP address.

### 2. **MikroTik Network CIDR Address List:**
```
address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```
Example:
```
/ip firewall address-list
add address=8.8.8.0/24 list=WHOIS_NET_LIST
```

### 3. **MikroTik ASN CIDR Address List:**
```
address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```
Example:
```
/ip firewall address-list
add address=8.8.8.0/24 list=WHOIS_ASN_LIST
```

---

## 🚀 How to Run
1. Install the required Python library:
```
pip install ipwhois
```
2. Prepare `input_ips.txt`.
3. Run:
```
python3 script.py
```

---

## 🛠 MikroTik Import Example
```
/import address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc
/import address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```

---

## 📝 Notes
- Checks if `input_ips.txt` exists.
- De-duplicates CIDRs.
- Processes multiple NETWORK_CIDR entries.
- Handles ASN_CIDR separately.

---

## 🌐 Example Use Cases
- Blocking networks or ASN ranges
- Building blocklists
- Visualizing IP ownership

---

## 🤖 AI-Generated Content Notice
This README content was generated with the assistance of AI.

---

# RDAP до MikroTik Address-List генератор (українською)

## 📂 Опис

Цей Python-скрипт обробляє список публічних IP-адрес, отримує RDAP (WHOIS) дані для кожної адреси та створює два готових до імпорту файли `.rsc` для MikroTik RouterOS:

- **address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc** — містить CIDR-мережі (NETWORK_CIDR) згідно з WHOIS
- **address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc** — містить CIDR-мережі автономних систем (ASN_CIDR), анонсовані через BGP

Також генерується CSV-звiт з повною зібраною інформацією.

---

## 🔢 Вхідний файл: `input_ips.txt`

Звичайний текстовий файл зі списком IP-адрес по одній в кожному рядку:

```
8.8.8.8
1.1.1.1
185.189.49.6
```

Скрипт автоматично видаляє дублікати та сортує IP-адреси.

---

## 📄 Результати виконання

### 1. **CSV-звіт:**
```
result_YYYY-MM-DD_HH-MM-SS.csv
```
Містить детальну RDAP-інформацію по кожній IP-адресі:
- IP
- ASN
- ASN CIDR
- Країна ASN
- Опис ASN
- Назва мережі
- NETWORK CIDR
- Країна мережі
- Контактні Emails

### 2. **MikroTik список мереж NETWORK CIDR:**
```
address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```
Приклад формату:
```
/ip firewall address-list
add address=8.8.8.0/24 list=WHOIS_NET_LIST
add address=185.189.48.0/22 list=WHOIS_NET_LIST
```

### 3. **MikroTik список ASN CIDR:**
```
address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```
Приклад формату:
```
/ip firewall address-list
add address=8.8.8.0/24 list=WHOIS_ASN_LIST
add address=185.189.48.0/22 list=WHOIS_ASN_LIST
```

---

## 🚀 Як запустити

### 1. Встановіть необхідну бібліотеку:
```
pip install ipwhois
```

### 2. Підготуйте файл `input_ips.txt` зі списком IP-адрес.

### 3. Запустіть скрипт:
```
python3 script.py
```

### 4. Результат:
- CSV-файл з деталями RDAP
- Два `.rsc` файли для імпорту в MikroTik

---

## 🔧 Приклад імпорту в MikroTik
На вашому MikroTik роутері виконайте:
```
/import address_networks_cidr_YYYY-MM-DD_HH-MM-SS.rsc
/import address_asn_cidr_YYYY-MM-DD_HH-MM-SS.rsc
```

---

## 📝 Особливості
- Скрипт перевіряє наявність файлу `input_ips.txt` перед запуском
- Всі CIDR-мережі унікалізуються
- `NETWORK_CIDR` може містити кілька мереж через кому — скрипт обробляє кожну окремо
- `ASN_CIDR` обробляється окремо як ширший блок

---

## 🌐 Приклади застосування
- Блокування окремих мереж або цілих ASN на MikroTik
- Формування динамічних IP-блоклистів
- Візуалізація власності IP-адрес

---

## 🤖 Застереження про AI-генерацію
Цей README згенеровано за допомогою штучного інтелекту (ШІ).
