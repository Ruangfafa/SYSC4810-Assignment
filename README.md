# SYSC4810 - Assignment
## justInvest Access Control System

A role-based access control (RBAC) system implementing authentication, authorization, and proactive password checking for the SYSC4810 assignment.
report link: https://docs.google.com/document/d/17TKuROq2SC2BZ7gYlcm7ubmVmscW0wIL8J4RNIUvHgE
---

### Project Structure

```
app/
  common/
    config_loader.py
    constant.py
    enum.py
  service/
    mysql_service.py
    security_service.py
    authorization_service.py
    logging_service.py
  view/
    system_view.py
  application.py
```

---

### Features

#### 1. Authentication (PBKDF2-HMAC-SHA256)

* Uses PBKDF2-HMAC-SHA256  
* 128-bit salt (16 bytes) generated using `os.urandom(16)`  
* 100000 iterations  
* 256-bit derived key  
* Salt and hash stored in `passwd.txt`  
* Passwords are never stored in plaintext  

---

#### 2. Role-Based Authorization (RBAC)

User permissions are defined in `role_permission.ini` as an 8-element vector:

* `0` = deny  
* `1` = allow  
* `2` = conditional (ex: time-based for Teller)

Permission index mapping:

```
0: view account balance  
1: view investment portfolio  
2: modify investment portfolio  
3: view contact detail of FA  
4: view contact detail of FP  
5: view money market instrument  
6: view private consumer instrument  
7: access system
```

---

#### 3. Self-Enrollment (Registration)

* Username must be unique  
* Password must pass proactive validation  
* System generates a UUID automatically  
* Writes to:
  * `user.ini`
  * `passwd.txt`

---

#### 4. Proactive Password Checking

Password must satisfy:

* Length 8 to 12 characters  
* At least:
  * one uppercase letter  
  * one lowercase letter  
  * one digit  
  * one special character: ! @ # $ % * &
* Only characters allowed:  
  A-Z, a-z, 0-9, ! @ # $ % * &
* Must not match username  
* Must not be in `weak_passwd.ini`  

---

### How to Run

Run the application:

```
python3 app/application.py
```

Menu:

```
1. Login  
2. Register  
3. Exit
```

---

### Configuration Files

#### 1. user.ini  
Format:

```
[uuid]
username = value
name = value
role = C|PC|FA|FP|T
```

---

#### 2. passwd.txt  
Format:

```
[uuid]
salt_hex = <hexstring>
hash_hex = <hexstring>
```

---

#### 3. role_permission.ini  
Example:

```
[permission]
C  = 1,1,0,1,0,0,0,1
PC = 1,1,1,1,1,0,0,1
FA = 1,1,1,0,0,0,1,1
FP = 1,1,1,0,0,1,1,1
T  = 1,1,0,0,0,0,0,2
```

---

#### 4. weak_passwd.ini  
Format:

```
[weak_passwd]
list = password,123456,qwerty,admin,abc123,...
```

---

### Python Requirements
This project uses Python 3.12 and requires the following dependencies:
```
colorlog==6.10.1
python-dotenv==1.2.1
```
You can download and install all required packages using:
```
python -m pip install -r requirements.txt
```

---

### Notes

* All salts are generated using `os.urandom(16)`  
* Probability of salt collision is negligible (1/2^{128})  
* Password verification uses PBKDF2 recomputation  
* Authorization strictly enforces RBAC

---
