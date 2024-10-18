import onnx

# ONNX 모델 파일 불러오기
def load_model(model_path):
    # ONNX 모델을 불러옵니다
    model = onnx.load(model_path)
    return model

# 메타데이터 파싱 함수
def parse_metadata(model):
    metadata = {}

    # 모델 이름
    if model.model_version:
        metadata['Model Version'] = model.model_version

    # 도메인
    if model.domain:
        metadata['Domain'] = model.domain

    # 생성 시간 및 프로듀서 정보
    if model.producer_name:
        metadata['Producer Name'] = model.producer_name
    if model.producer_version:
        metadata['Producer Version'] = model.producer_version

    # 모델의 메타데이터 (key-value pair)
    if model.metadata_props:
        metadata['Metadata Properties'] = {
            prop.key: prop.value for prop in model.metadata_props
        }

    return metadata

# 모델의 입력, 출력 정보 파싱 함수
def parse_graph_info(model):
    graph_info = {}

    # 입력 정보
    graph_info['Inputs'] = [{
        'name': inp.name,
        'type': onnx.helper.printable_type(inp.type)
    } for inp in model.graph.input]

    # 출력 정보
    graph_info['Outputs'] = [{
        'name': out.name,
        'type': onnx.helper.printable_type(out.type)
    } for out in model.graph.output]

    # 노드 정보
    graph_info['Nodes'] = [{
        'name': node.name,
        'op_type': node.op_type,
        'inputs': node.input,
        'outputs': node.output
    } for node in model.graph.node]

    return graph_info

# ONNX 모델 메타데이터 및 그래프 정보 출력
def display_model_info(model_path):
    # 모델 불러오기
    model = load_model(model_path)

    # 메타데이터 파싱
    metadata = parse_metadata(model)
    print("=== Model Metadata ===")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # 그래프 정보 파싱
    graph_info = parse_graph_info(model)
    print("\n=== Graph Information ===")
    print("Inputs:")
    for inp in graph_info['Inputs']:
        print(f"  - Name: {inp['name']}, Type: {inp['type']}")
    
    print("Outputs:")
    for out in graph_info['Outputs']:
        print(f"  - Name: {out['name']}, Type: {out['type']}")

    print("Nodes:")
    for node in graph_info['Nodes']:
        print(f"  - Node Name: {node['name']}, Op Type: {node['op_type']}")
        print(f"    Inputs: {node['inputs']}")
        print(f"    Outputs: {node['outputs']}")

# Example usage
model_path = 'your_model.onnx'
display_model_info(model_path)
