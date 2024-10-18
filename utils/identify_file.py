import sys
import onnx

def identify_file_format(file_path):
    # 파일의 초기 4바이트 읽기
    with open(file_path, 'rb') as f:
        magic_number = f.read(4)
    
    # GGUF 파일 여부 확인
    if magic_number == b'\x47\x47\x55\x46':  # 'GGUF'
        return "GGUF"
    
    # TFLite 파일 여부 확인 (파일 내에 'TFL3' 문자열 찾기)
    with open(file_path, 'rb') as f:
        file_content = f.read()
        if b'TFL3' in file_content:  # TFLite magic string
            return "TFLite"
    
    # ONNX 파일 여부 확인 (ONNX 모델을 로드해보기)
    try:
        onnx_model = onnx.load(file_path)  # 성공하면 ONNX 파일임
        return "ONNX"
    except Exception:
        pass
    
    return "Unknown format"

# Example usage
file_path = sys.argv[1]
file_format = identify_file_format(file_path)
print(f"The file format is: {file_format}")
