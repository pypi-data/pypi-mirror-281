from flask import redirect, url_for, request, render_template, jsonify
import hashlib
import os
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from appdirs import user_data_dir
from datetime import datetime
from .util import get_file_path

def get_cpu_info():
    # 获取CPU序列号
    cpu_info = os.popen("wmic cpu get ProcessorId").read() .strip().split("\n") [2]
    return cpu_info

def get_disk_info():
    # 获取硬盘序列号
    disk_info = os.popen("wmic diskdrive get SerialNumber").read().strip().split("\n")[2]
    return disk_info

def get_mac_address():
    # 获取MAC地址
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

def generate_machine_code():
    cpu_info = get_cpu_info()
    disk_info = get_disk_info()
    mac_address = get_mac_address()
    
    # 组合硬件信息生成唯一字符串
    unique_string = f"{cpu_info}-{disk_info}-{mac_address}"
    
    # 使用SHA-256哈希算法生成机器码
    machine_code = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return machine_code

def load_public_key():
    public_key_path = os.path.join(os.path.dirname(__file__), 'keys/public_key.pem')
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

# 验证授权码（使用公钥）
def verify_authorization_code(authorization_code):
    if authorization_code is None:
        return False, '没有授权文件'
    try:
        current_machine_code = generate_machine_code()
        public_key = load_public_key()
        # 分离授权信息和签名
        authorization_info, signature = authorization_code.rsplit('|', 1)
        signature = bytes.fromhex(signature)
        
        # 使用公钥验证签名
        public_key.verify(
            signature,
            authorization_info.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # 提取并验证机器码和授权截止日期
        machine_code, expiration_date_str = authorization_info.split('|')
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        
        # 检查授权是否过期
        if datetime.now() > expiration_date:
            return False, "Authorization has expired"
        
        # 检查当前机器码是否匹配
        if current_machine_code != machine_code:
            return False, "Machine code does not match"

        return True, f"Authorization is valid for machine: {machine_code} until {expiration_date_str}"
    except Exception as e:
        return False, str(e)
    
def store_authorization_code(authorization_code):
    # 构建授权码文件路径
    file_path = get_file_path('authorization_code.txt')

    # 将授权码写入文件
    with open(file_path, 'w') as f:
        f.write(authorization_code)

def read_authorization_code():
    
    # 构建授权码文件路径
    file_path = get_file_path('authorization_code.txt')

    # 尝试打开文件并读取授权码
    try:
        with open(file_path, 'r') as f:
            authorization_code = f.read().strip()
            return authorization_code
    except FileNotFoundError:
        return None
    
authorization_status = {}
    
def init_auth(app):

    @app.before_request
    def check_authorization():
        if (request.endpoint in ['auth', 'authorize'] or request.path.startswith('/static')):
            return
        today = datetime.now().date()
        
        if today in authorization_status:
            return
        else:
            authorization_code = read_authorization_code()
            is_valid, message = verify_authorization_code(authorization_code)
            if not is_valid:
                return redirect(url_for('auth'))
            else:
                authorization_status[today] = is_valid

    @app.route('/auth')
    def auth():
        data = {'machine_code': generate_machine_code()}
        return render_template('auth.html', data=data)

    @app.route('/authorize', methods=['POST'])
    def authorize():
        authorization_code = request.json.get('authorization_code')
        is_valid, message = verify_authorization_code(authorization_code)
        if is_valid:
            store_authorization_code(authorization_code)
            response = {'status': 'success', 'message': message}
        else:
            response = {'status': 'failed', 'message': message}
        return jsonify(response)
